"""
Flexible Phone Detector
More lenient detection for rectangular objects that could be phones
"""

import cv2
import numpy as np
from typing import List, Dict, Any, Tuple
import mediapipe as mp

class FlexiblePhoneDetector:
    """
    Flexible phone detector with more lenient criteria
    """
    
    def __init__(self):
        # iPhone X and newer detection schemas
        self.iphone_models = {
            # iPhone X series (X, XS, 11 Pro, 12, 13, 14, 15)
            "iPhone X": {"ratio": 2.03, "width": 70.9, "height": 143.6},
            "iPhone 11 Pro": {"ratio": 2.02, "width": 71.4, "height": 144.0},
            "iPhone 12": {"ratio": 2.05, "width": 71.5, "height": 146.7},
            "iPhone 13": {"ratio": 2.05, "width": 71.5, "height": 146.7},
            "iPhone 14": {"ratio": 2.05, "width": 71.5, "height": 146.7},
            "iPhone 15": {"ratio": 2.08, "width": 70.9, "height": 147.6},
        }
        # Acceptable ranges based on iPhone X and up
        self.min_aspect_ratio = 2.0  # iPhone X+ minimum
        self.max_aspect_ratio = 2.1  # iPhone X+ maximum
        self.min_area = 2000  # iPhone minimum area
        self.max_area = 50000  # iPhone maximum area
        self.ideal_ratio = 2.05  # Average of iPhone X series
        
        # Initialize MediaPipe Hands for phone-in-hand detection
        # (Phone-in-hand detection inspired by Roboflow approach)
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.hand_landmarks = None
        
    def detect_phone_objects(self, frame: np.ndarray) -> List[Dict[str, Any]]:
        """
        Detect phone-like objects with flexible criteria
        
        Args:
            frame: Input frame (BGR format)
            
        Returns:
            List of detected phone objects
        """
        detections = []
        
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Apply Gaussian blur
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            
            # Edge detection
            edges = cv2.Canny(blurred, 30, 100)  # More sensitive
            
            # Find contours
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            for contour in contours:
                # Approximate contour to polygon
                perimeter = cv2.arcLength(contour, True)
                if perimeter < 50:  # Skip very small contours
                    continue
                    
                approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
                
                # Check if it's roughly rectangular (3-6 corners)
                if 3 <= len(approx) <= 6:
                    # Get bounding rectangle
                    x, y, w, h = cv2.boundingRect(approx)
                    area = cv2.contourArea(contour)
                    aspect_ratio = float(w) / h
                    
                    # iPhone-specific detection
                    if self._is_phone_like(x, y, w, h, area, aspect_ratio):
                        # Calculate confidence based on iPhone dimensions
                        confidence = self._calculate_phone_confidence(w, h, area, aspect_ratio)
                        
                        detections.append({
                            'class_id': 67,  # Cell phone class
                            'class_name': 'iPhone',
                            'confidence': confidence,
                            'bbox': (x, y, x + w, y + h),
                            'center': (x + w // 2, y + h // 2),
                            'area': area,
                            'aspect_ratio': aspect_ratio
                        })
            
            # Sort by confidence
            detections.sort(key=lambda x: x['confidence'], reverse=True)
            
            return detections
            
        except Exception as e:
            print(f"Phone detection error: {e}")
            return []
    
    def _is_phone_like(self, x: int, y: int, w: int, h: int, area: float, aspect_ratio: float) -> bool:
        """
        iPhone-specific detection criteria
        """
        # Check aspect ratio (iPhones have specific dimensions)
        if not (self.min_aspect_ratio <= aspect_ratio <= self.max_aspect_ratio):
            return False
        
        # Check area (iPhone-sized)
        if not (self.min_area <= area <= self.max_area):
            return False
        
        # Check size (reasonable iPhone size)
        if w < 30 or h < 50:  # Too small for iPhone
            return False
        if w > 200 or h > 400:  # Too large for iPhone
            return False
        
        # Check if it's roughly rectangular (iPhones are very rectangular)
        rect_area = w * h
        if area / rect_area < 0.7:  # iPhones are very rectangular
            return False
        
        return True
    
    def _calculate_phone_confidence(self, w: int, h: int, area: float, aspect_ratio: float) -> float:
        """
        Calculate confidence that object is an iPhone X or newer
        Uses actual build schemas of iPhone X, 11 Pro, 12, 13, 14, 15
        """
        confidence = 0.0
        
        # iPhone X+ aspect ratio confidence (closer to 2.05 is better)
        ideal_ratio = 2.05  # Average of iPhone X series
        ratio_diff = abs(aspect_ratio - ideal_ratio)
        ratio_confidence = max(0.0, 1.0 - (ratio_diff / ideal_ratio))
        confidence += ratio_confidence * 0.4
        
        # Area confidence (prefer iPhone X+ sized objects)
        ideal_area = 15000  # Ideal iPhone X+ area in pixels
        area_diff = abs(area - ideal_area)
        area_confidence = max(0.0, 1.0 - (area_diff / ideal_area))
        confidence += area_confidence * 0.3
        
        # Size confidence (prefer iPhone X+ dimensions ~70x140mm scaled)
        ideal_width = 70  # Scaled from actual 71mm iPhone width
        ideal_height = 145  # Scaled from actual 146mm iPhone height
        width_diff = abs(w - ideal_width)
        height_diff = abs(h - ideal_height)
        size_confidence = max(0.0, 1.0 - ((width_diff / ideal_width) + (height_diff / ideal_height)) / 2)
        confidence += size_confidence * 0.3
        
        return min(1.0, confidence)
    
    def detect_hands(self, frame: np.ndarray) -> List[Dict[str, Any]]:
        """
        Detect hands using MediaPipe (phone-in-hand detection)
        Inspired by Roboflow phone-in-hand approach
        """
        self.hand_landmarks = []
        
        try:
            # Convert BGR to RGB for MediaPipe
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(rgb_frame)
            
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Get hand bounding box
                    h, w, _ = frame.shape
                    x_coords = [landmark.x * w for landmark in hand_landmarks.landmark]
                    y_coords = [landmark.y * h for landmark in hand_landmarks.landmark]
                    
                    x_min, x_max = int(min(x_coords)), int(max(x_coords))
                    y_min, y_max = int(min(y_coords)), int(max(y_coords))
                    
                    # Key landmarks for phone-in-hand detection
                    # Thumb tip, index tip, middle tip, ring tip, pinky tip
                    thumb_tip = (int(hand_landmarks.landmark[4].x * w), int(hand_landmarks.landmark[4].y * h))
                    index_tip = (int(hand_landmarks.landmark[8].x * w), int(hand_landmarks.landmark[8].y * h))
                    middle_tip = (int(hand_landmarks.landmark[12].x * w), int(hand_landmarks.landmark[12].y * h))
                    
                    self.hand_landmarks.append({
                        'bbox': (x_min, y_min, x_max, y_max),
                        'thumb': thumb_tip,
                        'index': index_tip,
                        'middle': middle_tip,
                        'center': ((x_min + x_max) // 2, (y_min + y_max) // 2),
                        'landmarks': hand_landmarks
                    })
        except Exception as e:
            print(f"Hand detection error: {e}")
            
        return self.hand_landmarks
    
    def is_phone_near_hand(self, phone_bbox: Tuple[int, int, int, int], hand_bbox: Tuple[int, int, int, int]) -> bool:
        """
        Check if phone is near hand (phone-in-hand detection)
        Returns True if phone overlaps with hand or is very close to it
        """
        px1, py1, px2, py2 = phone_bbox
        hx1, hy1, hx2, hy2 = hand_bbox
        
        # Check for overlap
        overlap_x = max(0, min(px2, hx2) - max(px1, hx1))
        overlap_y = max(0, min(py2, hy2) - max(py1, hy1))
        overlap_area = overlap_x * overlap_y
        
        # Phone and hand areas
        phone_area = (px2 - px1) * (py2 - py1)
        hand_area = (hx2 - hx1) * (hy2 - hy1)
        
        # If there's significant overlap, it's phone-in-hand
        if overlap_area > 0.1 * min(phone_area, hand_area):
            return True
        
        # Check proximity
        phone_center = ((px1 + px2) // 2, (py1 + py2) // 2)
        hand_center = ((hx1 + hx2) // 2, (hy1 + hy2) // 2)
        distance = np.sqrt((phone_center[0] - hand_center[0])**2 + (phone_center[1] - hand_center[1])**2)
        
        # Check if phone center is near hand
        max_distance = 80  # pixels
        return distance < max_distance
    
    def detect_phones_near_face(self, frame: np.ndarray, face_bbox: Tuple[int, int, int, int]) -> List[Dict[str, Any]]:
        """
        Detect phones specifically near the face area
        Now includes phone-in-hand detection logic
        """
        if not face_bbox:
            return []
        
        fx1, fy1, fx2, fy2 = face_bbox
        
        # Expand face area for detection
        margin = 150  # Larger margin
        search_x1 = max(0, fx1 - margin)
        search_y1 = max(0, fy1 - margin)
        search_x2 = min(frame.shape[1], fx2 + margin)
        search_y2 = min(frame.shape[0], fy2 + margin)
        
        # Crop frame to face area
        face_region = frame[search_y1:search_y2, search_x1:search_x2]
        
        if face_region.size == 0:
            return []
        
        # Detect phones in face region
        detections = self.detect_phone_objects(face_region)
        
        # Detect hands for phone-in-hand detection (Roboflow approach)
        detected_hands = self.detect_hands(frame)
        
        # Adjust coordinates back to full frame and check for phone-in-hand
        enhanced_detections = []
        for detection in detections:
            x1, y1, x2, y2 = detection['bbox']
            detection['bbox'] = (x1 + search_x1, y1 + search_y1, x2 + search_x1, y2 + search_y1)
            detection['center'] = (detection['center'][0] + search_x1, detection['center'][1] + search_y1)
            
            # Check if phone is near any hand (phone-in-hand detection)
            phone_in_hand = False
            if detected_hands:
                for hand in detected_hands:
                    if self.is_phone_near_hand(detection['bbox'], hand['bbox']):
                        phone_in_hand = True
                        detection['confidence'] = min(1.0, detection['confidence'] * 1.2)  # Boost confidence
                        detection['near_hand'] = True
                        break
            
            enhanced_detections.append(detection)
        
        return enhanced_detections
    
    def draw_detections(self, frame: np.ndarray, detections: List[Dict[str, Any]]) -> np.ndarray:
        """
        Draw phone detection boxes on frame
        Includes phone-in-hand detection visualization
        """
        for detection in detections:
            x1, y1, x2, y2 = detection['bbox']
            confidence = detection['confidence']
            is_in_hand = detection.get('near_hand', False)
            
            # Use different color if phone is in hand
            color = (0, 255, 255) if is_in_hand else (0, 255, 0)  # Cyan if in hand, green otherwise
            
            # Draw bounding box
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            
            # Draw label with phone-in-hand status
            if is_in_hand:
                label = f"iPhone in Hand: {confidence:.2f}"
            else:
                label = f"iPhone: {confidence:.2f}"
            cv2.putText(frame, label, (x1, y1 - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        
        return frame
