#!/usr/bin/env python3
"""
Force AI Popup Demo
==================

This will definitely show you the AI popup in action by bypassing throttling.
"""

import cv2
import numpy as np
from precise_attention_tracker import PreciseAttentionTracker

class ForceAIPopupTracker(PreciseAttentionTracker):
    """Force AI popup to show for demonstration"""
    
    def __init__(self):
        super().__init__()
        # Override AI helper with immediate triggering
        from simulated_ai_helper import SimulatedAIHelper
        self.ai_helper = SimulatedAIHelper(detection_probability=0.9)  # 90% chance
        # Remove throttling
        self.ai_helper.throttle_seconds = 0.0
        print("Force AI Popup Tracker initialized")
    
    def process_frame(self, frame):
        """Override to force AI helper to trigger"""
        metrics = super().process_frame(frame)
        
        # Force phone confidence to trigger AI helper
        metrics['phone_confidence'] = 0.45  # In trigger range
        
        # Force AI helper to run every frame (bypass throttling)
        if self.ai_helper:
            # Get hand bounding boxes for AI helper
            hand_bboxes = []
            if hasattr(self, '_last_hand_landmarks') and self._last_hand_landmarks:
                for hand in self._last_hand_landmarks:
                    hand_x = [lm.x for lm in hand.landmark]
                    hand_y = [lm.y for lm in hand.landmark]
                    if hand_x and hand_y:
                        h_x_min = int(min(hand_x) * self.frame_width)
                        h_x_max = int(max(hand_x) * self.frame_width)
                        h_y_min = int(min(hand_y) * self.frame_height)
                        h_y_max = int(max(hand_y) * self.frame_height)
                        hand_bboxes.append((h_x_min, h_y_min, h_x_max, h_y_max))
            
            # Force AI helper to run
            ai_result = self.ai_helper.check_phone_with_vlm(
                frame=frame,
                face_bbox=(100, 100, 200, 200) if metrics.get('face_visible') else None,
                hand_bboxes=hand_bboxes,
                phone_bboxes=[],
                phone_confidence=0.45
            )
            
            # Update metrics with AI results
            metrics['ai_detected_phone'] = ai_result.get('ai_detected_phone', False)
            metrics['ai_confidence'] = ai_result.get('ai_confidence', 0.0)
            metrics['ai_triggered'] = ai_result.get('ai_triggered', False)
            
            # Force popup if AI detects phone
            if ai_result.get('ai_detected_phone', False) and ai_result.get('ai_triggered', False):
                self.ai_popup_alpha = 255
                self.ai_popup_timer = 60  # 2 seconds at 30 FPS
                self.ai_popup_message = "You're on your phone"
        
        return metrics

def demo_ai_popup():
    """Demo the AI popup functionality"""
    print("AI Popup Demo - This will show popups when AI detects phone usage")
    print("The AI helper will randomly detect 'phone usage' to demonstrate popups")
    print("Press 'q' to quit")
    
    tracker = ForceAIPopupTracker()
    tracker.run()

if __name__ == "__main__":
    demo_ai_popup()
