#!/usr/bin/env python3
"""
Test script for AI Helper VLM
Tests the AI helper without running the full tracker
"""

import cv2
import numpy as np
from ai_helper_vlm import AIHelperVLM

def test_ai_helper():
    """Test the AI helper with a dummy frame"""
    print("Testing AI Helper VLM...")
    
    # Initialize AI helper
    try:
        helper = AIHelperVLM(
            model_name="llava:7b",
            backend="ollama",
            throttle_seconds=0.5  # Faster for testing
        )
        print("AI Helper initialized successfully")
    except Exception as e:
        print(f"AI Helper initialization failed: {e}")
        return False
    
    # Create dummy frame
    dummy_frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
    
    # Test with different scenarios
    test_cases = [
        {
            "name": "Ambiguous phone confidence",
            "face_bbox": (100, 100, 200, 200),
            "hand_bboxes": [(150, 150, 250, 250)],
            "phone_bboxes": [],
            "phone_confidence": 0.4
        },
        {
            "name": "High phone confidence (should skip)",
            "face_bbox": (100, 100, 200, 200),
            "hand_bboxes": [(150, 150, 250, 250)],
            "phone_bboxes": [(120, 120, 180, 180)],
            "phone_confidence": 0.8
        },
        {
            "name": "Low phone confidence (should skip)",
            "face_bbox": (100, 100, 200, 200),
            "hand_bboxes": [(150, 150, 250, 250)],
            "phone_bboxes": [],
            "phone_confidence": 0.1
        }
    ]
    
    for i, test_case in enumerate(test_cases):
        print(f"\nTest Case {i+1}: {test_case['name']}")
        
        result = helper.check_phone_with_vlm(
            frame=dummy_frame,
            face_bbox=test_case["face_bbox"],
            hand_bboxes=test_case["hand_bboxes"],
            phone_bboxes=test_case["phone_bboxes"],
            phone_confidence=test_case["phone_confidence"]
        )
        
        print(f"   Result: {result}")
        
        # Check if result is valid
        required_keys = ["ai_detected_phone", "ai_confidence", "ai_triggered", "ai_reason"]
        for key in required_keys:
            if key not in result:
                print(f"   Missing key: {key}")
                return False
        
        print(f"   All required keys present")
    
    # Test stats
    stats = helper.get_stats()
    print(f"\nAI Helper Stats: {stats}")
    
    print("\nAI Helper test completed successfully!")
    return True

if __name__ == "__main__":
    success = test_ai_helper()
    if success:
        print("\nAll tests passed!")
    else:
        print("\nSome tests failed!")
