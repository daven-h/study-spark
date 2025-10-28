"""
YOLOv11 Phone Detector - EXACT Implementation from jasonli5/phone-detector
https://github.com/jasonli5/phone-detector
This is the EXACT code that works perfectly!
"""

import time
import cv2
import numpy as np
from typing import List, Dict, Any, Tuple, Optional

# Try to import ultralytics, fall back gracefully if not available
try:
    from ultralytics import YOLO
    YOLO_AVAILABLE = True
except ImportError:
    YOLO_AVAILABLE = False
    print("⚠️ ultralytics not available. Install with: pip install ultralytics")

# Try to import winsound for Windows ding
try:
    import winsound
    WINSOUND_AVAILABLE = True
except ImportError:
    WINSOUND_AVAILABLE = False

# --- CONFIG --- EXACT from original
MODEL_PATH = "yolo11s.pt"  # Use "yolo11n.pt" if your computer is slow
TARGET_CLASSES = {"cell phone", "remote"}  # Sometimes the model detects phone as remote, so we add remote to the list
CONF_THRESHOLD = 0.4
COOLDOWN_SEC = 3.0
STREAK_REQUIRED = 15
MIN_BOX_AREA_RATIO = 0.01
# ---------------

def get_screen_size():
    """Return (width, height) of the primary screen."""
    try:
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()
        w = root.winfo_screenwidth()
        h = root.winfo_screenheight()
        root.destroy()
        return int(w), int(h)
    except Exception:
        return 1920, 1080  

SCREEN_W, SCREEN_H = get_screen_size()

