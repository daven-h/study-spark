"""
Simple Enhanced Attention Tracker
Uses rectangle detection without YOLOv8 dependency issues
"""

import cv2
import numpy as np
import time
import json
from typing import Dict, Any
from tracker import FocusTracker
from focus_logic import FocusEvaluator
from visualizer import FocusVisualizer
# FPSCounter will be defined inline

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


class SimpleEnhancedAttentionTracker:
    """
    Simple enhanced attention tracker with rectangle detection
    """
    
    def __init__(self):
        """Initialize the simple enhanced tracker"""
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
    
    def detect_rectangles(self, frame: np.ndarray, face_bbox: tuple = None) -> Dict[str, Any]:
        """
        Simple rectangle detection for phone-like objects
        
        Args:
            frame: Input frame
            face_bbox: Face bounding box (x1, y1, x2, y2)
            
        Returns:
            Rectangle detection results
        """
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Edge detection
        edges = cv2.Canny(blurred, 50, 150)
        
        # Find contours
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        rectangles = []
        phone_near_face = False
        max_confidence = 0.0
        
        for contour in contours:
            # Calculate area
            area = cv2.contourArea(contour)
            
            # Filter by area (phone-like size)
            if 2000 < area < 50000:
                # Approximate contour
                epsilon = 0.02 * cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, epsilon, True)
                
                # Check if roughly rectangular
                if len(approx) == 4:
                    # Get bounding rectangle
                    x, y, w, h = cv2.boundingRect(contour)
                    aspect_ratio = w / h if h > 0 else 0
                    
                    # Check if aspect ratio is phone-like
                    if 0.4 < aspect_ratio < 2.5:
                        # Calculate confidence
                        confidence = min(area / 20000, 1.0)
                        
                        rect_info = {
                            'bbox': (x, y, x + w, y + h),
                            'area': area,
                            'aspect_ratio': aspect_ratio,
                            'center': (x + w // 2, y + h // 2),
                            'confidence': confidence,
                            'near_face': False
                        }
                        
                        # Check if near face
                        if face_bbox:
                            fx1, fy1, fx2, fy2 = face_bbox
                            margin = 100
                            if (x + w > fx1 - margin and x < fx2 + margin and 
                                y + h > fy1 - margin and y < fy2 + margin):
                                rect_info['near_face'] = True
                                phone_near_face = True
                                max_confidence = max(max_confidence, confidence)
                        
                        rectangles.append(rect_info)
        
        return {
            'phone_objects': rectangles,
            'phone_near_face': phone_near_face,
            'max_confidence': max_confidence,
            'total_detections': len(rectangles)
        }
    
    def process_frame(self, frame: np.ndarray) -> Dict[str, Any]:
        """
        Process a single frame with enhanced detection
        
        Args:
            frame: Input frame
            
        Returns:
            Enhanced focus metrics
        """
        # Get MediaPipe detection results
        results = self.tracker.process_frame(frame)
        
        # Get face bounding box for rectangle detection
        face_bbox = results["face"].get("face_bbox")
        
        # Detect rectangles
        rectangle_detections = self.detect_rectangles(frame, face_bbox)
        
        # Add rectangle data to results
        results["rectangles"] = rectangle_detections
        
        # Evaluate focus with enhanced logic
        focus_metrics = self.evaluator.evaluate_focus(
            results["face"], results["hands"], results["pose"],
            self.frame_width, self.frame_height, results["objects"], results
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
        Draw enhanced overlay on frame
        
        Args:
            frame: Input frame
            focus_metrics: Focus evaluation results
            detection_results: Detection results
            
        Returns:
            Frame with enhanced overlay
        """
        # Draw attention ring
        if self.show_attention_ring:
            frame = self.visualizer.draw_focus_ring(
                frame, focus_metrics.get("focused", False), 
                focus_metrics.get("focus_score", 0.0), 
                self.frame_width, self.frame_height
            )
        
        # Draw detection overlays
        if self.show_detections:
            frame = self.draw_rectangle_overlays(frame, detection_results)
        
        # Draw landmarks if enabled
        if self.show_landmarks:
            frame = self.visualizer.draw_landmarks_overlay(frame, detection_results)
        
        # Draw enhanced status overlay
        frame = self.visualizer.draw_status_text(
            frame, focus_metrics, focus_metrics["fps"], 
            self.frame_width, self.frame_height
        )
        
        return frame
    
    def draw_rectangle_overlays(self, frame: np.ndarray, results: Dict[str, Any]) -> np.ndarray:
        """
        Draw rectangle detection overlays
        
        Args:
            frame: Input frame
            results: Detection results
            
        Returns:
            Frame with rectangle overlays
        """
        rectangles = results.get("rectangles", {}).get("phone_objects", [])
        
        for rect in rectangles:
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
    
    def print_focus_metrics(self, focus_metrics: Dict[str, Any]):
        """Print focus metrics as JSON"""
        # Create JSON output
        output = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "focused": focus_metrics["focused"],
            "focus_score": round(focus_metrics["focus_score"], 2),
            "face_visible": focus_metrics["face_visible"],
            "yaw": round(focus_metrics.get("yaw", 0), 3),
            "pitch": round(focus_metrics.get("pitch", 0), 3),
            "hand_near_face": focus_metrics["hand_near_face"],
            "rectangle_phone_detected": focus_metrics.get("rectangle_phone_detected", False),
            "rectangle_confidence": round(focus_metrics.get("rectangle_confidence", 0), 2),
            "posture_stable": focus_metrics["posture_stable"],
            "fps": round(focus_metrics["fps"], 1)
        }
        
        print(json.dumps(output))
    
    def run(self):
        """Run the simple enhanced attention tracker"""
        print("🚀 Starting Simple Enhanced Attention Tracker...")
        print("📱 Rectangle Detection (No YOLOv8)")
        print("🎯 Phone vs Hand Detection")
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
                cv2.imshow("Simple Enhanced Attention Tracker", frame)
                
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
                    filename = f"enhanced_screenshot_{int(time.time())}.jpg"
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
        print("✅ Simple Enhanced Attention Tracker stopped")


def main():
    """Main function"""
    tracker = SimpleEnhancedAttentionTracker()
    tracker.run()


if __name__ == "__main__":
    main()
