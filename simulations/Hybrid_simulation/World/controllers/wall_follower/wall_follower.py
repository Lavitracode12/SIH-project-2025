"""Wall Follower Controller with Hybrid Plant Health Analysis - Based on working keyboard controller"""

from controller import Robot
import cv2
import numpy as np
import torch
from ultralytics import YOLO
from transformers import ViTImageProcessor, ViTForImageClassification
from PIL import Image
import time
import os
import sys
from robot_tracker import RobotTracker

# Add path to hybrid system
sys.path.append("../../Hybrid system/leaf detection")
from hybrid_plant_analyzer import HybridPlantAnalyzer

# ---------------- HYBRID SYSTEM SETUP ----------------
# Override torch.load to disable weights_only for compatibility
original_torch_load = torch.load
def custom_load(*args, **kwargs):
    kwargs['weights_only'] = False
    return original_torch_load(*args, **kwargs)
torch.load = custom_load

# Plant leaf class names for detection (from hybrid system)
PLANT_CLASSES = {
    0: 'alstonia_scholaris', 1: 'arjun', 2: 'bael', 3: 'basil', 4: 'chinar', 
    5: 'guava', 6: 'jamun', 7: 'jatropha', 8: 'lemon', 9: 'mango', 
    10: 'moringa', 11: 'neem', 12: 'oleander', 13: 'parijat', 14: 'peepal', 
    15: 'plumeria', 16: 'pomegranate', 17: 'ashoka', 18: 'jackfruit', 19: 'coconut',
    20: 'betel', 21: 'drumstick', 22: 'lemon_grass', 23: 'senna', 24: 'rose_apple',
    25: 'curry', 26: 'cherry', 27: 'amla', 28: 'banana', 29: 'tea',
    30: 'mint', 31: 'ficus', 32: 'camphor', 33: 'bamboo', 34: 'rubber',
    35: 'eucalyptus', 36: 'papaya', 37: 'hibiscus', 38: 'cotton', 39: 'pomelo',
    40: 'indian_mustard', 41: 'tulsi', 42: 'tamarind', 43: 'castor', 44: 'insulin',
    45: 'cardamom', 46: 'unknown'
}

# Initialize hybrid plant analyzer
hybrid_analyzer = None
detection_enabled = True

def ensure_detection_compatibility(detections):
    """Ensure detection results are compatible with robot tracker"""
    if not detections:
        return detections
    
    # Convert hybrid format to tracker-compatible format if needed
    compatible_detections = []
    for det in detections:
        if 'species' in det and 'plant' not in det:
            # Add 'plant' key for backward compatibility
            det['plant'] = det['species']
        compatible_detections.append(det)
    
    return compatible_detections

def init_hybrid_system():
    """Initialize the hybrid plant health analysis system"""
    global hybrid_analyzer, detection_enabled
    try:
        print("Loading hybrid plant health analysis system...")
        # Initialize with correct paths for the controller directory
        leaf_model_path = "../../Hybrid system/leaf detection/plant_leaf_model.pt"
        disease_models_dir = "../../Hybrid system/Disease detection/local_models"
        
        hybrid_analyzer = HybridPlantAnalyzer(
            leaf_model_path=leaf_model_path,
            disease_models_dir=disease_models_dir
        )
        
        if hybrid_analyzer.is_ready():
            print("✅ Hybrid plant health analysis system loaded successfully!")
            print("🌿 Leaf detection: 47 plant species")
            print("🏥 Disease detection: 13 disease types")
            return True
        else:
            print("❌ Failed to initialize hybrid system models")
            print("Continuing without plant health analysis...")
            detection_enabled = False
            return False
    except Exception as e:
        print(f"❌ Error loading hybrid system: {e}")
        print("Continuing without plant health analysis...")
        detection_enabled = False
        return False

def process_camera_image():
    """Convert Webots camera image to OpenCV format - optimized for speed"""
    try:
        # Get camera image
        image = camera.getImage()
        if image is None:
            return None
            
        # Get camera dimensions
        width = camera.getWidth()
        height = camera.getHeight()
        
        # Convert from Webots format to OpenCV format
        # Webots uses BGRA format, OpenCV uses BGR
        image_array = np.frombuffer(image, np.uint8).reshape((height, width, 4))
        
        # Convert BGRA to BGR (remove alpha channel)
        bgr_image = cv2.cvtColor(image_array, cv2.COLOR_BGRA2BGR)
        
        # Resize to a reasonable size for display and processing
        # Smaller size = faster processing
        display_width = 640  # Reduced from 800
        display_height = int(height * display_width / width)
        resized_image = cv2.resize(bgr_image, (display_width, display_height))
        
        return resized_image
    except Exception as e:
        return None

