# TIAGo_Pro_Navigation

Social Navigation with TIAGo Pro: A YOLO-Driven Costmap Approach
Project Overview
This project implements a Social Navigation framework for the PAL Robotics TIAGo Pro within a ROS 2, Gazebo, and RViz simulation environment. The core objective is to move beyond rigid obstacle avoidance toward a human-centric navigation model. By integrating real-time computer vision (YOLOv11n) with the Nav2 stack, we have developed a system that distinguishes human agents from static architecture, allowing the robot to respect social norms through dynamic costmap inflation.

Key Features
Vision-Integrated Perception: Utilizes a YOLOv11n pipeline to detect multiple people in the environment, translating 2D image detections into 3D spatial coordinates.

Layered Costmap Dynamics: Employs a sophisticated layered costmap architecture where human detections are injected into a dedicated Social Inflation Layer.

Optimized Path Planning: Leverages the A* global planner for pathfinding and the TEB (Timed Elastic Band) local planner for reactive, smooth trajectory generation that accounts for social comfort.

Balanced Inflation Strategy: Features a "Golden Ratio" inflation radius of 0.55m for both static and social layers. This configuration ensures the robot maintains a respectful berth around people while retaining the agility to navigate narrow corridors and doorways.

Simulation: Tested extensively in Gazebo (physics) and RViz (perception visualization) to ensure the framework is robust against real-time sensor data and dynamic human actors.

Technical Architecture
Robot: TIAGo Pro (PAL Robotics)

Detection: YOLOv11n (n-model for low-latency inference)

Navigation: ROS 2 Nav2 (A* Global / TEB Local)

Environment: Gazebo 3D Office Simulation

Methodology:
In this project, we treat the costmap as a spatial "brain," assigning values from 0 (free space) to 254 (lethal obstacle). By separating the Static Layer from our Social Inflation Layer, we successfully prevented "thick walls" while maintaining "soft" social buffers. This allows the TIAGo Pro to proactively adjust its trajectory when encountering humans, fostering a transparent and predictable interaction that enhances user trust and comfort in shared spaces.
