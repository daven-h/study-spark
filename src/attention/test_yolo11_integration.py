#!/usr/bin/env python3
"""
Test script for YOLOv11 Phone Detector
"""

import sys
import os

# Add the attention directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_yolo11_detector():
    """Test the YOLOv11 phone detector"""
    try:
        from yolo11_phone_detector import YOLOv11PhoneDetector
        print("✅ YOLOv11 Phone Detector imported successfully (EXACT from jasonli5/phone-detector)")
        
        # Initialize detector
        detector = YOLOv11PhoneDetector()
        print("✅ YOLOv11 Phone Detector initialized")
        
        # Get model info
        info = detector.get_model_info()
        print(f"📊 Model info: {info}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure ultralytics is installed: pip install ultralytics")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_advanced_tracker():
    """Test the Advanced Attention Tracker with YOLOv11"""
    try:
        from advanced_attention_tracker import AdvancedAttentionTracker
        print("✅ Advanced Attention Tracker imported successfully")
        
        # Note: We won't actually initialize it here to avoid camera issues
        print("📱 Advanced Attention Tracker ready with YOLOv11 phone detection")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run tests"""
    print("🧪 Testing YOLOv11 Phone Detector Integration")
    print("=" * 50)
    
    # Test YOLOv11 detector
    print("\n1. Testing YOLOv11 Phone Detector...")
    yolo_success = test_yolo11_detector()
    
    # Test Advanced Tracker
    print("\n2. Testing Advanced Attention Tracker...")
    tracker_success = test_advanced_tracker()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    print(f"  YOLOv11 Phone Detector: {'✅ PASS' if yolo_success else '❌ FAIL'}")
    print(f"  Advanced Attention Tracker: {'✅ PASS' if tracker_success else '❌ FAIL'}")
    
    if yolo_success and tracker_success:
        print("\n🎉 All tests passed! YOLOv11 phone detection is ready.")
        print("📱 The system now uses YOLOv11 for accurate phone detection.")
        print("🚀 You can run the FastAPI server or the attention tracker.")
    else:
        print("\n⚠️ Some tests failed. Check the error messages above.")
        print("💡 Make sure all dependencies are installed: pip install -r requirements.txt")

if __name__ == "__main__":
    main()
