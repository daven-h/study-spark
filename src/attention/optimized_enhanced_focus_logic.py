"""
Optimized Enhanced Focus Logic with YOLO + MediaPipe Integration
Properly distinguishes phone vs hand interactions using real detection data
"""

import time
import numpy as np
from typing import Dict, Any, List, Tuple, Optional
try:
    from .utils import calculate_yaw_pitch, is_posture_slouched
except ImportError:
    from utils import calculate_yaw_pitch, is_posture_slouched


class OptimizedEnhancedFocusEvaluator:
    """
    Optimized focus evaluator with proper YOLO + MediaPipe integration
    """
    
    def __init__(self):
        """Initialize the optimized focus evaluator"""
        # Focus thresholds
        self.yaw_threshold = 0.25
        self.pitch_threshold = 0.35
        self.posture_threshold = 0.3
        
        # Interaction weights
        self.weights = {
            "face_visibility": 0.3,
            "orientation": 0.25,
            "phone_interaction": 0.25,  # Higher weight for phone detection
            "hand_interaction": 0.1,   # Lower weight for hand-only
            "posture": 0.1
        }
    
    def evaluate_focus(self, detection_results: Dict[str, Any], 
                       pose_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Evaluate focus with optimized YOLO + MediaPipe integration
        
        Args:
            detection_results: Results from enhanced tracker with YOLO + MediaPipe
            pose_data: Optional pose data for posture analysis
            
        Returns:
            Optimized focus metrics with human-readable status
        """
        timestamp = time.time()
        
        # Extract YOLO results
        yolo_objects = detection_results.get("yolo_objects", [])
        phone_boxes = [(obj["x1"], obj["y1"], obj["x2"], obj["y2"]) 
                       for obj in yolo_objects if "phone" in obj.get("class", "").lower()]
        
        # Extract MediaPipe results
        face_bbox = detection_results.get("face_bbox")
        hand_landmarks = detection_results.get("hand_landmarks", [])
        face_landmarks = detection_results.get("face_landmarks")
        
        # Face visibility
        face_visible = face_bbox is not None
        
        # Phone detection using YOLO + face overlap
        phone_near_face = False
        phone_confidence = 0.0
        if face_bbox and phone_boxes:
            phone_near_face, phone_confidence = self._is_phone_near_face(face_bbox, phone_boxes)
        
        # Hand detection using MediaPipe landmarks
        hand_near_face = False
        if face_bbox and hand_landmarks:
            hand_near_face = self._is_hand_near_face(face_bbox, hand_landmarks)
        
        # Orientation analysis from face landmarks
        yaw, pitch = 0.0, 0.0
        orientation_good = True
        if face_visible and face_landmarks:
            yaw, pitch = self._calculate_face_orientation(face_landmarks)
            orientation_good = abs(yaw) < self.yaw_threshold and abs(pitch) < self.pitch_threshold
        
        # Posture analysis from pose landmarks
        posture_stable = True
        if pose_data and pose_data.get("pose_landmarks"):
            pose_landmarks = pose_data["pose_landmarks"]
            try:
                shoulders = pose_landmarks.landmark[11]
                hips = pose_landmarks.landmark[23]
                posture_stable = (hips.y - shoulders.y) > self.posture_threshold
            except (IndexError, AttributeError):
                # Fallback to original method if pose landmarks are invalid
                posture_stable = not is_posture_slouched(pose_landmarks, self.posture_threshold)
        
        # Enhanced interaction analysis
        distraction_reasons = []
        interaction_score = 1.0
        interaction_state = "no_interaction"
        
        if phone_near_face:
            distraction_reasons.append("phone_near_face")
            interaction_score = 0.0  # Phone is always distracting
            interaction_state = "phone_near_head"
        elif hand_near_face:
            distraction_reasons.append("hand_near_face")
            interaction_score = 0.7  # Hand is less distracting than phone
            interaction_state = "hand_near_head"
        else:
            distraction_reasons.append("no_interaction")
        
        if not face_visible:
            distraction_reasons.append("face_not_visible")
        
        if not orientation_good:
            if abs(yaw) > self.yaw_threshold:
                distraction_reasons.append("looking_sideways")
            if abs(pitch) > self.pitch_threshold:
                distraction_reasons.append("looking_up_down")
        
        if not posture_stable:
            distraction_reasons.append("poor_posture")
        
        # Calculate optimized focus score
        focus_components = {
            "face_visibility": 1.0 if face_visible else 0.0,
            "orientation": 1.0 if orientation_good else 0.0,
            "phone_interaction": 0.0 if phone_near_face else 1.0,
            "hand_interaction": interaction_score,
            "posture": 1.0 if posture_stable else 0.0
        }
        
        # Weighted focus score
        focus_score = sum(
            self.weights[component] * score 
            for component, score in focus_components.items()
        )
        
        # Overall focus determination
        focused = (focus_score > 0.7 and 
                  not phone_near_face and 
                  face_visible and 
                  orientation_good)
        
        # Generate smart status messages
        status_messages = self._generate_smart_status_messages(
            face_visible, orientation_good, phone_near_face, hand_near_face,
            phone_confidence, posture_stable, yaw, pitch
        )
        
        return {
            "timestamp": timestamp,
            "focused": focused,
            "focus_score": focus_score,
            "face_visible": face_visible,
            "orientation_good": orientation_good,
            "yaw": yaw,
            "pitch": pitch,
            "phone_near_face": phone_near_face,
            "hand_near_face": hand_near_face,
            "interaction_state": interaction_state,
            "phone_confidence": phone_confidence,
            "posture_stable": posture_stable,
            "distraction_reasons": distraction_reasons,
            "status_messages": status_messages,
            "focus_components": focus_components
        }
    
    def _is_phone_near_face(self, face_box: Tuple[int, int, int, int], 
                           phone_boxes: List[Tuple[int, int, int, int]], 
                           threshold: float = 0.1) -> Tuple[bool, float]:
        """
        Check if phone boxes overlap with face area
        
        Args:
            face_box: Face bounding box (x1, y1, x2, y2)
            phone_boxes: List of phone bounding boxes
            threshold: Overlap threshold for detection
            
        Returns:
            Tuple of (is_near_face, max_confidence)
        """
        fx1, fy1, fx2, fy2 = face_box
        face_area = (fx2 - fx1) * (fy2 - fy1)
        max_confidence = 0.0
        is_near_face = False
        
        for (x1, y1, x2, y2) in phone_boxes:
            # Calculate overlap
            overlap_x = max(0, min(fx2, x2) - max(fx1, x1))
            overlap_y = max(0, min(fy2, y2) - max(fy1, y1))
            overlap_area = overlap_x * overlap_y
            
            if face_area > 0:
                overlap_ratio = overlap_area / face_area
                if overlap_ratio > threshold:
                    is_near_face = True
                    max_confidence = max(max_confidence, overlap_ratio)
        
        return is_near_face, max_confidence
    
    def _is_hand_near_face(self, face_box: Tuple[int, int, int, int], 
                          hands: List, margin: float = 0.15) -> bool:
        """
        Check if hand landmarks are near face area
        
        Args:
            face_box: Face bounding box (x1, y1, x2, y2)
            hands: List of hand landmarks
            margin: Distance margin for detection
            
        Returns:
            True if hand is near face
        """
        fx1, fy1, fx2, fy2 = face_box
        face_center_x = (fx1 + fx2) / 2
        face_center_y = (fy1 + fy2) / 2
        
        for hand in hands:
            for lm in hand.landmark:
                # Convert normalized coordinates to pixel coordinates
                x = lm.x * 640  # Assuming 640x480 frame
                y = lm.y * 480
                
                # Check distance to face center
                distance = np.sqrt((x - face_center_x)**2 + (y - face_center_y)**2)
                if distance < margin * 100:  # Scale margin to pixels
                    return True
        
        return False
    
    def _calculate_face_orientation(self, face_landmarks) -> Tuple[float, float]:
        """
        Calculate yaw and pitch from face landmarks
        
        Args:
            face_landmarks: MediaPipe face landmarks
            
        Returns:
            Tuple of (yaw, pitch)
        """
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
    
    def _generate_smart_status_messages(self, face_visible: bool, orientation_good: bool,
                                      phone_near_face: bool, hand_near_face: bool,
                                      phone_confidence: float, posture_stable: bool, 
                                      yaw: float, pitch: float) -> Dict[str, Dict[str, str]]:
        """
        Generate smart, human-readable status messages
        
        Args:
            face_visible: Whether face is detected
            orientation_good: Whether head orientation is good
            phone_near_face: Whether phone is detected near face
            hand_near_face: Whether hand is detected near face
            phone_confidence: Confidence of phone detection
            posture_stable: Whether posture is stable
            yaw: Yaw angle
            pitch: Pitch angle
            
        Returns:
            Dictionary of status messages with colors
        """
        
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
        
        # Enhanced interaction status
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
