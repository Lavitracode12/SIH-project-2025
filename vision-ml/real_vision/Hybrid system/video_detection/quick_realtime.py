#!/usr/bin/env python3
"""
Quick Real-Time Plant Analysis Launcher
Simple interface for starting webcam-based plant analysis
"""

import sys
import os
from realtime_hybrid_analyzer import RealTimeHybridAnalyzer

def main():
    """Main function with command line arguments"""
    camera_id = 0  # Default to built-in camera
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] in ['-h', '--help']:
            print("🔬 Real-Time Hybrid Plant Analysis Launcher")
            print("Usage: python3 quick_realtime.py [camera_id]")
            print("")
            print("Arguments:")
            print("  camera_id   Camera device ID (default: 0)")
            print("              0 = Built-in webcam")
            print("              1 = External USB webcam")
            print("")
            print("Examples:")
            print("  python3 quick_realtime.py     # Use built-in camera")
            print("  python3 quick_realtime.py 1   # Use external camera")
            print("")
            print("Controls during analysis:")
            print("  [SPACE] - Pause/Resume analysis")
            print("  [S] - Save snapshot")
            print("  [UP/DOWN] - Adjust leaf detection confidence")
            print("  [LEFT/RIGHT] - Adjust disease detection confidence")
            print("  [Q] - Quit")
            return
        
        try:
            camera_id = int(sys.argv[1])
        except ValueError:
            print(f"⚠️  Invalid camera ID: {sys.argv[1]}, using default: 0")
    
    # Check if models are available
    leaf_model = "../leaf detection/plant_leaf_model.pt"
    disease_models = "../Disease detection/local_models"
    
    if not os.path.exists(leaf_model):
        print(f"❌ Leaf detection model not found: {leaf_model}")
        print("Please make sure you're running from the video_detection directory")
        print("and the hybrid system models are available.")
        return
    
    if not os.path.exists(disease_models):
        print(f"❌ Disease detection models not found: {disease_models}")
        print("Please make sure the hybrid system models are available.")
        return
    
    print("✅ All models found, starting real-time analysis...")
    print(f"📹 Using camera: {camera_id}")
    
    # Create and run analyzer
    analyzer = RealTimeHybridAnalyzer(
        camera_id=camera_id,
        frame_width=640,
        frame_height=480,
        window_width=1280,  # Large display window
        window_height=720
    )
    
    success = analyzer.run()
    
    if success:
        print("\n🎉 Real-time analysis session completed!")
    else:
        print("\n❌ Real-time analysis failed!")
        print("💡 Try:")
        print("   - Different camera ID (0 for built-in, 1 for external)")
        print("   - Check if camera is being used by another application")
        print("   - Verify camera permissions")

if __name__ == "__main__":
    main()