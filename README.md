# TIAGo_Pro_Navigation

## Author
**Endri Dibra**

---

## Social Navigation with TIAGo Pro: A YOLO-Driven Costmap Approach

## Project Overview

This project implements a **social navigation framework** for the :contentReference[oaicite:0]{index=0} within a **ROS 2, Gazebo, and RViz simulation environment**.

The goal is to move beyond classical obstacle avoidance and instead enable **human-aware navigation**, where the robot behaves in a socially acceptable manner in shared environments.

By integrating real-time computer vision using :contentReference[oaicite:1]{index=1} with the :contentReference[oaicite:2]{index=2} framework, the system dynamically distinguishes between static obstacles and humans, and adapts its navigation behavior accordingly.

---

## Key Features

### Vision-Integrated Perception
- Real-time human detection using YOLOv11n  
- Conversion of 2D detections into 3D spatial awareness  
- Multi-person tracking in dynamic environments  

### Layered Costmap Dynamics
- Extension of the ROS 2 costmap system  
- Dedicated **Social Inflation Layer**  
- Separation of:
  - Static obstacles (walls, furniture)
  - Dynamic social agents (humans)

### Optimized Path Planning
- Global planning using A* algorithm  
- Local trajectory optimization using TEB (Timed Elastic Band) planner  
- Smooth, collision-free, and socially compliant motion  

### Balanced Social Inflation Strategy
- Tuned inflation radius: **0.55m**  
- Represents a “social comfort zone”  
- Balances:
  - Human safety and comfort  
  - Robot agility in narrow spaces  

### Simulation Environment
- :contentReference[oaicite:3]{index=3} for physics-based testing  
- :contentReference[oaicite:4]{index=4} for perception and navigation debugging  
- Real-time interaction with dynamic human agents  

---

## Technical Architecture

- **Robot Platform:** :contentReference[oaicite:5]{index=5}  
- **Framework:** ROS 2 (Humble) + Nav2 stack  
- **Detection Model:** YOLOv11n (low-latency inference)  
- **Planner Stack:**
  - Global Planner → A*
  - Local Planner → TEB (Timed Elastic Band)  
- **Simulation World:** PAL Office Gazebo environment  

---

## Methodology

The system treats the **costmap as a spatial reasoning layer ("robot brain")**, where:

- `0` → Free space  
- `254` → Lethal obstacle  

Instead of treating all obstacles equally, the system introduces a **semantic separation**:

### 1. Static Layer
- Walls, furniture, and fixed objects  
- Hard constraints for navigation  

### 2. Social Inflation Layer
- Humans detected via YOLO  
- Soft, dynamic cost regions  
- Adjustable “comfort zones” around people  

This separation avoids over-inflation of the environment, preventing narrow corridors from becoming impassable while still maintaining safe human distances.

---

## Behavioral Outcome

The resulting robot behavior is:

- Predictable in human environments  
- Respectful of personal space  
- Capable of smooth trajectory adaptation  
- Robust in dynamic scenarios with moving people  

This significantly improves **human trust, comfort, and acceptance** in shared spaces.

---

## Automation Scripts

### advancedDetector.sh

This script launches the YOLO-based detection pipeline inside a Docker-based ROS 2 simulation container.

Key functions:
- Verifies container status (`tiago_sim`)
- Enters ROS 2 workspace
- Sources ROS 2 Humble environment  
- Executes detection node:
  - `advancedYoloDetector.py`
- Ensures simulation time synchronization (`use_sim_time:=true`)

Core role:
> Runs the real-time perception layer of the social navigation system.

---

### advancedNavigation.sh

This script initializes the full navigation simulation environment.

Key steps:

#### 1. System Cleanup
- Terminates:
  - Gazebo
  - RViz
  - ROS 2 processes  
- Removes existing Docker container  

#### 2. GUI Permissions
- Enables X11 forwarding for Docker GUI applications  

#### 3. Simulation Launch
Runs the :contentReference[oaicite:6]{index=6} launch system with:
- TIAGo Pro robot in Gazebo  
- Omni-directional base  
- Navigation enabled  
- PAL Office world loaded  

---

## System Pipeline

1. Camera stream → YOLOv11 detection  
2. Detection → 3D costmap injection  
3. Costmap layering → static + social inflation  
4. Nav2 planning:
   - Global path (A*)
   - Local refinement (TEB)  
5. Robot executes socially-aware trajectory  

---

## Summary

This project demonstrates a **human-centric evolution of robot navigation**, where motion planning is no longer purely geometric, but also **socially contextual**.

It bridges:
- Computer Vision  
- ROS 2 Robotics  
- Human-aware AI planning  
- Real-time simulation systems  

The result is a navigation system that behaves not just efficiently, but appropriately in shared human environments.

---
