"""
AI Helper VLM Module
===================

Optional VLM-based secondary checker for phone usage detection.
Uses local LLaVA or similar VLM to analyze ambiguous cases.

Requirements:
- pip install transformers torch pillow
- For LLaVA: pip install llava
- For Ollama: pip install ollama
"""

import cv2
import numpy as np
import hashlib
import time
import threading
from typing import Optional, Tuple, Dict, Any
import json

try:
    from transformers import LlavaNextProcessor, LlavaNextForConditionalGeneration
    import torch
    from PIL import Image
    VLM_AVAILABLE = True
except ImportError:
    VLM_AVAILABLE = False
    print("Warning: VLM dependencies not available. Install with: pip install transformers torch pillow")

try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False
    print("Warning: Ollama not available. Install with: pip install ollama")


class AIHelperVLM:
    """
    AI Helper using Vision Language Models for phone detection verification.
    
    Supports multiple backends:
    - LLaVA (Hugging Face)
    - Ollama (local models)
    - Future: CogVLM, Qwen-VL
    """
    
    def __init__(self, 
                 model_name: str = "llava",
                 backend: str = "ollama",  # "ollama" or "huggingface"
                 throttle_seconds: float = 1.0,
                 confidence_threshold: float = 0.5):
        """
        Initialize AI Helper VLM
        
        Args:
            model_name: Model to use ("llava", "llava:7b", "llava:13b", etc.)
            backend: "ollama" or "huggingface"
            throttle_seconds: Minimum time between inferences
            confidence_threshold: Minimum confidence for positive detection
        """
        self.model_name = model_name
        self.backend = backend
        self.throttle_seconds = throttle_seconds
        self.confidence_threshold = confidence_threshold
        
        # Performance tracking
        self.last_inference_time = 0
        self.inference_count = 0
        self.cache = {}  # Frame hash -> result cache
        
        # Thread safety
        self.lock = threading.Lock()
        self.last_result = None
        
        # Initialize model
        self.model = None
        self.processor = None
        self._initialize_model()
        
        print(f"AI Helper VLM initialized: {backend}/{model_name}")
    
    def _initialize_model(self):
        """Initialize the VLM model based on backend"""
        try:
            if self.backend == "ollama" and OLLAMA_AVAILABLE:
                # Test Ollama connection
                try:
                    ollama.list()  # Test connection
                    print("✅ Ollama connection successful")
                except Exception as e:
                    print(f"❌ Ollama connection failed: {e}")
                    self.backend = "huggingface"  # Fallback
            
            if self.backend == "huggingface" and VLM_AVAILABLE:
                # Load LLaVA model
                model_id = "llava-hf/llava-v1.6-mistral-7b-hf"
                print(f"Loading Hugging Face model: {model_id}")
                
                self.processor = LlavaNextProcessor.from_pretrained(model_id)
                self.model = LlavaNextForConditionalGeneration.from_pretrained(
                    model_id, 
                    torch_dtype=torch.float16,
                    device_map="auto"
                )
                print("✅ Hugging Face model loaded")
                
        except Exception as e:
            print(f"❌ Model initialization failed: {e}")
            self.model = None
            self.processor = None
    
    def _should_run_inference(self, frame_crop: np.ndarray) -> bool:
        """
        Check if we should run inference based on throttling and cache
        
        Args:
            frame_crop: Cropped frame to analyze
            
        Returns:
            bool: True if inference should run
        """
        current_time = time.time()
        
        # Throttle check
        if current_time - self.last_inference_time < self.throttle_seconds:
            return False
        
        # Cache check - hash the frame
        frame_hash = hashlib.md5(frame_crop.tobytes()).hexdigest()
        if frame_hash in self.cache:
            return False
        
        return True
    
    def _crop_region_of_interest(self, 
                                frame: np.ndarray,
                                face_bbox: Optional[Tuple[int, int, int, int]] = None,
                                hand_bboxes: list = None,
                                phone_bboxes: list = None,
                                padding: int = 20) -> np.ndarray:
        """
        Crop the region of interest combining face, hands, and phone areas
        
        Args:
            frame: Input frame
            face_bbox: (x1, y1, x2, y2) face bounding box
            hand_bboxes: List of hand bounding boxes
            phone_bboxes: List of phone bounding boxes
            padding: Extra padding around the region
            
        Returns:
            Cropped frame
        """
        h, w = frame.shape[:2]
        
        # Start with full frame bounds
        min_x, min_y = 0, 0
        max_x, max_y = w, h
        
        # Expand bounds based on detections
        if face_bbox:
            x1, y1, x2, y2 = face_bbox
            min_x = min(min_x, max(0, x1 - padding))
            min_y = min(min_y, max(0, y1 - padding))
            max_x = max(max_x, min(w, x2 + padding))
            max_y = max(max_y, min(h, y2 + padding))
        
        if hand_bboxes:
            for bbox in hand_bboxes:
                if bbox:
                    x1, y1, x2, y2 = bbox
                    min_x = min(min_x, max(0, x1 - padding))
                    min_y = min(min_y, max(0, y1 - padding))
                    max_x = max(max_x, min(w, x2 + padding))
                    max_y = max(max_y, min(h, y2 + padding))
        
        if phone_bboxes:
            for bbox in phone_bboxes:
                if bbox:
                    x1, y1, x2, y2 = bbox
                    min_x = min(min_x, max(0, x1 - padding))
                    min_y = min(min_y, max(0, y1 - padding))
                    max_x = max(max_x, min(w, x2 + padding))
                    max_y = max(max_y, min(h, y2 + padding))
        
        # Ensure valid bounds
        min_x, min_y = max(0, min_x), max(0, min_y)
        max_x, max_y = min(w, max_x), min(h, max_y)
        
        # Crop the region
        crop = frame[min_y:max_y, min_x:max_x]
        
        # Ensure minimum size
        if crop.shape[0] < 50 or crop.shape[1] < 50:
            # Fallback to center crop
            center_x, center_y = w // 2, h // 2
            size = 200
            min_x = max(0, center_x - size // 2)
            min_y = max(0, center_y - size // 2)
            max_x = min(w, center_x + size // 2)
            max_y = min(h, center_y + size // 2)
            crop = frame[min_y:max_y, min_x:max_x]
        
        return crop
    
    def _inference_ollama(self, frame_crop: np.ndarray) -> Tuple[bool, float]:
        """
        Run inference using Ollama
        
        Args:
            frame_crop: Cropped frame
            
        Returns:
            (is_phone_used, confidence)
        """
        try:
            # Convert to PIL Image
            pil_image = Image.fromarray(cv2.cvtColor(frame_crop, cv2.COLOR_BGR2RGB))
            
            # Prepare prompt
            prompt = "Is the person using their phone in this image? Answer true or false."
            
            # Run inference
            response = ollama.chat(
                model=self.model_name,
                messages=[
                    {
                        'role': 'user',
                        'content': prompt,
                        'images': [pil_image]
                    }
                ]
            )
            
            # Parse response
            response_text = response['message']['content'].lower()
            
            # Extract boolean result
            is_phone = "true" in response_text and "false" not in response_text
            
            # Extract confidence (if available)
            confidence = 0.8 if is_phone else 0.2  # Default confidence
            
            # Try to extract numeric confidence
            import re
            conf_match = re.search(r'confidence[:\s]*(\d+\.?\d*)', response_text)
            if conf_match:
                confidence = float(conf_match.group(1))
            
            return is_phone, confidence
            
        except Exception as e:
            print(f"Ollama inference error: {e}")
            return False, 0.0
    
    def _inference_huggingface(self, frame_crop: np.ndarray) -> Tuple[bool, float]:
        """
        Run inference using Hugging Face LLaVA
        
        Args:
            frame_crop: Cropped frame
            
        Returns:
            (is_phone_used, confidence)
        """
        try:
            if not self.model or not self.processor:
                return False, 0.0
            
            # Convert to PIL Image
            pil_image = Image.fromarray(cv2.cvtColor(frame_crop, cv2.COLOR_BGR2RGB))
            
            # Prepare prompt
            prompt = "Is the person using their phone in this image? Answer true or false."
            
            # Process inputs
            inputs = self.processor(prompt, pil_image, return_tensors="pt")
            
            # Run inference
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=50,
                    do_sample=False,
                    temperature=0.1
                )
            
            # Decode response
            response = self.processor.decode(outputs[0], skip_special_tokens=True)
            response_text = response.lower()
            
            # Parse result
            is_phone = "true" in response_text and "false" not in response_text
            confidence = 0.8 if is_phone else 0.2
            
            return is_phone, confidence
            
        except Exception as e:
            print(f"Hugging Face inference error: {e}")
            return False, 0.0
    
    def check_phone_with_vlm(self, 
                           frame: np.ndarray,
                           face_bbox: Optional[Tuple[int, int, int, int]] = None,
                           hand_bboxes: list = None,
                           phone_bboxes: list = None,
                           phone_confidence: float = 0.0) -> Dict[str, Any]:
        """
        Check if person is using phone using VLM
        
        Args:
            frame: Input frame
            face_bbox: Face bounding box
            hand_bboxes: List of hand bounding boxes
            phone_bboxes: List of phone bounding boxes
            phone_confidence: Current phone detection confidence
            
        Returns:
            Dict with ai_detected_phone, ai_confidence, and metadata
        """
        result = {
            "ai_detected_phone": False,
            "ai_confidence": 0.0,
            "ai_triggered": False,
            "ai_reason": "not_triggered"
        }
        
        # Check if we should run inference
        if phone_confidence < 0.3 or phone_confidence > 0.6:
            result["ai_reason"] = f"confidence_out_of_range_{phone_confidence:.2f}"
            return result
        
        # Crop region of interest
        try:
            frame_crop = self._crop_region_of_interest(
                frame, face_bbox, hand_bboxes, phone_bboxes
            )
        except Exception as e:
            result["ai_reason"] = f"crop_error_{str(e)}"
            return result
        
        # Check throttling and cache
        if not self._should_run_inference(frame_crop):
            result["ai_reason"] = "throttled_or_cached"
            return result
        
        # Run inference
        try:
            if self.backend == "ollama" and OLLAMA_AVAILABLE:
                is_phone, confidence = self._inference_ollama(frame_crop)
            elif self.backend == "huggingface" and VLM_AVAILABLE:
                is_phone, confidence = self._inference_huggingface(frame_crop)
            else:
                result["ai_reason"] = "no_available_backend"
                return result
            
            # Update result
            result["ai_detected_phone"] = is_phone
            result["ai_confidence"] = confidence
            result["ai_triggered"] = True
            result["ai_reason"] = "success"
            
            # Update tracking
            with self.lock:
                self.last_inference_time = time.time()
                self.inference_count += 1
                self.last_result = result
                
                # Cache result
                frame_hash = hashlib.md5(frame_crop.tobytes()).hexdigest()
                self.cache[frame_hash] = result
                
                # Clean old cache entries
                if len(self.cache) > 10:
                    oldest_key = next(iter(self.cache))
                    del self.cache[oldest_key]
            
        except Exception as e:
            result["ai_reason"] = f"inference_error_{str(e)}"
        
        return result
    
    def get_stats(self) -> Dict[str, Any]:
        """Get AI helper statistics"""
        with self.lock:
            return {
                "inference_count": self.inference_count,
                "last_inference_time": self.last_inference_time,
                "cache_size": len(self.cache),
                "backend": self.backend,
                "model_name": self.model_name,
                "throttle_seconds": self.throttle_seconds
            }


# Example usage and testing
if __name__ == "__main__":
    # Test the AI helper
    print("Testing AI Helper VLM...")
    
    # Initialize helper
    helper = AIHelperVLM(
        model_name="llava:7b",
        backend="ollama",
        throttle_seconds=1.0
    )
    
    # Create dummy frame
    dummy_frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
    
    # Test inference
    result = helper.check_phone_with_vlm(
        frame=dummy_frame,
        face_bbox=(100, 100, 200, 200),
        hand_bboxes=[(150, 150, 250, 250)],
        phone_bboxes=[],
        phone_confidence=0.4
    )
    
    print(f"Test result: {result}")
    print(f"Stats: {helper.get_stats()}")
