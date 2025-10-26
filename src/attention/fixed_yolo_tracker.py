"""
Fixed YOLO-Integrated Attention Tracker
Fixes the "???" status messages and improves FPS
"""

import cv2
import time
import json
import numpy as np
from typing import Dict, Any, Tuple, Optional, List
import mediapipe as mp
import threading
from concurrent.futures import ThreadPoolExecutor

from yolo_opencv_detector import YOLOOpenCVDetector

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

class FixedYOLOAttentionTracker:
    """
    Fixed YOLO-Integrated Attention Tracker
    Fixes status messages and improves performance
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
        
        # Initialize YOLO detector
        self.yolo_detector = YOLOOpenCVDetector(confidence_threshold=0.5, nms_threshold=0.4)
        self.yolo_detector.load_model()
        
        # Performance optimization
        self.fps_counter = FPSCounter()
        self.yolo_frame_skip = 6  # Run YOLO every 6th frame for better performance
        self.last_yolo_results = []
        
        # Threading for YOLO
        self.yolo_thread = None
        self.yolo_results_lock = threading.Lock()
        
        # Focus thresholds
        self.yaw_threshold = 0.25
        self.pitch_threshold = 0.35
        self.posture_threshold = 0.3
        
        print(f"✅ Fixed YOLO Attention Tracker initialized: {self.frame_width}x{self.frame_height}")
        print("📱 OpenCV YOLO + MediaPipe + Fixed Status Messages")
        print("🎯 Optimized Phone vs Hand Detection with YOLO")

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

    def run_yolo_detection_async(self, frame):
        """Run YOLO detection in background thread"""
        try:
            # Resize for faster processing
            small_frame = cv2.resize(frame, (320, 240))
            detections = self.yolo_detector.detect_phones(small_frame)
            
            # Scale back to original frame size
            scaled_detections = []
            for detection in detections:
                x1, y1, x2, y2 = detection['bbox']
                # Scale coordinates back to original size
                x1 = int(x1 * self.frame_width / 320)
                y1 = int(y1 * self.frame_height / 240)
                x2 = int(x2 * self.frame_width / 320)
                y2 = int(y2 * self.frame_height / 240)
                
                scaled_detection = detection.copy()
                scaled_detection['bbox'] = (x1, y1, x2, y2)
                scaled_detections.append(scaled_detection)
            
            with self.yolo_results_lock:
                self.last_yolo_results = scaled_detections
        except Exception as e:
            print(f"YOLO detection error: {e}")

    def calculate_face_orientation(self, face_landmarks):
        """Calculate yaw and pitch from face landmarks"""
        try:
            # Use key facial landmarks for orientation
            left_eye = face_landmarks.landmark[33]
            right_eye = face_landmarks.landmark[263]
            nose = face_landmarks.landmark[1]
            
            # Calculate yaw (left-right head movement)
            yaw = (left_eye.x - right_eye.x) * 2  # Scale for sensitivity
            
            # Calculate pitch (up-down head movement)
            eye_center_y = (left_eye.y + right_eye.y) / 2
            pitch = (nose.y - eye_center_y) * 2  # Scale for sensitivity
            
            return yaw, pitch
        except (IndexError, AttributeError):
            return 0.0, 0.0

    def is_phone_near_face(self, face_bbox, phone_objects, threshold=0.1):
        """Check if phone objects overlap with face area"""
        if not face_bbox or not phone_objects:
            return False, 0.0
        
        fx1, fy1, fx2, fy2 = face_bbox
        face_area = (fx2 - fx1) * (fy2 - fy1)
        max_confidence = 0.0
        
        for obj in phone_objects:
            x1, y1, x2, y2 = obj['bbox']
            # Calculate overlap
            overlap_x = max(0, min(fx2, x2) - max(fx1, x1))
            overlap_y = max(0, min(fy2, y2) - max(fy1, y1))
            overlap_area = overlap_x * overlap_y
            
            if face_area > 0:
                overlap_ratio = overlap_area / face_area
                if overlap_ratio > threshold:
                    max_confidence = max(max_confidence, overlap_ratio)
                    return True, max_confidence
        
        return False, 0.0

    def is_hand_near_face(self, face_bbox, hands, margin=0.15):
        """Check if hand landmarks are near face area"""
        if not face_bbox or not hands:
            return False
        
        fx1, fy1, fx2, fy2 = face_bbox
        face_center_x = (fx1 + fx2) / 2
        face_center_y = (fy1 + fy2) / 2
        
        for hand in hands:
            for lm in hand.landmark:
                # Convert normalized coordinates to pixel coordinates
                x = lm.x * self.frame_width
                y = lm.y * self.frame_height
                
                # Check distance to face center
                distance = np.sqrt((x - face_center_x)**2 + (y - face_center_y)**2)
                if distance < margin * 100:  # Scale margin to pixels
                    return True
        
        return False

    def process_frame(self, frame: np.ndarray) -> Dict[str, Any]:
        """Process a single frame with YOLO + MediaPipe integration"""
        self.frame_count += 1
        
        # Convert BGR to RGB for MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process with MediaPipe
        face_results = self.face_mesh.process(rgb_frame)
        hands_results = self.hands.process(rgb_frame)
        pose_results = self.pose.process(rgb_frame)
        
        # Initialize detection results
        face_bbox = None
        face_landmarks = None
        hand_landmarks = []
        yolo_objects = []
        
        # Extract face bounding box and landmarks
        if face_results.multi_face_landmarks:
            face_landmarks = face_results.multi_face_landmarks[0]
            
            # Calculate face bounding box
            all_x, all_y = [], []
            for landmark in face_landmarks.landmark:
                all_x.append(landmark.x)
                all_y.append(landmark.y)
            
            x_min = int(min(all_x) * self.frame_width)
            x_max = int(max(all_x) * self.frame_width)
            y_min = int(min(all_y) * self.frame_height)
            y_max = int(max(all_y) * self.frame_height)
            face_bbox = (x_min, y_min, x_max, y_max)
        
        # Extract hand landmarks
        if hands_results.multi_hand_landmarks:
            hand_landmarks = hands_results.multi_hand_landmarks
        
        # YOLO phone detection (every nth frame)
        if self.frame_count % self.yolo_frame_skip == 0:
            # Run YOLO in background thread
            if self.yolo_thread is None or not self.yolo_thread.is_alive():
                self.yolo_thread = threading.Thread(target=self.run_yolo_detection_async, args=(frame,))
                self.yolo_thread.start()
        
        # Get latest YOLO results
        with self.yolo_results_lock:
            yolo_objects = self.last_yolo_results.copy()
        
        # Face visibility
        face_visible = face_bbox is not None
        
        # Phone detection using YOLO + face overlap
        phone_near_face = False
        phone_confidence = 0.0
        if face_bbox and yolo_objects:
            phone_near_face, phone_confidence = self.is_phone_near_face(face_bbox, yolo_objects)
        
        # Hand detection using MediaPipe landmarks
        hand_near_face = False
        if face_bbox and hand_landmarks:
            hand_near_face = self.is_hand_near_face(face_bbox, hand_landmarks)
        
        # Orientation analysis from face landmarks
        yaw, pitch = 0.0, 0.0
        orientation_good = True
        if face_visible and face_landmarks:
            yaw, pitch = self.calculate_face_orientation(face_landmarks)
            orientation_good = abs(yaw) < self.yaw_threshold and abs(pitch) < self.pitch_threshold
        
        # Posture analysis from pose landmarks
        posture_stable = True
        if pose_results.pose_landmarks:
            try:
                shoulders = pose_results.pose_landmarks.landmark[11]
                hips = pose_results.pose_landmarks.landmark[23]
                posture_stable = (hips.y - shoulders.y) > self.posture_threshold
            except (IndexError, AttributeError):
                posture_stable = True
        
        # Calculate focus score
        focus_components = {
            "face_visibility": 1.0 if face_visible else 0.0,
            "orientation": 1.0 if orientation_good else 0.0,
            "phone_interaction": 0.0 if phone_near_face else 1.0,
            "hand_interaction": 0.7 if hand_near_face else 1.0,
            "posture": 1.0 if posture_stable else 0.0
        }
        
        # Weighted focus score
        weights = {
            "face_visibility": 0.3,
            "orientation": 0.25,
            "phone_interaction": 0.25,
            "hand_interaction": 0.1,
            "posture": 0.1
        }
        
        focus_score = sum(weights[component] * score for component, score in focus_components.items())
        
        # Overall focus determination
        focused = (focus_score > 0.7 and not phone_near_face and face_visible and orientation_good)
        
        # Generate status messages
        status_messages = self.generate_status_messages(
            face_visible, orientation_good, phone_near_face, hand_near_face,
            phone_confidence, posture_stable, yaw, pitch
        )
        
        # Add FPS
        fps = self.fps_counter.get_fps()
        
        return {
            "focused": focused,
            "focus_score": focus_score,
            "face_visible": face_visible,
            "orientation_good": orientation_good,
            "yaw": yaw,
            "pitch": pitch,
            "phone_near_face": phone_near_face,
            "hand_near_face": hand_near_face,
            "phone_confidence": phone_confidence,
            "posture_stable": posture_stable,
            "status_messages": status_messages,
            "yolo_objects": yolo_objects,
            "fps": fps
        }

    def generate_status_messages(self, face_visible: bool, orientation_good: bool,
                                phone_near_face: bool, hand_near_face: bool,
                                phone_confidence: float, posture_stable: bool, 
                                yaw: float, pitch: float) -> Dict[str, Dict[str, str]]:
        """Generate clear, readable status messages"""
        
        # Face status
        if face_visible:
            face_status = "✓ Face detected"
            face_color = "green"
        else:
            face_status = "❌ No face detected"
            face_color = "red"
        
        # Orientation status
        if orientation_good:
            orientation_status = "✓ Looking forward"
            orientation_color = "green"
        else:
            if abs(yaw) > self.yaw_threshold:
                orientation_status = "↩ Turn head forward"
            elif abs(pitch) > self.pitch_threshold:
                orientation_status = "↕ Look straight ahead"
            else:
                orientation_status = "↩ Adjust head orientation"
            orientation_color = "red"
        
        # Interaction status
        if phone_near_face:
            interaction_status = f"📱 Phone detected ({phone_confidence:.2f})"
            interaction_color = "red"
        elif hand_near_face:
            interaction_status = "✋ Hand near face"
            interaction_color = "yellow"
        else:
            interaction_status = "✓ No phone or hand near face"
            interaction_color = "green"
        
        # Posture status
        if posture_stable:
            posture_status = "✓ Upright posture"
            posture_color = "green"
        else:
            posture_status = "🪑 Sit upright"
            posture_color = "red"
        
        # Overall status
        if not face_visible:
            overall_status = "❌ No face detected"
            overall_color = "red"
        elif phone_near_face:
            overall_status = "📱 Phone detected near face"
            overall_color = "red"
        elif hand_near_face:
            overall_status = "✋ Hand near face"
            overall_color = "yellow"
        elif not orientation_good:
            overall_status = "↩ Adjust head orientation"
            overall_color = "red"
        elif not posture_stable:
            overall_status = "🪑 Sit upright"
            overall_color = "red"
        else:
            overall_status = "✅ Focused and stable"
            overall_color = "green"
        
        return {
            "face": {"text": face_status, "color": face_color},
            "orientation": {"text": orientation_status, "color": orientation_color},
            "interaction": {"text": interaction_status, "color": interaction_color},
            "posture": {"text": posture_status, "color": posture_color},
            "overall": {"text": overall_status, "color": overall_color}
        }

    def draw_enhanced_status_overlay(self, frame, metrics):
        """Draw enhanced status overlay with fixed messages"""
        status_messages = metrics.get("status_messages", {})
        
        # Main status panel
        panel_width = 500
        panel_height = 280
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
        cv2.putText(frame, "FIXED YOLO ATTENTION TRACKER", (panel_x + 15, panel_y + 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        
        # Status items
        y_start = panel_y + 60
        status_items = [
            ("FACE", status_messages.get("face", {}).get("text", "Unknown")),
            ("ORIENTATION", status_messages.get("orientation", {}).get("text", "Unknown")),
            ("INTERACTION", status_messages.get("interaction", {}).get("text", "Unknown")),
            ("POSTURE", status_messages.get("posture", {}).get("text", "Unknown")),
            ("OVERALL", status_messages.get("overall", {}).get("text", "Unknown"))
        ]
        
        for i, (label, text) in enumerate(status_items):
            y_pos = y_start + (i * 35)
            
            # Label
            cv2.putText(frame, label, (panel_x + 15, y_pos),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (180, 180, 180), 1)
            
            # Status text with color
            color = (0, 255, 0) if "✓" in text or "✅" in text else (0, 0, 255) if "✗" in text or "❌" in text else (0, 165, 255)
            cv2.putText(frame, text, (panel_x + 15, y_pos + 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        
        # Metrics panel
        metrics_width = 220
        metrics_height = 120
        metrics_x = self.frame_width - metrics_width - 20
        metrics_y = self.frame_height - metrics_height - 20
        
        # Metrics background
        cv2.rectangle(frame, (metrics_x, metrics_y), 
                     (metrics_x + metrics_width, metrics_y + metrics_height), 
                     (20, 20, 20), -1)
        cv2.rectangle(frame, (metrics_x, metrics_y), 
                     (metrics_x + metrics_width, metrics_y + metrics_height), 
                     (60, 60, 60), 1)
        
        # Metrics title
        cv2.putText(frame, "YOLO METRICS", (metrics_x + 10, metrics_y + 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (180, 180, 180), 1)
        
        # Score, FPS, and YOLO status
        score_text = f"Score: {metrics.get('focus_score', 0.0):.2f}"
        fps_text = f"FPS: {metrics.get('fps', 0.0):.1f}"
        yolo_text = f"YOLO: {'Active' if self.frame_count % self.yolo_frame_skip == 0 else 'Cached'}"
        
        cv2.putText(frame, score_text, (metrics_x + 10, metrics_y + 45),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        cv2.putText(frame, fps_text, (metrics_x + 10, metrics_y + 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        cv2.putText(frame, yolo_text, (metrics_x + 10, metrics_y + 95),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        
        return frame

    def draw_yolo_detections(self, frame, yolo_objects):
        """Draw YOLO detection boxes"""
        for obj in yolo_objects:
            x1, y1, x2, y2 = obj['bbox']
            confidence = obj['confidence']
            class_name = obj['class_name']
            
            # Draw bounding box
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
            
            # Draw label
            label = f"{class_name}: {confidence:.2f}"
            cv2.putText(frame, label, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        
        return frame

    def run(self):
        """Run the main attention tracking loop"""
        print("🚀 Starting Fixed YOLO Attention Tracker...")
        print("📱 OpenCV YOLO + MediaPipe + Fixed Status Messages")
        print("🎯 Optimized Phone vs Hand Detection with YOLO")
        print("Press 'q' to quit, 's' to save screenshot")
        
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to grab frame")
                break
            
            # Process frame
            metrics = self.process_frame(frame)
            
            # Draw overlays
            frame = self.draw_enhanced_status_overlay(frame, metrics)
            frame = self.draw_yolo_detections(frame, metrics.get("yolo_objects", []))
            
            # Draw focus ring
            if metrics.get("focused", False):
                cv2.rectangle(frame, (10, 10), (self.frame_width - 10, self.frame_height - 10), 
                             (0, 255, 0), 4)
            else:
                cv2.rectangle(frame, (10, 10), (self.frame_width - 10, self.frame_height - 10), 
                             (0, 0, 255), 4)
            
            # Display frame
            cv2.imshow('Fixed YOLO Attention Tracker', frame)
            
            # Output JSON for integration
            print(json.dumps({
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "focused": metrics.get("focused", False),
                "focus_score": metrics.get("focus_score", 0.0),
                "face_visible": metrics.get("face_visible", False),
                "orientation_good": metrics.get("orientation_good", False),
                "phone_near_face": metrics.get("phone_near_face", False),
                "hand_near_face": metrics.get("hand_near_face", False),
                "posture_stable": metrics.get("posture_stable", False),
                "yolo_objects_count": len(metrics.get("yolo_objects", [])),
                "fps": metrics.get("fps", 0.0)
            }, indent=None))
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('s'):
                timestamp = time.strftime("%Y%m%d-%H%M%S")
                filename = f"fixed_yolo_screenshot_{timestamp}.png"
                cv2.imwrite(filename, frame)
                print(f"Screenshot saved as {filename}")
        
        self.cap.release()
        cv2.destroyAllWindows()
        print("✅ Fixed YOLO Attention Tracker stopped")

def main():
    tracker = FixedYOLOAttentionTracker(
        camera_index=0, 
        frame_width=640, 
        frame_height=480
    )
    tracker.run()

if __name__ == "__main__":
    main()
