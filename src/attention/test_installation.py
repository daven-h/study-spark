#!/usr/bin/env python3
"""
Test script to verify the attention tracking engine installation.
Run this to check if all dependencies are properly installed.
"""

import sys
import importlib

def test_import(module_name, package_name=None):
    """Test if a module can be imported."""
    try:
        if package_name:
            importlib.import_module(module_name, package_name)
        else:
            importlib.import_module(module_name)
        print(f"✓ {module_name} - OK")
        return True
    except ImportError as e:
        print(f"✗ {module_name} - FAILED: {e}")
        return False

def test_opencv_camera():
    """Test if OpenCV can access camera."""
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            print("✓ OpenCV Camera - OK")
            cap.release()
            return True
        else:
            print("✗ OpenCV Camera - FAILED: Camera not accessible")
            return False
    except Exception as e:
        print(f"✗ OpenCV Camera - FAILED: {e}")
        return False

def test_mediapipe():
    """Test if MediaPipe can initialize."""
    try:
        import mediapipe as mp
        
        # Test face mesh
        face_mesh = mp.solutions.face_mesh.FaceMesh()
        print("✓ MediaPipe FaceMesh - OK")
        
        # Test hands
        hands = mp.solutions.hands.Hands()
        print("✓ MediaPipe Hands - OK")
        
        # Test pose
        pose = mp.solutions.pose.Pose()
        print("✓ MediaPipe Pose - OK")
        
        return True
    except Exception as e:
        print(f"✗ MediaPipe - FAILED: {e}")
        return False

def test_local_modules():
    """Test if local modules can be imported."""
    modules = [
        "tracker",
        "focus_logic", 
        "visualizer",
        "utils"
    ]
    
    all_ok = True
    for module in modules:
        try:
            importlib.import_module(module)
            print(f"✓ {module}.py - OK")
        except ImportError as e:
            print(f"✗ {module}.py - FAILED: {e}")
            all_ok = False
    
    return all_ok

def main():
    """Run all installation tests."""
    print("Python Attention Tracking Engine - Installation Test")
    print("=" * 60)
    
    # Test Python version
    python_version = sys.version_info
    if python_version >= (3, 7):
        print(f"✓ Python {python_version.major}.{python_version.minor} - OK")
    else:
        print(f"✗ Python {python_version.major}.{python_version.minor} - FAILED: Requires Python 3.7+")
        return False
    
    print("\nTesting dependencies...")
    
    # Test required packages
    required_packages = [
        "cv2",
        "numpy", 
        "mediapipe",
        "websockets"
    ]
    
    all_deps_ok = True
    for package in required_packages:
        if not test_import(package):
            all_deps_ok = False
    
    if not all_deps_ok:
        print("\n❌ Some dependencies are missing. Please run:")
        print("pip install -r requirements.txt")
        return False
    
    print("\nTesting MediaPipe components...")
    if not test_mediapipe():
        print("\n❌ MediaPipe test failed. Please check MediaPipe installation.")
        return False
    
    print("\nTesting camera access...")
    if not test_opencv_camera():
        print("\n⚠️  Camera test failed. This might be due to:")
        print("   - Camera being used by another application")
        print("   - Camera permissions not granted")
        print("   - No camera connected")
        print("   The attention tracker may still work if camera becomes available.")
    
    print("\nTesting local modules...")
    if not test_local_modules():
        print("\n❌ Local module test failed. Please check file structure.")
        return False
    
    print("\n" + "=" * 60)
    print("✅ Installation test completed successfully!")
    print("\nYou can now run the attention tracker:")
    print("  python main.py")
    print("\nOr start the WebSocket server:")
    print("  python server.py")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
