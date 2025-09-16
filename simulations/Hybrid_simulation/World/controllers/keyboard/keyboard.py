from controller import Robot, Keyboard

# ---------------- ROBOT INIT ----------------
robot = Robot()
timestep = int(robot.getBasicTimeStep())

# ---------------- WHEEL MOTORS ----------------
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

# ---------------- ARM MOTORS (3-AXIS) ----------------
# Base rotation motor (Z-axis)
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

# ---------------- DISTANCE SENSORS ----------------
ds_left = robot.getDevice("distance sensor left")
ds_right = robot.getDevice("distance sensor right")
ds_left.enable(timestep)
ds_right.enable(timestep)

# ---------------- MOTOR PARAMETERS ----------------
LEFT_FORWARD_SIGN = -1
RIGHT_FORWARD_SIGN = -1
MAX_SPEED = 6.28
ARM_SPEED = 2.0  # Arm movement speed

def set_motor_speeds(left_speed, right_speed):
    """Control wheel motors"""
    # Right motors
    for i in range(3):
        motors[i].setVelocity(RIGHT_FORWARD_SIGN * right_speed)
    # Left motors
    for i in range(3, 6):
        motors[i].setVelocity(LEFT_FORWARD_SIGN * left_speed)

def set_arm_speeds(base_speed, down_speed, up_speed):
    """Control 3-axis arm motors"""
    arm_base.setVelocity(base_speed)
    arm_down.setVelocity(down_speed)
    arm_up.setVelocity(up_speed)

def stop_all():
    """Emergency stop all motors"""
    set_motor_speeds(0.0, 0.0)
    set_arm_speeds(0.0, 0.0, 0.0)

# ---------------- KEYBOARD ----------------
keyboard = Keyboard()
keyboard.enable(timestep)

# ---------------- MAIN LOOP ----------------
print("🤖 Agricultural Robot Keyboard Controller")
print("=" * 50)
print("MOVEMENT CONTROLS:")
print("  W/S - Forward/Backward")
print("  A/D - Turn Left/Right")
print("")
print("ARM CONTROLS (3-AXIS):")
print("  Q/E - Base Rotate Left/Right")
print("  R/F - Lower Arm Up/Down") 
print("  T/G - Upper Arm Up/Down")
print("")
print("SPECIAL:")
print("  SPACE - Emergency Stop")
print("  C - Camera Info")
print("  ESC - Exit")
print("=" * 50)

while robot.step(timestep) != -1:
    key = keyboard.getKey()
    
    # Default speeds
    left_speed = 0.0
    right_speed = 0.0
    base_speed = 0.0
    down_speed = 0.0
    up_speed = 0.0
    
    # Read sensors for display
    l_val = ds_left.getValue()
    r_val = ds_right.getValue()

    while key != -1:
        # ============ MOVEMENT CONTROLS ============
        if key == ord('W'):  # Forward
            left_speed = MAX_SPEED
            right_speed = MAX_SPEED
            print("🚀 Moving Forward")
            
        elif key == ord('S'):  # Backward
            left_speed = -MAX_SPEED
            right_speed = -MAX_SPEED
            print("⬅️ Moving Backward")
            
        elif key == ord('D'):  # Hard right turn
            left_speed = -MAX_SPEED
            right_speed = MAX_SPEED
            print("↪️ Turning Right")
            
        elif key == ord('A'):  # Hard left turn
            left_speed = MAX_SPEED
            right_speed = -MAX_SPEED
            print("↩️ Turning Left")
            
        # ============ ARM CONTROLS (3-AXIS) ============
        elif key == ord('Q'):  # Base rotate left
            base_speed = -ARM_SPEED
            print("🔄 Base Rotating Left")
            
        elif key == ord('E'):  # Base rotate right
            base_speed = ARM_SPEED
            print("🔄 Base Rotating Right")
            
        elif key == ord('R'):  # Lower arm up
            down_speed = ARM_SPEED
            print("📈 Lower Arm Up")
            
        elif key == ord('F'):  # Lower arm down
            down_speed = -ARM_SPEED
            print("📉 Lower Arm Down")
            
        elif key == ord('T'):  # Upper arm up
            up_speed = ARM_SPEED
            print("📈 Upper Arm Up")
            
        elif key == ord('G'):  # Upper arm down
            up_speed = -ARM_SPEED
            print("📉 Upper Arm Down")
            
        # ============ SPECIAL CONTROLS ============
        elif key == ord(' '):  # Emergency stop
            stop_all()
            print("🛑 EMERGENCY STOP - All motors stopped")
            
        elif key == ord('C'):  # Camera info
            print(f"📷 Camera: {camera.getWidth()}x{camera.getHeight()} @ {camera.getFov():.2f} FOV")
            print(f"📊 Sensors: Left={l_val:.1f}, Right={r_val:.1f}")
            
        elif key == 27:  # ESC key
            print("👋 Exiting controller...")
            stop_all()
            exit()
            
        key = keyboard.getKey()

    # Apply all motor speeds
    set_motor_speeds(left_speed, right_speed)
    set_arm_speeds(base_speed, down_speed, up_speed)
