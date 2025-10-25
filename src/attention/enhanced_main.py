"""
Enhanced Attention Tracker Main Application
Integrates YOLOv8 + MediaPipe for phone vs hand detection
"""

import cv2
import numpy as np
import time
import json
from typing import Dict, Any
from enhanced_tracker import EnhancedFocusTracker
from enhanced_focus_logic import EnhancedFocusEvaluator
from enhanced_visualizer import EnhancedVisualizer
from utils import FPSCounter


class EnhancedAttentionTracker:
    """
    Enhanced attention tracker with phone vs hand detection
    """
    
    def __init__(self):
        """Initialize the enhanced attention tracker"""
        # Initialize components
        self.tracker = EnhancedFocusTracker()
        self.evaluator = EnhancedFocusEvaluator()
        self.visualizer = EnhancedVisualizer()
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
    
    def process_frame(self, frame: np.ndarray) -> Dict[str, Any]:
        """
        Process a single frame with enhanced detection
        
        Args:
            frame: Input frame
            
        Returns:
            Enhanced focus metrics
        """
        # Get detection results
        detection_results = self.tracker.process_frame(frame)
        
        # Evaluate focus with enhanced logic
        focus_metrics = self.evaluator.evaluate_focus(detection_results)
        
        # Add FPS
        fps = self.fps_counter.get_fps()
        focus_metrics["fps"] = fps
        
        # Update focus history
        self.focus_history.append(focus_metrics["focus_score"])
        if len(self.focus_history) > self.max_history:
            self.focus_history.pop(0)
        
        return focus_metrics, detection_results
    
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
            frame = self.visualizer.draw_attention_ring(frame, focus_metrics["focus_score"])
        
        # Draw detection overlays
        if self.show_detections:
            frame = self.visualizer.draw_detection_overlays(frame, detection_results)
        
        # Draw enhanced status overlay
        frame = self.visualizer.draw_enhanced_status_overlay(
            frame, focus_metrics, focus_metrics["fps"]
        )
        
        return frame
    
    def print_focus_metrics(self, focus_metrics: Dict[str, Any]):
        """Print focus metrics as JSON"""
        # Create JSON output
        output = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "focused": focus_metrics["focused"],
            "focus_score": round(focus_metrics["focus_score"], 2),
            "face_visible": focus_metrics["face_visible"],
            "orientation_good": focus_metrics["orientation_good"],
            "yaw": round(focus_metrics.get("yaw", 0), 3),
            "pitch": round(focus_metrics.get("pitch", 0), 3),
            "phone_near_face": focus_metrics["phone_near_face"],
            "hand_near_face": focus_metrics["hand_near_face"],
            "interaction_state": focus_metrics["interaction_state"],
            "phone_confidence": round(focus_metrics.get("phone_confidence", 0), 2),
            "posture_stable": focus_metrics["posture_stable"],
            "fps": round(focus_metrics["fps"], 1)
        }
        
        print(json.dumps(output))
    
    def run(self):
        """Run the enhanced attention tracker"""
        print("🚀 Starting Enhanced Attention Tracker...")
        print("📱 YOLOv8 + MediaPipe Integration")
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
                cv2.imshow("Enhanced Attention Tracker", frame)
                
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
        print("✅ Enhanced Attention Tracker stopped")


def main():
    """Main function"""
    tracker = EnhancedAttentionTracker()
    tracker.run()


if __name__ == "__main__":
    main()
