"""
Simplified Advanced Attention Tracker (MediaPipe-only version)
Uses MediaPipe for facial analysis without dlib dependency
"""

import cv2
import time
import json
import numpy as np
import math
from typing import Dict, Any, Tuple, Optional, List
import mediapipe as mp
import threading
from scipy.spatial import distance as dist

from flexible_phone_detector import FlexiblePhoneDetector

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

class AdvancedAttentionTracker:
    """
    Advanced Attention Tracker using MediaPipe (simplified version)
    More accurate gaze, eye, and mouth detection
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
        
        # Initialize flexible phone detector
        self.phone_detector = FlexiblePhoneDetector()
        
        # Performance optimization
        self.fps_counter = FPSCounter()
        self.detection_frame_skip = 2
        self.last_phone_results = []
        
        # Threading for detection
        self.detection_thread = None
        self.detection_results_lock = threading.Lock()
        
        # Advanced thresholds
        self.eye_ar_threshold = 0.20
        self.mouth_ar_threshold = 0.88
        self.eye_ar_consec_frames = 3
        self.head_tilt_threshold = 45.0  # degrees (more lenient)
        
        # Model points for head pose estimation
        self.model_points = np.array([
            (0.0, 0.0, 0.0),
            (0.0, -330.0, -65.0),
            (-225.0, 170.0, -135.0),
            (225.0, 170.0, -135.0),
            (-150.0, -150.0, -125.0),
            (150.0, -150.0, -125.0)
        ])
        
        # Eye closure counter
        self.eye_closure_counter = 0
        
        print(f"✅ Advanced Attention Tracker initialized: {self.frame_width}x{self.frame_height}")
        print("📱 MediaPipe + Advanced Gaze Analysis + Phone Detection")
        print("🎯 Advanced Eye, Mouth, and Head Pose Analysis")

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

    def eye_aspect_ratio(self, eye):
        """Calculate eye aspect ratio (EAR)"""
        A = dist.euclidean(eye[1], eye[5])
        B = dist.euclidean(eye[2], eye[4])
        C = dist.euclidean(eye[0], eye[3])
        ear = (A + B) / (2.0 * C)
        return ear

    def mouth_aspect_ratio(self, mouth):
        """Calculate mouth aspect ratio (MAR)"""
        A = dist.euclidean(mouth[2], mouth[10])
        B = dist.euclidean(mouth[4], mouth[8])
        C = dist.euclidean(mouth[0], mouth[6])
        mar = (A + B) / (2.0 * C)
        return mar

    def get_mediapipe_eye_landmarks(self, face_landmarks):
        """Extract eye landmarks from MediaPipe face mesh"""
        # MediaPipe face mesh eye indices
        left_eye_indices = [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246]
        right_eye_indices = [362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398]
        
        left_eye = []
        right_eye = []
        
        for idx in left_eye_indices:
            if idx < len(face_landmarks.landmark):
                lm = face_landmarks.landmark[idx]
                left_eye.append([lm.x * self.frame_width, lm.y * self.frame_height])
        
        for idx in right_eye_indices:
            if idx < len(face_landmarks.landmark):
                lm = face_landmarks.landmark[idx]
                right_eye.append([lm.x * self.frame_width, lm.y * self.frame_height])
        
        return np.array(left_eye), np.array(right_eye)

    def get_mediapipe_mouth_landmarks(self, face_landmarks):
        """Extract mouth landmarks from MediaPipe face mesh"""
        # MediaPipe face mesh mouth indices
        mouth_indices = [61, 84, 17, 314, 405, 320, 307, 375, 321, 308, 324, 318]
        
        mouth = []
        for idx in mouth_indices:
            if idx < len(face_landmarks.landmark):
                lm = face_landmarks.landmark[idx]
                mouth.append([lm.x * self.frame_width, lm.y * self.frame_height])
        
        return np.array(mouth)

    def get_head_pose_from_mediapipe(self, frame, face_landmarks):
        """Calculate head pose using MediaPipe landmarks"""
        # Key facial landmarks for head pose
        key_indices = [33, 8, 36, 45, 48, 54]  # Nose tip, chin, eye corners, mouth corners
        image_points = []
        
        for idx in key_indices:
            if idx < len(face_landmarks.landmark):
                lm = face_landmarks.landmark[idx]
                image_points.append([lm.x * self.frame_width, lm.y * self.frame_height])
        
        if len(image_points) != 6:
            return 0.0, 0.0, 0.0
        
        image_points = np.array(image_points, dtype="double")
        
        # Camera parameters
        focal_length = frame.shape[1]
        center = (frame.shape[1] / 2, frame.shape[0] / 2)
        camera_matrix = np.array(
            [[focal_length, 0, center[0]], [0, focal_length, center[1]], [0, 0, 1]],
            dtype="double"
        )
        dist_coeffs = np.zeros((4, 1))

        # Solve PnP
        success, rotation_vector, translation_vector = cv2.solvePnP(
            self.model_points,
            image_points,
            camera_matrix,
            dist_coeffs,
            flags=cv2.SOLVEPNP_ITERATIVE
        )

        if success:
            rotation_matrix, _ = cv2.Rodrigues(rotation_vector)
            euler_angles = self.calculate_euler_angles(rotation_matrix)
            
            # Convert to degrees
            yaw = np.rad2deg(euler_angles[1])
            pitch = np.rad2deg(euler_angles[0])
            roll = np.rad2deg(euler_angles[2])
            
            return yaw, pitch, roll
        else:
            return 0.0, 0.0, 0.0

    def calculate_euler_angles(self, matrix):
        """Calculate Euler angles from rotation matrix"""
        sy = math.sqrt(matrix[0, 0] * matrix[0, 0] + matrix[1, 0] * matrix[1, 0])
        singular = sy < 1e-6

        if not singular:
            x_angle = math.atan2(matrix[2, 1], matrix[2, 2])
            y_angle = math.atan2(-matrix[2, 0], sy)
            z_angle = math.atan2(matrix[1, 0], matrix[0, 0])
        else:
            x_angle = math.atan2(-matrix[1, 2], matrix[1, 1])
            y_angle = math.atan2(-matrix[2, 0], sy)
            z_angle = 0

        return np.array([x_angle, y_angle, z_angle])

    def run_phone_detection_async(self, frame, face_bbox):
        """Run phone detection in background thread"""
        try:
            detections = self.phone_detector.detect_phones_near_face(frame, face_bbox)
            with self.detection_results_lock:
                self.last_phone_results = detections
                if detections:
                    print(f"DEBUG: Found {len(detections)} phone objects!")
        except Exception as e:
            print(f"Phone detection error: {e}")

    def is_hand_near_face(self, face_bbox, hands, margin=0.2):
        """Check if hand landmarks are near face area"""
        if not face_bbox or not hands:
            return False
        
        fx1, fy1, fx2, fy2 = face_bbox
        face_width = fx2 - fx1
        face_height = fy2 - fy1
        face_center_x = (fx1 + fx2) / 2
        face_center_y = (fy1 + fy2) / 2
        
        dynamic_margin = max(face_width, face_height) * margin
        
        for hand in hands:
            key_landmarks = [0, 4, 8, 12, 16, 20]
            for lm_idx in key_landmarks:
                if lm_idx < len(hand.landmark):
                    lm = hand.landmark[lm_idx]
                    x = lm.x * self.frame_width
                    y = lm.y * self.frame_height
                    
                    distance = np.sqrt((x - face_center_x)**2 + (y - face_center_y)**2)
                    if distance < dynamic_margin:
                        return True
            
            for lm in hand.landmark:
                x = lm.x * self.frame_width
                y = lm.y * self.frame_height
                
                if (fx1 - 50 < x < fx2 + 50 and fy1 - 50 < y < fy2 + 50):
                    return True
        
        return False

    def is_phone_near_face(self, face_bbox, phone_objects, threshold=0.1):
        """Check if phone objects overlap with face area"""
        if not face_bbox or not phone_objects:
            return False, 0.0
        
        fx1, fy1, fx2, fy2 = face_bbox
        face_area = (fx2 - fx1) * (fy2 - fy1)
        max_confidence = 0.0
        
        for obj in phone_objects:
            x1, y1, x2, y2 = obj['bbox']
            overlap_x = max(0, min(fx2, x2) - max(fx1, x1))
            overlap_y = max(0, min(fy2, y2) - max(fy1, y1))
            overlap_area = overlap_x * overlap_y
            
            if face_area > 0:
                overlap_ratio = overlap_area / face_area
                if overlap_ratio > threshold:
                    max_confidence = max(max_confidence, overlap_ratio)
                    return True, max_confidence
        
        return False, 0.0

    def process_frame(self, frame: np.ndarray) -> Dict[str, Any]:
        """Process a single frame with advanced facial analysis"""
        self.frame_count += 1
        
        # Convert to RGB for MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process with MediaPipe
        face_results = self.face_mesh.process(rgb_frame)
        hands_results = self.hands.process(rgb_frame)
        pose_results = self.pose.process(rgb_frame)
        
        # Initialize results
        face_visible = False
        face_bbox = None
        eye_closed = False
        yawning = False
        head_tilt = 0.0
        yaw = 0.0
        pitch = 0.0
        roll = 0.0
        orientation_good = True
        ear = 0.0
        mar = 0.0
        
        # Process face landmarks
        if face_results.multi_face_landmarks:
            face_visible = True
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
            
            # Extract eye landmarks and calculate EAR
            left_eye, right_eye = self.get_mediapipe_eye_landmarks(face_landmarks)
            if len(left_eye) >= 6 and len(right_eye) >= 6:
                left_ear = self.eye_aspect_ratio(left_eye)
                right_ear = self.eye_aspect_ratio(right_eye)
                ear = (left_ear + right_ear) / 2.0
                
                # Check for eye closure
                if ear < self.eye_ar_threshold:
                    self.eye_closure_counter += 1
                    if self.eye_closure_counter >= self.eye_ar_consec_frames:
                        eye_closed = True
                else:
                    self.eye_closure_counter = 0
            
            # Extract mouth landmarks and calculate MAR
            mouth = self.get_mediapipe_mouth_landmarks(face_landmarks)
            if len(mouth) >= 12:
                mar = self.mouth_aspect_ratio(mouth)
                
                if mar > self.mouth_ar_threshold:
                    yawning = True
            
            # Calculate head pose
            yaw, pitch, roll = self.get_head_pose_from_mediapipe(frame, face_landmarks)
            head_tilt = abs(roll)
            
            # Orientation analysis - more lenient thresholds
            orientation_good = (abs(yaw) < 30.0 and abs(pitch) < 30.0 and head_tilt < 45.0)
        
        # Hand detection
        hand_landmarks = []
        hand_near_face = False
        
        if hands_results.multi_hand_landmarks:
            hand_landmarks = hands_results.multi_hand_landmarks
            if face_bbox:
                hand_near_face = self.is_hand_near_face(face_bbox, hand_landmarks)
        
        # Phone detection
        phone_near_face = False
        phone_confidence = 0.0
        phone_objects = []
        
        if self.frame_count % self.detection_frame_skip == 0:
            if self.detection_thread is None or not self.detection_thread.is_alive():
                self.detection_thread = threading.Thread(target=self.run_phone_detection_async, args=(frame, face_bbox))
                self.detection_thread.start()
        
        with self.detection_results_lock:
            phone_objects = self.last_phone_results.copy()
        
        if face_bbox and phone_objects:
            phone_near_face, phone_confidence = self.is_phone_near_face(face_bbox, phone_objects)
        
        # Posture analysis
        posture_stable = True
        if pose_results.pose_landmarks:
            try:
                shoulders = pose_results.pose_landmarks.landmark[11]
                hips = pose_results.pose_landmarks.landmark[23]
                posture_stable = (hips.y - shoulders.y) > 0.3
            except (IndexError, AttributeError):
                posture_stable = True
        
        # Calculate focus score using advanced metrics
        focus_components = {
            "face_visibility": 1.0 if face_visible else 0.0,
            "orientation": 1.0 if orientation_good else 0.0,
            "eye_open": 0.0 if eye_closed else 1.0,
            "not_yawning": 0.0 if yawning else 1.0,
            "phone_interaction": 0.0 if phone_near_face else 1.0,
            "hand_interaction": 0.7 if hand_near_face else 1.0,
            "posture": 1.0 if posture_stable else 0.0
        }
        
        # Weighted focus score
        weights = {
            "face_visibility": 0.2,
            "orientation": 0.2,
            "eye_open": 0.2,
            "not_yawning": 0.1,
            "phone_interaction": 0.15,
            "hand_interaction": 0.05,
            "posture": 0.1
        }
        
        focus_score = sum(weights[component] * score for component, score in focus_components.items())
        
        # Overall focus determination - more lenient criteria
        focused = (focus_score > 0.5 and not phone_near_face and face_visible)
        
        # Generate status messages
        status_messages = self.generate_status_messages(
            face_visible, orientation_good, phone_near_face, hand_near_face,
            phone_confidence, posture_stable, eye_closed, yawning, yaw, pitch, head_tilt, ear, mar
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
            "roll": roll,
            "head_tilt": head_tilt,
            "eye_closed": eye_closed,
            "yawning": yawning,
            "ear": ear,
            "mar": mar,
            "phone_near_face": phone_near_face,
            "hand_near_face": hand_near_face,
            "phone_confidence": phone_confidence,
            "posture_stable": posture_stable,
            "status_messages": status_messages,
            "phone_objects": phone_objects,
            "fps": fps
        }

    def generate_status_messages(self, face_visible: bool, orientation_good: bool,
                                phone_near_face: bool, hand_near_face: bool,
                                phone_confidence: float, posture_stable: bool,
                                eye_closed: bool, yawning: bool, yaw: float, pitch: float, head_tilt: float,
                                ear: float, mar: float) -> Dict[str, Dict[str, str]]:
        """Generate clear, readable status messages with precise metrics"""
        
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
            if abs(yaw) > 15.0:
                orientation_status = f"↩ Turn head forward (yaw: {yaw:.1f}°)"
            elif abs(pitch) > 15.0:
                orientation_status = f"↕ Look straight ahead (pitch: {pitch:.1f}°)"
            elif head_tilt > self.head_tilt_threshold:
                orientation_status = f"↻ Straighten head (tilt: {head_tilt:.1f}°)"
            else:
                orientation_status = "↩ Adjust head orientation"
            orientation_color = "red"
        
        # Eye status with EAR
        if eye_closed:
            eye_status = f"😴 Eyes closed (EAR: {ear:.3f})"
            eye_color = "red"
        else:
            eye_status = f"👁 Eyes open (EAR: {ear:.3f})"
            eye_color = "green"
        
        # Mouth status with MAR
        if yawning:
            mouth_status = f"😴 Yawning (MAR: {mar:.3f})"
            mouth_color = "red"
        else:
            mouth_status = f"😐 Normal (MAR: {mar:.3f})"
            mouth_color = "green"
        
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
        elif eye_closed:
            overall_status = "😴 Eyes closed"
            overall_color = "red"
        elif yawning:
            overall_status = "😴 Yawning detected"
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
            "eye": {"text": eye_status, "color": eye_color},
            "mouth": {"text": mouth_status, "color": mouth_color},
            "interaction": {"text": interaction_status, "color": interaction_color},
            "posture": {"text": posture_status, "color": posture_color},
            "overall": {"text": overall_status, "color": overall_color}
        }