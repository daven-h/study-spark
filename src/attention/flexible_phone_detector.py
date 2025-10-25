"""
Flexible Phone Detector
More lenient detection for rectangular objects that could be phones
"""

import cv2
import numpy as np
from typing import List, Dict, Any, Tuple

class FlexiblePhoneDetector:
    """
    Flexible phone detector with more lenient criteria
    """
    
    def __init__(self):
        # More flexible phone detection criteria
        self.min_aspect_ratio = 1.3  # Much more lenient
        self.max_aspect_ratio = 3.0  # Allow wider range
        self.min_area = 500  # Smaller minimum area
        self.max_area = 100000  # Larger maximum area
        
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
                    
                    # More flexible phone detection
                    if self._is_phone_like(x, y, w, h, area, aspect_ratio):
                        # Calculate confidence
                        confidence = self._calculate_phone_confidence(w, h, area, aspect_ratio)
                        
                        detections.append({
                            'class_id': 67,  # Cell phone class
                            'class_name': 'Phone',
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
        More flexible phone detection criteria
        """
        # Check aspect ratio (phones are usually taller than wide)
        if not (self.min_aspect_ratio <= aspect_ratio <= self.max_aspect_ratio):
            return False
        
        # Check area
        if not (self.min_area <= area <= self.max_area):
            return False
        
        # Check size (reasonable phone size)
        if w < 20 or h < 30:  # Very small
            return False
        if w > 300 or h > 500:  # Very large
            return False
        
        # Check if it's roughly rectangular
        rect_area = w * h
        if area / rect_area < 0.5:  # More lenient rectangularity
            return False
        
        return True
    
    def _calculate_phone_confidence(self, w: int, h: int, area: float, aspect_ratio: float) -> float:
        """
        Calculate confidence that object is a phone
        """
        confidence = 0.0
        
        # Aspect ratio confidence (prefer taller objects)
        if 1.5 <= aspect_ratio <= 2.5:
            confidence += 0.4
        elif 1.3 <= aspect_ratio <= 3.0:
            confidence += 0.2
        
        # Area confidence (prefer medium-sized objects)
        if 2000 <= area <= 20000:
            confidence += 0.3
        elif 500 <= area <= 50000:
            confidence += 0.1
        
        # Size confidence (prefer reasonable phone sizes)
        if 40 <= w <= 150 and 60 <= h <= 250:
            confidence += 0.3
        elif 20 <= w <= 300 and 30 <= h <= 500:
            confidence += 0.1
        
        return min(1.0, confidence)
    
    def detect_phones_near_face(self, frame: np.ndarray, face_bbox: Tuple[int, int, int, int]) -> List[Dict[str, Any]]:
        """
        Detect phones specifically near the face area
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
        
        # Adjust coordinates back to full frame
        for detection in detections:
            x1, y1, x2, y2 = detection['bbox']
            detection['bbox'] = (x1 + search_x1, y1 + search_y1, x2 + search_x1, y2 + search_y1)
            detection['center'] = (detection['center'][0] + search_x1, detection['center'][1] + search_y1)
        
        return detections
    
    def draw_detections(self, frame: np.ndarray, detections: List[Dict[str, Any]]) -> np.ndarray:
        """
        Draw phone detection boxes on frame
        """
        for detection in detections:
            x1, y1, x2, y2 = detection['bbox']
            confidence = detection['confidence']
            
            # Draw bounding box
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            # Draw label
            label = f"Phone: {confidence:.2f}"
            cv2.putText(frame, label, (x1, y1 - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        return frame
