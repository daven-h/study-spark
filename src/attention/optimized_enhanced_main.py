"""
Optimized Enhanced Attention Tracker
Uses MediaPipe Objectron for phone detection (no custom rectangle detection)
"""

import cv2
import numpy as np
import time
import json
from typing import Dict, Any
from tracker import FocusTracker
from focus_logic import FocusEvaluator
from visualizer import FocusVisualizer


class FPSCounter:
    """Simple FPS counter"""
    def __init__(self):
        self.frame_count = 0
        self.start_time = time.time()
    
    def get_fps(self):
        self.frame_count += 1
        elapsed = time.time() - self.start_time
        if elapsed > 0:
            return self.frame_count / elapsed
        return 0.0


class OptimizedEnhancedAttentionTracker:
    """
    Optimized enhanced attention tracker with MediaPipe Objectron phone detection
    """
    
    def __init__(self):
        """Initialize the optimized enhanced tracker"""
        # Initialize components
        self.tracker = FocusTracker()
        self.evaluator = FocusEvaluator()
        self.visualizer = FocusVisualizer()
        self.fps_counter = FPSCounter()
        
        # Camera settings
        self.camera_index = 0
        self.cap = None
        self.frame_width = 640
        self.frame_height = 480
        
        # Display settings
        self.show_detections = True
        self.show_landmarks = True
        self.show_attention_ring = True
        
        # Focus tracking
        self.focus_history = []
        self.max_history = 100
        
        # Phone detection settings
        self.phone_confidence_threshold = 0.5
        self.phone_proximity_threshold = 100  # pixels
        
        # Hand gesture analysis for phone detection
        self.hand_phone_threshold = 0.15  # Distance threshold for hand near face
        
    def initialize_camera(self) -> bool:
        """Initialize camera capture"""
        try:
            self.cap = cv2.VideoCapture(self.camera_index)
            if not self.cap.isOpened():
                print(f"❌ Could not open camera {self.camera_index}")
                return False
            
            # Set camera properties
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.frame_width)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.frame_height)
            self.cap.set(cv2.CAP_PROP_FPS, 30)
            
            print(f"✅ Camera initialized: {self.frame_width}x{self.frame_height}")
            return True
            
        except Exception as e:
            print(f"❌ Camera initialization failed: {e}")
            return False
    
    def detect_phone_objects(self, frame: np.ndarray, face_bbox: tuple = None) -> Dict[str, Any]:
        """
        Enhanced phone detection with shape and texture analysis to distinguish phones from water bottles
        
        Args:
            frame: Input frame
            face_bbox: Face bounding box (x1, y1, x2, y2)
            
        Returns:
            Phone detection results
        """
        # Get MediaPipe object detection results
        results = self.tracker.process_frame(frame)
        object_results = results.get("objects", {})
        
        # Extract phone detections
        phone_objects = []
        phone_near_face = False
        max_confidence = 0.0
        
        # Check MediaPipe object detection
        if object_results.get("phone_detected", False):
            objects_detected = object_results.get("objects_detected", [])
            
            for obj in objects_detected:
                if obj.get("type") == "phone":
                    confidence = obj.get("confidence", 0.0)
                    landmarks = obj.get("landmarks")
                    
                    if confidence > self.phone_confidence_threshold:
                        # Calculate bounding box from landmarks if available
                        if landmarks:
                            # Convert landmarks to bounding box
                            x_coords = [lm[0] for lm in landmarks]
                            y_coords = [lm[1] for lm in landmarks]
                            
                            x1 = int(min(x_coords) * self.frame_width)
                            y1 = int(min(y_coords) * self.frame_height)
                            x2 = int(max(x_coords) * self.frame_width)
                            y2 = int(max(y_coords) * self.frame_height)
                            
                            # Enhanced phone validation using shape analysis
                            is_likely_phone = self.validate_phone_shape(frame, x1, y1, x2, y2)
                            
                            if is_likely_phone:
                                phone_obj = {
                                    'bbox': (x1, y1, x2, y2),
                                    'confidence': confidence,
                                    'center': ((x1 + x2) // 2, (y1 + y2) // 2),
                                    'near_face': False
                                }
                                
                                # Check if phone is near face
                                if face_bbox:
                                    fx1, fy1, fx2, fy2 = face_bbox
                                    if (x2 > fx1 - self.phone_proximity_threshold and 
                                        x1 < fx2 + self.phone_proximity_threshold and
                                        y2 > fy1 - self.phone_proximity_threshold and 
                                        y1 < fy2 + self.phone_proximity_threshold):
                                        phone_obj['near_face'] = True
                                        phone_near_face = True
                                        max_confidence = max(max_confidence, confidence)
                                
                                phone_objects.append(phone_obj)
        
        return {
            'phone_objects': phone_objects,
            'phone_near_face': phone_near_face,
            'max_confidence': max_confidence,
            'total_detections': len(phone_objects)
        }
    
    def validate_phone_shape(self, frame: np.ndarray, x1: int, y1: int, x2: int, y2: int) -> bool:
        """
        Validate if detected object is likely a phone based on shape characteristics
        
        Args:
            frame: Input frame
            x1, y1, x2, y2: Bounding box coordinates
            
        Returns:
            True if object is likely a phone, False otherwise
        """
        try:
            # Extract region of interest
            roi = frame[y1:y2, x1:x2]
            if roi.size == 0:
                return False
            
            # Calculate aspect ratio
            width = x2 - x1
            height = y2 - y1
            aspect_ratio = width / height if height > 0 else 0
            
            # Phone characteristics:
            # - Aspect ratio should be between 0.4 and 2.5 (rectangular, not too square, not too thin)
            # - Should have reasonable size (not too small, not too large)
            # - Should have some rectangular characteristics
            
            # Check aspect ratio (phones are typically rectangular)
            if not (0.4 <= aspect_ratio <= 2.5):
                return False
            
            # Check size (not too small or too large relative to frame)
            frame_area = self.frame_width * self.frame_height
            object_area = width * height
            area_ratio = object_area / frame_area
            
            # Phone should be reasonable size (not tiny, not huge)
            if not (0.001 <= area_ratio <= 0.1):
                return False
            
            # Analyze shape using contour detection
            gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray_roi, 50, 150)
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            if contours:
                # Get largest contour
                largest_contour = max(contours, key=cv2.contourArea)
                
                # Calculate contour properties
                area = cv2.contourArea(largest_contour)
                perimeter = cv2.arcLength(largest_contour, True)
                
                if perimeter > 0:
                    # Calculate solidity (how "solid" the shape is)
                    hull = cv2.convexHull(largest_contour)
                    hull_area = cv2.contourArea(hull)
                    solidity = area / hull_area if hull_area > 0 else 0
                    
                    # Calculate extent (how much of the bounding box is filled)
                    bbox_area = width * height
                    extent = area / bbox_area if bbox_area > 0 else 0
                    
                    # Phone characteristics:
                    # - High solidity (not too irregular)
                    # - Good extent (fills bounding box reasonably)
                    # - Not too circular (water bottles are more circular)
                    
                    if solidity > 0.7 and extent > 0.6:
                        # Additional check: analyze for rectangular characteristics
                        # Approximate contour to polygon
                        epsilon = 0.02 * perimeter
                        approx = cv2.approxPolyDP(largest_contour, epsilon, True)
                        
                        # Phones typically have 4 corners (rectangular)
                        # Water bottles are more circular/oval
                        if len(approx) >= 4:  # Has corners (rectangular)
                            return True
                        elif len(approx) <= 3:  # Very smooth (circular/oval like water bottle)
                            return False
                        else:
                            # In between - use other characteristics
                            return solidity > 0.8 and extent > 0.7
            
            return False
            
        except Exception as e:
            # If analysis fails, default to original confidence
            return True
    
    def analyze_hand_phone_gesture(self, hands_landmarks: list, face_landmarks: Any) -> Dict[str, Any]:
        """
        Enhanced hand gesture analysis to detect phone usage patterns
        
        Args:
            hands_landmarks: List of hand landmarks from MediaPipe
            face_landmarks: Face landmarks from MediaPipe
            
        Returns:
            Hand gesture analysis results
        """
        phone_gesture_detected = False
        gesture_confidence = 0.0
        gesture_type = "none"
        
        if not hands_landmarks or not face_landmarks:
            return {
                "phone_gesture_detected": False,
                "gesture_confidence": 0.0,
                "gesture_type": "none"
            }
        
        for hand_landmarks in hands_landmarks:
            # Get key hand points
            thumb_tip = hand_landmarks.landmark[4]  # Thumb tip
            thumb_ip = hand_landmarks.landmark[3]   # Thumb IP joint
            thumb_mcp = hand_landmarks.landmark[2]   # Thumb MCP joint
            index_tip = hand_landmarks.landmark[8]  # Index finger tip
            index_pip = hand_landmarks.landmark[6]  # Index PIP joint
            index_mcp = hand_landmarks.landmark[5]  # Index MCP joint
            middle_tip = hand_landmarks.landmark[12]  # Middle finger tip
            middle_pip = hand_landmarks.landmark[10]  # Middle PIP joint
            middle_mcp = hand_landmarks.landmark[9]   # Middle MCP joint
            ring_tip = hand_landmarks.landmark[16]  # Ring finger tip
            pinky_tip = hand_landmarks.landmark[20]  # Pinky tip
            
            # Get face center for distance calculation
            face_center_x = (face_landmarks.landmark[1].x + face_landmarks.landmark[2].x) / 2
            face_center_y = (face_landmarks.landmark[1].y + face_landmarks.landmark[2].y) / 2
            
            # Calculate distances from fingertips to face center
            thumb_distance = ((thumb_tip.x - face_center_x) ** 2 + (thumb_tip.y - face_center_y) ** 2) ** 0.5
            index_distance = ((index_tip.x - face_center_x) ** 2 + (index_tip.y - face_center_y) ** 2) ** 0.5
            middle_distance = ((middle_tip.x - face_center_x) ** 2 + (middle_tip.y - face_center_y) ** 2) ** 0.5
            
            # Check if hand is near face
            hand_near_face = any(dist < self.hand_phone_threshold for dist in [thumb_distance, index_distance, middle_distance])
            
            if hand_near_face:
                # Enhanced phone detection logic
                
                # 1. Check for phone holding grip (thumb and index finger close together)
                thumb_index_distance = ((thumb_tip.x - index_tip.x) ** 2 + (thumb_tip.y - index_tip.y) ** 2) ** 0.5
                
                # 2. Check finger extension (how extended the fingers are)
                # Calculate finger extension ratios
                index_extension = ((index_tip.x - index_mcp.x) ** 2 + (index_tip.y - index_mcp.y) ** 2) ** 0.5
                middle_extension = ((middle_tip.x - middle_mcp.x) ** 2 + (middle_tip.y - middle_mcp.y) ** 2) ** 0.5
                thumb_extension = ((thumb_tip.x - thumb_mcp.x) ** 2 + (thumb_tip.y - thumb_mcp.y) ** 2) ** 0.5
                
                # 3. Check for specific phone holding patterns
                # Phone holding typically involves:
                # - Thumb and index finger close together (pinching)
                # - Other fingers extended or slightly bent
                # - Hand positioned for holding a rectangular object
                
                # Calculate finger bend ratios (how bent the fingers are)
                index_bend = ((index_pip.x - index_mcp.x) ** 2 + (index_pip.y - index_mcp.y) ** 2) ** 0.5
                middle_bend = ((middle_pip.x - middle_mcp.x) ** 2 + (middle_pip.y - middle_mcp.y) ** 2) ** 0.5
                
                # Phone detection criteria - more lenient thresholds
                is_pinching = thumb_index_distance < 0.06  # Thumb and index close (more lenient)
                fingers_extended = index_extension > 0.04 and middle_extension > 0.04  # Fingers extended (more lenient)
                proper_grip = index_bend > 0.02 and middle_bend > 0.02  # Fingers properly bent for grip (more lenient)
                
                # Additional check: hand orientation (phone is typically held vertically)
                hand_orientation = abs(index_tip.y - thumb_tip.y)  # Vertical orientation
                
                # More comprehensive phone detection
                # Check if hand is in a position that could be holding a phone
                hand_phone_likelihood = 0.0
                
                # Base likelihood from hand position
                if hand_near_face:
                    hand_phone_likelihood += 0.3
                
                # Pinching gesture (thumb and index close)
                if is_pinching:
                    hand_phone_likelihood += 0.4
                else:
                    # Even if not pinching, check if fingers are in phone-holding position
                    if index_extension > 0.03 and middle_extension > 0.03:
                        hand_phone_likelihood += 0.2
                
                # Finger extension (holding something)
                if fingers_extended:
                    hand_phone_likelihood += 0.3
                elif index_extension > 0.02 or middle_extension > 0.02:
                    hand_phone_likelihood += 0.1
                
                # Hand orientation
                if hand_orientation > 0.03:  # Some vertical orientation
                    hand_phone_likelihood += 0.2
                
                # Phone holding detection with threshold
                if hand_phone_likelihood > 0.6:  # High confidence threshold
                    phone_gesture_detected = True
                    gesture_confidence = min(0.95, hand_phone_likelihood)
                    gesture_type = "phone_holding"
                elif hand_phone_likelihood > 0.4:  # Medium confidence
                    phone_gesture_detected = False
                    gesture_confidence = hand_phone_likelihood
                    gesture_type = "holding_object"
                elif hand_phone_likelihood > 0.2:  # Low confidence
                    phone_gesture_detected = False
                    gesture_confidence = hand_phone_likelihood
                    gesture_type = "hand_resting"
                else:
                    # Very low confidence
                    phone_gesture_detected = False
                    gesture_confidence = hand_phone_likelihood
                    gesture_type = "unclear_gesture"
            else:
                # Hand not near face
                phone_gesture_detected = False
                gesture_confidence = 0.0
                gesture_type = "hand_away"
        
        return {
            "phone_gesture_detected": phone_gesture_detected,
            "gesture_confidence": gesture_confidence,
            "gesture_type": gesture_type
        }
    
    def process_frame(self, frame: np.ndarray) -> Dict[str, Any]:
        """
        Process a single frame with optimized phone detection
        
        Args:
            frame: Input frame
            
        Returns:
            Enhanced focus metrics
        """
        # Get MediaPipe detection results
        results = self.tracker.process_frame(frame)
        
        # Get face bounding box for phone detection
        face_bbox = results["face"].get("face_bbox")
        
        # Detect phone objects using MediaPipe Objectron
        phone_detections = self.detect_phone_objects(frame, face_bbox)
        
        # Analyze hand gestures for phone usage
        hands_landmarks = results["hands"].get("hands_landmarks", [])
        face_landmarks = results["face"].get("face_landmarks")
        gesture_analysis = self.analyze_hand_phone_gesture(hands_landmarks, face_landmarks)
        
        # Enhanced phone detection: if hands are near face, consider it phone usage
        hand_near_face = results["hands"].get("hands_detected", 0) > 0 and face_landmarks
        if hand_near_face and not gesture_analysis["phone_gesture_detected"]:
            # If hands detected near face but no clear gesture, still flag as potential phone
            gesture_analysis["phone_gesture_detected"] = True
            gesture_analysis["gesture_confidence"] = 0.7
            gesture_analysis["gesture_type"] = "hand_near_face"
        
        # Add phone detection data to results
        results["phone_detections"] = phone_detections
        results["gesture_analysis"] = gesture_analysis
        
        # Evaluate focus with enhanced logic
        focus_metrics = self.evaluator.evaluate_focus(
            results["face"], results["hands"], results["pose"],
            self.frame_width, self.frame_height, results["objects"], results
        )
        
        # Add phone detection metrics
        focus_metrics["phone_near_face"] = phone_detections["phone_near_face"]
        focus_metrics["phone_confidence"] = phone_detections["max_confidence"]
        focus_metrics["phone_objects_count"] = phone_detections["total_detections"]
        
        # Add gesture analysis metrics
        focus_metrics["phone_gesture_detected"] = gesture_analysis["phone_gesture_detected"]
        focus_metrics["gesture_confidence"] = gesture_analysis["gesture_confidence"]
        focus_metrics["gesture_type"] = gesture_analysis["gesture_type"]
        
        # Combined phone detection (object detection OR gesture analysis)
        focus_metrics["phone_detected_combined"] = (
            phone_detections["phone_near_face"] or 
            gesture_analysis["phone_gesture_detected"]
        )
        
        # Add FPS
        fps = self.fps_counter.get_fps()
        focus_metrics["fps"] = fps
        
        # Update focus history
        self.focus_history.append(focus_metrics["focus_score"])
        if len(self.focus_history) > self.max_history:
            self.focus_history.pop(0)
        
        return focus_metrics, results
    
    def draw_overlay(self, frame: np.ndarray, focus_metrics: Dict[str, Any], 
                    detection_results: Dict[str, Any]) -> np.ndarray:
        """
        Draw optimized overlay on frame
        
        Args:
            frame: Input frame
            focus_metrics: Focus evaluation results
            detection_results: Detection results
            
        Returns:
            Frame with optimized overlay
        """
        # Draw attention ring
        if self.show_attention_ring:
            frame = self.visualizer.draw_focus_ring(
                frame, focus_metrics.get("focused", False), 
                focus_metrics.get("focus_score", 0.0), 
                self.frame_width, self.frame_height
            )
        
        # Draw phone detection overlays
        if self.show_detections:
            frame = self.draw_phone_overlays(frame, detection_results)
        
        # Draw landmarks if enabled
        if self.show_landmarks:
            frame = self.visualizer.draw_landmarks_overlay(frame, detection_results)
        
        # Draw enhanced status overlay
        frame = self.draw_enhanced_status_overlay(frame, focus_metrics)
        
        # Draw debug gesture information
        frame = self.draw_gesture_debug(frame, focus_metrics)
        
        return frame
    
    def draw_phone_overlays(self, frame: np.ndarray, results: Dict[str, Any]) -> np.ndarray:
        """
        Draw phone detection overlays using MediaPipe Objectron
        
        Args:
            frame: Input frame
            results: Detection results
            
        Returns:
            Frame with phone overlays
        """
        phone_detections = results.get("phone_detections", {})
        phone_objects = phone_detections.get("phone_objects", [])
        phone_near_face = phone_detections.get("phone_near_face", False)
        
        for phone_obj in phone_objects:
            x1, y1, x2, y2 = phone_obj["bbox"]
            confidence = phone_obj["confidence"]
            near_face = phone_obj["near_face"]
            
            # Color based on proximity to face
            if near_face:
                color = (0, 0, 255)  # Red for phone near face
                thickness = 3
                label = f"📱 Phone {confidence:.2f}"
            else:
                color = (255, 0, 0)  # Blue for phone not near face
                thickness = 2
                label = f"📱 Phone {confidence:.2f}"
            
            # Draw phone bounding box
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, thickness)
            
            # Draw confidence label
            cv2.putText(frame, label, (x1, y1 - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
            
            # Draw center point
            center_x, center_y = phone_obj["center"]
            cv2.circle(frame, (center_x, center_y), 5, color, -1)
        
        # Draw overall phone status
        if phone_near_face:
            status_text = "📱 PHONE DETECTED"
            status_color = (0, 0, 255)
        else:
            status_text = "✅ NO PHONE"
            status_color = (0, 255, 0)
        
        # Draw status in top right
        cv2.putText(frame, status_text, (self.frame_width - 200, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, status_color, 2)
        
        return frame
    
    def draw_enhanced_status_overlay(self, frame: np.ndarray, focus_metrics: Dict[str, Any]) -> np.ndarray:
        """
        Draw enhanced status overlay with phone detection
        
        Args:
            frame: Input frame
            focus_metrics: Focus evaluation results
            
        Returns:
            Frame with enhanced status overlay
        """
        # Extract metrics
        focused = focus_metrics.get("focused", False)
        focus_score = focus_metrics.get("focus_score", 0.0)
        face_visible = focus_metrics.get("face_visible", False)
        yaw = focus_metrics.get("yaw", 0)
        pitch = focus_metrics.get("pitch", 0)
        hand_near_face = focus_metrics.get("hand_near_face", False)
        phone_near_face = focus_metrics.get("phone_near_face", False)
        phone_confidence = focus_metrics.get("phone_confidence", 0.0)
        posture_stable = focus_metrics.get("posture_stable", True)
        fps = focus_metrics.get("fps", 0.0)
        
        # Status messages
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
        
        # Enhanced phone detection status with detailed gesture analysis
        phone_gesture_detected = focus_metrics.get("phone_gesture_detected", False)
        gesture_type = focus_metrics.get("gesture_type", "none")
        gesture_confidence = focus_metrics.get("gesture_confidence", 0.0)
        phone_detected_combined = focus_metrics.get("phone_detected_combined", False)
        
        if phone_detected_combined:
            if phone_near_face:
                hand_status = f"✗ Phone detected ({phone_confidence:.2f})"
            elif phone_gesture_detected:
                hand_status = f"✗ Phone gesture ({gesture_type})"
            else:
                hand_status = "✗ Put phone down"
            hand_color = (0, 0, 255)
        elif hand_near_face:
            # Hand near face but no phone detected - analyze gesture type
            if gesture_type == "phone_holding":
                hand_status = f"✗ Phone detected ({gesture_confidence:.2f})"
                hand_color = (0, 0, 255)
            elif gesture_type == "hand_resting":
                hand_status = "✓ Hand resting (not phone)"
                hand_color = (0, 255, 0)
            elif gesture_type == "holding_object":
                hand_status = f"⚠ Holding object ({gesture_confidence:.2f})"
                hand_color = (0, 165, 255)  # Orange
            elif gesture_type == "open_hand":
                hand_status = "⚠ Open hand near face"
                hand_color = (0, 165, 255)  # Orange
            elif gesture_type == "unclear_gesture":
                hand_status = f"⚠ Unclear gesture ({gesture_confidence:.2f})"
                hand_color = (0, 165, 255)  # Orange
            else:
                hand_status = "⚠ Hand near face"
                hand_color = (0, 165, 255)  # Orange
        else:
            hand_status = "✓ No phone"
            hand_color = (0, 255, 0)
        
        if posture_stable:
            posture_status = "✓ Sit up straight"
            posture_color = (0, 255, 0)
        else:
            posture_status = "✗ Straighten posture"
            posture_color = (0, 0, 255)
        
        # Main panel
        panel_width = 350
        panel_height = 180
        panel_x = 20
        panel_y = 20
        
        # Background panel
        cv2.rectangle(frame, (panel_x, panel_y), 
                     (panel_x + panel_width, panel_y + panel_height), 
                     (20, 20, 20), -1)
        cv2.rectangle(frame, (panel_x, panel_y), 
                     (panel_x + panel_width, panel_y + panel_height), 
                     (60, 60, 60), 1)
        
        # Title
        cv2.putText(frame, "OPTIMIZED ATTENTION TRACKER", (panel_x + 15, panel_y + 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Status items
        y_start = panel_y + 50
        items = [
            ("FACE", face_status, face_color),
            ("ORIENTATION", orientation_status, orientation_color),
            ("PHONE", hand_status, hand_color),
            ("POSTURE", posture_status, posture_color)
        ]
        
        for i, (label, status, color) in enumerate(items):
            y_pos = y_start + (i * 28)
            
            # Label
            cv2.putText(frame, label, (panel_x + 15, y_pos),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (180, 180, 180), 1)
            
            # Status
            cv2.putText(frame, status, (panel_x + 15, y_pos + 18),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        
        # Main status
        main_status = "FOCUSED" if focused else "DISTRACTED"
        main_color = (0, 255, 100) if focused else (255, 100, 100)
        
        status_bg_x = panel_x + 15
        status_bg_y = panel_y + 150
        cv2.rectangle(frame, (status_bg_x, status_bg_y), 
                     (status_bg_x + 200, status_bg_y + 25), 
                     (30, 30, 30), -1)
        
        cv2.putText(frame, main_status, (status_bg_x + 10, status_bg_y + 18),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, main_color, 2)
        
        # Metrics panel
        metrics_width = 180
        metrics_height = 80
        metrics_x = self.frame_width - metrics_width - 20
        metrics_y = self.frame_height - metrics_height - 20
        
        cv2.rectangle(frame, (metrics_x, metrics_y), 
                     (metrics_x + metrics_width, metrics_y + metrics_height), 
                     (20, 20, 20), -1)
        cv2.rectangle(frame, (metrics_x, metrics_y), 
                     (metrics_x + metrics_width, metrics_y + metrics_height), 
                     (60, 60, 60), 1)
        
        cv2.putText(frame, "METRICS", (metrics_x + 10, metrics_y + 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (180, 180, 180), 1)
        
        cv2.putText(frame, f"Score: {focus_score:.2f}", (metrics_x + 10, metrics_y + 45),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        cv2.putText(frame, f"FPS: {fps:.1f}", (metrics_x + 10, metrics_y + 65),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        return frame
    
    def draw_gesture_debug(self, frame: np.ndarray, focus_metrics: Dict[str, Any]) -> np.ndarray:
        """
        Draw debug information about gesture analysis
        
        Args:
            frame: Input frame
            focus_metrics: Focus evaluation results
            
        Returns:
            Frame with debug information
        """
        gesture_type = focus_metrics.get("gesture_type", "none")
        gesture_confidence = focus_metrics.get("gesture_confidence", 0.0)
        phone_gesture_detected = focus_metrics.get("phone_gesture_detected", False)
        
        # Debug panel in top right
        debug_x = self.frame_width - 250
        debug_y = 50
        
        # Background
        cv2.rectangle(frame, (debug_x, debug_y), (debug_x + 240, debug_y + 100), (0, 0, 0), -1)
        cv2.rectangle(frame, (debug_x, debug_y), (debug_x + 240, debug_y + 100), (100, 100, 100), 1)
        
        # Title
        cv2.putText(frame, "GESTURE DEBUG", (debug_x + 10, debug_y + 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Gesture type
        cv2.putText(frame, f"Type: {gesture_type}", (debug_x + 10, debug_y + 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
        
        # Confidence
        cv2.putText(frame, f"Confidence: {gesture_confidence:.2f}", (debug_x + 10, debug_y + 55),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
        
        # Phone detected
        phone_text = "YES" if phone_gesture_detected else "NO"
        phone_color = (0, 255, 0) if phone_gesture_detected else (0, 0, 255)
        cv2.putText(frame, f"Phone: {phone_text}", (debug_x + 10, debug_y + 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, phone_color, 1)
        
        # Gesture explanation
        if gesture_type == "phone_holding":
            explanation = "Pinching + Extended fingers"
        elif gesture_type == "hand_resting":
            explanation = "Curled fingers (resting)"
        elif gesture_type == "holding_object":
            explanation = "Pinching but horizontal"
        elif gesture_type == "open_hand":
            explanation = "Extended but not pinching"
        else:
            explanation = "No clear pattern"
        
        cv2.putText(frame, explanation, (debug_x + 10, debug_y + 85),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.3, (200, 200, 200), 1)
        
        return frame
    
    def print_focus_metrics(self, focus_metrics: Dict[str, Any]):
        """Print focus metrics as JSON"""
        output = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "focused": focus_metrics["focused"],
            "focus_score": round(focus_metrics["focus_score"], 2),
            "face_visible": focus_metrics["face_visible"],
            "yaw": round(focus_metrics.get("yaw", 0), 3),
            "pitch": round(focus_metrics.get("pitch", 0), 3),
            "hand_near_face": focus_metrics["hand_near_face"],
            "phone_near_face": focus_metrics.get("phone_near_face", False),
            "phone_confidence": round(focus_metrics.get("phone_confidence", 0), 2),
            "phone_objects_count": focus_metrics.get("phone_objects_count", 0),
            "posture_stable": focus_metrics["posture_stable"],
            "fps": round(focus_metrics["fps"], 1)
        }
        
        print(json.dumps(output))
    
    def run(self):
        """Run the optimized enhanced attention tracker"""
        print("🚀 Starting Optimized Enhanced Attention Tracker...")
        print("📱 MediaPipe Objectron Phone Detection")
        print("🎯 Optimized Phone vs Hand Detection")
        print("Press 'q' to quit, 'r' to reset, 's' to save screenshot")
        
        # Initialize camera
        if not self.initialize_camera():
            return
        
        try:
            while True:
                # Capture frame
                ret, frame = self.cap.read()
                if not ret:
                    print("❌ Failed to read frame")
                    break
                
                # Process frame
                focus_metrics, detection_results = self.process_frame(frame)
                
                # Draw overlay
                frame = self.draw_overlay(frame, focus_metrics, detection_results)
                
                # Display frame
                cv2.imshow("Optimized Enhanced Attention Tracker", frame)
                
                # Print metrics
                self.print_focus_metrics(focus_metrics)
                
                # Handle keyboard input
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
                elif key == ord('r'):
                    self.focus_history.clear()
                    print("🔄 Focus history reset")
                elif key == ord('s'):
                    filename = f"optimized_screenshot_{int(time.time())}.jpg"
                    cv2.imwrite(filename, frame)
                    print(f"📸 Screenshot saved: {filename}")
                elif key == ord('d'):
                    self.show_detections = not self.show_detections
                    print(f"🔍 Detections: {'ON' if self.show_detections else 'OFF'}")
                elif key == ord('l'):
                    self.show_landmarks = not self.show_landmarks
                    print(f"📍 Landmarks: {'ON' if self.show_landmarks else 'OFF'}")
                elif key == ord('a'):
                    self.show_attention_ring = not self.show_attention_ring
                    print(f"🎯 Attention Ring: {'ON' if self.show_attention_ring else 'OFF'}")
        
        except KeyboardInterrupt:
            print("\n⏹️ Interrupted by user")
        
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources"""
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
        print("✅ Optimized Enhanced Attention Tracker stopped")


def main():
    """Main function"""
    tracker = OptimizedEnhancedAttentionTracker()
    tracker.run()


if __name__ == "__main__":
    main()
