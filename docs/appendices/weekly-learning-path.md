---
sidebar_position: 4
title: "Weekly Breakdown and Learning Path"
description: 13-week course timeline for Physical AI and humanoid robotics
---

# Weekly Breakdown and Learning Path

This 13-week curriculum guides learners from ROS 2 fundamentals to deploying an autonomous voice-controlled humanoid robot. Each week combines conceptual learning with hands-on lab exercises, building progressively toward the capstone demonstration.

---

## Course Structure Overview

| Phase | Weeks | Focus | Modules |
|-------|-------|-------|---------|
| **Foundation** | 1-3 | ROS 2 and robot description | Module 1 |
| **Simulation** | 4-6 | Digital twin and physics | Module 2 |
| **Perception** | 7-9 | Isaac, VSLAM, navigation | Module 3 |
| **Intelligence** | 10-11 | VLA and natural language | Module 4 |
| **Integration** | 12-13 | Capstone project | Capstone |

---

## Phase 1: Foundation (Weeks 1-3)

### Week 1: Introduction to Physical AI and ROS 2

**Topics**:
- What is Physical AI? Embodied intelligence concepts
- ROS 2 architecture: nodes, topics, services, actions
- Development environment setup

**Lab**: Install ROS 2 Humble, create first workspace, run `ros2 topic` and `ros2 node` commands

**Reading**: Introduction, Module 1 (Architecture section)

**Outcome**: Explain ROS 2 communication primitives; run basic ROS 2 commands

---

### Week 2: ROS 2 Programming with Python

**Topics**:
- rclpy node development
- Publishers and subscribers
- Launch files and parameters
- QoS policies for sensor data

**Lab**: Build IMU publisher and sensor subscriber nodes; create multi-node launch file

**Reading**: Module 1 (Python, URDF section - first half)

**Outcome**: Create ROS 2 packages with Python nodes that communicate via topics

---

### Week 3: URDF and Humanoid Robot Description

**Topics**:
- URDF structure: links, joints, materials
- Joint types for humanoid robots
- Visualization with RViz2
- URDF validation and debugging

**Lab**: Build humanoid URDF (torso, head, arms); visualize in RViz2 with joint state publisher

**Reading**: Module 1 (URDF section)

**Outcome**: Create valid URDF for humanoid robot; visualize and manipulate joints in RViz2

**Assessment**: Quiz 1 - ROS 2 fundamentals and URDF concepts

---

## Phase 2: Simulation (Weeks 4-6)

### Week 4: Gazebo Fundamentals

**Topics**:
- Digital twin concepts and Sim2Real
- Gazebo architecture and SDF format
- Physics engines and simulation parameters
- Spawning robots in Gazebo worlds

**Lab**: Load humanoid URDF into Gazebo; configure physics for stable simulation

**Reading**: Module 2 (Gazebo section)

**Outcome**: Launch Gazebo simulation with humanoid robot responding to physics

---

### Week 5: Sensor Simulation

**Topics**:
- Gazebo sensor plugins (LiDAR, camera, IMU)
- Noise models for realistic sensing
- ROS 2 bridge configuration
- Visualizing sensor data in RViz2

**Lab**: Add LiDAR, depth camera, and IMU to humanoid; verify data on ROS 2 topics

**Reading**: Module 2 (Sensor simulation section)

**Outcome**: Configure simulated sensors publishing to ROS 2; visualize in RViz2

---

### Week 6: Unity Integration and Synthetic Data

**Topics**:
- Unity for high-fidelity visualization
- ROS-TCP-Connector setup
- Synthetic data generation concepts
- Domain randomization basics

**Lab**: Import humanoid to Unity; synchronize with Gazebo via ROS 2 bridge

**Reading**: Module 2 (Unity section)

**Outcome**: Run synchronized Gazebo physics + Unity visualization

**Assessment**: Lab Report 1 - Digital twin implementation with sensor data analysis

---

## Phase 3: Perception (Weeks 7-9)

### Week 7: NVIDIA Isaac Sim

**Topics**:
- Isaac Sim architecture and USD format
- Photorealistic rendering for perception
- Isaac Sim ROS 2 bridge
- Scene composition and lighting

**Lab**: Load humanoid in Isaac Sim; configure cameras and ROS 2 publishing

**Reading**: Module 3 (Isaac Sim section)

**Outcome**: Run Isaac Sim with humanoid robot and sensor streams

---

### Week 8: Visual SLAM and Perception

**Topics**:
- VSLAM fundamentals and Isaac ROS
- GPU-accelerated perception pipelines
- Depth processing and point clouds
- Localization accuracy evaluation

