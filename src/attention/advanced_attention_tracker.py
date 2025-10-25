"""
Advanced Attention Tracker using dlib 68-point facial landmarks
More accurate gaze, eye, and mouth detection
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
import imutils
from imutils import face_utils
from imutils.video import VideoStream
import dlib

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
    Advanced Attention Tracker using dlib 68-point facial landmarks
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
        
        # Initialize dlib face detector and predictor
        self.detector = dlib.get_frontal_face_detector()
        try:
            self.predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
            print("✅ dlib predictor loaded")
        except:
            print("⚠️ dlib predictor not found, using MediaPipe fallback")
            self.predictor = None
        
        # Initialize MediaPipe as fallback
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
        self.head_tilt_threshold = 15.0  # degrees
        
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
        print("📱 dlib 68-point landmarks + Flexible Phone Detection")
        print("🎯 Advanced Gaze, Eye, and Mouth Analysis")

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

    def is_rotation_matrix(self, matrix):
        """Check if matrix is a rotation matrix"""
        matrix_t = np.transpose(matrix)
        identity_should_be = np.dot(matrix_t, matrix)
        identity_matrix = np.identity(3, dtype=matrix.dtype)
        return np.linalg.norm(identity_matrix - identity_should_be) < 1e-6

    def calculate_euler_angles(self, matrix):
        """Calculate Euler angles from rotation matrix"""
        assert (self.is_rotation_matrix(matrix))
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

    def get_head_pose(self, frame, landmarks):
        """Calculate head pose using 6 key facial landmarks"""
        # Key facial landmarks for head pose
        image_points = np.array([
            landmarks[33],  # Nose tip
            landmarks[8],   # Chin
            landmarks[36],  # Left eye left corner
            landmarks[45],  # Right eye right corner
            landmarks[48],  # Left mouth corner
            landmarks[54]   # Right mouth corner
        ], dtype="double")
        
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
            # Convert rotation vector to rotation matrix
            rotation_matrix, _ = cv2.Rodrigues(rotation_vector)
            euler_angles = self.calculate_euler_angles(rotation_matrix)
            
            # Convert to degrees
            yaw = np.rad2deg(euler_angles[1])
            pitch = np.rad2deg(euler_angles[0])
            roll = np.rad2deg(euler_angles[2])
            
            return yaw, pitch, roll
        else:
            return 0.0, 0.0, 0.0

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
        
        # Convert to grayscale for dlib
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
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
        
        # Try dlib first (more accurate)
        if self.predictor is not None:
            rects = self.detector(gray, 0)
            
            if len(rects) > 0:
                face_visible = True
                rect = rects[0]
                
                # Get facial landmarks
                shape = self.predictor(gray, rect)
                shape = face_utils.shape_to_np(shape)
                
                # Calculate face bounding box
                (bX, bY, bW, bH) = face_utils.rect_to_bb(rect)
                face_bbox = (bX, bY, bX + bW, bY + bH)
                
                # Eye aspect ratio analysis
                (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
                (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
                (mStart, mEnd) = (49, 68)
                
                left_eye = shape[lStart:lEnd]
                right_eye = shape[rStart:rEnd]
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
                
                # Mouth aspect ratio analysis
                mouth = shape[mStart:mEnd]
                mar = self.mouth_aspect_ratio(mouth)
                
                if mar > self.mouth_ar_threshold:
                    yawning = True
                
                # Head pose analysis
                yaw, pitch, roll = self.get_head_pose(frame, shape)
                head_tilt = abs(roll)
                
                # Orientation analysis
                orientation_good = (abs(yaw) < 15.0 and abs(pitch) < 15.0 and head_tilt < self.head_tilt_threshold)
        
        # Fallback to MediaPipe if dlib fails
        if not face_visible:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_results = self.face_mesh.process(rgb_frame)
            
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
        
        # Hand detection using MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        hands_results = self.hands.process(rgb_frame)
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
        
        # Enhanced phone detection
        if hand_near_face and phone_objects:
            phone_near_face = True
            phone_confidence = max(phone_confidence, max(obj.get('confidence', 0.0) for obj in phone_objects))
        
        # Posture analysis
        pose_results = self.pose.process(rgb_frame)
        posture_stable = True
        if pose_results.pose_landmarks:
            try:
                shoulders = pose_results.pose_landmarks.landmark[11]
                hips = pose_results.pose_landmarks.landmark[23]
                posture_stable = (hips.y - shoulders.y) > 0.3
            except (IndexError, AttributeError):
                posture_stable = True
        
        # Calculate focus score
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
        
        # Overall focus determination
        focused = (focus_score > 0.7 and not phone_near_face and face_visible and 
                  orientation_good and not eye_closed and not yawning)
        
        # Generate status messages
        status_messages = self.generate_status_messages(
            face_visible, orientation_good, phone_near_face, hand_near_face,
            phone_confidence, posture_stable, eye_closed, yawning, yaw, pitch, head_tilt
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
                                eye_closed: bool, yawning: bool, yaw: float, pitch: float, head_tilt: float) -> Dict[str, Dict[str, str]]:
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
            if abs(yaw) > 15.0:
                orientation_status = "↩ Turn head forward"
            elif abs(pitch) > 15.0:
                orientation_status = "↕ Look straight ahead"
            elif head_tilt > self.head_tilt_threshold:
                orientation_status = "↻ Straighten head"
            else:
                orientation_status = "↩ Adjust head orientation"
            orientation_color = "red"
        
        # Eye status
        if eye_closed:
            eye_status = "😴 Eyes closed"
            eye_color = "red"
        else:
            eye_status = "👁 Eyes open"
            eye_color = "green"
        
        # Mouth status
        if yawning:
            mouth_status = "😴 Yawning"
            mouth_color = "red"
        else:
            mouth_status = "😐 Normal"
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

    def draw_advanced_status_overlay(self, frame, metrics):
        """Draw advanced status overlay with detailed analysis"""
        status_messages = metrics.get("status_messages", {})
        
        # Main status panel
        panel_width = 350
        panel_height = 280
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
        cv2.putText(frame, "ADVANCED ATTENTION TRACKER", (panel_x + 10, panel_y + 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Status items
        y_start = panel_y + 50
        status_items = [
            ("FACE", status_messages.get("face", {}).get("text", "No face detected")),
            ("ORIENTATION", status_messages.get("orientation", {}).get("text", "Looking forward")),
            ("EYE", status_messages.get("eye", {}).get("text", "Eyes open")),
            ("MOUTH", status_messages.get("mouth", {}).get("text", "Normal")),
            ("INTERACTION", status_messages.get("interaction", {}).get("text", "No interaction")),
            ("POSTURE", status_messages.get("posture", {}).get("text", "Good posture")),
            ("OVERALL", status_messages.get("overall", {}).get("text", "Focused"))
        ]
        
        for i, (label, text) in enumerate(status_items):
            y_pos = y_start + (i * 30)
            
            # Label
            cv2.putText(frame, label, (panel_x + 10, y_pos),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.4, (180, 180, 180), 1)
            
            # Status text with color
            color = (0, 255, 0) if "✓" in text or "✅" in text else (0, 0, 255) if "✗" in text or "❌" in text else (0, 165, 255)
            cv2.putText(frame, text, (panel_x + 10, y_pos + 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
        
        # Metrics panel
        metrics_width = 200
        metrics_height = 100
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
        cv2.putText(frame, "METRICS", (metrics_x + 10, metrics_y + 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (180, 180, 180), 1)
        
        # Score and FPS
        score_text = f"Score: {metrics.get('focus_score', 0.0):.2f}"
        fps_text = f"FPS: {metrics.get('fps', 0.0):.1f}"
        
        cv2.putText(frame, score_text, (metrics_x + 10, metrics_y + 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(frame, fps_text, (metrics_x + 10, metrics_y + 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        return frame

    def draw_phone_detections(self, frame, phone_objects):
        """Draw phone detection boxes"""
        for obj in phone_objects:
            x1, y1, x2, y2 = obj['bbox']
            confidence = obj['confidence']
            
            # Draw bounding box
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            # Draw label
            label = f"Phone: {confidence:.2f}"
            cv2.putText(frame, label, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        return frame

    def run(self):
        """Run the main attention tracking loop"""
        print("🚀 Starting Advanced Attention Tracker...")
        print("📱 dlib 68-point landmarks + Flexible Phone Detection")
        print("🎯 Advanced Gaze, Eye, and Mouth Analysis")
        print("Press 'q' to quit, 's' to save screenshot")
        
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to grab frame")
                break
            
            # Process frame
            metrics = self.process_frame(frame)
            
            # Draw overlays
            frame = self.draw_advanced_status_overlay(frame, metrics)
            frame = self.draw_phone_detections(frame, metrics.get("phone_objects", []))
            
            # Draw focus ring
            if metrics.get("focused", False):
                cv2.rectangle(frame, (10, 10), (self.frame_width - 10, self.frame_height - 10), 
                             (0, 255, 0), 4)
            else:
                cv2.rectangle(frame, (10, 10), (self.frame_width - 10, self.frame_height - 10), 
                             (0, 0, 255), 4)
            
            # Display frame
            cv2.imshow('Advanced Attention Tracker', frame)
            
            # Output JSON for integration
            print(json.dumps({
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "focused": metrics.get("focused", False),
                "focus_score": metrics.get("focus_score", 0.0),
                "face_visible": metrics.get("face_visible", False),
                "orientation_good": metrics.get("orientation_good", False),
                "yaw": metrics.get("yaw", 0.0),
                "pitch": metrics.get("pitch", 0.0),
                "roll": metrics.get("roll", 0.0),
                "head_tilt": metrics.get("head_tilt", 0.0),
                "eye_closed": metrics.get("eye_closed", False),
                "yawning": metrics.get("yawning", False),
                "phone_near_face": metrics.get("phone_near_face", False),
                "hand_near_face": metrics.get("hand_near_face", False),
                "posture_stable": metrics.get("posture_stable", False),
                "phone_objects_count": len(metrics.get("phone_objects", [])),
                "fps": metrics.get("fps", 0.0)
            }, indent=None))
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('s'):
                timestamp = time.strftime("%Y%m%d-%H%M%S")
                filename = f"advanced_attention_screenshot_{timestamp}.png"
                cv2.imwrite(filename, frame)
                print(f"Screenshot saved as {filename}")
        
        self.cap.release()
        cv2.destroyAllWindows()
        print("✅ Advanced Attention Tracker stopped")

def main():
    tracker = AdvancedAttentionTracker(
        camera_index=0, 
        frame_width=640, 
        frame_height=480
    )
    tracker.run()

if __name__ == "__main__":
    main()
