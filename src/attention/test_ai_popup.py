#!/usr/bin/env python3
"""
Test AI Popup with Forced Triggering
====================================

This will force the AI helper to trigger so you can see the popup in action.
"""

import cv2
import numpy as np
from precise_attention_tracker import PreciseAttentionTracker

class TestAITracker(PreciseAttentionTracker):
    """Test version that forces AI helper to trigger"""
    
    def __init__(self):
        super().__init__()
        # Override AI helper with high detection probability
        from simulated_ai_helper import SimulatedAIHelper
        self.ai_helper = SimulatedAIHelper(detection_probability=0.8)  # 80% chance
        print("Test AI Tracker initialized with forced AI helper")
    
    def process_frame(self, frame):
        """Override to force phone confidence in AI trigger range"""
        metrics = super().process_frame(frame)
        
        # Force phone confidence to trigger AI helper (0.3-0.6 range)
        if 'phone_confidence' in metrics:
            metrics['phone_confidence'] = 0.45  # Force into AI trigger range
        
        return metrics

def test_ai_popup():
    """Test the AI popup functionality"""
    print("Testing AI Popup with Forced Triggering...")
    print("This will show popups when AI detects phone usage")
    print("Press 'q' to quit")
    
    tracker = TestAITracker()
    tracker.run()

if __name__ == "__main__":
    test_ai_popup()