def detect_plants_with_health_analysis(current_step):
    """Run hybrid plant health analysis with visual display - real-time disease detection"""
    global hybrid_analyzer, detection_enabled, window_created, WINDOW_NAME
    
    if not detection_enabled or hybrid_analyzer is None:
        return []
    
    try:
        # Get processed camera image
        frame = process_camera_image()
        if frame is None:
            return []
        
        # Check if frame is valid (not blank/white)
        if frame.shape[0] < 10 or frame.shape[1] < 10:
            return []
            
        # Create a copy for visualization
        display_frame = frame.copy()
        
        # Check mean intensity quietly (no print statements during simulation)
        mean_intensity = np.mean(frame)
        
        # Run hybrid analysis only if image seems valid
        detections = []
        if mean_intensity > 5 and mean_intensity < 250:
            # Convert OpenCV frame to PIL Image for hybrid analyzer
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(frame_rgb)
            
            # Step 1: Detect leaves using YOLO
            leaf_detections = hybrid_analyzer.detect_leaves(pil_image, confidence=0.10)
            
            for i, leaf_detection in enumerate(leaf_detections):
                # Extract leaf information
                species = leaf_detection['species']
                species_conf = leaf_detection['confidence']
                bbox = leaf_detection['bbox']
                
                # Step 2: Crop leaf region for disease analysis
                leaf_crop = hybrid_analyzer.crop_leaf_region(frame, bbox, padding=8)
                
                if leaf_crop is not None:
                    # Step 3: Classify leaf health
                    health_result = hybrid_analyzer.classify_leaf_health(leaf_crop, min_confidence=0.40)
                    
                    # Prepare detection result
                    detection = {
                        'species': species,
                        'species_confidence': species_conf,
                        'bbox': bbox,
                        'health_status': 'Unknown',
                        'disease': 'Unknown',
                        'health_confidence': 0.0,
                        'is_healthy': None
                    }
                    
                    # Update with health information if available
                    if health_result and health_result['disease'] != 'Invalid':
                        detection.update({
                            'health_status': health_result['health_status'],
                            'disease': health_result['disease'],
                            'health_confidence': health_result['confidence'],
                            'is_healthy': health_result['is_healthy']
                        })
                    
                    detections.append(detection)
                    
                    # Draw bounding box on display frame
                    x1, y1, x2, y2 = map(int, bbox)
                    
                    # Choose color based on health status
                    if detection['is_healthy'] is True:
                        color = (0, 255, 0)  # Green for healthy
                        status_text = "HEALTHY"
                    elif detection['is_healthy'] is False:
                        color = (0, 0, 255)  # Red for diseased
                        status_text = "DISEASED"
                    else:
                        color = (0, 255, 255)  # Yellow for unknown/low confidence
                        status_text = "ANALYZING"
                    
                    # Draw bounding box
                    cv2.rectangle(display_frame, (x1, y1), (x2, y2), color, 2)
                    
                    # Prepare label text
                    species_display = species.replace('_', ' ').title()
                    
                    # Create label with health information
                    if detection['is_healthy'] is not None:
                        label_line1 = f"{species_display}"
                        label_line2 = f"{status_text}: {detection['disease'].split('___')[-1]}"
                        label_line3 = f"Conf: {detection['health_confidence']:.2f}"
                    else:
                        label_line1 = f"{species_display}"
                        label_line2 = f"Species: {species_conf:.2f}"
                        label_line3 = "Health: Analyzing..."
                    
                    # Draw label background
                    label_height = 60
                    cv2.rectangle(display_frame, (x1, y1 - label_height), (x1 + 200, y1), color, -1)
                    
                    # Draw text labels
                    cv2.putText(display_frame, label_line1, 
                               (x1 + 5, y1 - 45), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                    cv2.putText(display_frame, label_line2, 
                               (x1 + 5, y1 - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
                    cv2.putText(display_frame, label_line3, 
                               (x1 + 5, y1 - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
        
        # Enhanced information overlay
        cv2.rectangle(display_frame, (5, 5), (400, 100), (0, 0, 0), -1)
        cv2.putText(display_frame, f"🌿 Plants: {len(detections)} | Step: {current_step}", 
                   (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        # Count health status
        healthy_count = sum(1 for d in detections if d['is_healthy'] is True)
        diseased_count = sum(1 for d in detections if d['is_healthy'] is False)
        unknown_count = len(detections) - healthy_count - diseased_count
        
        cv2.putText(display_frame, f"✅ Healthy: {healthy_count} | ⚠️ Diseased: {diseased_count} | 🔍 Analyzing: {unknown_count}", 
                   (10, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(display_frame, f"Frame: {display_frame.shape[1]}x{display_frame.shape[0]} | Press 'q' to close, 's' to save", 
                   (10, 65), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
        cv2.putText(display_frame, "🌿 Hybrid Plant Health Analysis - Real-time Disease Detection", 
                   (10, 85), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 255), 1)
        
        # Create window only once
        if not window_created:
            cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
            cv2.resizeWindow(WINDOW_NAME, 800, 600)  # Larger window for detailed health info
            window_created = True
        
        # Update the existing window with new frame
        cv2.imshow(WINDOW_NAME, display_frame)
        
        # Non-blocking key check
        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):
            save_detection_screenshot(display_frame, current_step, detections)
        elif key == ord('q'):
            cv2.destroyWindow(WINDOW_NAME)
            window_created = False
            return []
        
        return detections
    
    except Exception as e:
        # Silent error handling during simulation - print errors for debugging
        print(f"⚠️ Detection error at step {current_step}: {e}")
        return []

def print_health_analysis_results(detections, step_count):
    """Print hybrid health analysis results in a formatted way with health tracking"""
    global plant_database, total_detections, detection_count
    
    if not detections:
        return
    
    detection_count += 1
    total_detections += len(detections)
    
    print(f"\n🌿🏥 HYBRID PLANT HEALTH ANALYSIS #{detection_count} - Step {step_count}")
    print(f"📍 Found {len(detections)} plant(s) with health analysis:")
    
    healthy_plants = []
    diseased_plants = []
    analyzing_plants = []
    
    for i, det in enumerate(detections, 1):
        species_name = det['species'].replace('_', ' ').title()
        species_conf = det['species_confidence']
        health_status = det['health_status']
        disease = det['disease']
        health_conf = det['health_confidence']
        
        print(f"  {i}. {species_name} (species conf: {species_conf:.2f})")
        
        if det['is_healthy'] is True:
            print(f"     ✅ HEALTHY - {disease} (conf: {health_conf:.2f})")
            healthy_plants.append(species_name)
        elif det['is_healthy'] is False:
            print(f"     ⚠️ DISEASED - {disease} (conf: {health_conf:.2f})")
            diseased_plants.append(species_name)
        else:
            print(f"     🔍 ANALYZING - Low confidence or processing")
            analyzing_plants.append(species_name)
        
        # Update plant database with health information
        plant_key = det['species']
        if plant_key in plant_database:
            plant_database[plant_key]['count'] += 1
            plant_database[plant_key]['last_seen'] = step_count
            plant_database[plant_key]['total_confidence'] += species_conf
            # Add health tracking
            if det['is_healthy'] is not None:
                if 'health_data' not in plant_database[plant_key]:
                    plant_database[plant_key]['health_data'] = {'healthy': 0, 'diseased': 0}
                if det['is_healthy']:
                    plant_database[plant_key]['health_data']['healthy'] += 1
                else:
                    plant_database[plant_key]['health_data']['diseased'] += 1
        else:
            health_data = {'healthy': 0, 'diseased': 0}
            if det['is_healthy'] is True:
                health_data['healthy'] = 1
            elif det['is_healthy'] is False:
                health_data['diseased'] = 1
                
            plant_database[plant_key] = {
                'count': 1,
                'first_seen': step_count,
                'last_seen': step_count,
                'total_confidence': species_conf,
                'name': species_name,
                'health_data': health_data
            }
    
    # Show health summary
    if healthy_plants or diseased_plants:
        print(f"  🏥 Health Summary: ✅ {len(healthy_plants)} healthy, ⚠️ {len(diseased_plants)} diseased, 🔍 {len(analyzing_plants)} analyzing")
    
    # Show running statistics every 3 detections (more frequent for health data)
    if detection_count % 3 == 0:
        print(f"\n📊 PLANT HEALTH JOURNEY SUMMARY (Analysis #{detection_count}):")
        print(f"🔢 Total plants analyzed: {total_detections}")
        print(f"🌱 Unique species found: {len(plant_database)}")
        
        # Calculate overall health statistics
        total_healthy = sum(data.get('health_data', {}).get('healthy', 0) for data in plant_database.values())
        total_diseased = sum(data.get('health_data', {}).get('diseased', 0) for data in plant_database.values())
        total_health_analyzed = total_healthy + total_diseased
        
        if total_health_analyzed > 0:
            health_ratio = (total_healthy / total_health_analyzed) * 100
            print(f"🏥 Overall Health: {total_healthy} healthy, {total_diseased} diseased ({health_ratio:.1f}% healthy)")
        
        # Show top 3 most common plants with health data
        sorted_plants = sorted(plant_database.items(), 
                             key=lambda x: x[1]['count'], 
                             reverse=True)
        
        print(f"🏆 Most detected plants:")
        for i, (plant_key, data) in enumerate(sorted_plants[:3], 1):
            avg_conf = data['total_confidence'] / data['count']
            health_info = data.get('health_data', {'healthy': 0, 'diseased': 0})
            total_health_checks = health_info['healthy'] + health_info['diseased']
            health_status = ""
            if total_health_checks > 0:
                health_pct = (health_info['healthy'] / total_health_checks) * 100
                health_status = f" (Health: {health_pct:.0f}% healthy)"
            print(f"  {i}. {data['name']}: {data['count']}x (avg conf: {avg_conf:.2f}){health_status}")
    
    print("=" * 70)

def show_final_plant_health_summary():
    """Show complete plant health analysis summary"""
    global plant_database, total_detections, detection_count
    
    print(f"\n🌿🏥 FINAL PLANT HEALTH ANALYSIS SUMMARY 🏥🌿")
    print(f"=" * 70)
    print(f"🔢 Total health analysis scans: {detection_count}")
    print(f"📱 Total plants analyzed: {total_detections}")
    print(f"🌱 Unique species identified: {len(plant_database)}")
    
    # Calculate overall health statistics
    total_healthy = sum(data.get('health_data', {}).get('healthy', 0) for data in plant_database.values())
    total_diseased = sum(data.get('health_data', {}).get('diseased', 0) for data in plant_database.values())
    total_health_analyzed = total_healthy + total_diseased
    
    if total_health_analyzed > 0:
        health_ratio = (total_healthy / total_health_analyzed) * 100
        print(f"🏥 OVERALL PLANT HEALTH: {total_healthy} healthy, {total_diseased} diseased")
        print(f"📊 Health Ratio: {health_ratio:.1f}% healthy plants")
        
        if health_ratio >= 80:
            print("🌟 EXCELLENT overall plant health!")
        elif health_ratio >= 60:
            print("👍 GOOD overall plant health")
        elif health_ratio >= 40:
            print("⚠️ MODERATE plant health - some issues detected")
        else:
            print("🚨 POOR overall plant health - attention needed!")
    
    if plant_database:
        print(f"\n📋 COMPLETE PLANT HEALTH CATALOG:")
        sorted_plants = sorted(plant_database.items(), 
                             key=lambda x: x[1]['count'], 
                             reverse=True)
        
        for i, (plant_key, data) in enumerate(sorted_plants, 1):
            avg_conf = data['total_confidence'] / data['count']
            health_info = data.get('health_data', {'healthy': 0, 'diseased': 0})
            total_health_checks = health_info['healthy'] + health_info['diseased']
            
            health_status_str = "No health data"
            if total_health_checks > 0:
                health_pct = (health_info['healthy'] / total_health_checks) * 100
                health_status_str = f"{health_pct:.0f}% healthy ({health_info['healthy']}✅/{health_info['diseased']}⚠️)"
            
            print(f"  {i:2d}. {data['name']:<20} | Count: {data['count']:3d} | Avg Confidence: {avg_conf:.2f}")
            print(f"      Health: {health_status_str}")
            print(f"      First seen: Step {data['first_seen']:<6} | Last seen: Step {data['last_seen']}")
    
    print(f"=" * 70)

def close_detection_window():
    """Close the OpenCV detection window"""
    try:
        cv2.destroyAllWindows()
        print("🖼️ Detection window closed.")
    except:
        pass

def save_detection_screenshot(frame, step_count, detections):
    """Save a screenshot of current detection"""
    try:
        filename = f"detection_screenshot.jpg"  # Fixed filename - always overwrites previous
        cv2.imwrite(filename, frame)
        print(f"📸 Screenshot saved: {filename} ({len(detections)} plants)")
        return filename
    except Exception as e:
        print(f"❌ Error saving screenshot: {e}")
        return None

# ---------------- ROBOT INIT ----------------
robot = Robot()
timestep = int(robot.getBasicTimeStep())

# ---------------- MOTORS ----------------
motor_names = [
    "rotational motor1", "rotational motor2", "rotational motor3",  # Right motors
    "rotational motor4", "rotational motor5", "rotational motor6"   # Left motors
]

motors = []
for name in motor_names:
    m = robot.getDevice(name)
    m.setPosition(float('inf'))  # velocity control
    m.setVelocity(0.0)
    motors.append(m)

# Motor configuration from working keyboard controller
LEFT_FORWARD_SIGN = -1
RIGHT_FORWARD_SIGN = -1
MAX_SPEED = 6.28  # Increased speed to ensure robot movement

def set_motor_speeds(left_speed, right_speed):
    """Set motor speeds using the proven working configuration"""
    # Right motors (indices 0,1,2 = motors 1,2,3)
    for i in range(3):
        motors[i].setVelocity(RIGHT_FORWARD_SIGN * right_speed)
    # Left motors (indices 3,4,5 = motors 4,5,6)
    for i in range(3, 6):
        motors[i].setVelocity(LEFT_FORWARD_SIGN * left_speed)

def set_arm_speeds(base_speed, down_speed, up_speed):
    """Control 3-axis arm motors - from keyboard controller"""
    arm_base.setVelocity(ARM_DIRECTION_SIGN * base_speed)  # Apply direction correction
    arm_down.setVelocity(down_speed)
    arm_up.setVelocity(up_speed)

def get_arm_base_speed(step_count):
    """Calculate autonomous arm base movement (continuous left-right sweep)"""
    # Total cycle = pause_left + move_right + pause_right + move_left
    total_cycle = ARM_PAUSE_PERIOD + ARM_SWEEP_PERIOD // 2 + ARM_PAUSE_PERIOD + ARM_SWEEP_PERIOD // 2
    cycle_position = step_count % total_cycle
    
    phase1_end = ARM_PAUSE_PERIOD                          # Pause left: 0-99
    phase2_end = phase1_end + ARM_SWEEP_PERIOD // 2        # Move right: 100-249  
    phase3_end = phase2_end + ARM_PAUSE_PERIOD             # Pause right: 250-349
    phase4_end = phase3_end + ARM_SWEEP_PERIOD // 2        # Move left: 350-499
    
    if cycle_position < phase1_end:
        # Phase 1: Pause at left position
        return 0.0
    elif cycle_position < phase2_end:
        # Phase 2: Move right
        return ARM_SPEED
    elif cycle_position < phase3_end:
        # Phase 3: Pause at right position
        return 0.0
    else:
        # Phase 4: Move left
        return -ARM_SPEED

# ---------------- ARM MOTORS ----------------
# Base rotation motor (Z-axis) - from keyboard controller
arm_base = robot.getDevice("rotational motor base")
arm_base.setPosition(float('inf'))  # velocity control
arm_base.setVelocity(0.0)

# Lower arm joint (Y-axis)
arm_down = robot.getDevice("rotational motor down")
arm_down.setPosition(float('inf'))  # velocity control
arm_down.setVelocity(0.0)

# Upper arm joint (Y-axis)
arm_up = robot.getDevice("rotational motor up")
arm_up.setPosition(float('inf'))  # velocity control
arm_up.setVelocity(0.0)

# ---------------- CAMERA ----------------
camera = robot.getDevice("arm_camera")
camera.enable(timestep)  # Activate camera

# Wait a few simulation steps for camera to initialize
print("📹 Initializing camera...")
for i in range(5):
    robot.step(timestep)
    
# Check camera properties
print(f"📹 Camera info: {camera.getWidth()}x{camera.getHeight()}, FOV: {camera.getFov()}")

# ---------------- SENSORS ----------------
ds_right = robot.getDevice("distance sensor right")
ds_left = robot.getDevice("distance sensor left")
ds_right.enable(timestep)
ds_left.enable(timestep)

# ---------------- WALL FOLLOWING PARAMETERS ----------------
TARGET_DISTANCE = 15.0      # Safer distance from walls
Kp = 0.8                     # Higher proportional gain for better response
FRONT_THRESHOLD = 25.0       # Earlier front obstacle detection
JUNCTION_THRESHOLD = 80.0    # Open junction detection
TURN_SPEED_FACTOR = 0.6      # Speed factor for turns
DEADZONE = 1.0               # Smaller deadzone for better control

# ---------------- ARM PARAMETERS ----------------
ARM_SPEED = 0.2              # Slow arm movement for image recognition
ARM_SWEEP_PERIOD = 600       # Longer period for complete left-right sweep
ARM_PAUSE_PERIOD = 0       # Longer pause at each end for image processing
ARM_DIRECTION_SIGN = 1       # Changed to 1 for anti-clockwise rotation

# ---------------- MAIN LOOP ----------------
print("Wall Follower Controller with Leaf Detection Started!")
print(f"Target distance: {TARGET_DISTANCE}")
print(f"Junction threshold: {JUNCTION_THRESHOLD}")
print(f"Arm sweep period: {ARM_SWEEP_PERIOD} steps")

# Initialize hybrid plant health analysis system
print("\n🤖 Initializing hybrid plant health analysis system...")
init_hybrid_system()

# Initialize OpenCV window once
window_created = False
WINDOW_NAME = '🌿🏥 Robot Plant Health Analysis - Live Feed 🤖'

# Initialize robot coordinate tracker
tracker = RobotTracker("robot_coordinates.json")
print("📍 Robot coordinate tracking initialized")

if detection_enabled:
    print("🖼️ Visual Health Analysis Window Controls:")
    print("   - Press 's' to save screenshot")
    print("   - Press 'q' to close detection window")
    print("   - Bounding box colors: 🟢 Green=Healthy, 🔴 Red=Diseased, 🟡 Yellow=Analyzing")
    print("   - Real-time disease classification with confidence scores")

# Plant tracking database
plant_database = {}  # Dictionary to store all detected plants
total_detections = 0
detection_count = 0

# Simulation configuration
test_steps = 0
last_detection_step = 0
DETECTION_INTERVAL = 5  # Increased interval for disease analysis: Run every 5 steps instead of 8

# Stopping conditions - simulation will auto-stop after:
MAX_RUNTIME = 300       # Increased runtime for health analysis (5 minutes)

import time
start_time = time.time()

print(f"🚀 Starting hybrid plant health analysis simulation:")
print(f"   ⏱️  Max runtime: {MAX_RUNTIME}s")
print(f"   🔍 Analysis interval: every {DETECTION_INTERVAL} steps")
print(f"   � YOLO leaf detection + 🏥 ViT disease classification")
print(f"   �🎯 Will auto-generate health analysis graphs when stopped!")

while robot.step(timestep) != -1:
    test_steps += 1
    
    # Check stopping conditions
    current_time = time.time()
    runtime = current_time - start_time
    current_distance = tracker.total_distance
    
    if (runtime >= MAX_RUNTIME):
        
        print(f"\n🛑 AUTO-STOPPING SIMULATION:")
        print(f"   📊 Steps: {test_steps}")
        print(f"   📏 Distance: {current_distance:.2f}m")
        print(f"   ⏱️  Runtime: {runtime:.1f}/{MAX_RUNTIME}s")
        print(f"   🎯 Generating final analysis graphs...")
        break
    
    # Calculate autonomous arm base movement
    arm_base_speed = get_arm_base_speed(test_steps)
    
    # Continuous hybrid plant health analysis (every DETECTION_INTERVAL steps)
    if (detection_enabled and test_steps - last_detection_step >= DETECTION_INTERVAL):
        
        # Run hybrid analysis with health detection
        detections = detect_plants_with_health_analysis(test_steps)
        
        # Ensure compatibility with robot tracker
        detections = ensure_detection_compatibility(detections)
        
        if detections:
            print_health_analysis_results(detections, test_steps)
        # Reduced frequent "no plants detected" messages for cleaner output
        
        last_detection_step = test_steps
    
    if test_steps <= 50:
        # Simple forward test
        set_motor_speeds(MAX_SPEED, MAX_SPEED)
        set_arm_speeds(arm_base_speed, 0.0, 0.0)  # Only move base during test
        if test_steps % 10 == 0:
            arm_status = "Left" if arm_base_speed < 0 else "Right" if arm_base_speed > 0 else "Paused"
            print(f"FORWARD TEST: Step {test_steps}, Arm: {arm_status}")
        
        # Add coordinate tracking for forward test (with default sensor values)
        if test_steps % 5 == 0:
            # Ensure detections variable exists for forward test
            current_detections = detections if 'detections' in locals() and detections else None
            tracker.add_coordinate(test_steps, 50.0, 50.0, MAX_SPEED, MAX_SPEED, current_detections)
        continue
    test_steps += 1
    
    # Calculate autonomous arm base movement
    arm_base_speed = get_arm_base_speed(test_steps)
    
    if test_steps <= 50:
        # Simple forward test
        set_motor_speeds(MAX_SPEED, MAX_SPEED)
        set_arm_speeds(arm_base_speed, 0.0, 0.0)  # Only move base during test
        if test_steps % 10 == 0:
            arm_status = "Left" if arm_base_speed < 0 else "Right" if arm_base_speed > 0 else "Paused"
            print(f"FORWARD TEST: Step {test_steps}, Arm: {arm_status}")
        continue
    
    # Read sensors
    r_val = ds_right.getValue()
    l_val = ds_left.getValue()
    
    # Debug: Print sensor values and arm status every 10 steps for better tracking
    if test_steps % 10 == 0:
        total_cycle = ARM_PAUSE_PERIOD + ARM_SWEEP_PERIOD // 2 + ARM_PAUSE_PERIOD + ARM_SWEEP_PERIOD // 2
        cycle_pos = test_steps % total_cycle
        actual_motor_speed = ARM_DIRECTION_SIGN * arm_base_speed
        
        # Determine phase
        phase1_end = ARM_PAUSE_PERIOD
        phase2_end = phase1_end + ARM_SWEEP_PERIOD // 2
        phase3_end = phase2_end + ARM_PAUSE_PERIOD
        
        if cycle_pos < phase1_end:
            phase = "Phase 1: Pause Left"
        elif cycle_pos < phase2_end:
            phase = "Phase 2: Move Right"
        elif cycle_pos < phase3_end:
            phase = "Phase 3: Pause Right"
        else:
            phase = "Phase 4: Move Left"
            
        arm_status = "⬅️ Left" if arm_base_speed < 0 else "➡️ Right" if arm_base_speed > 0 else "⏸️ Paused"
        print(f"Step {test_steps} | {phase} | Arm: {arm_status} (Motor: {actual_motor_speed:.1f}) | Cycle: {cycle_pos}/{total_cycle}")
    
    # Default forward speeds
    left_speed = MAX_SPEED
    right_speed = MAX_SPEED
    
    # Check for junctions (open spaces)
    right_junction = r_val > JUNCTION_THRESHOLD
    left_junction = l_val > JUNCTION_THRESHOLD
    
    # PRIORITY 1: Junction handling
    if right_junction and not left_junction:
        # Right junction - turn right using hard turn from keyboard controller
        left_speed = -MAX_SPEED * TURN_SPEED_FACTOR
        right_speed = MAX_SPEED * TURN_SPEED_FACTOR
        print(f"RIGHT JUNCTION: Turning right (L={l_val:.1f}, R={r_val:.1f})")
        
    elif left_junction and not right_junction:
        # Left junction - turn left using hard turn from keyboard controller
        left_speed = MAX_SPEED * TURN_SPEED_FACTOR
        right_speed = -MAX_SPEED * TURN_SPEED_FACTOR
        print(f"LEFT JUNCTION: Turning left (L={l_val:.1f}, R={r_val:.1f})")
        
    elif right_junction and left_junction:
        # Both sides open - continue straight
        left_speed = MAX_SPEED
        right_speed = MAX_SPEED
        print(f"OPEN AREA: Moving straight (L={l_val:.1f}, R={r_val:.1f})")
    
    # PRIORITY 2: Front obstacle avoidance (improved thresholds)
    elif r_val < FRONT_THRESHOLD or l_val < FRONT_THRESHOLD:
        if r_val < FRONT_THRESHOLD and l_val < FRONT_THRESHOLD:
            # Front obstacle - execute U-turn
            left_speed = -MAX_SPEED * 0.7
            right_speed = MAX_SPEED * 0.7
            print(f"FRONT OBSTACLE: U-turn (L={l_val:.1f}, R={r_val:.1f})")
        elif r_val < FRONT_THRESHOLD:
            # Front-right obstacle - turn left
            left_speed = MAX_SPEED * 0.7
            right_speed = -MAX_SPEED * 0.7
            print(f"FRONT-RIGHT OBSTACLE: Turn left (L={l_val:.1f}, R={r_val:.1f})")
        elif l_val < FRONT_THRESHOLD:
            # Front-left obstacle - turn right
            left_speed = -MAX_SPEED * 0.7
            right_speed = MAX_SPEED * 0.7
            print(f"FRONT-LEFT OBSTACLE: Turn right (L={l_val:.1f}, R={r_val:.1f})")
    
    # PRIORITY 3: Normal wall following
    else:
        # Calculate wall following error
        error_right = TARGET_DISTANCE - r_val
        error_left = l_val - TARGET_DISTANCE
        error = error_right - error_left  # positive = steer right
        
        if abs(error) > DEADZONE:
            # Apply proportional correction
            correction = Kp * error
            left_speed = MAX_SPEED + correction
            right_speed = MAX_SPEED - correction
            
            # Clamp speeds to reasonable range
            left_speed = max(0.2 * MAX_SPEED, min(MAX_SPEED, left_speed))
            right_speed = max(0.2 * MAX_SPEED, min(MAX_SPEED, right_speed))
            
            print(f"WALL FOLLOW: Error={error:.1f}, L_speed={left_speed:.1f}, R_speed={right_speed:.1f}")
        else:
            # Within deadzone - go straight
            left_speed = MAX_SPEED
            right_speed = MAX_SPEED
            print(f"STRAIGHT: L={l_val:.1f}, R={r_val:.1f}")
    
    # Apply motor speeds
    set_motor_speeds(left_speed, right_speed)
    
    # Apply autonomous arm movement (continuous left-right sweep)
    set_arm_speeds(arm_base_speed, 0.0, 0.0)  # Only base movement, other joints stationary
    
    # Add coordinate tracking every 5 steps for detailed path mapping
    if test_steps % 5 == 0:
        # Ensure detections variable exists and handle both detection formats
        current_detections = detections if 'detections' in locals() and detections else None
        tracker.add_coordinate(test_steps, l_val, r_val, left_speed, right_speed, current_detections)
    
    # Save coordinates every 50 steps
    if test_steps % 50 == 0:
        tracker.save_coordinates()
        
        # Progress indicator every 100 steps
        if test_steps % 100 == 0:
            stats = tracker.get_statistics()
            progress_time = (runtime / MAX_RUNTIME) * 100
            print(f"📍 PROGRESS - Step {test_steps}: Distance {stats['total_distance']:.2f}m, "
                  f"Plants: {stats['plant_detections']}, "
                  f"Time Progress: {progress_time:.1f}%")

# Cleanup when simulation ends
if window_created:
    cv2.destroyWindow(WINDOW_NAME)
    print("🖼️ Detection window closed on exit")

# Save final coordinates and generate analysis graphs
print("\n📊 Generating final analysis graphs...")
tracker.save_coordinates()

# Generate comprehensive analysis
try:
    print("📈 Creating distance and movement graphs...")
    tracker.plot_distance_graph(save_image=True)
    
    print("🌿 Creating plant detection map...")
    tracker.plot_plant_detection_map()
    
    # Print final statistics
    stats = tracker.get_statistics()
    print("\n🎯 FINAL ROBOT MISSION STATISTICS:")
    print("=" * 50)
    print(f"   🚀 Total distance traveled: {stats['total_distance']:.2f} meters")
    print(f"   📍 Total coordinate points: {stats['total_points']}")
    print(f"   ⏱️  Mission duration: {stats['session_duration_steps']} steps")
    print(f"   📏 Average speed: {stats['average_speed']:.3f} m/step")
    print(f"   🌿 Total plants detected: {stats['plant_detections']}")
    print(f"   📍 Detection locations: {stats['detection_locations']}")
    print("=" * 50)
    print("📊 Analysis graphs saved as PNG files!")
    
except Exception as e:
    print(f"⚠️ Error generating graphs: {e}")
    print("📍 Coordinate data still saved in JSON file")

# Show final plant health summary if any detections were made
if detection_count > 0:
    show_final_plant_health_summary()
else:
    print("🌿 No plants were detected during this session.")

