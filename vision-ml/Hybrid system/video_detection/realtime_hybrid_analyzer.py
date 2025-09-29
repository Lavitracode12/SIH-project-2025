#!/usr/bin/env python3
"""
Real-Time Hybrid Plant Analysis System
Combines webcam capture with leaf detection and disease classification for live analysis
"""

import cv2
import numpy as np
import time
import os
import sys
from collections import deque
from datetime import datetime

# Add parent directory to path to import hybrid analyzer
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'leaf detection'))
from hybrid_plant_analyzer import HybridPlantAnalyzer

class RealTimeHybridAnalyzer:
    """Real-time webcam-based plant analysis system"""
    
    def __init__(self, camera_id=0, frame_width=640, frame_height=480, window_width=1280, window_height=720):
        """Initialize the real-time analyzer
        
        Args:
            camera_id: Camera device ID (0 for default webcam, 1 for external)
            frame_width: Video frame width
            frame_height: Video frame height
            window_width: Display window width (default: 1280)
            window_height: Display window height (default: 720)
        """
        self.camera_id = camera_id
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.window_width = window_width
        self.window_height = window_height
        self.cap = None
        
        # Initialize the hybrid analyzer
        print("🔄 Initializing Hybrid Plant Analysis Models...")
        self.analyzer = HybridPlantAnalyzer(
            leaf_model_path="../leaf detection/plant_leaf_model.pt",
            disease_models_dir="../Disease detection/local_models"
        )
        
        # Analysis settings
        self.leaf_confidence = 0.10
        self.disease_confidence = 0.30
        self.analysis_enabled = True
        self.save_snapshots = False
        
        # Performance tracking
        self.fps_queue = deque(maxlen=30)  # Track last 30 frames for FPS
        self.frame_count = 0
        self.skip_frames = 3  # Process every Nth frame for performance
        
        # Analysis results cache
        self.last_analysis_time = 0
        self.analysis_interval = 1.0  # Analyze every 1 second
        self.current_detections = []
        
        # Display settings
        self.show_fps = True
        self.show_confidence = True
        self.show_health_status = True
        self.show_status_overlay = True  # Toggle for status overlay
        
    def initialize_camera(self):
        """Initialize the webcam capture"""
        print(f"🎥 Initializing camera {self.camera_id}...")
        
        self.cap = cv2.VideoCapture(self.camera_id)
        
        if not self.cap.isOpened():
            print(f"❌ Failed to open camera {self.camera_id}")
            return False
        
        # Set camera properties
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.frame_width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.frame_height)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        
        # Get actual camera properties
        actual_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        actual_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        actual_fps = self.cap.get(cv2.CAP_PROP_FPS)
        
        print(f"✅ Camera initialized: {actual_width}x{actual_height} @ {actual_fps:.1f}fps")
        
        return True
    
    def is_ready(self):
        """Check if the system is ready for analysis"""
        return (self.analyzer.is_ready() and 
                self.cap is not None and 
                self.cap.isOpened())
    
    def process_frame(self, frame):
        """Process a single frame for plant analysis"""
        if not self.analysis_enabled:
            return self.draw_status_overlay(frame, "Analysis Paused")
        
        current_time = time.time()
        
        # Check if it's time for a new analysis
        if (current_time - self.last_analysis_time) >= self.analysis_interval:
            if self.frame_count % self.skip_frames == 0:
                # Perform leaf detection
                detections = self.analyzer.detect_leaves(frame, confidence=self.leaf_confidence)
                
                # Process each detected leaf
                processed_detections = []
                for detection in detections:
                    bbox = detection['bbox']
                    
                    # Crop leaf region
                    leaf_crop = self.analyzer.crop_leaf_region(frame, bbox, padding=10)
                    
                    if leaf_crop is not None:
                        # Classify leaf health
                        health_result = self.analyzer.classify_leaf_health(
                            leaf_crop, 
                            min_confidence=self.disease_confidence
                        )
                        
                        # Combine detection and health results
                        combined_result = {
                            'species': detection['species'],
                            'bbox': bbox,
                            'leaf_confidence': detection['confidence'],
                            'health_result': health_result
                        }
                        processed_detections.append(combined_result)
                
                self.current_detections = processed_detections
                self.last_analysis_time = current_time
        
        # Draw annotations on frame
        annotated_frame = self.draw_annotations(frame, self.current_detections)
        
        return annotated_frame
    
    def draw_annotations(self, frame, detections):
        """Draw bounding boxes and labels on frame"""
        annotated_frame = frame.copy()
        
        for detection in detections:
            bbox = detection['bbox']
            species = detection['species']
            leaf_conf = detection['leaf_confidence']
            health_result = detection['health_result']
            
            # Draw bounding box
            x1, y1, x2, y2 = [int(coord) for coord in bbox]
            
            # Color based on health status
            if health_result and health_result['is_healthy']:
                color = (0, 255, 0)  # Green for healthy
                health_text = f"Healthy ({health_result['confidence']:.2f})"
            elif health_result:
                color = (0, 0, 255)  # Red for diseased
                disease = health_result['disease'].replace('___', ' ')
                health_text = f"{disease} ({health_result['confidence']:.2f})"
            else:
                color = (255, 165, 0)  # Orange for unknown health
                health_text = "Analyzing..."
            
            # Draw bounding box
            cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), color, 2)
            
            # Prepare label text
            species_text = f"{species} ({leaf_conf:.2f})"
            
            # Draw background for text
            label_height = 50 if self.show_health_status else 25
            cv2.rectangle(annotated_frame, (x1, y1 - label_height), (x2, y1), color, -1)
            
            # Draw species text
            cv2.putText(annotated_frame, species_text, (x1 + 5, y1 - 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            # Draw health status if enabled
            if self.show_health_status:
                cv2.putText(annotated_frame, health_text, (x1 + 5, y1 - 10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
        
        # Draw status overlay only if enabled
        if self.show_status_overlay:
            return self.draw_status_overlay(annotated_frame)
        else:
            return annotated_frame
    
    def draw_status_overlay(self, frame, status_message="Real-time Analysis"):
        """Draw status information overlay"""
        overlay_frame = frame.copy()
        
        # Calculate FPS
        current_fps = 0
        if len(self.fps_queue) > 1:
            current_fps = len(self.fps_queue) / (self.fps_queue[-1] - self.fps_queue[0])
        
        # Prepare status text - compact version
        status_lines = [
            f"🌿 {status_message} | Cam:{self.camera_id}",
            f"FPS:{current_fps:.1f} | Det:{len(self.current_detections)} | L:{self.leaf_confidence:.2f} D:{self.disease_confidence:.2f}" if self.show_fps else f"Det:{len(self.current_detections)} | L:{self.leaf_confidence:.2f} D:{self.disease_confidence:.2f}",
            "[SPACE]Pause [S]Save [I]Hide [Q]Quit"
        ]
        
        # Filter out empty lines
        status_lines = [line for line in status_lines if line]
        
        # Draw compact semi-transparent background in top-right corner
        overlay_height = len(status_lines) * 15 + 10
        overlay_width = 400
        frame_height, frame_width = overlay_frame.shape[:2]
        x_start = frame_width - overlay_width - 10
        y_start = 10
        
        cv2.rectangle(overlay_frame, (x_start, y_start), (frame_width - 10, y_start + overlay_height), (0, 0, 0), -1)
        cv2.rectangle(overlay_frame, (x_start, y_start), (frame_width - 10, y_start + overlay_height), (255, 255, 255), 1)
        
        # Draw status text - smaller font
        for i, line in enumerate(status_lines):
            y_pos = y_start + 15 + i * 15
            color = (0, 255, 0) if i == 0 else (255, 255, 255)
            cv2.putText(overlay_frame, line, (x_start + 5, y_pos), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.35, color, 1)
        
        return overlay_frame
    
    def save_snapshot(self, frame):
        """Save current frame as snapshot"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"realtime_snapshot_{timestamp}.jpg"
        
        cv2.imwrite(filename, frame)
        print(f"📸 Snapshot saved: {filename}")
    
    def handle_keyboard_input(self, key):
        """Handle keyboard input for controls"""
        if key == ord('q') or key == ord('Q'):
            return False
        elif key == ord(' '):  # Space bar
            self.analysis_enabled = not self.analysis_enabled
            status = "enabled" if self.analysis_enabled else "disabled"
            print(f"🔄 Analysis {status}")
        elif key == ord('s') or key == ord('S'):
            self.save_snapshots = True
        elif key == ord('c') or key == ord('C'):
            self.show_confidence = not self.show_confidence
            print(f"📊 Confidence display: {self.show_confidence}")
        elif key == ord('h') or key == ord('H'):
            self.show_health_status = not self.show_health_status
            print(f"🏥 Health status display: {self.show_health_status}")
        elif key == ord('f') or key == ord('F'):
            self.show_fps = not self.show_fps
            print(f"⚡ FPS display: {self.show_fps}")
        elif key == ord('i') or key == ord('I'):
            self.show_status_overlay = not self.show_status_overlay
            print(f"📊 Status overlay: {'shown' if self.show_status_overlay else 'hidden'}")
        elif key == 82 or key == 2490368:  # Up arrow
            self.leaf_confidence = min(1.0, self.leaf_confidence + 0.05)
            print(f"🌿 Leaf confidence: {self.leaf_confidence:.2f}")
        elif key == 84 or key == 2621440:  # Down arrow
            self.leaf_confidence = max(0.01, self.leaf_confidence - 0.05)
            print(f"🌿 Leaf confidence: {self.leaf_confidence:.2f}")
        elif key == 83 or key == 2555904:  # Right arrow
            self.disease_confidence = min(1.0, self.disease_confidence + 0.05)
            print(f"🏥 Disease confidence: {self.disease_confidence:.2f}")
        elif key == 81 or key == 2424832:  # Left arrow
            self.disease_confidence = max(0.01, self.disease_confidence - 0.05)
            print(f"🏥 Disease confidence: {self.disease_confidence:.2f}")
        
        return True
    
    def run(self):
        """Main loop for real-time analysis"""
        if not self.analyzer.is_ready():
            print("❌ Hybrid analyzer not ready!")
            return False
        
        if not self.initialize_camera():
            print("❌ Failed to initialize camera!")
            return False
        
        print("\n🎥 Starting real-time hybrid plant analysis...")
        print("📋 Controls:")
        print("   [SPACE] - Pause/Resume analysis")
        print("   [S] - Save snapshot")
        print("   [I] - Hide/Show status overlay")
        print("   [UP/DOWN] - Adjust leaf detection confidence")
        print("   [LEFT/RIGHT] - Adjust disease detection confidence")
        print("   [C] - Toggle confidence display")
        print("   [H] - Toggle health status display")
        print("   [F] - Toggle FPS display")
        print("   [Q] - Quit")
        print("\n🚀 Starting camera feed...")
        
        # Create resizable window with larger size
        window_name = 'Real-Time Hybrid Plant Analysis'
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(window_name, self.window_width, self.window_height)
        
        try:
            while True:
                # Capture frame
                ret, frame = self.cap.read()
                if not ret:
                    print("❌ Failed to capture frame")
                    break
                
                # Process frame
                processed_frame = self.process_frame(frame)
                
                # Save snapshot if requested
                if self.save_snapshots:
                    self.save_snapshot(processed_frame)
                    self.save_snapshots = False
                
                # Display frame
                cv2.imshow(window_name, processed_frame)
                
                # Update FPS tracking
                self.fps_queue.append(time.time())
                self.frame_count += 1
                
                # Handle keyboard input
                key = cv2.waitKey(1) & 0xFF
                if key != 255:  # Key was pressed
                    if not self.handle_keyboard_input(key):
                        break
                
        except KeyboardInterrupt:
            print("\n🛑 Interrupted by user")
        except Exception as e:
            print(f"❌ Error during analysis: {e}")
        finally:
            self.cleanup()
        
        return True
    
    def cleanup(self):
        """Clean up resources"""
        print("\n🧹 Cleaning up...")
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
        print("✅ Cleanup completed")

def main():
    """Main function"""
    print("🌿🔬 Real-Time Hybrid Plant Analysis System")
    print("=" * 50)
    
    # Create analyzer with external webcam (camera_id=1)
    # Change to camera_id=0 for built-in webcam
    analyzer = RealTimeHybridAnalyzer(
        camera_id=1,  # External webcam
        frame_width=640,
        frame_height=480,
        window_width=1280,  # Large display window
        window_height=720
    )
    
    # Run analysis
    success = analyzer.run()
    
    if success:
        print("✅ Real-time analysis completed successfully!")
    else:
        print("❌ Real-time analysis failed!")

if __name__ == "__main__":
    main()
