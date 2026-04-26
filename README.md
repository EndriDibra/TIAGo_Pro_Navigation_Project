# TIAGo_Pro_Navigation

## Author
**Endri Dibra**

---

## Social Navigation with TIAGo Pro: A YOLO-Driven Costmap Approach

## Project Overview

This project implements a **social navigation framework** in a **ROS 2, Gazebo, and RViz simulation environment**.

The goal is to extend classical robotic navigation into **human-aware motion planning**, where the robot adapts its path based on social context rather than purely geometric constraints.

The system integrates real-time perception to generate socially compliant trajectories.

---

# Key Features

## Vision-Integrated Perception
- Real-time person detection using YOLOv11n
- RGB + Depth fusion for 3D localization
- Conversion of detections into navigation-relevant spatial coordinates

## Social Costmap Injection
- Virtual obstacle generation from human detections
- Injection into ROS 2 costmap as dynamic obstacles
- Human-aware “social inflation layer”

## Navigation Stack
- Global Planner: A*
- Local Planner: TEB (Timed Elastic Band)
- Smooth and reactive trajectory execution

## Simulation Environment
- **Gazebo** for physics simulation
- **RViz** for real-time visualization

---

# System Architecture

- **Robot Platform:** TIAGo Pro from PAL 
- **Framework:** ROS 2 Humble  
- **Detection Model:** YOLOv11n  
- **Sensors:**
  - RGB camera
  - Depth camera  
- **Output:**
  - Virtual `/human_detection_scan` topic (LaserScan)
  - Dynamic costmap updates for Nav2  

---

# Methodology

The system transforms vision detections into navigation constraints:

### Pipeline

1. RGB image → YOLO person detection  
2. Depth image → distance estimation  
3. Pixel → 3D spatial projection  
4. Detection → Virtual LaserScan generation  
5. LaserScan → costmap injection  
6. Nav2 → dynamic replanning  

---

# Advanced Detector Node

## File: `advancedYoloDetector.py`

### Purpose
A ROS 2 node that detects humans and injects them into the navigation stack as dynamic obstacles.

---

### Behavior

- Subscribes to:
  - `/head_front_camera/rgb/image_raw`
  - `/head_front_camera/depth/image_raw`

- Publishes:
  - `/human_detection_scan` (LaserScan)

- Uses YOLOv11n to detect people in real time
- Uses depth camera to estimate distance
- Converts detections into angular laser slices
- Injects synthetic obstacles into Nav2 costmap

---

### Core Python Dependencies

```bash
pip install numpy
pip install opencv-python
pip install ultralytics
pip install rclpy
pip install cv_bridge

# ROS 2 Dependencies
sudo apt install ros-humble-nav2-bringup
sudo apt install ros-humble-sensor-msgs
sudo apt install ros-humble-cv-bridge
sudo apt install ros-humble-vision-opencv
```
---

# Installation Guide (Full System Setup)

## Step 1 Create Workspace

```bash
mkdir -p ~/tiago_ws/src
cd ~/tiago_ws/src
```

---

## Step 2 Clone TIAGo Pro Official Packages

```bash
git clone https://github.com/pal-robotics/tiago_simulation.git
git clone https://github.com/pal-robotics/tiago_robot.git
git clone https://github.com/pal-robotics/pal_navigation_msgs.git
git clone https://github.com/pal-robotics/pal_gazebo_plugins.git
```

---

## Step 3 Install Dependencies

```bash
cd ~/tiago_ws
rosdep install --from-paths src --ignore-src -r -y
```

---

## Step 4 Build Workspace

```bash
colcon build
source install/setup.bash
```

---

## Step 5 Launch Simulation (Gazebo + Nav2)

```bash
ros2 launch tiago_gazebo tiago_gazebo.launch.py \
  base_type:=omni_base \
  navigation:=True \
  is_public_sim:=True \
  world_name:=pal_office
```

---

## Step 6 Run Advanced YOLO Detector

```bash
python3 advancedYoloDetector.py --ros-args -p use_sim_time:=true
```

---

## Step 7 Docker Execution (Optional)

### Start Simalation

```bash
bash advancedNavigation.sh
```

### Start Detector Node

```bash
bash advancedDetector.sh
```

---

# Docker Scripts

## advancedNavigation.sh

Cleans Gazebo, RViz, ROS processes
Launches TIAGo Pro simulation container
Loads PAL Office world
Enables Nav2 navigation stack
Sets up GUI forwarding (X11)

## advancedDetector.sh

Checks running Docker container (tiago_sim)
Enters ROS 2 workspace
Sources ROS environment
Runs:

```bash
./advancedYoloDetector.py
```
Enables synchronized simulation time

# System Behavior

When running correctly:

1. TIAGo Pro moves in Gazebo environment
2. YOLO detects humans in real time
3. Depth camera estimates distance
4. Virtual LaserScan is generated
5. Nav2 updates costmap dynamically
6. Robot replans path socially

# Result

The robot demonstrates socially-aware navigation, characterized by:

Maintaining safe distances from humans
Smooth trajectory adaptation
Predictable and non-intrusive motion
Real-time environment awareness
Seamless integration of perception and planning

# Summary

This project combines:

Computer Vision (YOLOv11)
ROS 2 Navigation (Nav2)
3D Simulation (Gazebo + RViz)
Depth-based perception
Social costmap engineering
Real-time robotic control

The result is a human-aware autonomous navigation system capable of operating safely and naturally in shared human environments.
