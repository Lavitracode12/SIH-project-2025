# 🎮 Webots Simulation Environment

## 🔍 Overview

The **Webots Simulation Environment** provides a comprehensive virtual testing platform for the Smart Pesticide Spraying System. This physics-based simulation allows for safe development, testing, and validation of rover control algorithms, AI models, and autonomous behaviors before deployment on physical hardware.

## 🏗️ Simulation Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Webots Simulation Platform                   │
├─────────────────────────────────────────────────────────────────┤
│  🌍 Virtual World        │  🤖 Robot Models      │  🎮 Controllers│
│  - Agricultural field    │  - 6-wheel rover      │  - Manual ctrl │
│  - Plant models          │  - 3-axis arm         │  - Autonomous  │
│  - Environmental setup   │  - Camera systems     │  - Wall follow │
├─────────────────────────────────────────────────────────────────┤
│  ⚙️ Physics Engine       │  📡 Sensor Simulation │  🧠 AI Integration│
│  - Realistic dynamics   │  - Distance sensors   │  - Vision proc │
│  - Collision detection  │  - Camera feed        │  - ML inference│
│  - Terrain interaction  │  - IMU & GPS         │  - Decision AI │
└─────────────────────────────────────────────────────────────────┘
```

## 🚀 Key Features

### 🌍 Virtual Agricultural Environment
- **Realistic Field Simulation**: Physics-accurate terrain with proper soil dynamics
- **3D Plant Models**: Detailed crop representations including corn, tomato, and various species
- **Environmental Conditions**: Configurable lighting, weather, and seasonal variations
- **Boundary Systems**: Realistic field boundaries and obstacle placement
- **Scalable Fields**: Adjustable field sizes from small plots to large agricultural areas

### 🤖 Accurate Robot Simulation
- **Physical Rover Model**: Precise mechanical simulation of 6-wheel drive system
- **Robotic Arm**: Accurate 3-axis arm with realistic joint constraints and physics
- **Sensor Suite**: Virtual distance sensors, cameras, and navigation systems
- **Spray Mechanism**: Simulated spray system with particle effects and coverage tracking
- **Battery Simulation**: Realistic power consumption and charging cycles

### 🎮 Multi-Mode Controllers
- **Manual Control**: Keyboard and joystick input for direct operator control
- **Autonomous Navigation**: AI-driven path planning and obstacle avoidance
- **Hybrid Operation**: Semi-autonomous mode with human oversight
- **Testing Scenarios**: Predefined test cases for validation and benchmarking

## 📁 Project Structure

```
Simulation/World/
├── 🌍 worlds/                        # Simulation world files
│   ├── field.wbt                    # Main agricultural field world
│   ├── greenhouse.wbt               # Indoor growing simulation
│   └── test_environment.wbt         # Development testing world
│
├── 🤖 controllers/                   # Robot control programs
│   ├── keyboard/                    # Manual control system
│   │   ├── keyboard.py              # Main control script
│   │   └── keyboard.ini             # Controller configuration
│   │
│   ├── wall_follower/              # Autonomous navigation
│   │   ├── wall_follower.py        # Path following algorithm
│   │   └── navigation_utils.py     # Helper functions
│   │
│   └── my_controller/              # Custom control logic
│       ├── my_controller.py        # Base controller template
│       └── config.json            # Controller settings
│
├── 🏗️ protos/                       # Custom robot definitions
│   ├── AgriculturalRover.proto     # Main rover prototype
│   ├── SprayArm.proto              # Robotic arm assembly
│   └── FieldSensors.proto          # Sensor package definition
│
├── 🌱 model/                        # 3D models and textures
│   ├── plants/                     # Crop models
│   │   ├── corn.dae                # Corn plant model
│   │   ├── tomato.dae              # Tomato plant model
│   │   └── maize.dae               # Maize crop model
│   │
│   ├── textures/                   # Surface materials
│   │   ├── soil_texture.jpg        # Ground materials
│   │   ├── plant_textures/         # Plant surface textures
│   │   └── rover_materials/        # Robot surface materials
│   │
│   └── environment/                # Environmental assets
│       ├── greenhouse.dae          # Greenhouse structure
│       └── field_boundaries.dae    # Field border models
│
├── 🔧 rovers/                       # Rover component models
│   ├── chassis_rotated.stl         # Main chassis model
│   ├── tire_rotated.stl           # Wheel models
│   ├── arm_base.stl               # Arm base component
│   ├── arm_link_base.stl          # Lower arm segment
│   ├── arm_link_up.stl            # Upper arm segment
│   └── Base_rotated.stl           # Support structures
│
├── 🔌 plugins/                      # Webots extensions
│   ├── physics/                    # Custom physics plugins
│   ├── remote_controls/            # Remote control interfaces
│   └── robot_windows/              # Custom UI windows
│
└── 📋 libraries/                    # Shared code libraries
    ├── sensor_utils/               # Sensor processing utilities
    ├── navigation/                 # Path planning algorithms
    └── ai_integration/            # ML model integration
