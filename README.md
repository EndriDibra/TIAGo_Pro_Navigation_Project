# TIAGo_Pro_Navigation

## Author
**Endri Dibra**

---

## Social Navigation with TIAGo Pro: A YOLO-Driven Costmap Approach

## Project Overview

This project implements a **social navigation framework** for the :contentReference[oaicite:0]{index=0} in a **ROS 2, Gazebo, and RViz simulation environment**.

The goal is to extend classical robotic navigation into **human-aware motion planning**, where the robot adapts its path based on social context rather than purely geometric constraints.

The system integrates real-time perception using :contentReference[oaicite:1]{index=1} with the :contentReference[oaicite:2]{index=2} to generate socially compliant trajectories.

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
- :contentReference[oaicite:3]{index=3} for physics simulation
- :contentReference[oaicite:4]{index=4} for real-time visualization

---

# System Architecture

- **Robot Platform:** :contentReference[oaicite:5]{index=5}  
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
