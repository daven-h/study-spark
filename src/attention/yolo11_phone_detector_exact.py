"""
YOLOv11 Phone Detector - EXACT Implementation from jasonli5/phone-detector
https://github.com/jasonli5/phone-detector
"""

import cv2
import numpy as np
from typing import List, Dict, Any, Tuple, Optional
import time

# Try to import ultralytics, fall back gracefully if not available
try:
    from ultralytics import YOLO
    YOLO_AVAILABLE = True
except ImportError:
    YOLO_AVAILABLE = False
    print("⚠️ ultralytics not available. Install with: pip install ultralytics")

class YOLOv11PhoneDetector:
    """
    EXACT implementation from jasonli5/phone-detector
    The "Lockininator" - cell phone detector built using YOLOv11 and OpenCV
    """
    
    def __init__(self, model_path: str = "yolo11s.pt", confidence_threshold: float = 0.4):
        """
        Initialize with EXACT parameters from the original implementation
        """
        # EXACT configuration from the original
        self.MODEL_PATH = model_path
        self.CONF_THRESHOLD = confidence_threshold
        self.TARGET_CLASSES = {"cell phone", "remote"}  # EXACT from original
        self.COOLDOWN_SEC = 3.0  # EXACT from original
        self.STREAK_REQUIRED = 15  # EXACT from original
        self.MIN_BOX_AREA_RATIO = 0.01  # EXACT from original
        
        # State tracking - EXACT from original
        self.last_trigger_time = 0
        self.consecutive_detections = 0
        self.last_detection_time = 0
        
        # Initialize YOLO model
        self.model = None
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
            # Run YOLO inference - EXACT from original
            results = self.model(frame, verbose=False)
            
            detections = []
            
            for result in results:
                if result.boxes is not None:
                    boxes = result.boxes
                    
                    for i in range(len(boxes)):
                        # Get box coordinates and confidence - EXACT from original
                        box = boxes.xyxy[i].cpu().numpy()
                        confidence = boxes.conf[i].cpu().numpy()
                        class_id = int(boxes.cls[i].cpu().numpy())
                        
                        # Get class name - EXACT from original
                        class_name = self.model.names[class_id]
                        
                        # EXACT filtering logic from original
                        if class_name in self.TARGET_CLASSES and confidence >= self.CONF_THRESHOLD:
                            x1, y1, x2, y2 = box.astype(int)
                            
                            # EXACT area ratio calculation from original
                            frame_area = frame.shape[0] * frame.shape[1]
                            box_area = (x2 - x1) * (y2 - y1)
                            area_ratio = box_area / frame_area
                            
                            # EXACT minimum size requirement from original
                            if area_ratio >= self.MIN_BOX_AREA_RATIO:
                                detection = {
                                    'class_id': class_id,
                                    'class_name': class_name,
                                    'confidence': float(confidence),
                                    'bbox': (x1, y1, x2, y2),
                                    'center': ((x1 + x2) // 2, (y1 + y2) // 2),
                                    'area': box_area,
                                    'area_ratio': area_ratio
                                }
                                detections.append(detection)
            
            # Sort by confidence - EXACT from original
            detections.sort(key=lambda x: x['confidence'], reverse=True)
            
            return detections
            
        except Exception as e:
            print(f"YOLO detection error: {e}")
            return []
    
    def is_phone_detected(self, frame: np.ndarray) -> Tuple[bool, float]:
        """
        EXACT debouncing logic from the original implementation
        """
        detections = self.detect_phones(frame)
        
        if not detections:
            self.consecutive_detections = 0
            return False, 0.0
        
        # Get highest confidence detection - EXACT from original
        best_detection = detections[0]
        confidence = best_detection['confidence']
        
        current_time = time.time()
        
        # EXACT debouncing logic from original
        if self.consecutive_detections >= self.STREAK_REQUIRED:
            # Check cooldown - EXACT from original
            if current_time - self.last_trigger_time >= self.COOLDOWN_SEC:
                self.last_trigger_time = current_time
                self.consecutive_detections = 0
                return True, confidence
        
        # EXACT consecutive detection logic from original
        if current_time - self.last_detection_time < 0.1:  # Within 100ms
            self.consecutive_detections += 1
        else:
            self.consecutive_detections = 1
        
        self.last_detection_time = current_time
        
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
