from controller import Robot

robot = Robot()
timestep = int(robot.getBasicTimeStep())

# ================== MOTORS ==================
motor_names = [
    "rotational motor1", "rotational motor2", "rotational motor3",  # Right
    "rotational motor4", "rotational motor5", "rotational motor6",  # Left
]

motors = []
for name in motor_names:
    m = robot.getDevice(name)
    m.setPosition(float('inf'))  # velocity control
    m.setVelocity(0.0)
    motors.append(m)

MAX_SPEED = 6.28

# ================== DISTANCE SENSORS ==================
ds_right = robot.getDevice("distance sensor right")
ds_left = robot.getDevice("distance sensor left")
ds_right.enable(timestep)
ds_left.enable(timestep)

# ================== MOTOR ORIENTATION ==================
LEFT_FORWARD_SIGN = -1   # adjust if left moves backward
RIGHT_FORWARD_SIGN = 1  # adjust if right moves backward

# ================== TARGETS & CONTROLLER ==================
TARGET_DISTANCE_RIGHT = 5.0
TARGET_DISTANCE_LEFT = 5.0
Kp = 0.5
FRONT_THRESHOLD = 50.0
DEADZONE = 0.5
JUNCTION_THRESHOLD = 80.0  # When sensor reads above this, it's an open junction

# ================== HELPER FUNCTION ==================
def set_motor_speeds(left_speed, right_speed):
    left_motor_value = LEFT_FORWARD_SIGN * left_speed
    right_motor_value = RIGHT_FORWARD_SIGN * right_speed
    
    for i in range(3):  # left motors (motors 1,2,3)
        motors[i].setVelocity(left_motor_value)
    for i in range(3, 6):  # right motors (motors 4,5,6)
        motors[i].setVelocity(right_motor_value)
    
    # Debug output for motor values
    print(f"Motor debug: L_speed={left_speed:.2f} -> L_motor={left_motor_value:.2f}, R_speed={right_speed:.2f} -> R_motor={right_motor_value:.2f}")

# ================== MAIN LOOP ==================
while robot.step(timestep) != -1:
    r_val = ds_right.getValue()
    l_val = ds_left.getValue()

    # Default speeds
    left_speed = MAX_SPEED
    right_speed = MAX_SPEED

    # Check for junctions first (open paths)
    right_junction = r_val > JUNCTION_THRESHOLD
    left_junction = l_val > JUNCTION_THRESHOLD
    
    if right_junction and not left_junction:
        # Right junction detected - turn right
        # Slow down right side to turn right
        left_speed = MAX_SPEED
        right_speed = 0.2 * MAX_SPEED
        print(f"Right junction detected - turning right (L={l_val:.1f}, R={r_val:.1f})")
    
    elif left_junction and not right_junction:
        # Left junction detected - turn left
        # Slow down left side to turn left
        left_speed = 0.2 * MAX_SPEED
        right_speed = MAX_SPEED
        print(f"Left junction detected - turning left (L={l_val:.1f}, R={r_val:.1f})")
    
    elif right_junction and left_junction:
        # Both sides open - continue straight
        left_speed = MAX_SPEED
        right_speed = MAX_SPEED
        print(f"Open area - moving straight (L={l_val:.1f}, R={r_val:.1f})")
    
    # Safety: simple front obstacle
    elif l_val < FRONT_THRESHOLD and r_val < FRONT_THRESHOLD:
        left_speed = 0.5 * MAX_SPEED
        right_speed = -0.5 * MAX_SPEED
        print(f"Front obstacle - turning around (L={l_val:.1f}, R={r_val:.1f})")
    
    else:
        # Normal wall following between two walls
        # P-controller: balance between walls
        error_right = TARGET_DISTANCE_RIGHT - r_val
        error_left = l_val - TARGET_DISTANCE_LEFT
        error = error_right - error_left  # positive → steer right

        if abs(error) > DEADZONE:
            correction = Kp * error
            left_speed += correction
            right_speed -= correction

        # Clamp speeds
        left_speed = max(0.0, min(MAX_SPEED, left_speed))
        right_speed = max(0.0, min(MAX_SPEED, right_speed))
    set_motor_speeds(left_speed, right_speed)

    # Debug
    if right_junction or left_junction:
        print(f"JUNCTION: L={l_val:.1f}, R={r_val:.1f}, Left speed={left_speed:.2f}, Right speed={right_speed:.2f}")
    else:
        error_right = TARGET_DISTANCE_RIGHT - r_val if r_val <= JUNCTION_THRESHOLD else 0
        error_left = l_val - TARGET_DISTANCE_LEFT if l_val <= JUNCTION_THRESHOLD else 0
        error = error_right - error_left
        print(f"NORMAL: L={l_val:.1f}, R={r_val:.1f}, Error={error:.2f}, Left speed={left_speed:.2f}, Right speed={right_speed:.2f}")