```

## 🎮 Controller Systems

### ⌨️ Manual Control (keyboard.py)

#### **Control Scheme**
```python
# Movement Controls
W/S     - Forward/Backward motion
A/D     - Left/Right steering
Q/E     - Sharp turns (tank steering)

# Robotic Arm Controls
↑/↓     - Lower arm joint (shoulder)
←/→     - Upper arm joint (elbow) 
R/F     - Base rotation (Z-axis)
T/G     - Fine arm adjustments

# System Controls
SPACE   - Emergency stop
P       - Activate/deactivate spray
L       - Toggle LED lights
C       - Capture camera image
ESC     - Exit simulation
```

#### **Advanced Features**
```python
# Speed Control
1-5     - Speed levels (20%-100%)
SHIFT   - Precision mode (reduced sensitivity)
CTRL    - Turbo mode (maximum speed)

# Camera Controls
Z/X     - Zoom in/out
V       - Switch camera views
B       - Toggle bounding boxes
N       - Night vision mode
```

### 🧭 Autonomous Navigation (wall_follower.py)

#### **Navigation Algorithm**
```python
class WallFollowerController:
    def __init__(self):
        self.target_distance = 0.5    # meters from wall/boundary
        self.max_speed = 2.0          # maximum velocity
        self.pid_controller = PID()   # steering control
        
    def navigate(self):
        # Read distance sensors
        left_dist = self.get_sensor_value('distance_left')
        right_dist = self.get_sensor_value('distance_right')
        front_dist = self.get_sensor_value('distance_front')
        
        # Calculate steering correction
        error = left_dist - self.target_distance
        correction = self.pid_controller.update(error)
        
        # Apply movement commands
        self.set_wheel_speeds(forward_speed, correction)
```

#### **Behavior States**
- **Wall Following**: Maintain consistent distance from crop rows
- **Obstacle Avoidance**: Dynamic path adjustment around obstacles
- **Corner Handling**: Automatic turns at field boundaries
- **Coverage Optimization**: Systematic field scanning patterns
- **Return to Base**: Automated return when task complete

### 🎯 Custom Controller (my_controller.py)

#### **Modular Architecture**
```python
class CustomController:
    def __init__(self):
        self.navigation_module = NavigationSystem()
        self.vision_module = VisionProcessor()
        self.spray_module = SprayControl()
        self.sensor_module = SensorManager()
    
    def main_loop(self):
        while self.robot.step(self.timestep) != -1:
            # Sensor data acquisition
            sensor_data = self.sensor_module.read_all()
            
            # AI vision processing
            detections = self.vision_module.process_frame()
            
            # Navigation decision making
            navigation_cmd = self.navigation_module.plan_path()
            
            # Spray control logic
            if detections.disease_detected:
                self.spray_module.activate_spray()
```

## 🔧 Hardware Simulation

### 🚗 Rover Mechanics

#### **Drive System Simulation**
```yaml
Chassis Configuration:
  Wheelbase: 1.0m
  Track Width: 0.8m  
  Ground Clearance: 0.15m
  Weight Distribution: 60% rear, 40% front
  
Drive Motors:
  Type: DC motors with encoders
  Max Torque: 50 Nm per wheel
  Max RPM: 300 (variable speed)
  Gear Ratio: 30:1
  
Suspension System:
  Type: Independent wheel suspension
  Travel: ±50mm vertical movement
  Damping: Realistic spring-damper model
