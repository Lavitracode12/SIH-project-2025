# Robot Coordinate Tracking and Distance Plotting System

This system allows you to track your robot's coordinates, store them in JSON format, and generate beautiful distance and movement analysis graphs using matplotlib.

## Files Created:

1. **`robot_tracker.py`** - Main tracking module with coordinate storage and plotting
2. **`tracking_integration.py`** - Integration helper with examples
3. **`demo_tracking.py`** - Demo script to test the system
4. **`README.md`** - This instruction file

## Quick Start:

### 1. Test the System (Demo)
```bash
cd /home/shr/Desktop/World/controllers/wall_follower/
python3 demo_tracking.py
```
This will generate demo data and show you all the graphs and features.

### 2. Integrate with Your Robot (Optional)

Add these lines to your `wall_follower.py`:

```python
# At the top with other imports
from robot_tracker import RobotTracker

# After robot initialization
tracker = RobotTracker("robot_coordinates.json")

# In your main loop (where you read sensors and set speeds)
tracker.add_coordinate(test_steps, l_val, r_val, left_speed, right_speed, detections)

# Save periodically
if test_steps % 100 == 0:
    tracker.save_coordinates()

# At the end of your simulation
tracker.plot_distance_graph()
tracker.plot_plant_detection_map()
```

### 3. Analyze Existing Data
```bash
python3 tracking_integration.py
```
This will plot graphs from any existing coordinate data.

## Features:

### 📊 Distance Graphs
- **Cumulative distance traveled** over time
- **Sensor readings** (left/right distance sensors)
- **Robot path visualization** (X-Y coordinates)
- **Speed analysis** over time

### 🌿 Plant Detection Maps
- **Plant detection locations** on robot path
- **Detection density** visualization
- **Species distribution** mapping

### 💾 Data Storage
- **JSON format** for easy reading and processing
- **Timestamp tracking** for each coordinate
- **Sensor data** (left/right distance readings)
- **Movement data** (speeds, distance traveled)
- **Plant detection data** (if available)

### 📈 Statistics
- Total distance traveled
- Average speed
- Number of data points
- Plant detection counts
- Session duration

## JSON Data Format:

```json
{
  "session_info": {
    "start_time": "2025-09-15T10:30:00",
    "total_points": 150,
    "total_distance_traveled": 45.67
  },
  "coordinates": [
    {
      "timestamp": "2025-09-15T10:30:01",
      "step": 1,
      "position": {
        "x": 0.123,
        "y": 0.456,
        "heading": 0.789
      },
      "sensors": {
        "left_distance": 15.5,
        "right_distance": 20.3
      },
      "movement": {
        "left_speed": 3.2,
        "right_speed": 3.1,
        "distance_moved": 0.104
      },
      "total_distance": 0.104,
      "plant_detections": 2,
      "plants_found": ["mango", "neem"]
    }
  ]
}
```

## Output Files:

- **`robot_coordinates.json`** - Your robot's coordinate data
- **`robot_analysis_YYYYMMDD_HHMMSS.png`** - Distance and movement graphs
- **`plant_detection_map_YYYYMMDD_HHMMSS.png`** - Plant detection visualization

## Requirements:

- Python 3.x
- matplotlib
- numpy
- json (built-in)

## Installation:

```bash
pip install matplotlib numpy
```

## Usage Tips:

1. **Run the demo first** to see what the system can do
2. **Start with small integration** - just add coordinate tracking
3. **Generate plots periodically** to monitor robot performance
4. **Use saved JSON data** for further analysis in other tools
5. **Customize the plotting** by modifying `robot_tracker.py`

## Example Output:

The system generates comprehensive graphs showing:
- How far your robot has traveled
- Its path through the arena
- Speed variations over time
- Sensor readings and wall-following behavior
- Locations where plants were detected

Perfect for analyzing your robot's performance and navigation efficiency! 🚀🗺️📊