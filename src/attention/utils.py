import numpy as np
import math
from typing import List, Tuple, Optional, Any, Dict

def distance(point1: Tuple[float, float], point2: Tuple[float, float]) -> float:
    """
    Calculate Euclidean distance between two 2D points.
    
    Args:
        point1: First point (x, y)
        point2: Second point (x, y)
        
    Returns:
        Distance between the points
    """
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def calculate_yaw_pitch(face_landmarks: Any) -> Tuple[float, float]:
    """
    Calculate yaw and pitch angles from face landmarks.
    
    Args:
        face_landmarks: MediaPipe face landmarks
        
    Returns:
        Tuple of (yaw, pitch) in radians
    """
    if not face_landmarks or not hasattr(face_landmarks, 'landmark'):
        return 0.0, 0.0
    
    # Key face landmarks for head pose estimation
    # Using nose tip, chin, left/right eye corners, and forehead
    landmarks = face_landmarks.landmark
    
    # Nose tip (1), Chin (152), Left eye corner (33), Right eye corner (362)
    # Forehead (10), Left ear (234), Right ear (454)
    nose_tip = landmarks[1]
    chin = landmarks[152]
    left_eye = landmarks[33]
    right_eye = landmarks[362]
    forehead = landmarks[10]
    left_ear = landmarks[234]
    right_ear = landmarks[454]
    
    # Calculate yaw (left-right rotation)
    # Use the difference between left and right ear positions
    ear_center_x = (left_ear.x + right_ear.x) / 2
    nose_x = nose_tip.x
    yaw = (nose_x - ear_center_x) * 2  # Scale factor for sensitivity
    
    # Calculate pitch (up-down rotation)
    # Use the vertical relationship between nose, chin, and forehead
    nose_y = nose_tip.y
    chin_y = chin.y
    forehead_y = forehead.y
    
    # Normalize by face height
    face_height = abs(chin_y - forehead_y)
    if face_height > 0:
        pitch = (nose_y - (chin_y + forehead_y) / 2) / face_height * 2
    else:
        pitch = 0.0
    
    return yaw, pitch

def is_hand_near_face(hand_landmarks: List[Any], face_landmarks: Any, 
                     threshold: float = 0.15) -> bool:
    """
    Check if any hand is near the face (potential phone usage).
    
    Args:
        hand_landmarks: List of MediaPipe hand landmarks
        face_landmarks: MediaPipe face landmarks
        threshold: Distance threshold (normalized coordinates)
        
    Returns:
        True if any hand is near the face
    """
    if not hand_landmarks or not face_landmarks:
        return False
    
    if not hasattr(face_landmarks, 'landmark'):
        return False
    
    # Get face bounding box using key landmarks
    face_points = face_landmarks.landmark
    face_x_coords = [point.x for point in face_points]
    face_y_coords = [point.y for point in face_points]
    
    face_min_x = min(face_x_coords)
    face_max_x = max(face_x_coords)
    face_min_y = min(face_y_coords)
    face_max_y = max(face_y_coords)
    
    # Expand face bounding box slightly
    face_width = face_max_x - face_min_x
    face_height = face_max_y - face_min_y
    expanded_min_x = max(0, face_min_x - face_width * 0.1)
    expanded_max_x = min(1, face_max_x + face_width * 0.1)
    expanded_min_y = max(0, face_min_y - face_height * 0.1)
    expanded_max_y = min(1, face_max_y + face_height * 0.1)
    
    # Check each hand
    for hand in hand_landmarks:
        if not hasattr(hand, 'landmark'):
            continue
            
        # Check if any hand landmark is within the expanded face region
        for landmark in hand.landmark:
            if (expanded_min_x <= landmark.x <= expanded_max_x and 
                expanded_min_y <= landmark.y <= expanded_max_y):
                return True
    
    return False

