#!/usr/bin/env python3
"""
Main script for the Python Attention Tracking Engine.
Captures video from webcam, processes frames with MediaPipe,
and displays real-time focus tracking with attention ring overlay.
"""

import cv2
import json
import time
import argparse
import sys
import numpy as np
from typing import Dict, Any, Optional

from tracker import FocusTracker
from focus_logic import FocusEvaluator
from visualizer import FocusVisualizer

class AttentionTracker:
    """
    Main attention tracking application.
    Orchestrates webcam capture, processing, and visualization.
    """
    
    def __init__(self, camera_index: int = 0, show_landmarks: bool = False, 
                 show_grid: bool = True, output_json: bool = True):
        """
        Initialize the attention tracker.
        
        Args:
            camera_index: Camera device index
            show_landmarks: Whether to show MediaPipe landmarks
            show_grid: Whether to show focus grid
            output_json: Whether to output JSON data to console
        """
        self.camera_index = camera_index
        self.show_landmarks = show_landmarks
        self.show_grid = show_grid
        self.output_json = output_json
        
        # Initialize components
        self.tracker = FocusTracker()
        self.evaluator = FocusEvaluator()
        self.visualizer = FocusVisualizer()
        
        # FPS tracking
        self.fps_counter = FPSCounter()
        
        # Video capture
        self.cap = None
        self.frame_width = 640
        self.frame_height = 480
        
        # Running state
        self.running = False
    
    def initialize_camera(self) -> bool:
        """
        Initialize camera capture.
        
        Returns:
            True if camera initialized successfully
        """
        try:
            self.cap = cv2.VideoCapture(self.camera_index)
            if not self.cap.isOpened():
                print(f"Error: Could not open camera {self.camera_index}")
                return False
            
            # Set camera properties
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.frame_width)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.frame_height)
            self.cap.set(cv2.CAP_PROP_FPS, 30)
            
            # Get actual frame dimensions
            self.frame_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            self.frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            
            print(f"Camera initialized: {self.frame_width}x{self.frame_height}")
            return True
            
        except Exception as e:
            print(f"Error initializing camera: {e}")
            return False
    
    def process_frame(self, frame: np.ndarray) -> Dict[str, Any]:
        """
        Process a single frame and return focus metrics.
        
        Args:
            frame: Input frame from camera
            
        Returns:
            Focus evaluation results
        """
        # Get MediaPipe detection results
        results = self.tracker.process_frame(frame)
        
        # Evaluate focus with object detection data
        focus_metrics = self.evaluator.evaluate_focus(
            results["face"], results["hands"], results["pose"],
            self.frame_width, self.frame_height, results["objects"], results
        )
        
        # Add FPS to metrics
        fps = self.fps_counter.get_fps()
        focus_metrics["fps"] = fps
        
        return focus_metrics, results
    
    def run(self):
        """Run the main attention tracking loop."""
        if not self.initialize_camera():
            return
        
        print("Starting attention tracker...")
        print("Press 'q' to quit, 'r' to reset focus history, 's' to save screenshot")
        
        self.running = True
        
        try:
            while self.running:
                # Capture frame
                ret, frame = self.cap.read()
                if not ret:
                    print("Error: Could not read frame from camera")
                    break
                
                # Process frame
                focus_metrics, detection_results = self.process_frame(frame)
                
                # Draw overlay with landmarks
                frame = self.visualizer.draw_complete_overlay(
                    frame, focus_metrics, focus_metrics["fps"],
                    self.frame_width, self.frame_height,
                    show_grid=self.show_grid, show_landmarks=True,  # Always show landmarks
                    results=detection_results
                )
                
                # Display frame
                cv2.imshow("Attention Tracker", frame)
                
                # Output JSON data
                if self.output_json:
                    self._output_json(focus_metrics)
                
                # Handle keyboard input
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
                elif key == ord('r'):
                    self.evaluator.reset_history()
                    print("Focus history reset")
                elif key == ord('s'):
                    self._save_screenshot(frame)
                elif key == ord('l'):
                    self.show_landmarks = not self.show_landmarks
                    print(f"Landmarks display: {'ON' if self.show_landmarks else 'OFF'}")
                elif key == ord('g'):
                    self.show_grid = not self.show_grid
                    print(f"Focus grid: {'ON' if self.show_grid else 'OFF'}")
        
        except KeyboardInterrupt:
            print("\nInterrupted by user")
        
        finally:
            self.cleanup()
    
    def _output_json(self, focus_metrics: Dict[str, Any]):
        """Output focus metrics as JSON."""
        # Create clean JSON output
        json_output = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "focused": focus_metrics.get("focused", False),
            "focus_score": round(focus_metrics.get("focus_score", 0.0), 2),
            "yaw": round(focus_metrics.get("yaw", 0.0), 3),
            "pitch": round(focus_metrics.get("pitch", 0.0), 3),
            "hand_near_face": focus_metrics.get("hand_near_face", False),
            "posture_stable": focus_metrics.get("posture_stable", True),
            "fps": round(focus_metrics.get("fps", 0.0), 1)
        }
        
        print(json.dumps(json_output))
    
    def _save_screenshot(self, frame: np.ndarray):
        """Save current frame as screenshot."""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"attention_screenshot_{timestamp}.jpg"
        cv2.imwrite(filename, frame)
        print(f"Screenshot saved: {filename}")
    
    def cleanup(self):
        """Clean up resources."""
        self.running = False
        
        if self.cap:
            self.cap.release()
        
        cv2.destroyAllWindows()
        
        if self.tracker:
            self.tracker.release()
        
        print("Attention tracker stopped")

class FPSCounter:
    """Simple FPS counter for performance monitoring."""
    
    def __init__(self, window_size: int = 30):
        self.window_size = window_size
        self.frame_times = []
        self.last_time = time.time()
    
    def get_fps(self) -> float:
        """Get current FPS."""
        current_time = time.time()
        frame_time = current_time - self.last_time
        self.last_time = current_time
        
        self.frame_times.append(frame_time)
        if len(self.frame_times) > self.window_size:
            self.frame_times.pop(0)
        
        if self.frame_times:
            avg_frame_time = sum(self.frame_times) / len(self.frame_times)
            return 1.0 / avg_frame_time if avg_frame_time > 0 else 0.0
        
        return 0.0

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Python Attention Tracking Engine")
    parser.add_argument("--camera", type=int, default=0, help="Camera index (default: 0)")
    parser.add_argument("--no-landmarks", action="store_true", help="Hide MediaPipe landmarks")
    parser.add_argument("--no-grid", action="store_true", help="Hide focus grid")
    parser.add_argument("--no-json", action="store_true", help="Disable JSON output")
    parser.add_argument("--width", type=int, default=640, help="Frame width")
    parser.add_argument("--height", type=int, default=480, help="Frame height")
    
    args = parser.parse_args()
    
    # Create and run attention tracker
    tracker = AttentionTracker(
        camera_index=args.camera,
        show_landmarks=not args.no_landmarks,
        show_grid=not args.no_grid,
        output_json=not args.no_json
    )
    
    # Set frame dimensions
    tracker.frame_width = args.width
    tracker.frame_height = args.height
    
    try:
        tracker.run()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
