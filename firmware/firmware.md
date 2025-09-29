# ⚡ Firmware & Embedded Systems

## 🌟 Overview

The firmware layer provides low-level control and real-time operation for the Smart Pesticide Spraying System. This embedded software manages hardware interfaces, sensor data acquisition, motor control, and communication protocols between the rover's physical components and higher-level control systems.

## 🏗️ Firmware Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  Main Control Unit (MCU)                   │
├─────────────────────────────────────────────────────────────┤
│  Real-Time Operating System (RTOS)                         │
├─────────────────┬───────────────────┬──────────────────────┤
│  Motor Control  │   Sensor Manager  │  Communication Hub   │
│  - PWM drivers  │   - ADC readings  │  - UART/SPI/I2C    │
│  - PID control  │   - Sensor fusion │  - Wireless comm   │
│  - Safety logic │   - Calibration   │  - Protocol stack  │
├─────────────────┼───────────────────┼──────────────────────┤
│            Hardware Abstraction Layer (HAL)                │
│  - GPIO control │ - Timer management│ - Interrupt handling │
└─────────────────────────────────────────────────────────────┘
```

## 🔧 Hardware Platform

### 🖥️ Main Control Unit
- **Microcontroller**: ARM Cortex-M7 (STM32F7 series)
- **Clock Speed**: 216 MHz
- **Flash Memory**: 2MB (program storage)
- **RAM**: 512KB (runtime memory)
- **Peripherals**: Multiple UART, SPI, I2C, CAN interfaces

### 🔌 Interface Modules
- **Motor Driver Board**: 6-channel PWM with current sensing
- **Sensor Interface**: Multi-channel ADC with signal conditioning
- **Communication Module**: WiFi/Bluetooth for wireless connectivity
- **Safety Controller**: Independent watchdog and emergency stop

### ⚡ Power Management
- **Main Power**: 24V battery system with monitoring
- **Logic Power**: 5V/3.3V regulated supplies
- **Power Distribution**: Smart switching with overcurrent protection
- **Battery Management**: Charge monitoring and protection circuits

## 🚀 Real-Time Operating System

### 📋 Task Scheduling
```c
// Priority-based task management
Tasks:
  CRITICAL   (1ms):  Safety monitoring, emergency stop
  HIGH       (5ms):  Motor control, PID loops
  MEDIUM    (10ms):  Sensor reading, data processing
  LOW       (50ms):  Communication, logging
  BACKGROUND(100ms): Diagnostics, maintenance
```

### 🔄 Inter-Task Communication
- **Message Queues**: Asynchronous data exchange
- **Semaphores**: Resource protection and synchronization
- **Event Flags**: Status signaling between tasks
- **Shared Memory**: High-speed data sharing with mutex protection

## 🎮 Motor Control System

### 🚗 Wheel Motor Control
```c
// Six-wheel drive control
typedef struct {
    uint8_t motor_id;        // Motor identifier (1-6)
    int16_t target_speed;    // Target speed (RPM)
    int16_t current_speed;   // Actual speed feedback
    uint16_t pwm_duty;       // PWM duty cycle (0-1000)
    uint8_t direction;       // Forward/Reverse
    bool enabled;            // Motor enable status
} WheelMotor_t;

// PID control parameters
typedef struct {
    float kp, ki, kd;        // PID gains
    float integral;          // Integral term
    float prev_error;        // Previous error for derivative
    float output_limit;      // Output saturation limit
} PID_Controller_t;
```

### 🦾 Robotic Arm Control
```c
// Three-axis arm control
typedef struct {
    float base_angle;        // Base rotation (degrees)
    float lower_angle;       // Lower joint (degrees)
    float upper_angle;       // Upper joint (degrees)
    float target_x, target_y, target_z;  // Cartesian target
    bool position_reached;   // Target achievement flag
} ArmPosition_t;

// Servo control with position feedback
void Arm_SetPosition(ArmPosition_t* target);
void Arm_UpdateControl(void);  // Called at 100Hz
bool Arm_IsPositionReached(float tolerance);
```

## 📡 Sensor Management

### 📏 Distance Sensors
```c
// Ultrasonic sensor data structure
typedef struct {
    uint16_t distance_mm;    // Distance in millimeters
    uint8_t confidence;      // Measurement confidence (0-100)
    uint32_t timestamp;      // Measurement timestamp
    bool valid;              // Data validity flag
} DistanceSensor_t;

