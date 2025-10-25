# 🚀 Enhanced Attention Tracker - YOLOv8 + MediaPipe Integration

## 🎯 Overview

The Enhanced Attention Tracker combines **YOLOv8** and **MediaPipe** to provide sophisticated phone vs hand detection for improved focus tracking accuracy.

## ✨ Key Features

### 📱 **Phone vs Hand Detection**
- **YOLOv8 Object Detection**: Detects actual phone objects in the frame
- **MediaPipe Hand Tracking**: Tracks hand landmarks and positions
- **Smart Classification**: Distinguishes between phone calls and hand gestures
- **Confidence Scoring**: Provides confidence levels for each detection

### 🎯 **Enhanced Focus Analysis**
- **Phone Near Head**: Red alert when phone is detected near face
- **Hand Near Head**: Yellow warning for hand gestures near face
- **No Interaction**: Green status when clear
- **Weighted Scoring**: Different weights for phone vs hand interactions

### 🎨 **Advanced Visualization**
- **Color-coded Status**: Red (phone), Yellow (hand), Green (clear)
- **Detection Overlays**: Visual bounding boxes for phones and hands
- **Confidence Display**: Shows detection confidence levels
- **Real-time Metrics**: Live focus scores and interaction states

## 🛠️ Installation

### Prerequisites
```bash
# Install enhanced requirements
pip install ultralytics torch torchvision mediapipe opencv-python numpy websockets
```

### YOLOv8 Model Download
The system automatically downloads the YOLOv8n model on first run:
- **Model**: `yolov8n.pt` (lightweight, ~6MB)
- **Classes**: Includes "cell phone" detection
- **Performance**: Optimized for real-time inference

## 🚀 Usage

### Basic Usage
```bash
# Run enhanced tracker
python enhanced_main.py
```

### Test Components
```bash
# Test individual components
python test_enhanced.py
```

## 🎮 Controls

| Key | Action |
|-----|--------|
| `q` | Quit application |
| `r` | Reset focus history |
| `s` | Save screenshot |
| `d` | Toggle detection overlays |
| `l` | Toggle landmark display |
| `a` | Toggle attention ring |

## 📊 Enhanced Status Messages

### 🟢 **Good States**
- **Face**: "✓ Face detected"
- **Orientation**: "✓ Looking forward"
- **Interaction**: "✓ No interaction"
- **Posture**: "✓ Good posture"

### 🔴 **Phone Detection**
- **Interaction**: "✗ Phone detected (0.85)"
- **Status**: Red alert with confidence score
- **Action**: Immediate focus loss

### 🟡 **Hand Detection**
- **Interaction**: "⚠ Hand near head"
- **Status**: Yellow warning
- **Action**: Reduced focus score

### 🔴 **Other Issues**
- **Face**: "✗ Look at camera"
- **Orientation**: "✗ Turn head forward"
- **Posture**: "✗ Straighten up"

## 🏗️ Architecture

### Core Components

1. **EnhancedFocusTracker** (`enhanced_tracker.py`)
   - YOLOv8 phone detection
   - MediaPipe face/hand tracking
   - Smart interaction classification

2. **EnhancedFocusEvaluator** (`enhanced_focus_logic.py`)
   - Weighted focus scoring
   - Phone vs hand differentiation
   - Enhanced status messages

3. **EnhancedVisualizer** (`enhanced_visualizer.py`)
   - Color-coded overlays
   - Detection visualization
   - Status panels

4. **EnhancedAttentionTracker** (`enhanced_main.py`)
   - Main application
   - Component integration
   - User interface

## 🎯 Detection Logic

### Phone Detection
```python
# YOLOv8 detects phone objects
phones = yolo_model(frame)
phone_near_face = check_phone_proximity(phones, face_bbox)

# Result: "✗ Phone detected (0.85)"
```

### Hand Detection
```python
# MediaPipe tracks hand landmarks
hand_landmarks = hands_model.process(frame)
hand_near_face = check_hand_proximity(hand_landmarks, face_bbox)

# Result: "⚠ Hand near head"
```

### Smart Classification
```python
if phone_near_face:
    return "phone_near_head"  # Red alert
elif hand_near_face:
    return "hand_near_head"   # Yellow warning
else:
    return "no_interaction"    # Green status
```

## 📈 Performance Optimization

### YOLO Optimization
- **Frame Skipping**: YOLO runs every 10 frames
- **Caching**: Phone detection results cached
- **Lightweight Model**: YOLOv8n for speed

### MediaPipe Optimization
- **Real-time**: Face and hand tracking every frame
- **Efficient**: Optimized landmark detection
- **Smooth**: Continuous tracking for gestures

## 🔧 Configuration

### Detection Thresholds
```python
# Phone detection confidence
phone_threshold = 0.5

# Hand proximity to face
hand_face_margin = 80

# YOLO update interval
yolo_update_interval = 10
```

### Focus Weights
```python
weights = {
    "face_visibility": 0.3,
    "orientation": 0.25,
    "phone_interaction": 0.25,  # Higher weight
    "hand_interaction": 0.1,    # Lower weight
    "posture": 0.1
}
```

## 📊 JSON Output

### Enhanced Metrics
```json
{
  "timestamp": "2025-10-25T16:30:00Z",
  "focused": false,
  "focus_score": 0.65,
  "face_visible": true,
  "orientation_good": true,
  "phone_near_face": true,
  "hand_near_face": false,
  "interaction_state": "phone_near_head",
  "phone_confidence": 0.87,
  "posture_stable": true,
  "fps": 8.2
}
```

## 🎯 Use Cases

### 📱 **Phone Detection**
- **Video Calls**: Detect when user is on phone
- **Distraction Alert**: Immediate focus loss
- **Study Sessions**: Prevent phone usage

### ✋ **Hand Gestures**
- **Thinking Pose**: Hand on chin/head
- **Posture Analysis**: Hand positioning
- **Gesture Recognition**: Natural hand movements

### 🎓 **Educational Applications**
- **Online Learning**: Monitor attention during classes
- **Study Sessions**: Track focus and distractions
- **Exam Proctoring**: Detect phone usage during tests

## 🚀 Future Enhancements

### Planned Features
- **Posture Classification**: Upright vs slouched detection
- **Head Tilt Analysis**: Reading vs phone call angles
- **Distraction Duration**: Track time spent distracted
- **Multi-person Support**: Track multiple users
- **Custom Models**: Train on specific phone types

### Performance Improvements
- **GPU Acceleration**: CUDA support for YOLO
- **Model Quantization**: Reduce model size
- **Edge Deployment**: Mobile/embedded support
- **Real-time Streaming**: WebSocket integration

## 🐛 Troubleshooting

### Common Issues

1. **YOLOv8 Model Download**
   ```bash
   # Manual download if automatic fails
   python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"
   ```

2. **Camera Access**
   ```bash
   # Check camera permissions
   python -c "import cv2; print(cv2.VideoCapture(0).isOpened())"
   ```

3. **Performance Issues**
   ```bash
   # Reduce YOLO frequency
   yolo_update_interval = 20  # Every 20 frames
   ```

## 📚 References

- [YOLOv8 Documentation](https://docs.ultralytics.com/)
- [MediaPipe Solutions](https://developers.google.com/mediapipe/solutions)
- [OpenCV Python](https://opencv-python-tutroals.readthedocs.io/)

## 🤝 Contributing

Contributions welcome! Please see the main project README for guidelines.

---

**Enhanced Attention Tracker** - Powered by YOLOv8 + MediaPipe 🚀