```

#### **Robotic Arm Dynamics**
```yaml
Arm Specifications:
  Base Joint (Rotation): ±180° range, 360° continuous
  Shoulder Joint: -90° to +90° elevation
  Elbow Joint: -120° to +60° flexion
  
Joint Motors:
  Type: Servo motors with position feedback
  Precision: ±1° positioning accuracy
  Speed: 0.5-2.0 rad/s (adjustable)
  Load Capacity: 5kg at full extension
  
End Effector:
  Camera Mount: Stabilized gimbal system
  Spray Nozzle: Variable flow rate control
  Tool Exchange: Modular attachment system
```

### 📡 Sensor Simulation

#### **Distance Sensors**
```python
# Ultrasonic sensor configuration
distance_sensors = {
    'front': {'range': 4.0, 'fov': 15°, 'resolution': 0.01},
    'left':  {'range': 4.0, 'fov': 15°, 'resolution': 0.01},
    'right': {'range': 4.0, 'fov': 15°, 'resolution': 0.01},
    'rear':  {'range': 2.0, 'fov': 15°, 'resolution': 0.01}
}
```

#### **Vision System**
```python
# Camera specifications
camera_config = {
    'resolution': (1920, 1080),
    'framerate': 30,
    'fov_horizontal': 70°,
    'fov_vertical': 45°,
    'near_plane': 0.1,
    'far_plane': 100.0,
    'auto_exposure': True,
    'white_balance': 'auto'
}
```

## 🌍 World Environments

### 🌾 Agricultural Field (field.wbt)

#### **Environment Features**
- **Field Dimensions**: 100m x 80m agricultural plot
- **Crop Layout**: Organized rows with 2m spacing
- **Plant Variety**: Mixed crops including corn, tomato, and vegetables
- **Terrain**: Realistic soil texture with slight undulations
- **Boundaries**: Fence perimeter with gate access points
- **Lighting**: Configurable sun position and intensity
- **Weather Effects**: Optional rain, wind, and fog simulation

#### **Testing Scenarios**
1. **Row Following**: Navigate between crop rows maintaining alignment
2. **Disease Detection**: Identify and treat infected plants
3. **Obstacle Avoidance**: Navigate around field equipment and workers
4. **Coverage Optimization**: Complete field coverage with minimal overlap
5. **Battery Management**: Return to charging station when power low

### 🏠 Greenhouse Environment (greenhouse.wbt)

#### **Indoor Growing Simulation**
- **Structure**: 50m x 30m greenhouse with glass walls and roof
- **Climate Control**: Controlled lighting and temperature
- **Plant Density**: Higher density growing systems
- **Navigation Challenges**: Narrow aisles and overhead obstacles
- **Precision Requirements**: Closer proximity to plants for detailed inspection

## 🧪 Testing & Validation

### 📊 Performance Metrics

#### **Navigation Accuracy**
```yaml
Path Following:
  Deviation Tolerance: ±5cm from planned path
  Obstacle Detection Range: 0.3-4.0m
  Turning Radius: 0.5m minimum
  Speed Range: 0.1-2.0 m/s

Coverage Efficiency:
  Field Coverage: >95% area coverage
  Overlap Minimization: <5% redundant coverage
  Time Optimization: Shortest path algorithms
  Energy Efficiency: Minimal power consumption paths
```

#### **AI Integration Testing**
```yaml
Vision Processing:
  Detection Latency: <100ms per frame
  Classification Accuracy: >90% disease detection
  False Positive Rate: <5%
  Processing Throughput: 20-30 FPS

Decision Making:
  Response Time: <500ms from detection to action
  Decision Accuracy: >95% correct spray decisions  
  Safety Compliance: 100% emergency stop response
```

### 🔍 Debugging & Analysis

#### **Built-in Tools**
- **3D Visualization**: Real-time robot state display
- **Sensor Data Plots**: Live graphing of sensor readings
- **Path Tracking**: Visual representation of robot trajectory
- **Performance Profiler**: CPU and memory usage analysis
- **Physics Debug**: Collision detection and force visualization

#### **Data Export**
```python
# Simulation data logging
class SimulationLogger:
    def log_data(self):
        return {
            'timestamp': self.get_time(),
            'position': self.robot.get_position(),
            'orientation': self.robot.get_orientation(),
            'sensor_readings': self.get_all_sensors(),
            'motor_commands': self.get_motor_states(),
            'spray_status': self.spray_system.is_active(),
            'ai_detections': self.vision_system.get_results()
        }
