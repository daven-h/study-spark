# YOLOv11 Phone Detection Integration

This document explains the integration of YOLOv11 phone detection into the Study Spark attention tracking system, based on the implementation from [jasonli5/phone-detector](https://github.com/jasonli5/phone-detector).

## Overview

The system now uses **YOLOv11** for accurate, real-time phone detection instead of the previous OpenCV-based contour detection method. This provides much more reliable phone detection with higher accuracy.

## Key Features

- **Real-time YOLOv11 phone detection** using the `yolo11s.pt` model
- **Debouncing logic** to prevent false triggers (requires 15 consecutive detections)
- **Cooldown period** of 3 seconds between triggers
- **Face-aware detection** that focuses on the area around detected faces
- **Fallback mechanism** when YOLO dependencies are not available

## Files Modified

### New Files
- `yolo11_phone_detector.py` - Main YOLOv11 phone detector implementation
- `test_yolo11_integration.py` - Test script for the integration

### Modified Files
- `advanced_attention_tracker.py` - Updated to use YOLOv11 phone detector
- `fastapi_server.py` - Updated to reflect YOLOv11 phone detection
- `requirements.txt` - Added ultralytics and other dependencies

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. The YOLOv11 model (`yolo11s.pt`) will be automatically downloaded on first run.

## Configuration

The YOLOv11 phone detector can be configured with these parameters:

```python
# Detection parameters
confidence_threshold = 0.4  # Minimum confidence for detections
cooldown_sec = 3.0          # Minimum time between triggers
streak_required = 15        # Consecutive detections needed to trigger
min_box_area_ratio = 0.01   # Minimum detection size (1% of frame)

# Target classes
target_classes = {"cell phone", "remote"}
```

## How It Works

1. **Frame Processing**: Each video frame is processed by YOLOv11
2. **Object Detection**: YOLOv11 detects objects and filters for phones/remotes
3. **Confidence Filtering**: Only detections above the confidence threshold are kept
4. **Size Filtering**: Only detections above the minimum area ratio are kept
5. **Debouncing**: Requires 15 consecutive frames with valid detections
6. **Cooldown**: Prevents triggers for 3 seconds after a detection

## Integration with Attention Tracker

The YOLOv11 phone detector is integrated into the `AdvancedAttentionTracker` class:

- **Face-aware detection**: When a face is detected, phone detection focuses on the area around the face
- **Background processing**: Phone detection runs in a separate thread to avoid blocking the main tracking loop
- **Fallback support**: If YOLO is not available, the system gracefully falls back to no phone detection

## API Integration

The FastAPI server now reports YOLOv11 phone detection in its algorithm features:

```json
{
  "algorithm_features": [
    "MediaPipe Face Mesh (478 landmarks)",
    "MediaPipe Hands Detection", 
    "MediaPipe Pose Detection",
    "Advanced Eye Aspect Ratio (EAR)",
    "Mouth Aspect Ratio (MAR) for Yawning",
    "Head Pose Estimation (Yaw/Pitch/Roll)",
    "YOLOv11 Phone Detection",  // ← New feature
    "Hand Near Face Detection",
    "Posture Analysis",
    "Enhanced Focus Scoring"
  ]
}
```

## Testing

Run the test script to verify the integration:

```bash
python test_yolo11_integration.py
```

This will test:
- YOLOv11 phone detector import and initialization
- Advanced attention tracker integration
- Model loading and configuration

## Performance Considerations

- **Model Size**: The `yolo11s.pt` model is relatively lightweight (~22MB)
- **Processing Speed**: YOLOv11 is optimized for real-time inference
- **Threading**: Phone detection runs in background to avoid blocking main loop
- **Frame Skipping**: Phone detection can be configured to run every N frames for better performance

## Troubleshooting

### Common Issues

1. **Import Errors**: Make sure ultralytics is installed: `pip install ultralytics`
2. **Torch Errors**: Install PyTorch: `pip install torch torchvision`
3. **Model Download**: The model will be downloaded automatically on first run
4. **Performance**: If detection is slow, try using `yolo11n.pt` (nano model) instead

### Fallback Behavior

If YOLOv11 is not available, the system will:
- Print warning messages about missing dependencies
- Continue running without phone detection
- Return empty detection lists
- Not crash or break the attention tracking

## Benefits of YOLOv11 Integration

1. **Higher Accuracy**: YOLOv11 provides much more accurate phone detection than contour-based methods
2. **Real-time Performance**: Optimized for real-time inference
3. **Robust Detection**: Works well in various lighting conditions and angles
4. **Confidence Scoring**: Provides confidence scores for each detection
5. **Multiple Classes**: Can detect phones, remotes, and other objects
6. **Debouncing**: Built-in logic to prevent false triggers

## Future Enhancements

- **Custom Training**: Train YOLOv11 on specific phone models for better accuracy
- **Multi-object Detection**: Detect other distracting objects (tablets, laptops, etc.)
- **Spatial Analysis**: Analyze phone position relative to face for better context
- **Temporal Analysis**: Track phone usage patterns over time
