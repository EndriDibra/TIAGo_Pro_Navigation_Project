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

### Core Python Dependencies for ROS2 (Humble Distro)

```bash
pip install numpy
pip install opencv-python
pip install ultralytics
pip install rclpy
pip install cv_bridge
```
---

# Installation Guide (Full System Setup)

---

### Step 1: Open WSL Ubuntu (in PowerShell)

Install the Ubuntu terminal on Windows and Run on a PowerShell Terminal:

```bash
ubuntu
```

---

## Step 2: Build the Docker Image (in Ubuntu)

Inside the WSL terminal, create a Dockerfile and build the image. This installs ROS 2 Humble, PAL Robotics packages, and YOLO AI dependencies.

### Dockerfile: 

```bash
FROM osrf/ros:humble-desktop

# 1. Install System Dependencies & Python Tools
RUN apt-get update && apt-get install -y \
    python3-colcon-common-extensions \
    python3-pip \
    git wget python3-rosdep \
    && rm -rf /var/lib/apt/lists/*

# 2. Install TIAGo Pro & Nav2 ROS Dependencies
RUN apt-get update && apt-get install -y \
    ros-humble-nav2-bringup \
    ros-humble-navigation2 \
    ros-humble-robot-localization \
    ros-humble-slam-toolbox \
    ros-humble-twist-mux \
    ros-humble-teleop-twist-keyboard \
    ros-humble-gazebo-ros-pkgs \
    ros-humble-cartographer-ros \
    ros-humble-sensor-msgs \
    ros-humble-cv-bridge \
    ros-humble-vision-opencv \
    && rm -rf /var/lib/apt/lists/*

# 3. Install Python AI Dependencies
RUN pip3 install numpy opencv-python ultralytics

# 4. Create Workspace and Clone TIAGo Packages
WORKDIR /tiago_ws/src
RUN git clone https://github.com/pal-robotics/tiago_simulation.git && \
    git clone https://github.com/pal-robotics/tiago_robot.git && \
    git clone https://github.com/pal-robotics/pal_navigation_msgs.git && \
    git clone https://github.com/pal-robotics/pal_gazebo_plugins.git

# 5. Build the Workspace
WORKDIR /tiago_ws
RUN . /opt/ros/humble/setup.sh && \
    rosdep update && \
    rosdep install --from-paths src --ignore-src -r -y && \
    colcon build --symlink-install

# 6. Automatic Sourcing
RUN echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc \
    && echo "source /tiago_ws/install/setup.bash" >> ~/.bashrc

CMD ["bash"]
```

---

### Build Image:

```bash
docker build -t tiago_pro_image .
```

---

### Step 3: Create the Docker Container (in Ubuntu)

```bash
docker create -it \
    --name tiago_sim \
    --privileged \
    --net=host \
    -e DISPLAY=host.docker.internal:0.0 \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    tiago_pro_image
```

---

### Step 4: Setup GUI Forwarding-XLaunch (in Windows)

#### Before running the simulation, install and then start XLaunch on Windows with these settings:

- Multiple Windows
- Display Number: 0
- Start no client
- Check: "Disable access control"

### Step 5: Start the Docker Container (in Ubuntu)

Check containers:

```bash
docker ps -a
```

Start container:

```bash
docker start tiago_sim
```

Enter container:

```bash
docker exec -it tiago_sim bash
```

---

## Step 5: Prepare Execution Scripts (Inside Docker)

Ensure your scripts are executable

```bash
chmod +x advancedNavigation.sh
chmod +x advancedDetector.sh
```

---

## Step 6: Launch the System (Inside Docker)

1. Launch Simulation (Terminal 1)
Run the navigation script to start Gazebo and the TIAGo Pro navigation stack

```bash
./advancedNavigation.sh
```

2. Launch YOLO Detector (Terminal 2)
Once the simulation is running, open a new terminal and start the AI detection node

```bash
./advancedDetector.sh
```

---

## Step 7: VS Code (Inside Docker)

To edit your scripts or ROS 2 code directly inside the environment:

- Open VS Code.

- Use the Dev Containers extension.

- Select "Attach to Running Container" -> tiago_sim.

- Open the folder /tiago_ws/src to begin development.

# Docker Scripts

## advancedNavigation.sh

- Cleans Gazebo, RViz, ROS processes
- Launches TIAGo Pro simulation container
- Loads PAL Office world
- Enables Nav2 navigation stack
- Sets up GUI forwarding (X11)

## advancedDetector.sh

- Checks running Docker container (tiago_sim)
- Enters ROS 2 workspace
- Sources ROS environment
Runs:

```bash
./advancedYoloDetector.py
```
- Enables synchronized simulation time

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

- Maintaining safe distances from humans
- Smooth trajectory adaptation
- Predictable and non-intrusive motion
- Real-time environment awareness
- Seamless integration of perception and planning

# Summary

This project combines:

- Computer Vision (YOLOv11)
- ROS 2 Navigation (Nav2)
- 3D Simulation (Gazebo + RViz)
- Depth-based perception
- Social costmap engineering
- Real-time robotic control

The result is a human-aware autonomous navigation system capable of operating safely and naturally in shared human environments.
