"""
Simulated AI Helper for Testing
==============================

This simulates the AI helper behavior for testing without requiring
a full VLM installation. It will randomly detect "phone usage" 
to demonstrate the popup functionality.
"""

import cv2
import numpy as np
import time
import random
from typing import Dict, Any, Tuple, Optional, List

class SimulatedAIHelper:
    """
    Simulated AI Helper that randomly detects phone usage
    for testing the popup functionality
    """
    
    def __init__(self, detection_probability: float = 0.3):
        """
        Initialize simulated AI helper
        
        Args:
            detection_probability: Probability of detecting phone (0.0-1.0)
        """
        self.detection_probability = detection_probability
        self.last_inference_time = 0
        self.throttle_seconds = 1.0
        
        print("Simulated AI Helper initialized (for testing)")
    
    def check_phone_with_vlm(self, 
                           frame: np.ndarray,
                           face_bbox: Optional[Tuple[int, int, int, int]] = None,
                           hand_bboxes: list = None,
                           phone_bboxes: list = None,
                           phone_confidence: float = 0.0) -> Dict[str, Any]:
        """
        Simulate AI phone detection
        
        Args:
            frame: Input frame
            face_bbox: Face bounding box
            hand_bboxes: List of hand bounding boxes
            phone_bboxes: List of phone bounding boxes
            phone_confidence: Current phone detection confidence
            
        Returns:
            Dict with simulated AI results
        """
        result = {
            "ai_detected_phone": False,
            "ai_confidence": 0.0,
            "ai_triggered": False,
            "ai_reason": "not_triggered"
        }
        
        # Check if we should run inference (same logic as real AI helper)
        if phone_confidence < 0.3 or phone_confidence > 0.6:
            result["ai_reason"] = f"confidence_out_of_range_{phone_confidence:.2f}"
            return result
        
        # Check throttling
        current_time = time.time()
        if current_time - self.last_inference_time < self.throttle_seconds:
            result["ai_reason"] = "throttled"
            return result
        
        # Simulate AI inference
        try:
            # Randomly decide if AI detects phone usage
            if random.random() < self.detection_probability:
                result["ai_detected_phone"] = True
                result["ai_confidence"] = random.uniform(0.7, 0.95)
                result["ai_triggered"] = True
                result["ai_reason"] = "simulated_detection"
            else:
                result["ai_detected_phone"] = False
                result["ai_confidence"] = random.uniform(0.1, 0.4)
                result["ai_triggered"] = True
                result["ai_reason"] = "simulated_no_detection"
            
            # Update timing
            self.last_inference_time = current_time
            
        except Exception as e:
            result["ai_reason"] = f"simulation_error_{str(e)}"
        
        return result

# Test the simulated AI helper
if __name__ == "__main__":
    print("Testing Simulated AI Helper...")
    
    helper = SimulatedAIHelper(detection_probability=0.5)
    
    # Test multiple scenarios
    for i in range(5):
        result = helper.check_phone_with_vlm(
            frame=np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8),
            face_bbox=(100, 100, 200, 200),
            hand_bboxes=[(150, 150, 250, 250)],
            phone_bboxes=[],
            phone_confidence=0.4  # Should trigger AI
        )
        
        print(f"Test {i+1}: {result}")
        
        if result['ai_detected_phone'] and result['ai_triggered']:
            print("  -> Would show popup: 'You're on your phone'")
        else:
            print("  -> No popup")
        
        time.sleep(0.1)  # Small delay between tests
