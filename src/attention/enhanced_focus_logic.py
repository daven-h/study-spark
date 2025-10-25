"""
Enhanced Focus Logic with Phone vs Hand Detection
Uses YOLOv8 + MediaPipe for improved accuracy
"""

import time
from typing import Dict, Any, List
from .utils import calculate_yaw_pitch, is_posture_slouched


class EnhancedFocusEvaluator:
    """
    Enhanced focus evaluator with phone vs hand detection
    """
    
    def __init__(self):
        """Initialize the enhanced focus evaluator"""
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
        Evaluate focus with enhanced phone vs hand detection
        
        Args:
            detection_results: Results from enhanced tracker
            pose_data: Optional pose data for posture analysis
            
        Returns:
            Enhanced focus metrics
        """
        timestamp = time.time()
        
        # Extract detection data
        face_bbox = detection_results.get("face_bbox")
        phone_near_face = detection_results.get("phone_near_face", False)
        hand_near_face = detection_results.get("hand_near_face", False)
        interaction_state = detection_results.get("interaction_state", "no_interaction")
        interaction_confidence = detection_results.get("interaction_confidence", 0.0)
        phone_confidence = detection_results.get("phone_confidence", 0.0)
        
        # Face visibility
        face_visible = face_bbox is not None
        
        # Orientation analysis (if face landmarks available)
        yaw, pitch = 0.0, 0.0
        orientation_good = True
        if face_visible and pose_data and pose_data.get("pose_landmarks"):
            # Use pose landmarks for orientation if available
            pose_landmarks = pose_data["pose_landmarks"]
            # Calculate orientation from pose landmarks
            yaw, pitch = self._calculate_pose_orientation(pose_landmarks)
            orientation_good = abs(yaw) < self.yaw_threshold and abs(pitch) < self.pitch_threshold
        
        # Posture analysis
        posture_stable = True
        if pose_data and pose_data.get("pose_landmarks"):
            posture_stable = not is_posture_slouched(pose_data["pose_landmarks"], self.posture_threshold)
        
        # Enhanced interaction analysis
        distraction_reasons = []
        interaction_score = 1.0
        
        if phone_near_face:
            distraction_reasons.append("phone_near_face")
            interaction_score = 0.0  # Phone is always distracting
        elif hand_near_face:
            distraction_reasons.append("hand_near_face")
            interaction_score = 0.7  # Hand is less distracting than phone
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
        
        # Calculate enhanced focus score
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
        
        # Enhanced status messages
        status_messages = self._generate_status_messages(
            face_visible, orientation_good, interaction_state, 
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
            "interaction_confidence": interaction_confidence,
            "phone_confidence": phone_confidence,
            "posture_stable": posture_stable,
            "distraction_reasons": distraction_reasons,
            "status_messages": status_messages,
            "focus_components": focus_components
        }
    
    def _calculate_pose_orientation(self, pose_landmarks) -> tuple:
        """Calculate yaw and pitch from pose landmarks"""
        # Simplified orientation calculation from pose
        # This would need proper implementation based on pose landmarks
        return 0.0, 0.0
    
    def _generate_status_messages(self, face_visible: bool, orientation_good: bool,
                                interaction_state: str, phone_confidence: float,
                                posture_stable: bool, yaw: float, pitch: float) -> Dict[str, str]:
        """Generate enhanced status messages"""
        
        # Face status
        if face_visible:
            face_status = "✓ Face detected"
            face_color = "green"
        else:
            face_status = "✗ Look at camera"
            face_color = "red"
        
        # Orientation status
        if orientation_good:
            orientation_status = "✓ Looking forward"
            orientation_color = "green"
        else:
            if abs(yaw) > self.yaw_threshold:
                orientation_status = "✗ Turn head forward"
            else:
                orientation_status = "✗ Look straight ahead"
            orientation_color = "red"
        
        # Enhanced interaction status
        if interaction_state == "phone_near_head":
            interaction_status = f"✗ Phone detected ({phone_confidence:.2f})"
            interaction_color = "red"
        elif interaction_state == "hand_near_head":
            interaction_status = "⚠ Hand near head"
            interaction_color = "yellow"
        else:
            interaction_status = "✓ No interaction"
            interaction_color = "green"
        
        # Posture status
        if posture_stable:
            posture_status = "✓ Good posture"
            posture_color = "green"
        else:
            posture_status = "✗ Straighten up"
            posture_color = "red"
        
        return {
            "face": {"text": face_status, "color": face_color},
            "orientation": {"text": orientation_status, "color": orientation_color},
            "interaction": {"text": interaction_status, "color": interaction_color},
            "posture": {"text": posture_status, "color": posture_color}
        }
