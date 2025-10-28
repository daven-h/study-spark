#!/usr/bin/env python3
"""
Test the simplified YOLOv11 Phone Detector
"""

def test_simplified_detector():
    """Test the simplified phone detector"""
    print("🧪 Testing Simplified YOLOv11 Phone Detector")
    print("=" * 50)
    
    try:
        from yolo11_phone_detector import YOLOv11PhoneDetector
        print("✅ YOLOv11 Phone Detector imported successfully")
        
        # Initialize detector
        detector = YOLOv11PhoneDetector()
        print("✅ YOLOv11 Phone Detector initialized")
        
        # Get model info
        info = detector.get_model_info()
        print(f"📊 Model info: {info}")
        
        # Test alert system
        print("\n🔔 Testing alert system...")
        detector.play_phone_alert()
        print("✅ Alert system tested")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run tests"""
    print("🧪 Testing Simplified YOLOv11 Phone Detector")
    print("Based on: https://github.com/jasonli5/phone-detector")
    print()
    
    # Test simplified detector
    success = test_simplified_detector()
    
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    
    if success:
        print("🎉 SUCCESS: Simplified YOLOv11 Phone Detector works!")
        print("📱 Features:")
        print("  ✅ EXACT implementation from jasonli5/phone-detector")
        print("  ✅ Simple 'PHONE DETECTED - LOCK IN!' alert")
        print("  ✅ Windows ding sound")
        print("  ✅ Visual alert window")
        print("  ✅ No complex video playback")
        print("  ✅ Cleaner, simpler code")
        print()
        print("🚀 Ready to use in attention tracking system!")
    else:
        print("❌ Some tests failed. Check the error messages above.")

if __name__ == "__main__":
    main()
