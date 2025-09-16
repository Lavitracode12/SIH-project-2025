# 🎥🌿 Real-Time Hybrid Plant Analysis System

## 🔍 Overview
This system extends the Hybrid Plant Analysis System with **real-time webcam capabilities**, providing live plant health monitoring through your computer's camera.

## ✨ Features

### 🎯 Real-Time Capabilities
- **Live leaf detection** using YOLO model (47 plant species)
- **Real-time disease classification** using Vision Transformer
- **Webcam integration** with adjustable resolution
- **Interactive controls** for real-time parameter adjustment
- **Performance monitoring** with FPS display
- **Snapshot capture** for saving interesting detections

### 🎮 Interactive Controls
- **[SPACE]** - Pause/Resume analysis
- **[S]** - Save snapshot of current frame
- **[↑/↓]** - Adjust leaf detection confidence
- **[←/→]** - Adjust disease detection confidence  
- **[C]** - Toggle confidence display
- **[H]** - Toggle health status display
- **[F]** - Toggle FPS display
- **[Q]** - Quit application

### 📊 Visual Features
- **Bounding boxes** around detected leaves
- **Species identification** with confidence scores
- **Health status indicators** (Healthy/Diseased)
- **Color-coded annotations** (Green=Healthy, Red=Diseased, Orange=Analyzing)
- **Real-time statistics** overlay
- **Performance metrics** display

## 📁 Files

### Core System
- **`realtime_hybrid_analyzer.py`** - Main real-time analysis engine
- **`quick_realtime.py`** - Simple launcher for quick start
- **`run_realtime_analysis.sh`** - Interactive system launcher
- **`requirements.txt`** - Python dependencies
- **`README.md`** - This documentation

### Dependencies (from parent system)
- **`../leaf detection/plant_leaf_model.pt`** - YOLO leaf detection model
- **`../Disease detection/local_models/`** - ViT disease classification models
- **`../leaf detection/hybrid_plant_analyzer.py`** - Base hybrid analyzer

## 🚀 Quick Start

### Method 1: Interactive Launcher
```bash
bash run_realtime_analysis.sh
```
Choose from menu options for different configurations.

### Method 2: Quick Start
```bash
# Default camera and resolution
python3 quick_realtime.py

# Specific camera
python3 quick_realtime.py 1

# Custom resolution  
python3 quick_realtime.py 0 1280x720
```

### Method 3: Full Control
```bash
python3 realtime_hybrid_analyzer.py
```

## ⚙️ Configuration

### Camera Settings
- **Default Resolution**: 640x480 @ 30fps
- **Supported Resolutions**: 640x480, 1280x720, 1920x1080
- **Camera Selection**: Auto-detects available cameras (0, 1, 2, etc.)

### Analysis Parameters
- **Leaf Detection Confidence**: 0.10 (10%) - adjustable with ↑/↓
- **Disease Classification Confidence**: 0.30 (30%) - adjustable with ←/→
- **Analysis Interval**: 1.0 second between full analyses
- **Frame Skip**: Process every 3rd frame for performance

### Performance Optimization
- **Frame skipping** for smooth real-time operation
- **Selective analysis** to reduce computational load
- **FPS monitoring** for performance tracking
- **Memory-efficient** processing pipeline

## 🎯 Supported Detection

### Plant Species (47 types)
Common plants, trees, agricultural crops, and medicinal plants including:
- **Fruits**: Mango, Guava, Lemon, Pomegranate, Papaya
- **Herbs**: Basil, Mint, Tulsi, Neem, Moringa
- **Trees**: Eucalyptus, Bamboo, Coconut, Banyan
- **Agricultural**: Cotton, Tea, Cardamom, Rice

### Disease Types (12 categories)
- **Corn**: Common Rust, Gray Leaf Spot, Healthy
- **Potato**: Early Blight, Late Blight, Healthy
- **Rice**: Brown Spot, Leaf Blast, Healthy  
- **Wheat**: Brown Rust, Yellow Rust, Healthy

## 📊 Performance Tips

### For Best Results
- **Good Lighting**: Ensure adequate natural or artificial light
- **Steady Positioning**: Hold plants steady for 1-2 seconds
- **Clear Framing**: Position leaves clearly within camera view
- **Avoid Rapid Movement**: Smooth camera movements work best
- **Optimal Distance**: Keep plants 1-3 feet from camera

### Performance Optimization
- **Lower Resolution**: Use 640x480 for better FPS on slower hardware
- **Adjust Confidence**: Higher thresholds reduce false positives
- **Pause Analysis**: Use SPACE to pause when positioning camera
- **Close Other Apps**: Free up system resources for better performance

## 📸 Output Files

### Snapshots
- **Format**: JPEG images with timestamp
- **Naming**: `realtime_snapshot_YYYYMMDD_HHMMSS.jpg`
- **Content**: Annotated frames with detections and labels
- **Location**: Current working directory

## 🔧 Troubleshooting

### Camera Issues
```bash
# Check available cameras
ls /dev/video*

# Test camera access
python3 -c "import cv2; cap = cv2.VideoCapture(0); print('Camera OK' if cap.isOpened() else 'Camera Error')"
```

### Model Loading Issues
- Ensure parent hybrid system models are available
- Check paths to `../leaf detection/` and `../Disease detection/`
- Verify model files are not corrupted

### Performance Issues
- Lower camera resolution: Use 640x480 instead of HD
- Increase frame skip rate in code
- Close other applications using camera/CPU
- Use integrated graphics instead of discrete GPU if overheating

### Common Error Solutions
- **"Camera not found"**: Try different camera IDs (0, 1, 2)
- **"Models not ready"**: Check if base hybrid system works first
- **Low FPS**: Reduce resolution or increase frame skipping
- **High CPU usage**: Lower analysis frequency in settings

## 🎨 Customization

### Adjust Detection Parameters
Edit `realtime_hybrid_analyzer.py`:
```python
self.leaf_confidence = 0.10      # Leaf detection threshold
self.disease_confidence = 0.30   # Disease classification threshold
self.analysis_interval = 1.0     # Seconds between analyses
self.skip_frames = 3             # Process every Nth frame
```

### Modify Visual Display
Customize colors, fonts, and overlay information in the `draw_annotations()` method.

### Add New Controls
Extend the `handle_keyboard_input()` method to add new keyboard shortcuts.

## 🌐 System Requirements

### Hardware
- **Camera**: USB webcam or built-in camera
- **CPU**: Multi-core processor recommended
- **RAM**: 4GB+ (8GB+ recommended)
- **Storage**: 500MB for models

### Software
- **Python**: 3.8+ with pip
- **Operating System**: Linux, Windows, macOS
- **Dependencies**: See `requirements.txt`

## 📈 Future Enhancements

### Planned Features
- **Multi-camera support** for different angles
- **Recording capabilities** for time-lapse analysis
- **Database logging** of detection results
- **Web interface** for remote monitoring
- **Mobile app integration**
- **Cloud sync** for detection history

### Potential Improvements
- **GPU acceleration** for faster inference
- **Model fine-tuning** for specific environments
- **Custom disease training** for regional diseases
- **Integration with IoT sensors** for environmental data

## 🤝 Contributing
Feel free to submit issues, feature requests, or pull requests to improve the real-time analysis system.

## 📄 License
This system extends the original Hybrid Plant Analysis System and follows the same licensing terms.