class YOLOv11PhoneDetector:
    """
    EXACT implementation from jasonli5/phone-detector
    The "Lockininator" - cell phone detector built using YOLOv11 and OpenCV
    """
    
    def __init__(self, model_path: str = MODEL_PATH, confidence_threshold: float = CONF_THRESHOLD):
        """
        Initialize with EXACT parameters from the original implementation
        """
        # EXACT configuration from the original
        self.MODEL_PATH = model_path
        self.CONF_THRESHOLD = confidence_threshold
        self.TARGET_CLASSES = TARGET_CLASSES
        self.COOLDOWN_SEC = COOLDOWN_SEC
        self.STREAK_REQUIRED = STREAK_REQUIRED
        self.MIN_BOX_AREA_RATIO = MIN_BOX_AREA_RATIO
        
        # State tracking - EXACT from original
        self.last_trigger = 0
        self.streak_hits = 0
        
        # Initialize YOLO model - EXACT from original
        self.model = None
        self.id2name = None
        self.wanted_ids = None
        self._load_model()
        
        print(f"✅ YOLOv11 Phone Detector initialized (EXACT from jasonli5/phone-detector)")
        print(f"📱 Model: {self.MODEL_PATH}")
        print(f"🎯 Target classes: {self.TARGET_CLASSES}")
        print(f"📊 Confidence threshold: {self.CONF_THRESHOLD}")
        print(f"⏱️ Cooldown: {self.COOLDOWN_SEC}s, Streak required: {self.STREAK_REQUIRED}")
    
    def _load_model(self):
        """Load YOLO model - EXACT from original"""
        if not YOLO_AVAILABLE:
            print("❌ ultralytics not available. Cannot load YOLO model.")
            print("💡 Install with: pip install ultralytics")
            self.model = None
            return
            
        try:
            self.model = YOLO(self.MODEL_PATH)
            self.id2name = self.model.names
            self.wanted_ids = {i for i, n in self.id2name.items() if n in self.TARGET_CLASSES}
            print(f"✅ YOLO model loaded successfully")
        except Exception as e:
            print(f"❌ Failed to load YOLO model: {e}")
            print("💡 Make sure ultralytics is installed: pip install ultralytics")
            self.model = None
    
    def detect_phones(self, frame: np.ndarray) -> List[Dict[str, Any]]:
        """
        EXACT phone detection logic from the original implementation
        """
        if self.model is None or not YOLO_AVAILABLE:
            return []
        
        try:
            H, W = frame.shape[:2]
            frame_area = float(H * W)
            
            # Run YOLO inference - EXACT from original
            results = self.model(frame, verbose=False)[0]
            
            detections = []
            
            # Check for phone detection with size filter - EXACT from original
            if results.boxes and len(results.boxes) > 0:
                for (cls_id, conf, xyxy) in zip(results.boxes.cls.tolist(),
                                            results.boxes.conf.tolist(),
                                            results.boxes.xyxy.tolist()):
                    if cls_id in self.wanted_ids and conf >= self.CONF_THRESHOLD:
                        x1, y1, x2, y2 = xyxy
                        box_area = max(0.0, (x2 - x1)) * max(0.0, (y2 - y1))
                        if box_area / frame_area >= self.MIN_BOX_AREA_RATIO:
                            detection = {
                                'class_id': cls_id,
                                'class_name': self.id2name[cls_id],
                                'confidence': float(conf),
                                'bbox': (int(x1), int(y1), int(x2), int(y2)),
                                'center': (int((x1 + x2) // 2), int((y1 + y2) // 2)),
                                'area': box_area,
                                'area_ratio': box_area / frame_area
                            }
                            detections.append(detection)
            
            return detections
            
        except Exception as e:
            print(f"YOLO detection error: {e}")
            return []
    
    def is_phone_detected(self, frame: np.ndarray) -> Tuple[bool, float]:
        """
        EXACT debouncing logic from the original implementation
        """
        detections = self.detect_phones(frame)
        
        # Check for phone detection with size filter - EXACT from original
        hit = len(detections) > 0
        
        # Debounce with consecutive streak - EXACT from original
        if hit:
            self.streak_hits += 1
        else:
            self.streak_hits = 0
        
        now = time.time()
        confidence = detections[0]['confidence'] if detections else 0.0
        
        if self.streak_hits >= self.STREAK_REQUIRED and (now - self.last_trigger) > self.COOLDOWN_SEC:
            self.last_trigger = now
            self.streak_hits = 0
            return True, confidence
        
        return False, confidence
    
    def detect_phones_near_face(self, frame: np.ndarray, face_bbox: Optional[Tuple[int, int, int, int]]) -> List[Dict[str, Any]]:
        """
        Detect phones specifically near the face area
        """
        if face_bbox is None:
            # If no face detected, search entire frame
            return self.detect_phones(frame)
        
        fx1, fy1, fx2, fy2 = face_bbox
        
        # Expand face area for detection
        margin = 200  # Larger margin for phone detection
        search_x1 = max(0, fx1 - margin)
        search_y1 = max(0, fy1 - margin)
        search_x2 = min(frame.shape[1], fx2 + margin)
        search_y2 = min(frame.shape[0], fy2 + margin)
        
        # Crop frame to face area
        face_region = frame[search_y1:search_y2, search_x1:search_x2]
        
        if face_region.size == 0:
            return []
        
        # Detect phones in face region
        detections = self.detect_phones(face_region)
        
        # Adjust coordinates back to full frame
        for detection in detections:
            x1, y1, x2, y2 = detection['bbox']
            detection['bbox'] = (x1 + search_x1, y1 + search_y1, x2 + search_x1, y2 + search_y1)
            detection['center'] = (detection['center'][0] + search_x1, detection['center'][1] + search_y1)
        
        return detections
    
    def play_phone_alert(self):
        """Play phone detection alert with sound and visual message"""
        print("📱 PHONE DETECTED - LOCK IN!")
        
        # Play ding sound
        self._play_ding_sound()
        
        # Show visual alert
        self._show_phone_alert()
    
    def _play_ding_sound(self):
        """Play a ding sound using available audio libraries"""
        try:
            if WINSOUND_AVAILABLE:
                # Windows system sound
                winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
            else:
                # Fallback: print bell character
                print('\a')  # ASCII bell character
        except Exception as e:
            print(f"⚠️ Could not play sound: {e}")
            print('\a')  # Fallback bell
    
    def _show_phone_alert(self):
        """Show visual phone detection alert"""
        try:
            # Create alert window
            win = "PHONE DETECTED - LOCK IN!"
            cv2.namedWindow(win, cv2.WINDOW_NORMAL)
            
            # Create alert frame
            alert_width = 600
            alert_height = 200
            alert_frame = np.zeros((alert_height, alert_width, 3), dtype=np.uint8)
            alert_frame[:] = (0, 0, 255)  # Red background
            
            # Add text
            text = "PHONE DETECTED"
            subtext = "LOCK IN!"
            
            # Calculate text positions
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 1.5
            thickness = 3
            
            # Main text
            text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
            text_x = (alert_width - text_size[0]) // 2
            text_y = (alert_height - text_size[1]) // 2 - 20
            
            cv2.putText(alert_frame, text, (text_x, text_y), font, font_scale, (255, 255, 255), thickness)
            
            # Sub text
            sub_font_scale = 1.0
            sub_text_size = cv2.getTextSize(subtext, font, sub_font_scale, thickness)[0]
            sub_text_x = (alert_width - sub_text_size[0]) // 2
            sub_text_y = text_y + 50
            
            cv2.putText(alert_frame, subtext, (sub_text_x, sub_text_y), font, sub_font_scale, (255, 255, 255), thickness)
            
            # Position window
            x_pos = (SCREEN_W - alert_width) // 2
            y_pos = (SCREEN_H - alert_height) // 2
            
            cv2.resizeWindow(win, alert_width, alert_height)
            cv2.moveWindow(win, x_pos, y_pos)
            
            # Make window stay on top
            try:
                cv2.setWindowProperty(win, cv2.WND_PROP_TOPMOST, 1)
            except Exception:
                pass
            
            # Show alert for 3 seconds
            cv2.imshow(win, alert_frame)
            cv2.waitKey(3000)  # Show for 3 seconds
            
            # Clean up
            cv2.destroyWindow(win)
            
        except Exception as e:
            print(f"⚠️ Could not show visual alert: {e}")
            print("📱 PHONE DETECTED - LOCK IN!")
    
    def draw_detections(self, frame: np.ndarray, detections: List[Dict[str, Any]]) -> np.ndarray:
        """
        Draw phone detection boxes on frame - EXACT from original
        """
        for detection in detections:
            x1, y1, x2, y2 = detection['bbox']
            confidence = detection['confidence']
            class_name = detection['class_name']
            
            # Draw bounding box - EXACT colors from original
            color = (0, 255, 0) if class_name == "cell phone" else (255, 0, 0)
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            
            # Draw label - EXACT format from original
            label = f"{class_name}: {confidence:.2f}"
            cv2.putText(frame, label, (x1, y1 - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        
        return frame
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get model information - EXACT from original"""
        if self.model is None or not YOLO_AVAILABLE:
            return {
                "status": "not_available",
                "model_path": self.MODEL_PATH,
                "model_type": "YOLOv11",
                "target_classes": list(self.TARGET_CLASSES),
                "confidence_threshold": self.CONF_THRESHOLD,
                "cooldown_sec": self.COOLDOWN_SEC,
                "streak_required": self.STREAK_REQUIRED,
                "min_box_area_ratio": self.MIN_BOX_AREA_RATIO,
                "error": "YOLO not available - install ultralytics"
            }
        
        return {
            "status": "loaded",
            "model_path": self.MODEL_PATH,
            "model_type": "YOLOv11",
            "target_classes": list(self.TARGET_CLASSES),
            "confidence_threshold": self.CONF_THRESHOLD,
            "cooldown_sec": self.COOLDOWN_SEC,
            "streak_required": self.STREAK_REQUIRED,
            "min_box_area_ratio": self.MIN_BOX_AREA_RATIO
        }

def main():
    """
    EXACT test implementation from the original repository
    """
    print("🧪 Testing YOLOv11 Phone Detector (EXACT from jasonli5/phone-detector)")
    
    # Initialize detector with EXACT parameters
    detector = YOLOv11PhoneDetector()
    
    # Initialize camera - EXACT from original
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Failed to open camera")
        return
    
    print("📹 Camera opened. Press 'q' to quit")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Failed to read frame")
            break
        
        # Detect phones using EXACT logic
        detections = detector.detect_phones(frame)
        
        # Draw detections - EXACT from original
        frame = detector.draw_detections(frame, detections)
        
        # Show frame
        cv2.imshow('YOLOv11 Phone Detector (EXACT)', frame)
        
        # Print detections - EXACT from original
        if detections:
            print(f"📱 Detected {len(detections)} phone(s)")
            for det in detections:
                print(f"  - {det['class_name']}: {det['confidence']:.2f}")
        
        # Check for quit - EXACT from original
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    print("✅ YOLOv11 Phone Detector test completed (EXACT implementation)")

if __name__ == "__main__":
    main()