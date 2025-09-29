#!/bin/bash

# Real-Time Hybrid Plant Analysis System - Launcher
echo "🎥🌿 Real-Time Hybrid Plant Analysis System"
echo "============================================"
echo ""
echo "This system provides live webcam-based plant analysis combining:"
echo "1. 🎯 YOLO Leaf Detection (47 plant species)"
echo "2. 🏥 ViT Disease Classification (13 disease types)"
echo "3. 📹 Real-time video processing"
echo ""

# Check if models are available
echo "📋 System Status:"
if [ -f "../leaf detection/plant_leaf_model.pt" ]; then
    echo "✅ Leaf detection model: Available ($(du -h "../leaf detection/plant_leaf_model.pt" | cut -f1))"
else
    echo "❌ Leaf detection model: Missing"
fi

if [ -d "../Disease detection/local_models" ]; then
    echo "✅ Disease detection models: Available"
else
    echo "❌ Disease detection models: Missing"
fi

# Check camera availability
echo ""
echo "📹 Camera Status:"
if [ -e /dev/video0 ]; then
    echo "✅ Default camera (/dev/video0): Available"
else
    echo "⚠️  Default camera (/dev/video0): Not found"
fi

# List available cameras
camera_count=0
for i in {0..5}; do
    if [ -e "/dev/video$i" ]; then
        echo "📹 Camera $i: Available"
        ((camera_count++))
    fi
done

if [ $camera_count -eq 0 ]; then
    echo "❌ No cameras found!"
    echo "Please connect a webcam and try again."
    exit 1
fi

echo ""
echo "🚀 Available Commands:"
echo "1. python3 quick_realtime.py              - Quick start with default settings"
echo "2. python3 quick_realtime.py 1            - Use camera 1"  
echo "3. python3 quick_realtime.py 0 1280x720   - Use HD resolution"
echo "4. python3 realtime_hybrid_analyzer.py    - Full featured analyzer"
echo ""

echo "⚙️  Real-time Analysis Features:"
echo "🔄 Live leaf detection and species identification"
echo "🏥 Real-time disease classification"
echo "📊 Performance monitoring (FPS, confidence levels)"
echo "📸 Snapshot capture"
echo "🎛️  Interactive controls for confidence adjustment"
echo ""

echo "🎮 Runtime Controls:"
echo "[SPACE] - Pause/Resume analysis"
echo "[S] - Save snapshot of current frame"
echo "[↑/↓] - Adjust leaf detection confidence"
echo "[←/→] - Adjust disease detection confidence"
echo "[C] - Toggle confidence display"
echo "[H] - Toggle health status display"
echo "[F] - Toggle FPS display"
echo "[Q] - Quit application"
echo ""

echo "📁 Output Files:"
snapshots=$(ls realtime_snapshot_* 2>/dev/null | wc -l)
echo "📸 Snapshots: $snapshots files"

echo ""
echo "💡 Tips for Best Results:"
echo "• Ensure good lighting conditions"
echo "• Hold plants steady for 1-2 seconds for analysis"
echo "• Position leaves clearly in frame"
echo "• Avoid rapid camera movements"
echo "• Use 'S' to save interesting detections"
echo ""

# Ask user what they want to do
echo "Select an option:"
echo "1) Quick start (default camera, 640x480)"
echo "2) Quick start with HD resolution (1280x720)"
echo "3) Choose camera and resolution"
echo "4) Full analyzer with all features"
echo "5) Help and documentation"
echo ""

read -p "Enter choice (1-5): " choice

case $choice in
    1)
        echo "🚀 Starting quick analysis with default settings..."
        python3 quick_realtime.py
        ;;
    2)
        echo "🚀 Starting HD analysis..."
        python3 quick_realtime.py 0 1280x720
        ;;
    3)
        echo ""
        read -p "Enter camera ID (0-5): " camera_id
        read -p "Enter resolution (e.g., 640x480, 1280x720): " resolution
        echo "🚀 Starting analysis with camera $camera_id at $resolution..."
        python3 quick_realtime.py $camera_id $resolution
        ;;
    4)
        echo "🚀 Starting full analyzer..."
        python3 realtime_hybrid_analyzer.py
        ;;
    5)
        echo ""
        python3 quick_realtime.py --help
        ;;
    *)
        echo "🚀 Starting default analysis..."
        python3 quick_realtime.py
        ;;
esac

echo ""
echo "✅ Real-time analysis session ended."
echo "📁 Check the current directory for saved snapshots."