// Sensor positions
enum SensorPosition {
    SENSOR_LEFT,
    SENSOR_RIGHT,
    SENSOR_FRONT,
    SENSOR_BACK
};
```

### 🧭 IMU (Inertial Measurement Unit)
```c
// 9-DOF sensor data
typedef struct {
    float accel_x, accel_y, accel_z;     // Accelerometer (m/s²)
    float gyro_x, gyro_y, gyro_z;        // Gyroscope (°/s)
    float mag_x, mag_y, mag_z;           // Magnetometer (µT)
    float roll, pitch, yaw;              // Euler angles (degrees)
    uint32_t timestamp;                  // Data timestamp
} IMU_Data_t;
```

### 💧 Spray System Sensors
```c
// Spray system monitoring
typedef struct {
    uint16_t tank_level;     // Tank level (0-100%)
    uint16_t flow_rate;      // Flow rate (ml/min)
    uint16_t pressure;       // System pressure (PSI)
    bool pump_status;        // Pump on/off status
    bool leak_detected;      // Leak detection flag
} SpraySystem_t;
```

## 📡 Communication Protocols

### 🔗 UART Communication
```c
// High-level control interface
#define UART_BUFFER_SIZE 256
#define COMMAND_TIMEOUT_MS 1000

typedef enum {
    CMD_SET_SPEED,           // Set wheel speeds
    CMD_SET_ARM_POS,         // Set arm position
    CMD_SPRAY_CONTROL,       // Control spray system
    CMD_GET_STATUS,          // Request system status
    CMD_EMERGENCY_STOP       // Emergency stop command
} CommandType_t;

typedef struct {
    uint8_t header;          // Command header (0xAA)
    uint8_t cmd_type;        // Command type
    uint8_t data_length;     // Data payload length
    uint8_t data[32];        // Command data
    uint8_t checksum;        // Data integrity check
} Command_t;
```

### 📶 Wireless Communication
```c
// WiFi telemetry data
typedef struct {
    SystemStatus_t status;   // Overall system status
    SensorData_t sensors;    // All sensor readings
    MotorStatus_t motors;    // Motor status and feedback
    uint32_t timestamp;      // Data timestamp
    uint16_t packet_id;      // Sequential packet ID
} TelemetryPacket_t;

// Transmission every 100ms
void Telemetry_SendPacket(void);
void Telemetry_ProcessCommands(void);
```

## 🛡️ Safety & Diagnostics

### ⛔ Safety Monitoring
```c
// Critical safety checks
typedef struct {
    bool emergency_stop;     // Hardware emergency stop status
    bool communication_ok;   // Communication link status
    bool battery_ok;         // Battery voltage within limits
    bool motors_ok;          // All motors functioning normally
    bool sensors_ok;         // All sensors providing valid data
    bool spray_safe;         // Spray system safe to operate
} SafetyStatus_t;

// Safety task (highest priority)
void Safety_Monitor(void) {
    // Check all safety conditions every 1ms
    // Immediate shutdown if any critical condition fails
}
```

### 🔍 Diagnostic System
```c
// System health monitoring
typedef struct {
    uint32_t uptime_seconds;     // System uptime
    uint16_t cpu_usage_percent;  // CPU utilization
    uint16_t memory_usage_kb;    // RAM usage
    uint16_t error_count;        // Total error count
    uint8_t last_error_code;     // Most recent error
    float temperature_celsius;   // MCU temperature
} SystemDiagnostics_t;

// Error codes
enum ErrorCodes {
    ERR_NONE = 0x00,
    ERR_MOTOR_FAULT = 0x01,
    ERR_SENSOR_TIMEOUT = 0x02,
    ERR_COMMUNICATION_LOST = 0x03,
    ERR_BATTERY_LOW = 0x04,
    ERR_SPRAY_LEAK = 0x05
};
```

## ⚙️ Configuration & Calibration

### 📊 Parameter Storage
```c
// Non-volatile configuration storage
typedef struct {
    // Motor calibration
    float motor_gains[6][3];     // PID gains for each motor
    uint16_t motor_offsets[6];   // Zero-speed PWM offsets
    
    // Sensor calibration
    float sensor_scales[4];      // Distance sensor scale factors
    float imu_bias[9];           // IMU bias correction
    
    // System parameters
    uint16_t max_speed;          // Maximum allowed speed
    uint8_t safety_timeout;      // Safety timeout period
    uint32_t config_checksum;    // Configuration integrity
} SystemConfig_t;

