"""
Final YOLO-Integrated Attention Tracker
Uses OpenCV-based YOLO + MediaPipe for robust phone detection
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
from optimized_enhanced_focus_logic import OptimizedEnhancedFocusEvaluator

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

class FinalYOLOAttentionTracker:
    """
    Final YOLO-Integrated Attention Tracker
    Combines OpenCV YOLO + MediaPipe for accurate phone detection
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
        
        # Initialize enhanced focus evaluator
        self.focus_evaluator = OptimizedEnhancedFocusEvaluator()
        
        # Performance optimization
        self.fps_counter = FPSCounter()
        self.yolo_frame_skip = 4  # Run YOLO every 4th frame for better performance
        self.last_yolo_results = []
        
        # Threading for YOLO
        self.yolo_thread = None
        self.yolo_results_lock = threading.Lock()
        self.executor = ThreadPoolExecutor(max_workers=2)
        
        print(f"✅ Final YOLO Attention Tracker initialized: {self.frame_width}x{self.frame_height}")
        print("📱 OpenCV YOLO + MediaPipe + Enhanced Focus Logic")
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
        detection_results = {
            "face_bbox": None,
            "face_landmarks": None,
            "hand_landmarks": [],
            "yolo_objects": []
        }
        
        # Extract face bounding box and landmarks
        if face_results.multi_face_landmarks:
            face_landmarks = face_results.multi_face_landmarks[0]
            detection_results["face_landmarks"] = face_landmarks
            
            # Calculate face bounding box
            all_x, all_y = [], []
            for landmark in face_landmarks.landmark:
                all_x.append(landmark.x)
                all_y.append(landmark.y)
            
            x_min = int(min(all_x) * self.frame_width)
            x_max = int(max(all_x) * self.frame_width)
            y_min = int(min(all_y) * self.frame_height)
            y_max = int(max(all_y) * self.frame_height)
            detection_results["face_bbox"] = (x_min, y_min, x_max, y_max)
        
        # Extract hand landmarks
        if hands_results.multi_hand_landmarks:
            detection_results["hand_landmarks"] = hands_results.multi_hand_landmarks
        
        # YOLO phone detection (every nth frame)
        if self.frame_count % self.yolo_frame_skip == 0:
            # Run YOLO in background thread
            if self.yolo_thread is None or not self.yolo_thread.is_alive():
                self.yolo_thread = threading.Thread(target=self.run_yolo_detection_async, args=(frame,))
                self.yolo_thread.start()
        
        # Get latest YOLO results
        with self.yolo_results_lock:
            detection_results["yolo_objects"] = self.last_yolo_results.copy()
        
        # Prepare pose data for focus evaluator
        pose_data = {
            "pose_landmarks": pose_results.pose_landmarks
        }
        
        # Evaluate focus using optimized evaluator
        focus_metrics = self.focus_evaluator.evaluate_focus(detection_results, pose_data)
        
        # Add FPS
        focus_metrics["fps"] = self.fps_counter.get_fps()
        
        return focus_metrics

    def draw_enhanced_status_overlay(self, frame, metrics):
        """Draw enhanced status overlay with smart messages"""
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
        cv2.putText(frame, "FINAL YOLO ATTENTION TRACKER", (panel_x + 15, panel_y + 30),
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

    def draw_landmarks(self, frame, detection_results):
        """Draw MediaPipe landmarks"""
        # Draw face mesh
        if detection_results.get("face_landmarks"):
            self.mp_drawing.draw_landmarks(
                frame, detection_results["face_landmarks"],
                self.mp_face_mesh.FACEMESH_CONTOURS,
                None,
                self.mp_drawing_styles.get_default_face_mesh_contours_style()
            )
        
        # Draw hands
        if detection_results.get("hand_landmarks"):
            for hand_landmarks in detection_results["hand_landmarks"]:
                self.mp_drawing.draw_landmarks(
                    frame, hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS,
                    self.mp_drawing_styles.get_default_hand_landmarks_style(),
                    self.mp_drawing_styles.get_default_hand_connections_style()
                )
        
        return frame

    def run(self):
        """Run the main attention tracking loop"""
        print("🚀 Starting Final YOLO Attention Tracker...")
        print("📱 OpenCV YOLO + MediaPipe + Enhanced Focus Logic")
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
            cv2.imshow('Final YOLO Attention Tracker', frame)
            
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
                filename = f"yolo_screenshot_{timestamp}.png"
                cv2.imwrite(filename, frame)
                print(f"Screenshot saved as {filename}")
        
        self.cap.release()
        cv2.destroyAllWindows()
        self.executor.shutdown(wait=True)
        print("✅ Final YOLO Attention Tracker stopped")

def main():
    tracker = FinalYOLOAttentionTracker(
        camera_index=0, 
        frame_width=640, 
        frame_height=480
    )
    tracker.run()

if __name__ == "__main__":
    main()
