"""
Test script for Enhanced Attention Tracker
Tests YOLOv8 + MediaPipe integration
"""

import cv2
import numpy as np
from enhanced_tracker import EnhancedFocusTracker
from enhanced_focus_logic import EnhancedFocusEvaluator
from enhanced_visualizer import EnhancedVisualizer


def test_enhanced_tracker():
    """Test the enhanced tracker components"""
    print("🧪 Testing Enhanced Attention Tracker...")
    
    # Initialize components
    tracker = EnhancedFocusTracker()
    evaluator = EnhancedFocusEvaluator()
    visualizer = EnhancedVisualizer()
    
    print("✅ Components initialized")
    
    # Test with camera
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Could not open camera")
        return
    
    print("📹 Camera opened, testing detection...")
    print("Press 'q' to quit test")
    
    frame_count = 0
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame_count += 1
            
            # Process frame
            detection_results = tracker.process_frame(frame)
            focus_metrics = evaluator.evaluate_focus(detection_results)
            
            # Draw overlays
            frame = visualizer.draw_detection_overlays(frame, detection_results)
            frame = visualizer.draw_enhanced_status_overlay(frame, focus_metrics, 30.0)
            
            # Display
            cv2.imshow("Enhanced Tracker Test", frame)
            
            # Print status every 30 frames
            if frame_count % 30 == 0:
                print(f"Frame {frame_count}: {focus_metrics['interaction_state']} "
                      f"(Score: {focus_metrics['focus_score']:.2f})")
            
            # Handle input
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
    
    except KeyboardInterrupt:
        print("\n⏹️ Test interrupted")
    
    finally:
        cap.release()
        cv2.destroyAllWindows()
        print("✅ Test completed")


if __name__ == "__main__":
    test_enhanced_tracker()
