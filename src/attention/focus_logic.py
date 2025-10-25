import time
from typing import Dict, Any, List
from utils import (
    calculate_yaw_pitch, is_hand_near_face, is_posture_slouched,
    calculate_face_orientation, is_face_centered, calculate_focus_quality
)

class FocusEvaluator:
    """
    Core attention and focus evaluation logic.
    Determines if a person is focused based on face, hands, and posture analysis.
    """
    
    def __init__(self):
        """Initialize focus evaluator with default thresholds."""
        # Focus thresholds
        self.yaw_threshold = 0.25      # Maximum yaw deviation (left-right)
        self.pitch_threshold = 0.35    # Maximum pitch deviation (up-down)
        self.hand_face_threshold = 0.15 # Hand near face threshold
        self.posture_threshold = 0.1   # Posture slouching threshold
        
        # Focus state tracking
        self.focus_history = []
        self.max_history = 10  # Keep last 10 frames for smoothing
        
        # Focus quality weights
        self.weights = {
            "face_visible": 0.3,
            "face_orientation": 0.25,
            "hand_position": 0.2,
            "posture": 0.15,
            "face_centered": 0.1
        }
    
    def evaluate_focus(self, face_data: Dict[str, Any], hands_data: Dict[str, Any], 
                      pose_data: Dict[str, Any], frame_width: int = 640, 
                      frame_height: int = 480, objects_data: Dict[str, Any] = None, 
                      results: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Evaluate focus state based on face, hands, and pose data.
        
        Args:
            face_data: Face detection results
            hands_data: Hands detection results
            pose_data: Pose detection results
            frame_width: Frame width for centering calculation
            frame_height: Frame height for centering calculation
            
        Returns:
            Dictionary containing focus evaluation results
        """
        # Extract data
        face_detected = face_data["face_detected"]
        face_landmarks = face_data["face_landmarks"]
        hands_detected = hands_data["hands_detected"]
        hands_landmarks = hands_data["hands_landmarks"]
        pose_landmarks = pose_data["pose_landmarks"]
        pose_confidence = pose_data["pose_confidence"]
        
        # Extract object detection data
        if objects_data:
            phone_detected = objects_data.get("phone_detected", False)
            objects_detected = objects_data.get("objects_detected", [])
        else:
            phone_detected = False
            objects_detected = []
        
        # Extract rectangle detection data
        if results:
            rectangles_data = results.get("rectangles", {})
            rectangle_phone_near_face = rectangles_data.get("phone_near_face", False)
            rectangle_phone_objects = rectangles_data.get("phone_objects", [])
            rectangle_confidence = rectangles_data.get("max_confidence", 0.0)
        else:
            rectangle_phone_near_face = False
            rectangle_phone_objects = []
            rectangle_confidence = 0.0
        
        # Initialize focus metrics
        focus_metrics = {
            "timestamp": time.time(),
            "face_visible": face_detected,
            "hands_detected": hands_detected,
            "pose_confidence": pose_confidence,
            "focused": False,
            "focus_score": 0.0,
            "yaw": 0.0,
            "pitch": 0.0,
            "hand_near_face": False,
            "posture_stable": True,
            "face_centered": False,
            "distraction_reasons": []
        }
        
        # 1. Face visibility check
        if not face_detected:
            focus_metrics["distraction_reasons"].append("face_not_visible")
            focus_metrics["focus_score"] = 0.0
            focus_metrics["focused"] = False
            self._update_focus_history(focus_metrics)
            return focus_metrics
        
        # 2. Face orientation analysis
        yaw, pitch = calculate_yaw_pitch(face_landmarks)
        focus_metrics["yaw"] = yaw
        focus_metrics["pitch"] = pitch
        
        # Check if looking away
        looking_away = (abs(yaw) > self.yaw_threshold or 
                       abs(pitch) > self.pitch_threshold)
        
        if looking_away:
            if abs(yaw) > self.yaw_threshold:
                focus_metrics["distraction_reasons"].append("looking_sideways")
            if abs(pitch) > self.pitch_threshold:
                focus_metrics["distraction_reasons"].append("looking_up_down")
        
        # 3. Hand position and phone detection analysis
        hand_near_face = is_hand_near_face(hands_landmarks, face_landmarks, 
                                          self.hand_face_threshold)
        
        # Check for phone object detection (YOLO + Rectangle detection)
        phone_near_face = phone_detected or hand_near_face or rectangle_phone_near_face
        focus_metrics["hand_near_face"] = phone_near_face
        focus_metrics["phone_detected"] = phone_detected
        focus_metrics["rectangle_phone_detected"] = rectangle_phone_near_face
        focus_metrics["rectangle_confidence"] = rectangle_confidence
        
        if phone_near_face:
            if phone_detected:
                focus_metrics["distraction_reasons"].append("phone_detected")
            elif rectangle_phone_near_face:
                focus_metrics["distraction_reasons"].append("rectangle_phone_detected")
            else:
                focus_metrics["distraction_reasons"].append("hand_near_face")
        
        # 4. Posture analysis
        posture_stable = not is_posture_slouched(pose_landmarks, self.posture_threshold)
        focus_metrics["posture_stable"] = posture_stable
        
        if not posture_stable:
            focus_metrics["distraction_reasons"].append("poor_posture")
        
        # 5. Face centering check
        face_centered = is_face_centered(face_landmarks, frame_width, frame_height)
        focus_metrics["face_centered"] = face_centered
        
        if not face_centered:
            focus_metrics["distraction_reasons"].append("face_not_centered")
        
        # 6. Calculate overall focus score
        focus_score = self._calculate_focus_score(
            face_detected, not looking_away, not hand_near_face, 
            posture_stable, face_centered
        )
        focus_metrics["focus_score"] = focus_score
        
        # 7. Determine if focused (with smoothing)
        focused = self._determine_focus_state(focus_score)
        focus_metrics["focused"] = focused
        
        # Update focus history for smoothing
        self._update_focus_history(focus_metrics)
        
        return focus_metrics
    
    def _calculate_focus_score(self, face_visible: bool, face_orientation_good: bool,
                             hand_position_good: bool, posture_good: bool, 
                             face_centered: bool) -> float:
        """
        Calculate weighted focus score based on multiple factors.
        
        Args:
            face_visible: Whether face is detected
            face_orientation_good: Whether face orientation is good
            hand_position_good: Whether hands are not near face
            posture_good: Whether posture is good
            face_centered: Whether face is centered
            
        Returns:
            Focus score between 0.0 and 1.0
        """
        if not face_visible:
            return 0.0
        
        score = 0.0
        score += self.weights["face_visible"] * (1.0 if face_visible else 0.0)
        score += self.weights["face_orientation"] * (1.0 if face_orientation_good else 0.0)
        score += self.weights["hand_position"] * (1.0 if hand_position_good else 0.0)
        score += self.weights["posture"] * (1.0 if posture_good else 0.0)
        score += self.weights["face_centered"] * (1.0 if face_centered else 0.0)
        
        return min(1.0, max(0.0, score))
    
    def _determine_focus_state(self, focus_score: float, threshold: float = 0.7) -> bool:
        """
        Determine if person is focused based on score and history.
        
        Args:
            focus_score: Current focus score
            threshold: Focus threshold
            
        Returns:
            True if focused, False otherwise
        """
        # Use history for smoothing to avoid flickering
        if len(self.focus_history) < 3:
            return focus_score >= threshold
        
        # Get recent focus scores
        recent_scores = [entry["focus_score"] for entry in self.focus_history[-3:]]
        avg_score = sum(recent_scores) / len(recent_scores)
        
        # Focused if current score and recent average are above threshold
        return focus_score >= threshold and avg_score >= (threshold * 0.8)
    
    def _update_focus_history(self, focus_metrics: Dict[str, Any]):
        """Update focus history for smoothing."""
        self.focus_history.append(focus_metrics.copy())
        if len(self.focus_history) > self.max_history:
            self.focus_history.pop(0)
    
    def get_focus_summary(self) -> Dict[str, Any]:
        """
        Get summary of recent focus state.
        
        Returns:
            Dictionary with focus summary statistics
        """
        if not self.focus_history:
            return {"focused_percentage": 0.0, "avg_score": 0.0, "total_frames": 0}
        
        focused_count = sum(1 for entry in self.focus_history if entry["focused"])
        avg_score = sum(entry["focus_score"] for entry in self.focus_history) / len(self.focus_history)
        
        return {
            "focused_percentage": (focused_count / len(self.focus_history)) * 100,
            "avg_score": avg_score,
            "total_frames": len(self.focus_history),
            "recent_focused": self.focus_history[-1]["focused"] if self.focus_history else False
        }
    
    def reset_history(self):
        """Reset focus history."""
        self.focus_history = []
    
    def update_thresholds(self, yaw: float = None, pitch: float = None, 
                         hand_face: float = None, posture: float = None):
        """
        Update focus evaluation thresholds.
        
        Args:
            yaw: New yaw threshold
            pitch: New pitch threshold
            hand_face: New hand near face threshold
            posture: New posture threshold
        """
        if yaw is not None:
            self.yaw_threshold = yaw
        if pitch is not None:
            self.pitch_threshold = pitch
        if hand_face is not None:
            self.hand_face_threshold = hand_face
        if posture is not None:
            self.posture_threshold = posture

# Convenience function for simple focus evaluation
def evaluate_focus(face_data: Dict[str, Any], hands_data: Dict[str, Any], 
                  pose_data: Dict[str, Any], frame_width: int = 640, 
                  frame_height: int = 480) -> Dict[str, Any]:
    """
    Simple function to evaluate focus without creating an evaluator instance.
    
    Args:
        face_data: Face detection results
        hands_data: Hands detection results
        pose_data: Pose detection results
        frame_width: Frame width
        frame_height: Frame height
        
    Returns:
        Focus evaluation results
    """
    evaluator = FocusEvaluator()
    return evaluator.evaluate_focus(face_data, hands_data, pose_data, frame_width, frame_height)
