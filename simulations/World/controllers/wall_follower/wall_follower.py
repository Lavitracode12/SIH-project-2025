"""Wall Follower Controller with Leaf Detection - Based on working keyboard controller"""

from controller import Robot
import cv2
import numpy as np
import torch
from ultralytics import YOLO
import time
import os
from robot_tracker import RobotTracker

# ---------------- LEAF DETECTION SETUP ----------------
# Override torch.load to disable weights_only for compatibility
original_torch_load = torch.load
def custom_load(*args, **kwargs):
    kwargs['weights_only'] = False
    return original_torch_load(*args, **kwargs)
torch.load = custom_load

# Plant leaf class names for detection
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

# Initialize leaf detection model
leaf_model = None
detection_enabled = True

def init_leaf_detection():
    """Initialize the YOLO leaf detection model"""
    global leaf_model, detection_enabled
    try:
        # Path to the model file relative to the controller directory
        model_path = "../../leaf detection/plant_leaf_model.pt"
        if os.path.exists(model_path):
            print("Loading leaf detection model...")
            leaf_model = YOLO(model_path)
            print("✅ Leaf detection model loaded successfully!")
            return True
        else:
            print(f"❌ Model file not found at: {model_path}")
            print("Continuing without leaf detection...")
            detection_enabled = False
            return False
    except Exception as e:
        print(f"❌ Error loading leaf detection model: {e}")
        print("Continuing without leaf detection...")
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