```

## 🚀 Advanced Features

### 🔄 Physics Customization

#### **Realistic Material Properties**
```python
# Soil interaction physics
soil_properties = {
    'friction': 0.8,           # Wheel-soil friction
    'compaction': 0.1,         # Soil compression
    'moisture': 0.3,           # Wet/dry conditions
    'slope_stability': 0.9     # Hillside traction
}

# Plant interaction physics  
plant_physics = {
    'stem_flexibility': 0.5,   # Plant bending
    'leaf_response': 0.2,      # Wind effects
    'spray_absorption': 0.8,   # Chemical uptake
    'growth_simulation': True  # Dynamic plant growth
}
```

#### **Weather Simulation**
```python
# Environmental conditions
weather_system = {
    'wind_speed': 2.5,         # m/s
    'wind_direction': 45,      # degrees
    'humidity': 65,            # percentage
    'temperature': 25,         # Celsius
    'light_intensity': 0.8,    # 0-1 scale
    'precipitation': 0.0       # mm/hour
}
```

## 🔮 Future Enhancements

### Phase 1 - Current Capabilities
- ✅ Basic rover simulation with physics
- ✅ Manual and autonomous control modes
- ✅ Simple agricultural environment
- ✅ Distance sensor simulation

### Phase 2 - Enhanced Realism
- 🔄 Advanced weather and seasonal effects
- 🔄 Dynamic plant growth simulation
- 🔄 GPS and RTK positioning systems
- 🔄 Multi-rover coordination scenarios

### Phase 3 - Advanced Simulation
- 🔄 Soil composition and moisture modeling
- 🔄 Detailed spray dynamics and drift simulation
- 🔄 Economic modeling and cost analysis
- 🔄 Integration with real farm management systems

## 🛠️ Development Workflow

### 🔧 Setting Up Development Environment

#### **Webots Installation**
```bash
# Ubuntu/Debian installation
wget https://github.com/cyberbotics/webots/releases/download/R2025a/webots_2025a_amd64.deb
sudo dpkg -i webots_2025a_amd64.deb

# Launch Webots
webots

# Open world file
# File → Open World → field.wbt
```

#### **Controller Development**
```bash
# Create new controller
mkdir controllers/my_new_controller
cd controllers/my_new_controller

# Create controller script
touch my_new_controller.py
chmod +x my_new_controller.py

# Edit controller in Webots built-in editor
# Or use external IDE with proper Python path
```

### 📝 Best Practices

#### **Controller Development**
1. **Modular Design**: Separate navigation, vision, and control logic
2. **Error Handling**: Robust error recovery and safety mechanisms  
3. **Performance Optimization**: Efficient sensor reading and processing
4. **Documentation**: Clear code comments and function documentation
5. **Testing**: Unit tests for individual controller functions

#### **World Design**
1. **Realistic Physics**: Accurate mass, friction, and dynamics
2. **Scalable Environments**: Adjustable field sizes and complexity
3. **Asset Optimization**: Efficient 3D models for smooth simulation
4. **Lighting Setup**: Proper illumination for vision system testing
5. **Boundary Definition**: Clear field limits and obstacle placement

## 📞 Support & Resources

### 📚 Documentation
- **Webots User Guide**: [cyberbotics.com/doc/guide](https://cyberbotics.com/doc/guide/)
- **Python API Reference**: [cyberbotics.com/doc/reference](https://cyberbotics.com/doc/reference/)
- **Controller Templates**: Available in `controllers/` directory
- **World Examples**: Sample worlds in `worlds/` directory

### 🐛 Troubleshooting
1. **Simulation Performance**: Reduce world complexity, disable shadows
2. **Controller Errors**: Check Python syntax and Webots API usage
3. **Physics Issues**: Verify mass properties and constraint settings
4. **Sensor Problems**: Calibrate sensor ranges and update rates

---

**🎮 Virtual testing ground for real-world agricultural automation**

*Enabling safe development and validation of autonomous farming systems* 🌾🤖