**Lab**: Configure Isaac ROS VSLAM; build map while navigating humanoid

**Reading**: Module 3 (Perception section)

**Outcome**: Run VSLAM with accurate pose estimation; generate environment map

---

### Week 9: Autonomous Navigation with Nav2

**Topics**:
- Nav2 architecture and costmaps
- Global and local planners
- Behavior trees for navigation logic
- Integration with Isaac perception

**Lab**: Configure Nav2 with VSLAM odometry; send navigation goals via RViz2

**Reading**: Module 3 (Navigation section)

**Outcome**: Humanoid navigates autonomously to goal positions avoiding obstacles

**Assessment**: Quiz 2 - Perception and navigation concepts

---

## Phase 4: Intelligence (Weeks 10-11)

### Week 10: Speech Recognition and LLM Planning

**Topics**:
- Vision-Language-Action paradigm
- Whisper for speech-to-text
- LLM-based cognitive planning
- Prompt engineering for robotics

**Lab**: Deploy Whisper node; build LLM planner generating action sequences

**Reading**: Module 4 (Speech and Planning sections)

**Outcome**: Voice commands transcribed and converted to structured action plans

---

### Week 11: Action Execution and Object Grounding

**Topics**:
- ROS 2 action execution patterns
- Object detection and 3D localization
- Connecting language to physical objects
- End-to-end VLA pipeline integration

**Lab**: Build action executor; integrate object detection for grounding commands

**Reading**: Module 4 (Execution and Vision sections)

**Outcome**: Complete VLA pipeline from voice command to robot action

**Assessment**: Lab Report 2 - VLA system demonstration with three command scenarios

---

## Phase 5: Integration (Weeks 12-13)

### Week 12: Capstone Integration

**Topics**:
- System integration patterns
- Error handling and recovery
- Performance optimization
- Testing and validation strategies

**Lab**: Integrate all modules into unified system; debug cross-component issues

**Reading**: Capstone documentation

**Outcome**: Fully integrated system accepting voice commands and executing tasks

---

### Week 13: Capstone Demonstration and Review

**Topics**:
- Demonstration best practices
- Documentation and presentation
- Future directions in Physical AI
- Course review and reflection

**Lab**: Final capstone demonstration; peer review and feedback

**Outcome**: Successfully demonstrate voice-commanded humanoid completing multi-step task

**Assessment**: Capstone Project - Live demonstration + technical report

---

## Assessment Overview

| Assessment | Week | Weight | Format |
|------------|------|--------|--------|
| Quiz 1 | 3 | 10% | ROS 2 and URDF concepts |
| Lab Report 1 | 6 | 20% | Digital twin implementation |
| Quiz 2 | 9 | 10% | Perception and navigation |
| Lab Report 2 | 11 | 20% | VLA system demonstration |
| Capstone | 13 | 40% | Live demo + report |

### Capstone Evaluation Criteria

| Criterion | Weight | Description |
|-----------|--------|-------------|
| Functionality | 40% | Robot completes commanded task |
| Integration | 25% | All modules work together seamlessly |
| Code Quality | 15% | Clean, documented, follows ROS 2 conventions |
| Presentation | 10% | Clear demonstration and explanation |
| Documentation | 10% | Technical report with architecture diagram |

---

## Learning Outcomes by Phase

### After Phase 1 (Foundation)
- Create ROS 2 packages with Python nodes
- Design humanoid robot descriptions with URDF
- Explain communication patterns for robotic systems

### After Phase 2 (Simulation)
- Build digital twins with physics simulation
- Configure simulated sensors with realistic properties
- Generate synthetic data for perception training

### After Phase 3 (Perception)
- Deploy GPU-accelerated perception pipelines
- Implement VSLAM for localization and mapping
- Configure autonomous navigation systems

### After Phase 4 (Intelligence)
- Integrate speech recognition with robotics
- Build LLM-based task planners
- Connect natural language to physical actions

### After Phase 5 (Integration)
- Integrate complex multi-component systems
- Debug cross-domain robotics issues
- Demonstrate autonomous humanoid capabilities

---

## Recommended Weekly Schedule

| Activity | Hours | Description |
|----------|-------|-------------|
| Reading | 2-3 | Module content and references |
| Lecture/Discussion | 2 | Conceptual overview and Q&A |
| Lab Work | 4-6 | Hands-on implementation |
| Review/Practice | 1-2 | Self-assessment and debugging |
| **Total** | **9-13** | Per week |

This schedule assumes students have programming experience and can dedicate part-time hours. Full-time learners may progress faster; working professionals may extend to 16-20 weeks.