def detect_leaves_with_display(current_step):
    """Run leaf detection with visual display window - optimized for smooth simulation"""
    global leaf_model, detection_enabled, window_created, WINDOW_NAME
    
    if not detection_enabled or leaf_model is None:
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
        
        # Run YOLO detection only if image seems valid - with optimized settings
        detections = []
        if mean_intensity > 5 and mean_intensity < 250:
            # Use smaller image for faster detection
            small_frame = cv2.resize(frame, (320, 240))  # Smaller for speed
            results = leaf_model.predict(small_frame, conf=0.3, verbose=False, imgsz=320)
            
            if results[0].boxes is not None:
                boxes = results[0].boxes.xyxy.cpu().numpy()
                confidences = results[0].boxes.conf.cpu().numpy()
                classes = results[0].boxes.cls.cpu().numpy()
                
                # Scale boxes back to original frame size
                scale_x = frame.shape[1] / 320
                scale_y = frame.shape[0] / 240
                
                for box, conf, cls in zip(boxes, confidences, classes):
                    class_id = int(cls)
                    plant_name = PLANT_CLASSES.get(class_id, f"Unknown_{class_id}")
                    
                    # Scale bounding box back to original size
                    scaled_box = [
                        box[0] * scale_x, box[1] * scale_y,
                        box[2] * scale_x, box[3] * scale_y
                    ]
                    
                    detection = {
                        'plant': plant_name,
                        'confidence': float(conf),
                        'bbox': scaled_box,
                        'class_id': class_id
                    }
                    detections.append(detection)
                    
                    # Draw bounding box on display frame
                    x1, y1, x2, y2 = map(int, scaled_box)
                    
                    # Choose color based on confidence
                    if conf >= 0.7:
                        color = (0, 255, 0)  # Green for high confidence
                    elif conf >= 0.5:
                        color = (0, 255, 255)  # Yellow for medium confidence
                    else:
                        color = (0, 0, 255)  # Red for low confidence
                    
                    # Draw bounding box
                    cv2.rectangle(display_frame, (x1, y1), (x2, y2), color, 2)
                    
                    # Prepare label text
                    plant_display_name = plant_name.replace('_', ' ').title()
                    label = f"{plant_display_name}: {conf:.2f}"
                    
                    # Draw label background and text (simplified)
                    cv2.putText(display_frame, label, 
                              (x1, y1 - 10), 
                              cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        
        # Simplified information overlay
        cv2.rectangle(display_frame, (5, 5), (350, 80), (0, 0, 0), -1)
        cv2.putText(display_frame, f"Plants: {len(detections)} | Step: {current_step}", 
                   (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        cv2.putText(display_frame, f"Frame: {display_frame.shape[1]}x{display_frame.shape[0]}", 
                   (10, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(display_frame, "Press 'q' to close | 's' to save", 
                   (10, 65), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
        
        # Create window only once
        if not window_created:
            cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
            cv2.resizeWindow(WINDOW_NAME, 640, 480)  # Smaller window for better performance
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
        # Silent error handling during simulation
        return []

def print_detection_results(detections, step_count):
    """Print leaf detection results in a formatted way with database tracking"""
    global plant_database, total_detections, detection_count
    
    if not detections:
        return
    
    detection_count += 1
    total_detections += len(detections)
    
    print(f"\n🌿 CONTINUOUS LEAF DETECTION #{detection_count} - Step {step_count}")
    print(f"📍 Found {len(detections)} plant(s) in current frame:")
    
    for i, det in enumerate(detections, 1):
        plant_name = det['plant'].replace('_', ' ').title()
        confidence = det['confidence']
        print(f"  {i}. {plant_name} (confidence: {confidence:.2f})")
        
        # Update plant database
        plant_key = det['plant']
        if plant_key in plant_database:
            plant_database[plant_key]['count'] += 1
            plant_database[plant_key]['last_seen'] = step_count
            plant_database[plant_key]['total_confidence'] += confidence
        else:
            plant_database[plant_key] = {
                'count': 1,
                'first_seen': step_count,
                'last_seen': step_count,
                'total_confidence': confidence,
                'name': plant_name
            }
    
    # Show running statistics every 5 detections
    if detection_count % 5 == 0:
        print(f"\n📊 PLANT JOURNEY SUMMARY (Detection #{detection_count}):")
        print(f"🔢 Total plants detected: {total_detections}")
        print(f"🌱 Unique species found: {len(plant_database)}")
        
        # Show top 3 most common plants
        sorted_plants = sorted(plant_database.items(), 
                             key=lambda x: x[1]['count'], 
                             reverse=True)
        
        print(f"🏆 Most common plants:")
        for i, (plant_key, data) in enumerate(sorted_plants[:3], 1):
            avg_conf = data['total_confidence'] / data['count']
            print(f"  {i}. {data['name']}: {data['count']}x (avg conf: {avg_conf:.2f})")
    
    print("=" * 60)

def show_final_plant_summary():
    """Show complete plant detection summary"""
    global plant_database, total_detections, detection_count
    
    print(f"\n🌿🤖 FINAL PLANT DETECTION SUMMARY 🤖🌿")
    print(f"=" * 60)
    print(f"🔢 Total detection scans: {detection_count}")
    print(f"📱 Total plants detected: {total_detections}")
    print(f"🌱 Unique species identified: {len(plant_database)}")
    
    if plant_database:
        print(f"\n📋 COMPLETE PLANT CATALOG:")
        sorted_plants = sorted(plant_database.items(), 
                             key=lambda x: x[1]['count'], 
                             reverse=True)
        
        for i, (plant_key, data) in enumerate(sorted_plants, 1):
            avg_conf = data['total_confidence'] / data['count']
            print(f"  {i:2d}. {data['name']:<20} | Count: {data['count']:3d} | Avg Confidence: {avg_conf:.2f}")
            print(f"      First seen: Step {data['first_seen']:<6} | Last seen: Step {data['last_seen']}")
    
    print(f"=" * 60)

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

# Initialize leaf detection system
print("\n🤖 Initializing systems...")
init_leaf_detection()

# Initialize OpenCV window once
window_created = False
WINDOW_NAME = '🌿 Robot Plant Detection - Live Feed 🤖'

# Initialize robot coordinate tracker
tracker = RobotTracker("robot_coordinates.json")
print("📍 Robot coordinate tracking initialized")

if detection_enabled:
    print("🖼️ Visual Detection Window Controls:")
    print("   - Press 's' to save screenshot")
    print("   - Press 'q' to close detection window")
    print("   - Bounding box colors: Green=High confidence, Yellow=Medium, Red=Low")

# Plant tracking database
plant_database = {}  # Dictionary to store all detected plants
total_detections = 0
detection_count = 0

# Simulation configuration
test_steps = 0
last_detection_step = 0
DETECTION_INTERVAL = 5  # Reduced frequency: Run detection every 30 steps instead of 10

# Stopping conditions - simulation will auto-stop after:
MAX_RUNTIME = 200       # Maximum runtime (seconds - 5 minutes)

import time
start_time = time.time()

print(f"🚀 Starting simulation with auto-stop conditions:")
print(f"   ⏱️  Max runtime: {MAX_RUNTIME}s")
print(f"   🎯 Will auto-generate graphs when stopped!")

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
    
    # Continuous leaf detection (every DETECTION_INTERVAL steps)
    if (detection_enabled and test_steps - last_detection_step >= DETECTION_INTERVAL):
        
        # Reduced console output for smoother simulation
        detections = detect_leaves_with_display(test_steps)
        
        if detections:
            print_detection_results(detections, test_steps)
        # Removed frequent "no plants detected" messages
        
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
            tracker.add_coordinate(test_steps, 50.0, 50.0, MAX_SPEED, MAX_SPEED, 
                                 detections if 'detections' in locals() else None)
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
        tracker.add_coordinate(test_steps, l_val, r_val, left_speed, right_speed, 
                             detections if 'detections' in locals() else None)
    
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

# Show final plant summary if any detections were made
if detection_count > 0:
    show_final_plant_summary()
else:
    print("🌿 No plants were detected during this session.")

