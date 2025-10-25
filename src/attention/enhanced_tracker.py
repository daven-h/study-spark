"""
Enhanced Attention Tracker with YOLOv8 + MediaPipe
Detects phone vs hand near head with improved accuracy
"""

import cv2
import numpy as np
import time
from typing import Dict, List, Tuple, Any, Optional
import mediapipe as mp
from ultralytics import YOLO


class EnhancedFocusTracker:
    """
    Enhanced focus tracker using YOLOv8 for phone detection and MediaPipe for pose/face
    """
    
    def __init__(self):
        """Initialize the enhanced tracker with YOLOv8 and MediaPipe"""
        # Initialize YOLOv8 model for phone detection
        try:
            self.yolo_model = YOLO('yolov8n.pt')  # Lightweight model
            self.yolo_enabled = True
            print("✅ YOLOv8 model loaded successfully")
        except Exception as e:
            print(f"⚠️ YOLOv8 not available: {e}")
            self.yolo_model = None
            self.yolo_enabled = False
        
        # MediaPipe solutions
        self.mp_face_mesh = mp.solutions.face_mesh
        self.mp_hands = mp.solutions.hands
        self.mp_pose = mp.solutions.pose
        
        # Initialize MediaPipe models
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            refine_landmarks=True,
            max_num_faces=1,
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
        
        # Detection state tracking
        self.frame_count = 0
        self.yolo_update_interval = 10  # Run YOLO every 10 frames
        self.last_phone_detection = None
        self.last_phone_confidence = 0.0
        
        # Drawing utilities
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        
    def detect_phones_yolo(self, frame: np.ndarray) -> List[Tuple[Tuple[int, int, int, int], float]]:
        """
        Detect phones using YOLOv8
        
        Args:
            frame: Input frame
            
        Returns:
            List of (bbox, confidence) tuples for detected phones
        """
        if not self.yolo_enabled:
            return []
            
        try:
            results = self.yolo_model(frame, verbose=False)
            phones = []
            
            for result in results:
                if result.boxes is not None:
                    for box in result.boxes:
                        cls_id = int(box.cls[0])
                        cls_name = self.yolo_model.names[cls_id]
                        confidence = float(box.conf[0])
                        
                        # Check if it's a phone-related class
                        if any(phone_word in cls_name.lower() for phone_word in 
                              ["cell phone", "mobile phone", "phone", "telephone"]):
                            x1, y1, x2, y2 = map(int, box.xyxy[0])
                            phones.append(((x1, y1, x2, y2), confidence))
                            
            return phones
            
        except Exception as e:
            print(f"YOLO detection error: {e}")
            return []
    
    def detect_face_bbox(self, frame: np.ndarray) -> Optional[Tuple[int, int, int, int]]:
        """
        Detect face bounding box using MediaPipe
        
        Args:
            frame: Input frame
            
        Returns:
            Face bounding box (x1, y1, x2, y2) or None
        """
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb)
        
        if results.multi_face_landmarks:
            face_landmarks = results.multi_face_landmarks[0]
            all_x, all_y = [], []
            
            for landmark in face_landmarks.landmark:
                all_x.append(landmark.x)
                all_y.append(landmark.y)
            
            h, w = frame.shape[:2]
            x_min = int(min(all_x) * w)
            x_max = int(max(all_x) * w)
            y_min = int(min(all_y) * h)
            y_max = int(max(all_y) * h)
            
            return (x_min, y_min, x_max, y_max)
        
        return None
    
    def detect_hand_landmarks(self, frame: np.ndarray) -> List[List[Tuple[float, float]]]:
        """
        Detect hand landmarks using MediaPipe
        
        Args:
            frame: Input frame
            
        Returns:
            List of hand landmark coordinates
        """
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb)
        
        hand_points = []
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                coords = [(lm.x, lm.y) for lm in hand_landmarks.landmark]
                hand_points.append(coords)
        
        return hand_points
    
    def is_phone_near_face(self, phones: List[Tuple[Tuple[int, int, int, int], float]], 
                          face_bbox: Tuple[int, int, int, int], 
                          threshold: float = 0.5) -> Tuple[bool, float]:
        """
        Check if any detected phone is near the face
        
        Args:
            phones: List of (bbox, confidence) tuples
            face_bbox: Face bounding box (x1, y1, x2, y2)
            threshold: Confidence threshold
            
        Returns:
            (is_phone_near, max_confidence)
        """
        if not phones or not face_bbox:
            return False, 0.0
        
        fx1, fy1, fx2, fy2 = face_bbox
        max_confidence = 0.0
        phone_near = False
        
        for (px1, py1, px2, py2), conf in phones:
            if conf > threshold:
                # Check if phone bbox overlaps with face area (with some margin)
                margin = 50
                if (px2 > fx1 - margin and px1 < fx2 + margin and 
                    py2 > fy1 - margin and py1 < fy2 + margin):
                    phone_near = True
                    max_confidence = max(max_confidence, conf)
        
        return phone_near, max_confidence
    
    def is_hand_near_face(self, hand_landmarks: List[List[Tuple[float, float]]], 
                         face_bbox: Tuple[int, int, int, int], 
                         frame_shape: Tuple[int, int]) -> bool:
        """
        Check if any hand is near the face
        
        Args:
            hand_landmarks: List of hand landmark coordinates
            face_bbox: Face bounding box (x1, y1, x2, y2)
            frame_shape: Frame dimensions (height, width)
            
        Returns:
            True if hand is near face
        """
        if not hand_landmarks or not face_bbox:
            return False
        
        fx1, fy1, fx2, fy2 = face_bbox
        h, w = frame_shape[:2]
        
        for hand in hand_landmarks:
            for hx, hy in hand:
                # Convert normalized coordinates to pixel coordinates
                px = int(hx * w)
                py = int(hy * h)
                
                # Check if hand point is near face (with margin)
                margin = 80
                if (fx1 - margin < px < fx2 + margin and 
                    fy1 - margin < py < fy2 + margin):
                    return True
        
        return False
    
    def process_frame(self, frame: np.ndarray) -> Dict[str, Any]:
        """
        Process frame with enhanced phone vs hand detection
        
        Args:
            frame: Input frame
            
        Returns:
            Dictionary with detection results
        """
        self.frame_count += 1
        
        # Always run MediaPipe for face and hands
        face_bbox = self.detect_face_bbox(frame)
        hand_landmarks = self.detect_hand_landmarks(frame)
        
        # Run YOLO periodically for phone detection
        phones = []
        if self.yolo_enabled and (self.frame_count % self.yolo_update_interval == 0):
            phones = self.detect_phones_yolo(frame)
            if phones:
                self.last_phone_detection = phones
                self.last_phone_confidence = max(conf for _, conf in phones)
        elif self.last_phone_detection:
            # Use cached phone detection
            phones = self.last_phone_detection
        
        # Determine interaction state
        phone_near_face = False
        hand_near_face = False
        phone_confidence = 0.0
        
        if face_bbox:
            phone_near_face, phone_confidence = self.is_phone_near_face(phones, face_bbox)
            hand_near_face = self.is_hand_near_face(hand_landmarks, face_bbox, frame.shape)
        
        # Classify the interaction
        if phone_near_face:
            interaction_state = "phone_near_head"
            interaction_confidence = phone_confidence
        elif hand_near_face:
            interaction_state = "hand_near_head"
            interaction_confidence = 0.8  # High confidence for hand detection
        else:
            interaction_state = "no_interaction"
            interaction_confidence = 0.0
        
        return {
            "face_bbox": face_bbox,
            "hand_landmarks": hand_landmarks,
            "phones": phones,
            "phone_near_face": phone_near_face,
            "hand_near_face": hand_near_face,
            "interaction_state": interaction_state,
            "interaction_confidence": interaction_confidence,
            "phone_confidence": phone_confidence,
            "frame_count": self.frame_count
        }
    
    def draw_detections(self, frame: np.ndarray, results: Dict[str, Any]) -> np.ndarray:
        """
        Draw detection results on frame
        
        Args:
            frame: Input frame
            results: Detection results
            
        Returns:
            Frame with visualizations
        """
        # Draw face bbox
        if results["face_bbox"]:
            fx1, fy1, fx2, fy2 = results["face_bbox"]
            cv2.rectangle(frame, (fx1, fy1), (fx2, fy2), (0, 255, 0), 2)
            cv2.putText(frame, "Face", (fx1, fy1 - 10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        # Draw phone detections
        for (px1, py1, px2, py2), conf in results["phones"]:
            color = (0, 0, 255) if results["phone_near_face"] else (255, 0, 0)
            cv2.rectangle(frame, (px1, py1), (px2, py2), color, 2)
            cv2.putText(frame, f"Phone {conf:.2f}", (px1, py1 - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        
        # Draw hand landmarks
        for hand in results["hand_landmarks"]:
            for hx, hy in hand:
                h, w = frame.shape[:2]
                px = int(hx * w)
                py = int(hy * h)
                cv2.circle(frame, (px, py), 3, (0, 255, 255), -1)
        
        return frame
