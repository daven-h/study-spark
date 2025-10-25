"""
Enhanced Visualizer with Phone vs Hand Detection
Shows improved status messages and detection overlays
"""

import cv2
import numpy as np
from typing import Dict, Any, List, Tuple


class EnhancedVisualizer:
    """
    Enhanced visualizer for phone vs hand detection
    """
    
    def __init__(self):
        """Initialize the enhanced visualizer"""
        # Colors for different states
        self.colors = {
            "green": (0, 255, 0),
            "red": (0, 0, 255),
            "yellow": (0, 255, 255),
            "blue": (255, 0, 0),
            "purple": (255, 0, 255),
            "white": (255, 255, 255),
            "black": (0, 0, 0),
            "background": (0, 0, 0)
        }
        
        # Font settings
        self.font_scale_small = 0.5
        self.font_scale_medium = 0.6
        self.font_scale_large = 0.8
        self.font_thickness = 2
    
    def draw_enhanced_status_overlay(self, frame: np.ndarray, 
                                   focus_metrics: Dict[str, Any],
                                   fps: float) -> np.ndarray:
        """
        Draw enhanced status overlay with phone vs hand detection
        
        Args:
            frame: Input frame
            focus_metrics: Enhanced focus metrics
            fps: Current FPS
            
        Returns:
            Frame with enhanced overlay
        """
        h, w = frame.shape[:2]
        
        # Enhanced status messages
        status_messages = focus_metrics.get("status_messages", {})
        
        # Draw main status panel
        panel_width = 350
        panel_height = 160
        panel_x = 10
        panel_y = 10
        
        # Background panel
        cv2.rectangle(frame, (panel_x, panel_y), 
                     (panel_x + panel_width, panel_y + panel_height), 
                     self.colors["black"], -1)
        cv2.rectangle(frame, (panel_x, panel_y), 
                     (panel_x + panel_width, panel_y + panel_height), 
                     self.colors["white"], 2)
        
        # Title
        cv2.putText(frame, "Enhanced Attention Tracker", 
                   (panel_x + 10, panel_y + 25),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, self.colors["white"], 2)
        
        # Status items
        y_offset = 50
        items = [
            ("Face", status_messages.get("face", {})),
            ("Orientation", status_messages.get("orientation", {})),
            ("Interaction", status_messages.get("interaction", {})),
            ("Posture", status_messages.get("posture", {}))
        ]
        
        for label, status_data in items:
            if status_data:
                text = status_data.get("text", f"{label}: Unknown")
                color_name = status_data.get("color", "white")
                color = self.colors.get(color_name, self.colors["white"])
                
                cv2.putText(frame, text, 
                           (panel_x + 10, panel_y + y_offset),
                           cv2.FONT_HERSHEY_SIMPLEX, self.font_scale_medium, 
                           color, self.font_thickness)
                y_offset += 25
        
        # Main focus status
        focused = focus_metrics.get("focused", False)
        focus_score = focus_metrics.get("focus_score", 0.0)
        
        main_status = "🎯 FOCUSED" if focused else "⚠️ DISTRACTED"
        main_color = self.colors["green"] if focused else self.colors["red"]
        
        cv2.putText(frame, main_status, 
                   (panel_x + 10, panel_y + y_offset + 10),
                   cv2.FONT_HERSHEY_SIMPLEX, self.font_scale_large, 
                   main_color, self.font_thickness)
        
        # Performance metrics (bottom right)
        metrics_x = w - 200
        metrics_y = h - 60
        
        # Background for metrics
        cv2.rectangle(frame, (metrics_x - 10, metrics_y - 30), 
                     (w - 10, h - 10), self.colors["black"], -1)
        cv2.rectangle(frame, (metrics_x - 10, metrics_y - 30), 
                     (w - 10, h - 10), self.colors["white"], 1)
        
        # Metrics text
        cv2.putText(frame, f"Score: {focus_score:.2f}", 
                   (metrics_x, metrics_y),
                   cv2.FONT_HERSHEY_SIMPLEX, self.font_scale_medium, 
                   self.colors["white"], self.font_thickness)
        
        cv2.putText(frame, f"FPS: {fps:.1f}", 
                   (metrics_x, metrics_y + 20),
                   cv2.FONT_HERSHEY_SIMPLEX, self.font_scale_medium, 
                   self.colors["white"], self.font_thickness)
        
        # Interaction details
        interaction_state = focus_metrics.get("interaction_state", "no_interaction")
        phone_confidence = focus_metrics.get("phone_confidence", 0.0)
        
        if interaction_state == "phone_near_head":
            cv2.putText(frame, f"📱 Phone: {phone_confidence:.2f}", 
                       (metrics_x, metrics_y + 40),
                       cv2.FONT_HERSHEY_SIMPLEX, self.font_scale_small, 
                       self.colors["red"], self.font_thickness)
        elif interaction_state == "hand_near_head":
            cv2.putText(frame, "✋ Hand detected", 
                       (metrics_x, metrics_y + 40),
                       cv2.FONT_HERSHEY_SIMPLEX, self.font_scale_small, 
                       self.colors["yellow"], self.font_thickness)
        
        return frame
    
    def draw_detection_overlays(self, frame: np.ndarray, 
                              detection_results: Dict[str, Any]) -> np.ndarray:
        """
        Draw detection overlays for phones, hands, and face
        
        Args:
            frame: Input frame
            detection_results: Detection results from enhanced tracker
            
        Returns:
            Frame with detection overlays
        """
        # Draw face bounding box
        face_bbox = detection_results.get("face_bbox")
        if face_bbox:
            fx1, fy1, fx2, fy2 = face_bbox
            cv2.rectangle(frame, (fx1, fy1), (fx2, fy2), self.colors["green"], 2)
            cv2.putText(frame, "Face", (fx1, fy1 - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, self.colors["green"], 2)
        
        # Draw phone detections
        phones = detection_results.get("phones", [])
        phone_near_face = detection_results.get("phone_near_face", False)
        
        for (px1, py1, px2, py2), conf in phones:
            # Color based on proximity to face
            color = self.colors["red"] if phone_near_face else self.colors["blue"]
            cv2.rectangle(frame, (px1, py1), (px2, py2), color, 2)
            cv2.putText(frame, f"Phone {conf:.2f}", (px1, py1 - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        
        # Draw hand landmarks
        hand_landmarks = detection_results.get("hand_landmarks", [])
        hand_near_face = detection_results.get("hand_near_face", False)
        
        for hand in hand_landmarks:
            for hx, hy in hand:
                h, w = frame.shape[:2]
                px = int(hx * w)
                py = int(hy * h)
                # Color based on proximity to face
                color = self.colors["yellow"] if hand_near_face else self.colors["purple"]
                cv2.circle(frame, (px, py), 3, color, -1)
        
        # Draw interaction state indicator
        interaction_state = detection_results.get("interaction_state", "no_interaction")
        self._draw_interaction_indicator(frame, interaction_state)
        
        return frame
    
    def _draw_interaction_indicator(self, frame: np.ndarray, interaction_state: str):
        """Draw interaction state indicator"""
        h, w = frame.shape[:2]
        
        # Position indicator in top right
        indicator_x = w - 150
        indicator_y = 50
        
        # Background
        cv2.rectangle(frame, (indicator_x - 10, indicator_y - 20), 
                     (w - 10, indicator_y + 30), self.colors["black"], -1)
        cv2.rectangle(frame, (indicator_x - 10, indicator_y - 20), 
                     (w - 10, indicator_y + 30), self.colors["white"], 1)
        
        # State text and color
        if interaction_state == "phone_near_head":
            text = "📱 PHONE"
            color = self.colors["red"]
        elif interaction_state == "hand_near_head":
            text = "✋ HAND"
            color = self.colors["yellow"]
        else:
            text = "✅ CLEAR"
            color = self.colors["green"]
        
        cv2.putText(frame, text, (indicator_x, indicator_y),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
    
    def draw_attention_ring(self, frame: np.ndarray, focus_score: float) -> np.ndarray:
        """
        Draw attention ring around the frame
        
        Args:
            frame: Input frame
            focus_score: Current focus score (0-1)
            
        Returns:
            Frame with attention ring
        """
        h, w = frame.shape[:2]
        
        # Ring parameters
        ring_thickness = 8
        ring_margin = 20
        
        # Color based on focus score
        if focus_score > 0.8:
            ring_color = self.colors["green"]
        elif focus_score > 0.5:
            ring_color = self.colors["yellow"]
        else:
            ring_color = self.colors["red"]
        
        # Draw ring around frame
        cv2.rectangle(frame, (ring_margin, ring_margin), 
                     (w - ring_margin, h - ring_margin), 
                     ring_color, ring_thickness)
        
        return frame
