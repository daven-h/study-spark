#!/usr/bin/env python3
"""
Test AI Helper with simulated phone detection
"""

import cv2
import numpy as np
from ai_helper_vlm import AIHelperVLM

def test_ai_helper_with_phone():
    """Test AI helper with a simulated phone scenario"""
    print("Testing AI Helper with phone scenario...")
    
    # Initialize AI helper
    helper = AIHelperVLM(
        model_name="llava:7b",
        backend="ollama",
        throttle_seconds=0.1  # Faster for testing
    )
    
    # Create a frame that looks like someone using a phone
    frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
    
    # Simulate phone detection scenario
    test_scenarios = [
        {
            "name": "Ambiguous phone confidence (should trigger AI)",
            "phone_confidence": 0.4,
            "expected_trigger": True
        },
        {
            "name": "High confidence (should skip AI)",
            "phone_confidence": 0.8,
            "expected_trigger": False
        },
        {
            "name": "Low confidence (should skip AI)",
            "phone_confidence": 0.1,
            "expected_trigger": False
        }
    ]
    
    for scenario in test_scenarios:
        print(f"\n--- {scenario['name']} ---")
        
        result = helper.check_phone_with_vlm(
            frame=frame,
            face_bbox=(100, 100, 200, 200),
            hand_bboxes=[(150, 150, 250, 250)],
            phone_bboxes=[],
            phone_confidence=scenario["phone_confidence"]
        )
        
        print(f"Result: {result}")
        print(f"Expected trigger: {scenario['expected_trigger']}")
        print(f"Actual triggered: {result['ai_triggered']}")
        print(f"Reason: {result['ai_reason']}")
        
        # Check if it would trigger (regardless of backend availability)
        would_trigger = result['ai_reason'] not in ['confidence_out_of_range_0.80', 'confidence_out_of_range_0.10']
        print(f"Would trigger AI: {would_trigger}")
    
    # Test popup logic
    print(f"\n--- Popup Logic Test ---")
    if result['ai_detected_phone'] and result['ai_triggered']:
        print("✅ Would show popup: '📱 You're on your phone'")
    else:
        print("❌ No popup would show")
        print(f"   ai_detected_phone: {result['ai_detected_phone']}")
        print(f"   ai_triggered: {result['ai_triggered']}")
        print(f"   reason: {result['ai_reason']}")

if __name__ == "__main__":
    test_ai_helper_with_phone()
