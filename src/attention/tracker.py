import cv2
import mediapipe as mp
import numpy as np
from typing import Dict, Any, Optional

class FocusTracker:
    """
    MediaPipe-based tracker for face, hands, and pose detection.
    Provides real-time landmark detection for attention tracking.
    """
    
    def __init__(self):
        """Initialize MediaPipe solutions for face, hands, and pose detection."""
        # Initialize MediaPipe solutions
        self.face_mesh = mp.solutions.face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        self.hands = mp.solutions.hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        self.pose = mp.solutions.pose.Pose(
            static_image_mode=False,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        # Object detection for phone detection
        self.object_detection = mp.solutions.objectron.Objectron(
            static_image_mode=False,
            max_num_objects=5,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        # Rectangle detection for phone-like objects
        from rectangle_detector import RectangleDetector
        self.rectangle_detector = RectangleDetector()
        
        # Drawing utilities
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
    
    def process_frame(self, frame: np.ndarray) -> Dict[str, Any]:
        """
        Process a single frame and return detection results.
        
        Args:
            frame: Input BGR frame from webcam
            
        Returns:
            Dictionary containing face, hands, and pose detection results
        """
        # Convert BGR to RGB for MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process with MediaPipe
        face_results = self.face_mesh.process(rgb_frame)
        hands_results = self.hands.process(rgb_frame)
        pose_results = self.pose.process(rgb_frame)
        object_results = self.object_detection.process(rgb_frame)
        
        # Get face bounding box for rectangle detection
        face_bbox = None
        if face_results.multi_face_landmarks:
            face_landmarks = face_results.multi_face_landmarks[0]
            all_x, all_y = [], []
            for landmark in face_landmarks.landmark:
                all_x.append(landmark.x)
                all_y.append(landmark.y)
            h, w = frame.shape[:2]
            x_min = int(min(all_x) * w)
            x_max = int(max(all_x) * w)
            y_min = int(min(all_y) * h)
            y_max = int(max(all_y) * h)
            face_bbox = (x_min, y_min, x_max, y_max)
        
        # Detect rectangular objects (phones)
        rectangle_detections = self.rectangle_detector.detect_phone_objects(frame, face_bbox)
        
        # Extract landmarks and confidence scores
        face_landmarks = None
        face_detected = False
        if face_results.multi_face_landmarks:
            face_landmarks = face_results.multi_face_landmarks[0]
            face_detected = True
        
        hands_landmarks = []
        hands_detected = 0
        if hands_results.multi_hand_landmarks:
            hands_landmarks = hands_results.multi_hand_landmarks
            hands_detected = len(hands_landmarks)
        
        pose_landmarks = None
        pose_confidence = 0.0
        if pose_results.pose_landmarks:
            pose_landmarks = pose_results.pose_landmarks
            # Calculate average confidence from pose landmarks
            if hasattr(pose_landmarks, 'landmark'):
                confidences = []
                for landmark in pose_landmarks.landmark:
                    if hasattr(landmark, 'visibility'):
                        confidences.append(landmark.visibility)
                pose_confidence = np.mean(confidences) if confidences else 0.0
        
        # Extract object detection results (phones, etc.)
        objects_detected = []
        phone_detected = False
        if object_results.detected_objects:
            for detected_object in object_results.detected_objects:
                # Check if it's a phone (MediaPipe can detect phones)
                if hasattr(detected_object, 'category_name'):
                    if 'phone' in detected_object.category_name.lower():
                        phone_detected = True
                        objects_detected.append({
                            'type': 'phone',
                            'confidence': getattr(detected_object, 'confidence', 0.0),
                            'landmarks': getattr(detected_object, 'landmarks_2d', None)
                        })
        
        return {
            "face": {
                "face_detected": face_detected,
                "face_landmarks": face_landmarks,
                "face_results": face_results,
                "face_bbox": face_bbox
            },
            "hands": {
                "hands_detected": hands_detected,
                "hands_landmarks": hands_landmarks,
                "hands_results": hands_results
            },
            "pose": {
                "pose_confidence": pose_confidence,
                "pose_landmarks": pose_landmarks,
                "pose_results": pose_results
            },
            "objects": {
                "objects_detected": objects_detected,
                "phone_detected": phone_detected,
                "object_results": object_results
            },
            "rectangles": {
                "phone_objects": rectangle_detections.get("phone_objects", []),
                "phone_near_face": rectangle_detections.get("phone_near_face", False),
                "max_confidence": rectangle_detections.get("max_confidence", 0.0),
                "total_detections": rectangle_detections.get("total_detections", 0)
            }
        }
    
    def draw_landmarks(self, frame: np.ndarray, results: Dict[str, Any], 
                      draw_face: bool = True, draw_hands: bool = True, 
                      draw_pose: bool = True) -> np.ndarray:
        """
        Draw MediaPipe landmarks on the frame for visualization.
        
        Args:
            frame: Input frame
            results: Detection results from process_frame
            draw_face: Whether to draw face landmarks
            draw_hands: Whether to draw hand landmarks
            draw_pose: Whether to draw pose landmarks
            
        Returns:
            Frame with landmarks drawn
        """
        annotated_frame = frame.copy()
        
        # Draw face landmarks
        if draw_face and results["face"]["face_detected"]:
            face_landmarks = results["face"]["face_landmarks"]
            if face_landmarks:
                self.mp_drawing.draw_landmarks(
                    annotated_frame,
                    face_landmarks,
                    mp.solutions.face_mesh.FACEMESH_CONTOURS,
                    None,
                    self.mp_drawing_styles.get_default_face_mesh_contours_style()
                )
        
        # Draw hand landmarks
        if draw_hands and results["hands"]["hands_detected"] > 0:
            for hand_landmarks in results["hands"]["hands_landmarks"]:
                self.mp_drawing.draw_landmarks(
                    annotated_frame,
                    hand_landmarks,
                    mp.solutions.hands.HAND_CONNECTIONS,
                    self.mp_drawing_styles.get_default_hand_landmarks_style(),
                    self.mp_drawing_styles.get_default_hand_connections_style()
                )
        
        # Draw pose landmarks
        if draw_pose and results["pose"]["pose_landmarks"]:
            self.mp_drawing.draw_landmarks(
                annotated_frame,
                results["pose"]["pose_landmarks"],
                mp.solutions.pose.POSE_CONNECTIONS,
                self.mp_drawing_styles.get_default_pose_landmarks_style()
            )
        
        return annotated_frame
    
    def release(self):
        """Release MediaPipe resources."""
        # MediaPipe solutions don't need explicit release in newer versions
        pass
