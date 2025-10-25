import cv2
import numpy as np
from typing import Dict, Any, Tuple, Optional

class FocusVisualizer:
    """
    Visual overlay for focus tracking results.
    Draws attention ring, status text, and metrics on video frames.
    """
    
    def __init__(self):
        """Initialize visualizer with default colors and settings."""
        # Colors (BGR format for OpenCV)
        self.colors = {
            "focused": (0, 255, 0),      # Green
            "distracted": (0, 0, 255),    # Red
            "warning": (0, 255, 255),    # Yellow
            "text": (255, 255, 255),     # White
            "background": (0, 0, 0),     # Black
            "ring_focused": (0, 255, 0), # Green ring
            "ring_distracted": (0, 0, 255), # Red ring
            "ring_pulse": (0, 255, 255)  # Yellow pulse
        }
        
        # Ring settings
        self.ring_radius_ratio = 0.3  # Ring radius as fraction of frame size
        self.ring_thickness = 4
        self.pulse_thickness = 8
        
        # Text settings
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.font_scale_large = 1.2
        self.font_scale_medium = 0.8
        self.font_scale_small = 0.6
        self.text_thickness = 2
        
        # Animation settings
        self.pulse_phase = 0.0
        self.pulse_speed = 0.1
    
    def draw_focus_ring(self, frame: np.ndarray, focused: bool, 
                       focus_score: float, frame_width: int, frame_height: int,
                       pulse: bool = True) -> np.ndarray:
        """
        Draw the main attention ring around the frame center.
        
        Args:
            frame: Input frame
            focused: Whether person is focused
            focus_score: Focus score (0.0 to 1.0)
            frame_width: Frame width
            frame_height: Frame height
            pulse: Whether to animate the ring
            
        Returns:
            Frame with attention ring drawn
        """
        # Clean ring colors
        if focus_score > 0.8:
            ring_color = (0, 255, 100)  # Clean green
        elif focus_score > 0.5:
            ring_color = (255, 200, 0)  # Clean yellow
        else:
            ring_color = (255, 100, 100)  # Clean red
        
        # Draw clean ring around frame
        ring_thickness = 4
        ring_margin = 15
        
        # Outer ring
        cv2.rectangle(frame, (ring_margin, ring_margin), 
                     (frame_width - ring_margin, frame_height - ring_margin), 
                     ring_color, ring_thickness)
        
        # Inner subtle ring
        inner_margin = ring_margin + 8
        cv2.rectangle(frame, (inner_margin, inner_margin), 
                     (frame_width - inner_margin, frame_height - inner_margin), 
                     (ring_color[0]//3, ring_color[1]//3, ring_color[2]//3), 1)
        
        return frame
    
    def draw_status_text(self, frame: np.ndarray, focus_metrics: Dict[str, Any], 
                        fps: float, frame_width: int, frame_height: int) -> np.ndarray:
        """
        Draw dynamic color-coded status text and metrics on the frame.
        
        Args:
            frame: Input frame
            focus_metrics: Focus evaluation results
            fps: Current FPS
            frame_width: Frame width
            frame_height: Frame height
            
        Returns:
            Frame with status text drawn
        """
        # Extract focus data
        focused = focus_metrics.get("focused", False)
        focus_score = focus_metrics.get("focus_score", 0.0)
        yaw = focus_metrics.get("yaw", 0)
        pitch = focus_metrics.get("pitch", 0)
        hand_near_face = focus_metrics.get("hand_near_face", False)
        phone_detected = focus_metrics.get("phone_detected", False)
        posture_stable = focus_metrics.get("posture_stable", True)
        face_visible = focus_metrics.get("face_visible", True)
        
        # Define actionable statuses and colors
        if face_visible:
            face_status = "✓ Face detected"
            face_color = (0, 255, 0)
        else:
            face_status = "✗ Look at camera"
            face_color = (0, 0, 255)
        
        if abs(yaw) < 0.25 and abs(pitch) < 0.35:
            orientation_status = "✓ Looking forward"
            orientation_color = (0, 255, 0)
        else:
            if abs(yaw) > 0.25:
                orientation_status = "✗ Turn head forward"
            else:
                orientation_status = "✗ Look straight ahead"
            orientation_color = (0, 0, 255)
        
        # Enhanced phone detection status
        rectangle_phone_detected = focus_metrics.get("rectangle_phone_detected", False)
        rectangle_confidence = focus_metrics.get("rectangle_confidence", 0.0)
        
        if phone_detected:
            hand_status = "✗ Phone detected"
            hand_color = (0, 0, 255)
        elif rectangle_phone_detected:
            hand_status = f"✗ Rectangle phone ({rectangle_confidence:.2f})"
            hand_color = (0, 0, 255)
        elif hand_near_face:
            hand_status = "✗ Put phone down"
            hand_color = (0, 0, 255)
        else:
            hand_status = "✓ No phone"
            hand_color = (0, 255, 0)
        
        if posture_stable:
            posture_status = "✓ Sit up straight"
            posture_color = (0, 255, 0)
        else:
            posture_status = "✗ Straighten posture"
            posture_color = (0, 0, 255)
        
        # Clean modern overlay with rounded corners effect
        panel_width = 320
        panel_height = 180
        panel_x = 20
        panel_y = 20
        
        # Main panel with gradient-like background
        cv2.rectangle(frame, (panel_x, panel_y), 
                     (panel_x + panel_width, panel_y + panel_height), 
                     (20, 20, 20), -1)
        
        # Subtle border
        cv2.rectangle(frame, (panel_x, panel_y), 
                     (panel_x + panel_width, panel_y + panel_height), 
                     (60, 60, 60), 1)
        
        # Title with better font
        cv2.putText(frame, "ATTENTION TRACKER", (panel_x + 15, panel_y + 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Status items with clean layout
        y_start = panel_y + 50
        items = [
            ("FACE", face_status, face_color),
            ("ORIENTATION", orientation_status, orientation_color),
            ("HANDS", hand_status, hand_color),
            ("POSTURE", posture_status, posture_color)
        ]
        
        for i, (label, status, color) in enumerate(items):
            y_pos = y_start + (i * 28)
            
            # Label in smaller font
            cv2.putText(frame, label, (panel_x + 15, y_pos),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (180, 180, 180), 1)
            
            # Status in larger, cleaner font
            cv2.putText(frame, status, (panel_x + 15, y_pos + 18),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        
        # Main status with emphasis
        main_status = "FOCUSED" if focused else "DISTRACTED"
        main_color = (0, 255, 100) if focused else (255, 100, 100)
        
        # Status background
        status_bg_x = panel_x + 15
        status_bg_y = panel_y + 150
        cv2.rectangle(frame, (status_bg_x, status_bg_y), 
                     (status_bg_x + 200, status_bg_y + 25), 
                     (30, 30, 30), -1)
        
        cv2.putText(frame, main_status, (status_bg_x + 10, status_bg_y + 18),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, main_color, 2)
        
        # Clean metrics panel in bottom right
        metrics_width = 180
        metrics_height = 80
        metrics_x = frame_width - metrics_width - 20
        metrics_y = frame_height - metrics_height - 20
        
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
        
        # Score and FPS with better formatting
        score_text = f"Score: {focus_score:.2f}"
        fps_text = f"FPS: {fps:.1f}"
        
        cv2.putText(frame, score_text, (metrics_x + 10, metrics_y + 45),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        cv2.putText(frame, fps_text, (metrics_x + 10, metrics_y + 65),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        return frame
    
    def draw_landmarks_overlay(self, frame: np.ndarray, results: Dict[str, Any],
                              show_face: bool = True, show_hands: bool = True, 
                              show_pose: bool = True) -> np.ndarray:
        """
        Draw MediaPipe landmarks overlay on the frame with detailed visualization.
        
        Args:
            frame: Input frame
            results: Detection results
            show_face: Whether to show face landmarks
            show_hands: Whether to show hand landmarks
            show_pose: Whether to show pose landmarks
            
        Returns:
            Frame with landmarks drawn
        """
        h, w, _ = frame.shape
        
        # Draw face mesh (purple dots and lines)
        if show_face and results and results["face"]["face_detected"]:
            face_landmarks = results["face"]["face_landmarks"]
            if face_landmarks:
                # Draw face mesh points
                for landmark in face_landmarks.landmark:
                    x = int(landmark.x * w)
                    y = int(landmark.y * h)
                    cv2.circle(frame, (x, y), 1, (255, 0, 255), -1)  # Purple dots
                
                # Draw face mesh connections (simplified)
                self._draw_face_mesh_connections(frame, face_landmarks, w, h)
        
        # Draw hand skeletons (red dots and lines)
        if show_hands and results and results["hands"]["hands_detected"] > 0:
            for hand_landmarks in results["hands"]["hands_landmarks"]:
                # Draw hand joints
                for landmark in hand_landmarks.landmark:
                    x = int(landmark.x * w)
                    y = int(landmark.y * h)
                    cv2.circle(frame, (x, y), 3, (0, 0, 255), -1)  # Red dots
                
                # Draw hand connections
                self._draw_hand_connections(frame, hand_landmarks, w, h)
        
        # Draw pose skeleton (yellow dots and lines)
        if show_pose and results and results["pose"]["pose_landmarks"]:
            pose_landmarks = results["pose"]["pose_landmarks"]
            # Draw pose joints
            for landmark in pose_landmarks.landmark:
                x = int(landmark.x * w)
                y = int(landmark.y * h)
                cv2.circle(frame, (x, y), 4, (0, 255, 255), -1)  # Yellow dots
            
            # Draw pose connections
            self._draw_pose_connections(frame, pose_landmarks, w, h)
        
        # Draw rectangle detections (phone-like objects)
        if results and results.get("rectangles", {}).get("phone_objects"):
            for rect in results["rectangles"]["phone_objects"]:
                x1, y1, x2, y2 = rect["bbox"]
                confidence = rect["confidence"]
                near_face = rect["near_face"]
                
                # Color based on proximity to face
                if near_face:
                    color = (0, 0, 255)  # Red for phone near face
                    thickness = 3
                else:
                    color = (255, 0, 0)  # Blue for phone not near face
                    thickness = 2
                
                # Draw rectangle
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, thickness)
                
                # Draw confidence text
                text = f"Phone {confidence:.2f}"
                cv2.putText(frame, text, (x1, y1 - 10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
                
                # Draw center point
                center_x, center_y = rect["center"]
                cv2.circle(frame, (center_x, center_y), 5, color, -1)
        
        return frame
    
    def draw_focus_grid(self, frame: np.ndarray, focus_metrics: Dict[str, Any],
                       frame_width: int, frame_height: int) -> np.ndarray:
        """
        Draw a grid showing different focus factors.
        
        Args:
            frame: Input frame
            focus_metrics: Focus evaluation results
            frame_width: Frame width
            frame_height: Frame height
            
        Returns:
            Frame with focus grid drawn
        """
        # Grid settings
        grid_x = frame_width - 200
        grid_y = 20
        grid_width = 180
        grid_height = 120
        
        # Draw grid background
        cv2.rectangle(frame, (grid_x, grid_y), 
                     (grid_x + grid_width, grid_y + grid_height), 
                     self.colors["background"], -1)
        cv2.rectangle(frame, (grid_x, grid_y), 
                     (grid_x + grid_width, grid_y + grid_height), 
                     self.colors["text"], 2)
        
        # Grid items
        items = [
            ("Face", focus_metrics.get("face_visible", False)),
            ("Orientation", not focus_metrics.get("distraction_reasons", []) or 
             not any("looking" in reason for reason in focus_metrics.get("distraction_reasons", []))),
            ("Hands", not focus_metrics.get("hand_near_face", False)),
            ("Posture", focus_metrics.get("posture_stable", True))
        ]
        
        for i, (name, status) in enumerate(items):
            item_y = grid_y + 20 + i * 25
            color = self.colors["focused"] if status else self.colors["distracted"]
            status_text = "✓" if status else "✗"
            
            cv2.putText(frame, f"{name}: {status_text}", 
                       (grid_x + 10, item_y), 
                       self.font, 0.5, color, 1)
        
        return frame
    
    def _get_score_color(self, score: float) -> Tuple[int, int, int]:
        """
        Get color based on focus score.
        
        Args:
            score: Focus score (0.0 to 1.0)
            
        Returns:
            BGR color tuple
        """
        if score >= 0.8:
            return self.colors["focused"]
        elif score >= 0.5:
            return self.colors["warning"]
        else:
            return self.colors["distracted"]
    
    def _draw_text_with_background(self, frame: np.ndarray, text: str, 
                                  position: Tuple[int, int], font_scale: float,
                                  text_color: Tuple[int, int, int], 
                                  bg_color: Tuple[int, int, int]) -> None:
        """
        Draw text with background rectangle.
        
        Args:
            frame: Input frame
            text: Text to draw
            position: Text position (x, y)
            font_scale: Font scale
            text_color: Text color
            bg_color: Background color
        """
        x, y = position
        
        # Get text size
        (text_width, text_height), baseline = cv2.getTextSize(
            text, self.font, font_scale, self.text_thickness
        )
        
        # Draw background rectangle
        cv2.rectangle(frame, (x - 5, y - text_height - 5), 
                     (x + text_width + 5, y + baseline + 5), 
                     bg_color, -1)
        
        # Draw text
        cv2.putText(frame, text, (x, y), self.font, font_scale, text_color, self.text_thickness)
    
    def _format_distraction_reason(self, reason: str) -> str:
        """
        Format distraction reason for display.
        
        Args:
            reason: Raw distraction reason
            
        Returns:
            Formatted reason string
        """
        reason_map = {
            "face_not_visible": "No Face Detected",
            "looking_sideways": "Looking Away",
            "looking_up_down": "Looking Up/Down",
            "hand_near_face": "Hand Near Face",
            "poor_posture": "Poor Posture",
            "face_not_centered": "Face Not Centered"
        }
        return reason_map.get(reason, reason.replace("_", " ").title())
    
    def _draw_face_mesh_connections(self, frame: np.ndarray, face_landmarks, w: int, h: int):
        """Draw face mesh connections (simplified version)."""
        # Key face connections for a simplified mesh
        connections = [
            # Face outline
            (0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9), (9, 10),
            # Eye connections
            (33, 7), (7, 163), (163, 144), (144, 145), (145, 153), (153, 154), (154, 155), (155, 133), (133, 173), (173, 157), (157, 158), (158, 159), (159, 160), (160, 161), (161, 246), (246, 33),
            # Nose
            (1, 2), (2, 5), (5, 4), (4, 19), (19, 20), (20, 94), (94, 125), (125, 141), (141, 235), (235, 236), (236, 3), (3, 51), (51, 48), (48, 115), (115, 131), (131, 134), (134, 102), (102, 49), (49, 220), (220, 305), (305, 281), (281, 360), (360, 279), (279, 331), (331, 294), (294, 327), (327, 326), (326, 2)
        ]
        
        for start_idx, end_idx in connections:
            if start_idx < len(face_landmarks.landmark) and end_idx < len(face_landmarks.landmark):
                start_point = face_landmarks.landmark[start_idx]
                end_point = face_landmarks.landmark[end_idx]
                start_x = int(start_point.x * w)
                start_y = int(start_point.y * h)
                end_x = int(end_point.x * w)
                end_y = int(end_point.y * h)
                cv2.line(frame, (start_x, start_y), (end_x, end_y), (255, 0, 255), 1)
    
    def _draw_hand_connections(self, frame: np.ndarray, hand_landmarks, w: int, h: int):
        """Draw hand skeleton connections."""
        # MediaPipe hand connections
        connections = [
            # Thumb
            (0, 1), (1, 2), (2, 3), (3, 4),
            # Index finger
            (0, 5), (5, 6), (6, 7), (7, 8),
            # Middle finger
            (0, 9), (9, 10), (10, 11), (11, 12),
            # Ring finger
            (0, 13), (13, 14), (14, 15), (15, 16),
            # Pinky
            (0, 17), (17, 18), (18, 19), (19, 20),
            # Palm connections
            (5, 9), (9, 13), (13, 17)
        ]
        
        for start_idx, end_idx in connections:
            if start_idx < len(hand_landmarks.landmark) and end_idx < len(hand_landmarks.landmark):
                start_point = hand_landmarks.landmark[start_idx]
                end_point = hand_landmarks.landmark[end_idx]
                start_x = int(start_point.x * w)
                start_y = int(start_point.y * h)
                end_x = int(end_point.x * w)
                end_y = int(end_point.y * h)
                cv2.line(frame, (start_x, start_y), (end_x, end_y), (0, 0, 255), 2)
    
    def _draw_pose_connections(self, frame: np.ndarray, pose_landmarks, w: int, h: int):
        """Draw pose skeleton connections."""
        # MediaPipe pose connections
        connections = [
            # Torso
            (11, 12), (11, 13), (12, 14), (11, 23), (12, 24), (23, 24),
            # Left arm
            (11, 13), (13, 15), (15, 17), (15, 19), (15, 21), (17, 19), (19, 21),
            # Right arm
            (12, 14), (14, 16), (16, 18), (16, 20), (16, 22), (18, 20), (20, 22),
            # Left leg
            (23, 25), (25, 27), (27, 29), (27, 31), (29, 31),
            # Right leg
            (24, 26), (26, 28), (28, 30), (28, 32), (30, 32),
            # Face connections
            (0, 1), (1, 2), (2, 3), (3, 7), (0, 4), (4, 5), (5, 6), (6, 8)
        ]
        
        for start_idx, end_idx in connections:
            if start_idx < len(pose_landmarks.landmark) and end_idx < len(pose_landmarks.landmark):
                start_point = pose_landmarks.landmark[start_idx]
                end_point = pose_landmarks.landmark[end_idx]
                start_x = int(start_point.x * w)
                start_y = int(start_point.y * h)
                end_x = int(end_point.x * w)
                end_y = int(end_point.y * h)
                cv2.line(frame, (start_x, start_y), (end_x, end_y), (0, 255, 255), 2)
    
    def draw_complete_overlay(self, frame: np.ndarray, focus_metrics: Dict[str, Any],
                            fps: float, frame_width: int, frame_height: int,
                            show_grid: bool = True, show_landmarks: bool = False,
                            results: Optional[Dict[str, Any]] = None) -> np.ndarray:
        """
        Draw complete focus tracking overlay.
        
        Args:
            frame: Input frame
            focus_metrics: Focus evaluation results
            fps: Current FPS
            frame_width: Frame width
            frame_height: Frame height
            show_grid: Whether to show focus grid
            show_landmarks: Whether to show landmarks
            results: Detection results for landmarks
            
        Returns:
            Frame with complete overlay
        """
        # Draw attention ring
        frame = self.draw_focus_ring(
            frame, focus_metrics.get("focused", False), 
            focus_metrics.get("focus_score", 0.0), 
            frame_width, frame_height
        )
        
        # Draw status text
        frame = self.draw_status_text(frame, focus_metrics, fps, frame_width, frame_height)
        
        # Draw focus grid
        if show_grid:
            frame = self.draw_focus_grid(frame, focus_metrics, frame_width, frame_height)
        
        # Draw landmarks if requested
        if show_landmarks and results is not None:
            frame = self.draw_landmarks_overlay(frame, results)
        
        return frame
