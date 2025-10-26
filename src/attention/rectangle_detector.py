"""
Rectangle Detector for Phone-like Objects
Detects rectangular shapes that could be phones near the face
"""

import cv2
import numpy as np
from typing import List, Tuple, Optional, Dict, Any


class RectangleDetector:
    """
    Detects rectangular objects (like phones) in the frame
    """
    
    def __init__(self):
        """Initialize the rectangle detector"""
        # Detection parameters
        self.min_area = 2000  # Minimum area for phone detection
        self.max_area = 50000  # Maximum area for phone detection
        self.aspect_ratio_range = (0.4, 2.5)  # Phone aspect ratio range
        self.contour_approximation = cv2.CHAIN_APPROX_SIMPLE
        
    def detect_rectangles(self, frame: np.ndarray, face_bbox: Optional[Tuple[int, int, int, int]] = None) -> List[Dict[str, Any]]:
        """
        Detect rectangular objects in the frame
        
        Args:
            frame: Input frame
            face_bbox: Face bounding box (x1, y1, x2, y2) for proximity check
            
        Returns:
            List of detected rectangles with properties
        """
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Apply edge detection
        edges = cv2.Canny(blurred, 50, 150)
        
        # Find contours
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, self.contour_approximation)
        
        rectangles = []
        
        for contour in contours:
            # Calculate contour area
            area = cv2.contourArea(contour)
            
            # Filter by area
            if self.min_area < area < self.max_area:
                # Approximate contour to polygon
                epsilon = 0.02 * cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, epsilon, True)
                
                # Check if it's roughly rectangular (4 corners)
                if len(approx) == 4:
                    # Get bounding rectangle
                    x, y, w, h = cv2.boundingRect(contour)
                    
                    # Calculate aspect ratio
                    aspect_ratio = w / h if h > 0 else 0
                    
                    # Check if aspect ratio is phone-like
                    if self.aspect_ratio_range[0] < aspect_ratio < self.aspect_ratio_range[1]:
                        # Calculate rectangle properties
                        rect_info = {
                            'bbox': (x, y, x + w, y + h),
                            'area': area,
                            'aspect_ratio': aspect_ratio,
                            'center': (x + w // 2, y + h // 2),
                            'confidence': self._calculate_confidence(contour, area, aspect_ratio),
                            'near_face': False
                        }
                        
                        # Check if rectangle is near face
                        if face_bbox:
                            rect_info['near_face'] = self._is_near_face(rect_info['bbox'], face_bbox)
                        
                        rectangles.append(rect_info)
        
        # Sort by confidence
        rectangles.sort(key=lambda x: x['confidence'], reverse=True)
        
        return rectangles
    
    def _calculate_confidence(self, contour: np.ndarray, area: float, aspect_ratio: float) -> float:
        """
        Calculate confidence score for rectangle detection
        
        Args:
            contour: Contour points
            area: Contour area
            aspect_ratio: Width/height ratio
            
        Returns:
            Confidence score (0-1)
        """
        # Base confidence from area (normalized)
        area_score = min(area / 20000, 1.0)
        
        # Aspect ratio score (prefer phone-like ratios)
        ideal_ratio = 0.6  # Typical phone ratio
        ratio_score = 1.0 - abs(aspect_ratio - ideal_ratio) / ideal_ratio
        ratio_score = max(0, min(1, ratio_score))
        
        # Contour regularity score
        perimeter = cv2.arcLength(contour, True)
        regularity_score = 1.0 - abs(4 * np.pi * area - perimeter * perimeter) / (perimeter * perimeter)
        regularity_score = max(0, min(1, regularity_score))
        
        # Combined confidence
        confidence = (area_score * 0.4 + ratio_score * 0.3 + regularity_score * 0.3)
        
        return min(1.0, max(0.0, confidence))
    
    def _is_near_face(self, rect_bbox: Tuple[int, int, int, int], 
                     face_bbox: Tuple[int, int, int, int], 
                     margin: int = 100) -> bool:
        """
        Check if rectangle is near the face
        
        Args:
            rect_bbox: Rectangle bounding box (x1, y1, x2, y2)
            face_bbox: Face bounding box (x1, y1, x2, y2)
            margin: Proximity margin in pixels
            
        Returns:
            True if rectangle is near face
        """
        rx1, ry1, rx2, ry2 = rect_bbox
        fx1, fy1, fx2, fy2 = face_bbox
        
        # Check if rectangles overlap or are close
        return (rx2 > fx1 - margin and rx1 < fx2 + margin and 
                ry2 > fy1 - margin and ry1 < fy2 + margin)
    
    def detect_phone_objects(self, frame: np.ndarray, face_bbox: Optional[Tuple[int, int, int, int]] = None) -> Dict[str, Any]:
        """
        Detect phone-like rectangular objects
        
        Args:
            frame: Input frame
            face_bbox: Face bounding box for proximity check
            
        Returns:
            Detection results
        """
        rectangles = self.detect_rectangles(frame, face_bbox)
        
        # Filter for phone-like objects
        phone_objects = []
        phone_near_face = False
        max_confidence = 0.0
        
        for rect in rectangles:
            if rect['confidence'] > 0.3:  # Minimum confidence threshold
                phone_objects.append(rect)
                max_confidence = max(max_confidence, rect['confidence'])
                
                if rect['near_face']:
                    phone_near_face = True
        
        return {
            'phone_objects': phone_objects,
            'phone_near_face': phone_near_face,
            'max_confidence': max_confidence,
            'total_detections': len(phone_objects)
        }
    
    def draw_detections(self, frame: np.ndarray, detections: Dict[str, Any]) -> np.ndarray:
        """
        Draw rectangle detections on frame
        
        Args:
            frame: Input frame
            detections: Detection results
            
        Returns:
            Frame with detections drawn
        """
        phone_objects = detections.get('phone_objects', [])
        phone_near_face = detections.get('phone_near_face', False)
        
        for i, rect in enumerate(phone_objects):
            x1, y1, x2, y2 = rect['bbox']
            confidence = rect['confidence']
            near_face = rect['near_face']
            
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
            center_x, center_y = rect['center']
            cv2.circle(frame, (center_x, center_y), 5, color, -1)
        
        return frame
