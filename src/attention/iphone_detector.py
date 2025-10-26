"""
iPhone Dimension Detector
Detects phones by analyzing rectangular objects with iPhone-like proportions
"""

import cv2
import numpy as np
from typing import List, Dict, Any, Tuple

class iPhoneDetector:
    """
    Detects phones by analyzing rectangular objects with iPhone-like dimensions
    """
    
    def __init__(self):
        # iPhone dimensions (approximate ratios)
        self.iphone_ratios = {
            "iPhone 15 Pro": (2.17, 0.46),  # width/height ratio, thickness ratio
            "iPhone 15": (2.17, 0.46),
            "iPhone 14 Pro": (2.17, 0.46),
            "iPhone 14": (2.17, 0.46),
            "iPhone 13 Pro": (2.17, 0.46),
            "iPhone 13": (2.17, 0.46),
            "iPhone 12 Pro": (2.17, 0.46),
            "iPhone 12": (2.17, 0.46),
            "iPhone 11 Pro": (2.17, 0.46),
            "iPhone 11": (2.17, 0.46),
            "iPhone X": (2.17, 0.46),
            "iPhone 8": (2.17, 0.46),
            "iPhone 7": (2.17, 0.46),
            "iPhone 6": (2.17, 0.46),
        }
        
        # Acceptable ratio ranges
        self.min_aspect_ratio = 1.8  # Minimum width/height ratio
        self.max_aspect_ratio = 2.5  # Maximum width/height ratio
        self.min_area = 2000  # Minimum area in pixels
        self.max_area = 50000  # Maximum area in pixels
        
    def detect_iphone_objects(self, frame: np.ndarray) -> List[Dict[str, Any]]:
        """
        Detect iPhone-like objects in frame
        
        Args:
            frame: Input frame (BGR format)
            
        Returns:
            List of detected iPhone objects
        """
        detections = []
        
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Apply Gaussian blur
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            
            # Edge detection
            edges = cv2.Canny(blurred, 50, 150)
            
            # Find contours
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            for contour in contours:
                # Approximate contour to polygon
                perimeter = cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
                
                # Check if it's rectangular (4 corners)
                if len(approx) == 4:
                    # Get bounding rectangle
                    x, y, w, h = cv2.boundingRect(approx)
                    area = cv2.contourArea(contour)
                    aspect_ratio = float(w) / h
                    
                    # Check if it matches iPhone dimensions
                    if self._is_iphone_like(x, y, w, h, area, aspect_ratio):
                        # Calculate confidence based on how close it is to iPhone ratios
                        confidence = self._calculate_iphone_confidence(w, h, area, aspect_ratio)
                        
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
            print(f"iPhone detection error: {e}")
            return []
    
    def _is_iphone_like(self, x: int, y: int, w: int, h: int, area: float, aspect_ratio: float) -> bool:
        """
        Check if object matches iPhone-like characteristics
        
        Args:
            x, y, w, h: Bounding box coordinates
            area: Contour area
            aspect_ratio: Width/height ratio
            
        Returns:
            True if object looks like an iPhone
        """
        # Check aspect ratio (iPhone is tall and narrow)
        if not (self.min_aspect_ratio <= aspect_ratio <= self.max_aspect_ratio):
            return False
        
        # Check area (not too small, not too large)
        if not (self.min_area <= area <= self.max_area):
            return False
        
        # Check size (reasonable phone size)
        if w < 30 or h < 50:  # Too small
            return False
        if w > 200 or h > 400:  # Too large
            return False
        
        # Check if it's roughly rectangular
        rect_area = w * h
        if area / rect_area < 0.7:  # Not rectangular enough
            return False
        
        return True
    
    def _calculate_iphone_confidence(self, w: int, h: int, area: float, aspect_ratio: float) -> float:
        """
        Calculate confidence that object is an iPhone
        
        Args:
            w, h: Width and height
            area: Contour area
            aspect_ratio: Width/height ratio
            
        Returns:
            Confidence score (0.0 to 1.0)
        """
        confidence = 0.0
        
        # Aspect ratio confidence (closer to 2.17 is better)
        ideal_ratio = 2.17
        ratio_diff = abs(aspect_ratio - ideal_ratio)
        ratio_confidence = max(0.0, 1.0 - (ratio_diff / ideal_ratio))
        confidence += ratio_confidence * 0.4
        
        # Area confidence (prefer medium-sized objects)
        ideal_area = 15000  # Ideal area in pixels
        area_diff = abs(area - ideal_area)
        area_confidence = max(0.0, 1.0 - (area_diff / ideal_area))
        confidence += area_confidence * 0.3
        
        # Size confidence (prefer reasonable phone sizes)
        ideal_width = 80
        ideal_height = 150
        width_diff = abs(w - ideal_width)
        height_diff = abs(h - ideal_height)
        size_confidence = max(0.0, 1.0 - ((width_diff / ideal_width) + (height_diff / ideal_height)) / 2)
        confidence += size_confidence * 0.3
        
        return min(1.0, confidence)
    
    def detect_phones_near_face(self, frame: np.ndarray, face_bbox: Tuple[int, int, int, int]) -> List[Dict[str, Any]]:
        """
        Detect phones specifically near the face area
        
        Args:
            frame: Input frame
            face_bbox: Face bounding box (x1, y1, x2, y2)
            
        Returns:
            List of phones near face
        """
        if not face_bbox:
            return []
        
        fx1, fy1, fx2, fy2 = face_bbox
        
        # Expand face area for detection
        margin = 100
        search_x1 = max(0, fx1 - margin)
        search_y1 = max(0, fy1 - margin)
        search_x2 = min(frame.shape[1], fx2 + margin)
        search_y2 = min(frame.shape[0], fy2 + margin)
        
        # Crop frame to face area
        face_region = frame[search_y1:search_y2, search_x1:search_x2]
        
        if face_region.size == 0:
            return []
        
        # Detect phones in face region
        detections = self.detect_iphone_objects(face_region)
        
        # Adjust coordinates back to full frame
        for detection in detections:
            x1, y1, x2, y2 = detection['bbox']
            detection['bbox'] = (x1 + search_x1, y1 + search_y1, x2 + search_x1, y2 + search_y1)
            detection['center'] = (detection['center'][0] + search_x1, detection['center'][1] + search_y1)
        
        return detections
    
    def draw_detections(self, frame: np.ndarray, detections: List[Dict[str, Any]]) -> np.ndarray:
        """
        Draw iPhone detection boxes on frame
        
        Args:
            frame: Input frame
            detections: List of detections
            
        Returns:
            Frame with drawn detections
        """
        for detection in detections:
            x1, y1, x2, y2 = detection['bbox']
            confidence = detection['confidence']
            
            # Draw bounding box
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            # Draw label
            label = f"iPhone: {confidence:.2f}"
            cv2.putText(frame, label, (x1, y1 - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        return frame
