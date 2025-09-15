"""
Robot Position Tracker Module
Stores robot coordinates and generates distance graphs
"""

import json
import time
import math
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

class RobotTracker:
    def __init__(self, json_file="robot_coordinates.json"):
        self.json_file = json_file
        self.coordinates = []
        self.start_time = time.time()
        self.last_position = None
        self.total_distance = 0.0
        
        # Initialize or load existing data
        self.load_coordinates()
        
    def load_coordinates(self):
        """Load existing coordinates from JSON file"""
        try:
            with open(self.json_file, 'r') as f:
                data = json.load(f)
                self.coordinates = data.get('coordinates', [])
                self.total_distance = data.get('total_distance', 0.0)
                print(f"📍 Loaded {len(self.coordinates)} existing coordinates")
        except FileNotFoundError:
            print(f"📍 Creating new coordinate file: {self.json_file}")
            self.coordinates = []
            self.total_distance = 0.0
    
    def save_coordinates(self):
        """Save coordinates to JSON file"""
        data = {
            'session_info': {
                'start_time': datetime.fromtimestamp(self.start_time).isoformat(),
                'total_points': len(self.coordinates),
                'total_distance_traveled': self.total_distance
            },
            'coordinates': self.coordinates,
            'total_distance': self.total_distance
        }
        
        with open(self.json_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def estimate_position_from_sensors(self, left_sensor, right_sensor, step_count, left_speed, right_speed):
        """
        Estimate robot position based on sensor readings and movement
        This is a simplified position estimation - in real SLAM you'd use odometry
        """
        # Simple position estimation based on wall following
        # This assumes the robot starts at origin (0, 0) facing forward
        
        # Estimate forward movement (simplified)
        avg_speed = (abs(left_speed) + abs(right_speed)) / 2
        time_step = 0.032  # Webots default timestep
        distance_moved = avg_speed * time_step
        
        # Estimate turning based on speed difference
        speed_diff = right_speed - left_speed
        turning_angle = speed_diff * time_step * 0.1  # Simplified turning estimation
        
        # If we have a previous position, calculate new position
        if self.last_position is None:
            # Starting position
            x, y, heading = 0.0, 0.0, 0.0
        else:
            x, y, heading = self.last_position['x'], self.last_position['y'], self.last_position['heading']
            
            # Update heading
            heading += turning_angle
            
            # Update position based on movement
            x += distance_moved * math.cos(heading)
            y += distance_moved * math.sin(heading)
        
        return x, y, heading, distance_moved
    
    def add_coordinate(self, step_count, left_sensor, right_sensor, left_speed, right_speed, detections=None):
        """Add a new coordinate point with sensor data"""
        
        # Estimate position
        x, y, heading, distance_moved = self.estimate_position_from_sensors(
            left_sensor, right_sensor, step_count, left_speed, right_speed
        )
        
        # Update total distance
        if distance_moved > 0:
            self.total_distance += distance_moved
        
        # Create coordinate entry
        coordinate = {
            'timestamp': datetime.now().isoformat(),
            'step': step_count,
            'position': {
                'x': round(x, 3),
                'y': round(y, 3),
                'heading': round(heading, 3)
            },
            'sensors': {
                'left_distance': round(left_sensor, 2),
                'right_distance': round(right_sensor, 2)
            },
            'movement': {
                'left_speed': round(left_speed, 2),
                'right_speed': round(right_speed, 2),
                'distance_moved': round(distance_moved, 3)
            },
            'total_distance': round(self.total_distance, 3)
        }
        
        # Add plant detections if provided
        if detections:
            coordinate['plant_detections'] = len(detections)
            coordinate['plants_found'] = [det['plant'] for det in detections]
        
        self.coordinates.append(coordinate)
        self.last_position = coordinate['position']
        
        # Save every 10 coordinates to avoid too frequent I/O
        if len(self.coordinates) % 10 == 0:
            self.save_coordinates()
    
    def plot_distance_graph(self, save_image=True):
        """Plot distance traveled over time"""
        if not self.coordinates:
            print("❌ No coordinates to plot")
            return
        
        # Extract data for plotting
        steps = [coord['step'] for coord in self.coordinates]
        distances = [coord['total_distance'] for coord in self.coordinates]
        left_sensors = [coord['sensors']['left_distance'] for coord in self.coordinates]
        right_sensors = [coord['sensors']['right_distance'] for coord in self.coordinates]
        
        # Create subplots
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle(f'Robot Movement Analysis - {len(self.coordinates)} data points', fontsize=16)
        
        # Plot 1: Total Distance Traveled
        ax1.plot(steps, distances, 'b-', linewidth=2, label='Total Distance')
        ax1.set_xlabel('Simulation Steps')
        ax1.set_ylabel('Distance Traveled (m)')
        ax1.set_title('Cumulative Distance Traveled')
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        
        # Plot 2: Sensor Readings
        ax2.plot(steps, left_sensors, 'r-', linewidth=1, label='Left Sensor', alpha=0.7)
        ax2.plot(steps, right_sensors, 'g-', linewidth=1, label='Right Sensor', alpha=0.7)
        ax2.set_xlabel('Simulation Steps')
        ax2.set_ylabel('Distance to Wall (units)')
        ax2.set_title('Sensor Readings Over Time')
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        
        # Plot 3: Robot Path (X-Y coordinates)
        x_coords = [coord['position']['x'] for coord in self.coordinates]
        y_coords = [coord['position']['y'] for coord in self.coordinates]
        
        # Color code by distance traveled
        colors = np.array(distances)
        scatter = ax3.scatter(x_coords, y_coords, c=colors, cmap='viridis', s=10, alpha=0.6)
        ax3.plot(x_coords, y_coords, 'k-', alpha=0.3, linewidth=0.5)
        ax3.set_xlabel('X Position (m)')
        ax3.set_ylabel('Y Position (m)')
        ax3.set_title('Robot Path (colored by distance traveled)')
        ax3.grid(True, alpha=0.3)
        ax3.axis('equal')
        plt.colorbar(scatter, ax=ax3, label='Distance Traveled (m)')
        
        # Plot 4: Movement Speed
        speeds = []
        for i, coord in enumerate(self.coordinates):
            if i > 0:
                dt = 1  # step difference
                dd = coord['total_distance'] - self.coordinates[i-1]['total_distance']
                speed = dd / dt if dt > 0 else 0
                speeds.append(speed)
            else:
                speeds.append(0)
        
        ax4.plot(steps, speeds, 'purple', linewidth=1, alpha=0.7)
        ax4.set_xlabel('Simulation Steps')
        ax4.set_ylabel('Speed (m/step)')
        ax4.set_title('Robot Speed Over Time')
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_image:
            filename = "robot_analysis.png"  # Fixed filename - always overwrites previous
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"📊 Graph saved as: {filename}")
        
        plt.show()
        
        # Print statistics
        print(f"\n📊 ROBOT MOVEMENT STATISTICS:")
        print(f"   🚀 Total distance traveled: {self.total_distance:.2f} meters")
        print(f"   📍 Total data points: {len(self.coordinates)}")
        print(f"   ⏱️  Session duration: {len(self.coordinates)} steps")
        print(f"   📏 Average speed: {self.total_distance/len(self.coordinates):.3f} m/step")
        
        # Sensor statistics
        avg_left = np.mean(left_sensors)
        avg_right = np.mean(right_sensors)
        print(f"   📡 Average left sensor: {avg_left:.2f}")
        print(f"   📡 Average right sensor: {avg_right:.2f}")
    
    def plot_plant_detection_map(self):
        """Plot a map showing where plants were detected"""
        if not self.coordinates:
            print("❌ No coordinates to plot")
            return
        
        # Filter coordinates with plant detections
        plant_coords = [coord for coord in self.coordinates if coord.get('plant_detections', 0) > 0]
        
        if not plant_coords:
            print("🌿 No plant detections found in coordinate data")
            return
        
        fig, ax = plt.subplots(1, 1, figsize=(12, 8))
        
        # Plot all robot positions
        all_x = [coord['position']['x'] for coord in self.coordinates]
        all_y = [coord['position']['y'] for coord in self.coordinates]
        ax.plot(all_x, all_y, 'lightgray', alpha=0.5, linewidth=1, label='Robot Path')
        
        # Plot plant detection locations
        plant_x = [coord['position']['x'] for coord in plant_coords]
        plant_y = [coord['position']['y'] for coord in plant_coords]
        plant_counts = [coord['plant_detections'] for coord in plant_coords]
        
        scatter = ax.scatter(plant_x, plant_y, c=plant_counts, cmap='Greens', 
                           s=100, alpha=0.8, edgecolors='darkgreen', linewidth=1)
        
        ax.set_xlabel('X Position (m)')
        ax.set_ylabel('Y Position (m)')
        ax.set_title(f'Plant Detection Map - {len(plant_coords)} detection locations')
        ax.grid(True, alpha=0.3)
        ax.legend()
        ax.axis('equal')
        
        plt.colorbar(scatter, ax=ax, label='Number of Plants Detected')
        
        filename = "plant_detection_map.png"  # Fixed filename - always overwrites previous
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"🌿 Plant detection map saved as: {filename}")
        
        plt.show()
    
    def get_statistics(self):
        """Get summary statistics"""
        if not self.coordinates:
            return {}
        
        return {
            'total_points': len(self.coordinates),
            'total_distance': self.total_distance,
            'session_duration_steps': len(self.coordinates),
            'average_speed': self.total_distance / len(self.coordinates) if self.coordinates else 0,
            'plant_detections': sum(coord.get('plant_detections', 0) for coord in self.coordinates),
            'detection_locations': len([c for c in self.coordinates if c.get('plant_detections', 0) > 0])
        }