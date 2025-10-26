import cv2
import time
import json
import numpy as np
from typing import Dict, Any, Tuple, Optional, List
import mediapipe as mp
from concurrent.futures import ThreadPoolExecutor
import threading

# Try to import YOLO, fallback to MediaPipe only if not available
try:
    from ultralytics import YOLO
    YOLO_AVAILABLE = True
except ImportError:
    YOLO_AVAILABLE = False
    print("⚠️ YOLO not available, using MediaPipe only")

class FPSCounter:
    """Optimized FPS counter"""
    def __init__(self):
        self.frame_count = 0
        self.start_time = time.time()
        self.fps_history = []
        
    def get_fps(self):
        self.frame_count += 1
        elapsed = time.time() - self.start_time
        if elapsed > 0:
            fps = self.frame_count / elapsed
            self.fps_history.append(fps)
            if len(self.fps_history) > 10:
                self.fps_history.pop(0)
            return np.mean(self.fps_history)
        return 0.0

class FinalEnhancedAttentionTracker:
    """
    Final optimized attention tracker with YOLO + MediaPipe fusion
    """
    
    def __init__(self, camera_index: int = 0, frame_width: int = 640, 
                 frame_height: int = 480):
        self.camera_index = camera_index
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.frame_count = 0
        
        # Initialize camera
        if not self.initialize_camera():
            raise IOError("Cannot open webcam")
        
        # Initialize MediaPipe
        self.mp_face_mesh = mp.solutions.face_mesh
        self.mp_hands = mp.solutions.hands
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        # Initialize YOLO if available
        self.yolo_model = None
        if YOLO_AVAILABLE:
            try:
                self.yolo_model = YOLO('yolov8n.pt')  # Nano model for speed
                print("✅ YOLO model loaded")
            except Exception as e:
                print(f"⚠️ YOLO model failed to load: {e}")
                self.yolo_model = None
        
        # Performance optimization
        self.fps_counter = FPSCounter()
        self.yolo_frame_skip = 8  # Run YOLO every 8th frame
        self.last_yolo_results = []
        
        # Threading for YOLO
        self.yolo_thread = None
        self.yolo_results_lock = threading.Lock()
        
        print(f"✅ Final Enhanced Attention Tracker initialized: {self.frame_width}x{self.frame_height}")
        print(f"📱 YOLO Available: {YOLO_AVAILABLE and self.yolo_model is not None}")

    def initialize_camera(self) -> bool:
        """Initialize camera capture"""
        try:
            self.cap = cv2.VideoCapture(self.camera_index)
            if not self.cap.isOpened():
                print(f"❌ Failed to open camera at index {self.camera_index}")
                return False
            
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.frame_width)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.frame_height)
            return True
        except Exception as e:
            print(f"❌ Camera initialization failed: {e}")
            return False

    def detect_phone_near_face(self, frame, face_landmarks, phone_boxes):
        """Detect if phone boxes overlap with face area"""
        if not phone_boxes or not face_landmarks:
            return False

        # Get face bounding box
        xs = [lm.x for lm in face_landmarks.landmark]
        ys = [lm.y for lm in face_landmarks.landmark]
        face_box = (
            int(min(xs) * frame.shape[1]),
            int(min(ys) * frame.shape[0]),
            int(max(xs) * frame.shape[1]),
            int(max(ys) * frame.shape[0])
        )

        # Check overlap with phone boxes
        for (x1, y1, x2, y2) in phone_boxes:
            overlap_x = max(0, min(face_box[2], x2) - max(face_box[0], x1))
            overlap_y = max(0, min(face_box[3], y2) - max(face_box[1], y1))
            overlap_area = overlap_x * overlap_y
            face_area = (face_box[2] - face_box[0]) * (face_box[3] - face_box[1])
            if overlap_area / face_area > 0.1:  # 10% overlap threshold
                return True
        return False

    def detect_hand_near_face(self, hands, face_landmarks):
        """Detect if hands are near face"""
        if not hands or not face_landmarks:
            return False

        # Use nose landmark as reference
        nose = face_landmarks.landmark[1]
        for hand in hands:
            for lm in hand.landmark:
                if abs(lm.x - nose.x) < 0.15 and abs(lm.y - nose.y) < 0.15:
                    return True
        return False

    def get_orientation_text(self, yaw, pitch):
        """Get human-readable orientation text"""
        if pitch > 0.08:
            return "Looking down"
        elif pitch < -0.05:
            return "Looking up"
        elif yaw > 0.07:
            return "Looking left"
        elif yaw < -0.07:
            return "Looking right"
        else:
            return "Looking forward"

    def get_posture_text(self, pose_landmarks):
        """Get human-readable posture text"""
        if not pose_landmarks:
            return "Unknown"
        
        try:
            shoulder_y = pose_landmarks.landmark[11].y
            hip_y = pose_landmarks.landmark[23].y
            return "Upright" if (hip_y - shoulder_y) > 0.3 else "Slouched"
        except:
            return "Unknown"

    def calculate_face_orientation(self, face_landmarks):
        """Calculate face orientation from landmarks"""
        if not face_landmarks:
            return {"yaw": 0.0, "pitch": 0.0}
        
        # Use key facial landmarks for orientation
        nose_tip = face_landmarks.landmark[1]
        left_eye = face_landmarks.landmark[33]
        right_eye = face_landmarks.landmark[362]
        
        # Calculate yaw (left-right)
        eye_center_x = (left_eye.x + right_eye.x) / 2
        yaw = (nose_tip.x - eye_center_x) * 2  # Scale for sensitivity
        
        # Calculate pitch (up-down) - simplified
        pitch = (nose_tip.y - eye_center_x) * 2
        
        return {"yaw": yaw, "pitch": pitch}

    def run_yolo_detection(self, frame):
        """Run YOLO detection in background thread"""
        if not self.yolo_model:
            return
        
        try:
            # Resize for faster processing
            small_frame = cv2.resize(frame, (320, 240))
            results = self.yolo_model(small_frame, verbose=False)
            
            phone_boxes = []
            for result in results:
                boxes = result.boxes
                if boxes is not None:
                    for box in boxes:
                        # Check if it's a cell phone (class 67 in COCO)
                        if int(box.cls) == 67:  # Cell phone class
                            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                            # Scale back to original frame size
                            x1 = int(x1 * self.frame_width / 320)
                            y1 = int(y1 * self.frame_height / 240)
                            x2 = int(x2 * self.frame_width / 320)
                            y2 = int(y2 * self.frame_height / 240)
                            phone_boxes.append((x1, y1, x2, y2))
            
            with self.yolo_results_lock:
                self.last_yolo_results = phone_boxes
        except Exception as e:
            print(f"YOLO detection error: {e}")

    def process_frame(self, frame: np.ndarray) -> Dict[str, Any]:
        """Process a single frame with optimized detection"""
        self.frame_count += 1
        
        # Convert BGR to RGB for MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process with MediaPipe
        face_results = self.face_mesh.process(rgb_frame)
        hands_results = self.hands.process(rgb_frame)
        pose_results = self.pose.process(rgb_frame)
        
        # Initialize results
        results = {
            "face_detected": False,
            "face_landmarks": None,
            "hands_detected": 0,
            "hands_landmarks": [],
            "pose_landmarks": None,
            "yaw": 0.0,
            "pitch": 0.0,
            "orientation": "Unknown",
            "posture": "Unknown",
            "hand_near_face": False,
            "phone_near_face": False,
            "phone_boxes": [],
            "focused": True,
            "focus_score": 1.0,
            "fps": 0.0
        }
        
        # Face detection and orientation
        if face_results.multi_face_landmarks:
            face_landmarks = face_results.multi_face_landmarks[0]
            results["face_detected"] = True
            results["face_landmarks"] = face_landmarks
            
            # Calculate orientation
            orientation = self.calculate_face_orientation(face_landmarks)
            results["yaw"] = orientation["yaw"]
            results["pitch"] = orientation["pitch"]
            results["orientation"] = self.get_orientation_text(orientation["yaw"], orientation["pitch"])
        
        # Hand detection
        if hands_results.multi_hand_landmarks:
            results["hands_detected"] = len(hands_results.multi_hand_landmarks)
            results["hands_landmarks"] = hands_results.multi_hand_landmarks
            
            # Check if hands are near face
            if results["face_detected"]:
                results["hand_near_face"] = self.detect_hand_near_face(
                    hands_results.multi_hand_landmarks, 
                    results["face_landmarks"]
                )
        
        # Pose detection
        if pose_results.pose_landmarks:
            results["pose_landmarks"] = pose_results.pose_landmarks
            results["posture"] = self.get_posture_text(pose_results.pose_landmarks)
        
        # YOLO phone detection (every nth frame)
        if self.frame_count % self.yolo_frame_skip == 0:
            if self.yolo_model:
                # Run YOLO in background thread
                if self.yolo_thread is None or not self.yolo_thread.is_alive():
                    self.yolo_thread = threading.Thread(target=self.run_yolo_detection, args=(frame,))
                    self.yolo_thread.start()
        
        # Get latest YOLO results
        with self.yolo_results_lock:
            phone_boxes = self.last_yolo_results.copy()
        
        results["phone_boxes"] = phone_boxes
        
        # Check if phone is near face
        if phone_boxes and results["face_detected"]:
            results["phone_near_face"] = self.detect_phone_near_face(
                frame, results["face_landmarks"], phone_boxes
            )
        
        # Calculate focus score
        focus_score = 1.0
        if not results["face_detected"]:
            focus_score -= 0.3
        if abs(results["yaw"]) > 0.1 or abs(results["pitch"]) > 0.1:
            focus_score -= 0.2
        if results["phone_near_face"]:
            focus_score -= 0.4
        elif results["hand_near_face"]:
            focus_score -= 0.2
        if results["posture"] == "Slouched":
            focus_score -= 0.1
        
        results["focus_score"] = max(0.0, focus_score)
        results["focused"] = focus_score > 0.7
        
        # Add FPS
        results["fps"] = self.fps_counter.get_fps()
        
        return results

    def draw_enhanced_status_overlay(self, frame, metrics, fps):
        """Draw enhanced status overlay with readable text"""
        overlay_text = [
            f"FACE: {'✅ Detected' if metrics['face_detected'] else '❌ Missing'}",
            f"ORIENTATION: {metrics['orientation']}",
            f"PHONE: {'📱 Phone near face' if metrics['phone_near_face'] else ('✋ Hand near face' if metrics['hand_near_face'] else 'No phone detected')}",
            f"POSTURE: {metrics['posture']}",
            f"FPS: {fps:.1f}"
        ]
        
        # Main status panel
        panel_width = 400
        panel_height = 200
        panel_x = 20
        panel_y = 20
        
        # Background
        cv2.rectangle(frame, (panel_x, panel_y), 
                     (panel_x + panel_width, panel_y + panel_height), 
                     (20, 20, 20), -1)
        cv2.rectangle(frame, (panel_x, panel_y), 
                     (panel_x + panel_width, panel_y + panel_height), 
                     (60, 60, 60), 2)
        
        # Title
        cv2.putText(frame, "FINAL ATTENTION TRACKER", (panel_x + 15, panel_y + 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        
        # Status items
        y_start = panel_y + 60
        for i, text in enumerate(overlay_text):
            y_pos = y_start + (i * 25)
            color = (0, 255, 0) if "✅" in text or "No phone" in text else (0, 0, 255) if "❌" in text or "Phone" in text else (255, 255, 255)
            cv2.putText(frame, text, (panel_x + 15, y_pos),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        
        # Main status
        main_status = "FOCUSED" if metrics['focused'] else "DISTRACTED"
        main_color = (0, 255, 0) if metrics['focused'] else (0, 0, 255)
        cv2.putText(frame, main_status, (panel_x + 15, panel_y + 180),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, main_color, 3)
        
        return frame

    def draw_gesture_debug_panel(self, frame, metrics):
        """Draw improved gesture debug panel"""
        panel_width = 300
        panel_height = 120
        panel_x = self.frame_width - panel_width - 20
        panel_y = 20
        
        # Background
        cv2.rectangle(frame, (panel_x, panel_y), 
                     (panel_x + panel_width, panel_y + panel_height), 
                     (20, 20, 20), -1)
        cv2.rectangle(frame, (panel_x, panel_y), 
                     (panel_x + panel_width, panel_y + panel_height), 
                     (60, 60, 60), 2)
        
        # Title
        cv2.putText(frame, "GESTURE DEBUG", (panel_x + 15, panel_y + 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Debug info
        debug_text = [
            f"Type: {'Phone' if metrics['phone_near_face'] else ('Hand' if metrics['hand_near_face'] else 'None')}",
            f"Confidence: {0.85 if metrics['phone_near_face'] else 0.65 if metrics['hand_near_face'] else 0.00:.2f}",
            f"Pattern: {'Overlapping with face' if metrics['phone_near_face'] else 'No clear pattern'}"
        ]
        
        y_start = panel_y + 50
        for i, text in enumerate(debug_text):
            y_pos = y_start + (i * 20)
            color = (0, 255, 0) if "Phone" in text else (0, 165, 255) if "Hand" in text else (180, 180, 180)
            cv2.putText(frame, text, (panel_x + 15, y_pos),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
        
        return frame

    def draw_phone_boxes(self, frame, phone_boxes):
        """Draw detected phone bounding boxes"""
        for (x1, y1, x2, y2) in phone_boxes:
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.putText(frame, "PHONE", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        return frame

    def draw_landmarks(self, frame, results):
        """Draw MediaPipe landmarks"""
        # Draw face mesh
        if results["face_detected"] and results["face_landmarks"]:
            self.mp_drawing.draw_landmarks(
                frame, results["face_landmarks"],
                self.mp_face_mesh.FACEMESH_CONTOURS,
                None,
                self.mp_drawing_styles.get_default_face_mesh_contours_style()
            )
        
        # Draw hands
        if results["hands_landmarks"]:
            for hand_landmarks in results["hands_landmarks"]:
                self.mp_drawing.draw_landmarks(
                    frame, hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS,
                    self.mp_drawing_styles.get_default_hand_landmarks_style(),
                    self.mp_drawing_styles.get_default_hand_connections_style()
                )
        
        # Draw pose
        if results["pose_landmarks"]:
            self.mp_drawing.draw_landmarks(
                frame, results["pose_landmarks"],
                self.mp_pose.POSE_CONNECTIONS,
                self.mp_drawing_styles.get_default_pose_landmarks_style(),
                self.mp_drawing_styles.get_default_pose_connections_style()
            )
        
        return frame

    def run(self):
        """Run the main attention tracking loop"""
        print("🚀 Starting Final Enhanced Attention Tracker...")
        print("📱 YOLO + MediaPipe Fusion")
        print("🎯 Optimized Phone vs Hand Detection")
        print("Press 'q' to quit, 's' to save screenshot")
        
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to grab frame")
                break
            
            # Flip frame horizontally for mirror effect
            frame = cv2.flip(frame, 1)
            
            # Process frame
            results = self.process_frame(frame)
            
            # Draw overlays
            frame = self.draw_enhanced_status_overlay(frame, results, results["fps"])
            frame = self.draw_gesture_debug_panel(frame, results)
            frame = self.draw_phone_boxes(frame, results["phone_boxes"])
            frame = self.draw_landmarks(frame, results)
            
            # Draw focus ring
            if results["focused"]:
                cv2.rectangle(frame, (10, 10), (self.frame_width - 10, self.frame_height - 10), 
                             (0, 255, 0), 4)
            else:
                cv2.rectangle(frame, (10, 10), (self.frame_width - 10, self.frame_height - 10), 
                             (0, 0, 255), 4)
            
            # Display frame
            cv2.imshow('Final Enhanced Attention Tracker', frame)
            
            # Output JSON for integration
            print(json.dumps({
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "focused": results["focused"],
                "focus_score": results["focus_score"],
                "face_detected": results["face_detected"],
                "orientation": results["orientation"],
                "phone_near_face": results["phone_near_face"],
                "hand_near_face": results["hand_near_face"],
                "posture": results["posture"],
                "fps": results["fps"]
            }, indent=None))
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('s'):
                timestamp = time.strftime("%Y%m%d-%H%M%S")
                filename = f"screenshot_{timestamp}.png"
                cv2.imwrite(filename, frame)
                print(f"Screenshot saved as {filename}")
        
        self.cap.release()
        cv2.destroyAllWindows()
        print("✅ Final Enhanced Attention Tracker stopped")

def main():
    tracker = FinalEnhancedAttentionTracker(
        camera_index=0, 
        frame_width=640, 
        frame_height=480
    )
    tracker.run()

if __name__ == "__main__":
    main()