// EEPROM storage functions
void Config_Save(void);
void Config_Load(void);
void Config_SetDefaults(void);
```

### 🎛️ Calibration Procedures
```c
// Motor calibration sequence
void Calibrate_Motors(void) {
    // 1. Zero speed calibration
    // 2. Speed response measurement
    // 3. PID parameter tuning
    // 4. Direction verification
}

// Sensor calibration
void Calibrate_Sensors(void) {
    // 1. Distance sensor ranging
    // 2. IMU bias calculation
    // 3. Cross-sensor validation
}
```

## 🔋 Power Management

### ⚡ Battery Monitoring
```c
// Battery management system
typedef struct {
    float voltage;           // Battery voltage (V)
    float current;           // Current draw (A)
    float capacity_remain;   // Remaining capacity (%)
    float temperature;       // Battery temperature (°C)
    uint16_t cycle_count;    // Charge cycle counter
    bool charging;           // Charging status
    bool fault;              // Battery fault flag
} BatteryStatus_t;

// Power saving modes
enum PowerMode {
    POWER_FULL,              // Full performance
    POWER_ECONOMY,           // Reduced performance
    POWER_SLEEP,             // Minimal power consumption
    POWER_SHUTDOWN           // Safe shutdown
};
```

### 🔌 Smart Power Distribution
```c
// Controllable power outputs
void Power_EnableSubsystem(uint8_t subsystem_id);
void Power_DisableSubsystem(uint8_t subsystem_id);
float Power_GetConsumption(uint8_t subsystem_id);
void Power_SetMode(enum PowerMode mode);
```

## 📈 Performance Optimization

### ⚡ Real-Time Constraints
- **Motor Control Loop**: 5ms cycle time with <1ms jitter
- **Safety Monitoring**: 1ms response time for emergency conditions
- **Communication**: <10ms latency for critical commands
- **Sensor Processing**: 10ms update rate with data fusion

### 🧮 Computational Efficiency
- **Fixed-Point Math**: Used where possible for speed
- **Lookup Tables**: Pre-calculated trigonometric functions
- **Interrupt-Driven**: Minimal polling for efficiency
- **Memory Management**: Static allocation for predictability

## 🛠️ Development & Testing

### 🔧 Development Tools
- **IDE**: STM32CubeIDE with integrated debugger
- **Compiler**: ARM GCC with optimization flags
- **Debugger**: ST-Link hardware debugger
- **Version Control**: Git with embedded-specific workflows

### 🧪 Testing Framework
```c
// Unit testing for embedded systems
#define ASSERT(condition) \
    if (!(condition)) { \
        Test_Fail(__FILE__, __LINE__); \
    }

// Hardware-in-the-loop testing
void Test_MotorControl(void);
void Test_SensorReading(void);
void Test_SafetySystems(void);
void Test_CommunicationProtocol(void);
```

### 📊 Performance Monitoring
- **Execution Time Profiling**: Real-time task timing analysis
- **Memory Usage Tracking**: Stack and heap utilization
- **Error Rate Monitoring**: System reliability metrics
- **Power Consumption Analysis**: Battery life optimization

## 🔮 Future Enhancements

### Phase 1 Improvements
- **Advanced Filtering**: Kalman filters for sensor fusion
- **Predictive Control**: Model-based control algorithms
- **Over-the-Air Updates**: Remote firmware update capability

### Phase 2 Development
- **Machine Learning**: On-device AI acceleration
- **Advanced Networking**: Mesh networking for multi-rover coordination
- **Enhanced Security**: Encrypted communication and secure boot

## 📚 Technical Specifications

### 🔧 Memory Requirements
- **Program Flash**: 1.2MB (60% utilization)
- **RAM Usage**: 320KB (62% utilization)
- **Stack Size**: 8KB per task (safety margin)
- **Heap Size**: 32KB for dynamic allocation

### ⏱️ Timing Requirements
- **Boot Time**: <5 seconds to operational state
- **Response Time**: <100ms for non-critical commands
- **Update Rate**: 100Hz control loop frequency
- **Watchdog Timeout**: 2 seconds for system reset

### 🌡️ Environmental Specifications
- **Operating Temperature**: -20°C to +70°C
- **Storage Temperature**: -40°C to +85°C
- **Humidity**: 0-95% non-condensing
- **Shock/Vibration**: Agricultural equipment standards

---

*The firmware serves as the foundational layer that transforms digital intelligence into precise physical actions, enabling reliable and safe operation in challenging agricultural environments.* ⚡🤖