"""
YOLO Object Detection using OpenCV DNN
Alternative to PyTorch-based YOLO for Windows compatibility
"""

import cv2
import numpy as np
from typing import List, Dict, Any, Tuple
import os
import urllib.request

class YOLOOpenCVDetector:
    """
    YOLO object detector using OpenCV DNN module
    Detects phones and other objects without PyTorch dependency
    """
    
    def __init__(self, confidence_threshold: float = 0.5, nms_threshold: float = 0.4):
        self.confidence_threshold = confidence_threshold
        self.nms_threshold = nms_threshold
        self.net = None
        self.class_names = []
        self.output_layers = []
        
        # COCO class names (80 classes)
        self.class_names = [
            'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat',
            'traffic light', 'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat',
            'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'backpack',
            'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
            'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket',
            'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
            'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake',
            'chair', 'couch', 'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop',
            'mouse', 'remote', 'keyboard', 'cell phone', 'microwave', 'oven', 'toaster', 'sink',
            'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush'
        ]
        
        # Phone class index in COCO dataset
        self.phone_class_id = 67  # 'cell phone'
        
    def load_model(self, model_path: str = None):
        """
        Load YOLO model from file or download if not available
        
        Args:
            model_path: Path to YOLO model file (.weights, .cfg, .names)
        """
        try:
            if model_path and os.path.exists(model_path):
                # Load custom model
                self.net = cv2.dnn.readNet(model_path)
            else:
                # Use a lightweight pre-trained model or create a simple detector
                self._create_simple_detector()
                
            # Set backend and target
            self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
            self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
            
            # Get output layer names
            layer_names = self.net.getLayerNames()
            self.output_layers = [layer_names[i - 1] for i in self.net.getUnconnectedOutLayers()]
            
            print("✅ YOLO OpenCV detector loaded successfully")
            return True
            
        except Exception as e:
            print(f"❌ Failed to load YOLO model: {e}")
            self._create_simple_detector()
            return False
    
    def _create_simple_detector(self):
        """Create a simple phone detector using OpenCV"""
        print("📱 Using simple phone detector (OpenCV-based)")
        # This is a fallback - we'll use MediaPipe for phone detection instead
        self.net = None
    
    def detect_objects(self, frame: np.ndarray) -> List[Dict[str, Any]]:
        """
        Detect objects in frame
        
        Args:
            frame: Input frame (BGR format)
            
        Returns:
            List of detected objects with bounding boxes and confidence
        """
        if self.net is None:
            # Fallback to simple detection
            return self._simple_phone_detection(frame)
        
        try:
            height, width, channels = frame.shape
            
            # Prepare input blob
            blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
            self.net.setInput(blob)
            
            # Run inference
            outputs = self.net.forward(self.output_layers)
            
            # Process detections
            detections = []
            for output in outputs:
                for detection in output:
                    scores = detection[5:]
                    class_id = np.argmax(scores)
                    confidence = scores[class_id]
                    
                    if confidence > self.confidence_threshold:
                        # Get bounding box coordinates
                        center_x = int(detection[0] * width)
                        center_y = int(detection[1] * height)
                        w = int(detection[2] * width)
                        h = int(detection[3] * height)
                        
                        # Calculate top-left corner
                        x = int(center_x - w / 2)
                        y = int(center_y - h / 2)
                        
                        detections.append({
                            'class_id': int(class_id),
                            'class_name': self.class_names[class_id] if class_id < len(self.class_names) else 'unknown',
                            'confidence': float(confidence),
                            'bbox': (x, y, x + w, y + h),
                            'center': (center_x, center_y)
                        })
            
            # Apply Non-Maximum Suppression
            detections = self._apply_nms(detections)
            
            return detections
            
        except Exception as e:
            print(f"Detection error: {e}")
            return self._simple_phone_detection(frame)
    
    def _simple_phone_detection(self, frame: np.ndarray) -> List[Dict[str, Any]]:
        """
        Simple phone detection using OpenCV contour detection
        This is a fallback when YOLO model is not available
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
                # Approximate contour
                perimeter = cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
                
                # Check if it's rectangular (phone-like)
                if len(approx) == 4:
                    x, y, w, h = cv2.boundingRect(approx)
                    area = cv2.contourArea(contour)
                    aspect_ratio = float(w) / h
                    
                    # Filter for phone-like objects
                    if (0.3 < aspect_ratio < 3.0 and 
                        area > 1000 and 
                        w > 50 and h > 50):
                        
                        # Calculate confidence based on shape properties
                        confidence = min(0.8, area / (frame.shape[0] * frame.shape[1] * 0.01))
                        
                        detections.append({
                            'class_id': 67,  # Cell phone class
                            'class_name': 'cell phone',
                            'confidence': confidence,
                            'bbox': (x, y, x + w, y + h),
                            'center': (x + w // 2, y + h // 2)
                        })
            
            return detections
            
        except Exception as e:
            print(f"Simple detection error: {e}")
            return []
    
    def _apply_nms(self, detections: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Apply Non-Maximum Suppression to remove overlapping detections"""
        if not detections:
            return []
        
        # Extract bounding boxes and confidence scores
        boxes = []
        confidences = []
        indices_to_keep = []
        
        for i, detection in enumerate(detections):
            x1, y1, x2, y2 = detection['bbox']
            boxes.append([x1, y1, x2 - x1, y2 - y1])  # Convert to (x, y, w, h) format
            confidences.append(detection['confidence'])
        
        # Apply NMS
        indices = cv2.dnn.NMSBoxes(boxes, confidences, self.confidence_threshold, self.nms_threshold)
        
        if len(indices) > 0:
            indices_to_keep = indices.flatten()
        
        # Return filtered detections
        return [detections[i] for i in indices_to_keep]
    
    def detect_phones(self, frame: np.ndarray) -> List[Dict[str, Any]]:
        """
        Detect phones specifically - Enhanced version
        
        Args:
            frame: Input frame (BGR format)
            
        Returns:
            List of detected phones with bounding boxes
        """
        detections = self.detect_objects(frame)
        
        # Filter for phones only
        phones = []
        for detection in detections:
            # Check for phone class or phone-related keywords
            if (detection['class_id'] == self.phone_class_id or 
                'phone' in detection['class_name'].lower() or
                'cell' in detection['class_name'].lower() or
                'mobile' in detection['class_name'].lower()):
                phones.append(detection)
        
        # If no phones detected via YOLO, try simple detection
        if not phones:
            phones = self._simple_phone_detection(frame)
        
        return phones
    
    def draw_detections(self, frame: np.ndarray, detections: List[Dict[str, Any]]) -> np.ndarray:
        """
        Draw detection boxes on frame
        
        Args:
            frame: Input frame
            detections: List of detections
            
        Returns:
            Frame with drawn detections
        """
        for detection in detections:
            x1, y1, x2, y2 = detection['bbox']
            confidence = detection['confidence']
            class_name = detection['class_name']
            
            # Draw bounding box
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
            
            # Draw label
            label = f"{class_name}: {confidence:.2f}"
            cv2.putText(frame, label, (x1, y1 - 10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        
        return frame