def is_posture_slouched(pose_landmarks: Any, threshold: float = 0.1) -> bool:
    """
    Check if the person is slouching based on pose landmarks.
    
    Args:
        pose_landmarks: MediaPipe pose landmarks
        threshold: Threshold for slouching detection
        
    Returns:
        True if person appears to be slouching
    """
    if not pose_landmarks or not hasattr(pose_landmarks, 'landmark'):
        return False
    
    landmarks = pose_landmarks.landmark
    
    # Key pose landmarks for posture analysis
    # Nose (0), Left shoulder (11), Right shoulder (12)
    # Left hip (23), Right hip (24), Left ear (7), Right ear (8)
    
    try:
        nose = landmarks[0]
        left_shoulder = landmarks[11]
        right_shoulder = landmarks[12]
        left_hip = landmarks[23]
        right_hip = landmarks[24]
        
        # Calculate shoulder center and hip center
        shoulder_center_y = (left_shoulder.y + right_shoulder.y) / 2
        hip_center_y = (left_hip.y + right_hip.y) / 2
        
        # Calculate the angle between shoulders and hips
        # If shoulders are significantly lower than expected relative to hips, person is slouching
        shoulder_hip_ratio = shoulder_center_y / hip_center_y if hip_center_y > 0 else 1.0
        
        # Check if head is too far forward (nose position relative to shoulders)
        nose_shoulder_diff = abs(nose.x - (left_shoulder.x + right_shoulder.x) / 2)
        
        # Person is slouching if:
        # 1. Shoulders are too low relative to hips
        # 2. Head is too far forward
        is_slouching = (shoulder_hip_ratio > (1.0 + threshold) or 
                       nose_shoulder_diff > threshold)
        
        return is_slouching
        
    except (IndexError, AttributeError):
        return False

def calculate_face_orientation(face_landmarks: Any) -> Dict[str, float]:
    """
    Calculate detailed face orientation metrics.
    
    Args:
        face_landmarks: MediaPipe face landmarks
        
    Returns:
        Dictionary with orientation metrics
    """
    if not face_landmarks or not hasattr(face_landmarks, 'landmark'):
        return {"yaw": 0.0, "pitch": 0.0, "roll": 0.0, "confidence": 0.0}
    
    yaw, pitch = calculate_yaw_pitch(face_landmarks)
    
    # Calculate roll (head tilt) using eye landmarks
    landmarks = face_landmarks.landmark
    left_eye = landmarks[33]
    right_eye = landmarks[362]
    
    # Calculate roll from eye line
    eye_dy = right_eye.y - left_eye.y
    eye_dx = right_eye.x - left_eye.x
    roll = math.atan2(eye_dy, eye_dx)
    
    # Calculate confidence based on landmark visibility
    confidence = 1.0  # Simplified for now
    
    return {
        "yaw": yaw,
        "pitch": pitch,
        "roll": roll,
        "confidence": confidence
    }

def is_face_centered(face_landmarks: Any, frame_width: int, frame_height: int, 
                   tolerance: float = 0.3) -> bool:
    """
    Check if the face is centered in the frame.
    
    Args:
        face_landmarks: MediaPipe face landmarks
        frame_width: Frame width
        frame_height: Frame height
        tolerance: Tolerance for centering (0.0 = perfectly centered)
        
    Returns:
        True if face is centered within tolerance
    """
    if not face_landmarks or not hasattr(face_landmarks, 'landmark'):
        return False
    
    landmarks = face_landmarks.landmark
    
    # Calculate face center
    face_x_coords = [point.x for point in landmarks]
    face_y_coords = [point.y for point in landmarks]
    
    face_center_x = np.mean(face_x_coords)
    face_center_y = np.mean(face_y_coords)
    
    # Check if face is within tolerance of frame center
    center_x = 0.5
    center_y = 0.5
    
    x_distance = abs(face_center_x - center_x)
    y_distance = abs(face_center_y - center_y)
    
    return x_distance <= tolerance and y_distance <= tolerance

def calculate_focus_quality(face_landmarks: Any, hands_landmarks: List[Any], 
                           pose_landmarks: Any) -> float:
    """
    Calculate overall focus quality score (0.0 to 1.0).
    
    Args:
        face_landmarks: MediaPipe face landmarks
        hands_landmarks: List of MediaPipe hand landmarks
        pose_landmarks: MediaPipe pose landmarks
        
    Returns:
        Focus quality score between 0.0 and 1.0
    """
    score = 1.0
    
    # Face visibility penalty
    if not face_landmarks:
        score -= 0.5
    else:
        # Check face orientation
        yaw, pitch = calculate_yaw_pitch(face_landmarks)
        if abs(yaw) > 0.3 or abs(pitch) > 0.4:
            score -= 0.3
    
    # Hand near face penalty
    if is_hand_near_face(hands_landmarks, face_landmarks):
        score -= 0.4
    
    # Posture penalty
    if is_posture_slouched(pose_landmarks):
        score -= 0.2
    
    return max(0.0, min(1.0, score))
