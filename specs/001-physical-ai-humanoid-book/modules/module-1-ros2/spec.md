# Module Specification: ROS 2 — The Robotic Nervous System

**Parent Feature**: `001-physical-ai-humanoid-book`
**Module**: 1 of 5
**Created**: 2025-12-16
**Status**: Draft
**Word Target**: 2,000–3,000 words

## Overview

This module introduces ROS 2 (Robot Operating System 2) as the foundational communication and control layer for humanoid robots. Students learn how ROS 2 functions as a "robotic nervous system" — enabling distributed sensor processing, motor control, and AI integration through a publish-subscribe architecture.

## User Scenarios & Testing

### User Story 1 - Understand ROS 2 Architecture (Priority: P1)

A robotics student new to ROS 2 wants to understand how the middleware enables communication between robot components. They read the architecture section and can explain nodes, topics, services, and actions with clear mental models.

**Why this priority**: Conceptual foundation required before any hands-on work. Without understanding the architecture, students cannot debug or extend ROS 2 systems.

**Independent Test**: Student can draw a ROS 2 node graph from a description and explain data flow.

**Acceptance Scenarios**:

1. **Given** a student with basic programming knowledge, **When** they complete the architecture section, **Then** they can explain the difference between topics (async) and services (sync)
2. **Given** the node graph diagram, **When** a student traces a sensor reading, **Then** they can identify publisher, subscriber, and message type
3. **Given** a robotic task description, **When** asked to design communication, **Then** student chooses appropriate ROS 2 primitives (topic vs service vs action)

---

### User Story 2 - Build First ROS 2 Package (Priority: P2)

A developer wants to create their first ROS 2 package with Python nodes that communicate. They follow the tutorial and have a working publisher-subscriber pair within 30 minutes.

**Why this priority**: Hands-on validation of concepts. Students need working code to build confidence and debug understanding.

**Independent Test**: Student runs `ros2 topic list` and sees their custom topic with messages flowing.

**Acceptance Scenarios**:

1. **Given** a fresh ROS 2 Humble installation, **When** student follows the package creation steps, **Then** `colcon build` succeeds without errors
2. **Given** a publisher node, **When** student runs `ros2 topic echo`, **Then** they see sensor data messages at expected frequency
3. **Given** publisher and subscriber nodes, **When** both are launched, **Then** subscriber callback executes and logs received data

---

### User Story 3 - Create Humanoid URDF (Priority: P3)

A maker wants to describe a humanoid robot's physical structure for simulation. They complete the URDF section and have a valid robot description that loads in RViz2.

**Why this priority**: URDF is prerequisite for Gazebo simulation (Module 2). Students need robot models before simulating physics.

**Independent Test**: Student runs `ros2 launch` with their URDF and sees humanoid skeleton in RViz2 with movable joints.

**Acceptance Scenarios**:

1. **Given** the URDF template, **When** student adds links and joints, **Then** `check_urdf` validates without errors
2. **Given** a valid URDF, **When** loaded in RViz2, **Then** robot displays with correct link hierarchy
3. **Given** joint state publisher, **When** student moves sliders, **Then** corresponding joints rotate in visualization

---

### User Story 4 - Integrate AI Agent with ROS 2 (Priority: P4)

A researcher wants to connect an LLM or control policy to ROS 2. They implement a Python node using rclpy that receives sensor data and publishes commands.

**Why this priority**: Bridges traditional robotics with modern AI. Prepares students for VLA module (Module 4).

**Independent Test**: Student's AI node receives simulated sensor data, processes it, and publishes motor commands.

**Acceptance Scenarios**:

1. **Given** rclpy node template, **When** student subscribes to `/imu/data`, **Then** callback receives IMU messages
2. **Given** decision logic in callback, **When** condition is met, **Then** node publishes to `/cmd_vel`
3. **Given** launch file with AI node, **When** executed, **Then** node initializes and connects to ROS 2 graph

---

### Edge Cases

- What if ROS 2 installation fails on student's system? Provide Docker container and WSL2 alternatives
- How to handle ROS 2 Humble vs Iron differences? Document version-specific commands with tabs
- What if `colcon build` fails with dependency errors? Include troubleshooting section with common fixes
- How to debug silent node failures? Teach `ros2 node list`, `ros2 topic hz`, and logging best practices

## Requirements

### Content Requirements

- **CR-001**: Chapter MUST explain ROS 2 architecture with node, topic, service, action definitions
- **CR-002**: Chapter MUST include at least one diagram showing ROS 2 node graph for humanoid robot
- **CR-003**: Chapter MUST provide complete, runnable Python examples for publisher and subscriber
- **CR-004**: Chapter MUST cover launch files with parameter configuration
- **CR-005**: Chapter MUST include humanoid URDF skeleton with at least torso, head, and one arm
- **CR-006**: Chapter MUST demonstrate rclpy integration pattern for AI agents

### Technical Requirements

- **TR-001**: All code MUST run on Ubuntu 22.04 with ROS 2 Humble
- **TR-002**: All packages MUST follow ROS 2 naming conventions (snake_case)
- **TR-003**: URDF MUST pass `check_urdf` validation
- **TR-004**: Examples MUST include expected terminal output for verification
- **TR-005**: Launch files MUST use ROS 2 Python launch format (not XML)

### Citation Requirements

- **CIT-001**: Chapter MUST cite official ROS 2 documentation for architecture concepts
- **CIT-002**: Chapter MUST reference at least 5 authoritative sources
- **CIT-003**: Sources MUST include ROS 2 design documents or peer-reviewed robotics papers
- **CIT-004**: All citations MUST follow APA 7th edition format

### Key Entities

- **Node**: A ROS 2 process that performs computation; communicates via topics/services/actions
- **Topic**: Named bus for asynchronous publish-subscribe messaging with typed messages
- **Service**: Synchronous request-response communication between nodes
- **Action**: Long-running tasks with feedback and cancellation support
- **URDF**: XML format describing robot's physical structure (links, joints, visuals, collisions)
- **Launch File**: Python script that starts multiple nodes with configuration
- **rclpy**: Python client library for ROS 2 node development

## Chapter Outline

### 1. Introduction to the Robotic Nervous System (300 words)
- Why robots need middleware
- ROS 2 vs ROS 1: key improvements (DDS, real-time, security)
- The nervous system analogy: sensors → processing → actuators

### 2. ROS 2 Architecture Deep Dive (500 words)
- **Nodes**: Processes and executors
- **Topics**: Publish-subscribe with QoS policies
- **Services**: Synchronous request-response
- **Actions**: Goal-feedback-result lifecycle
- **Diagram**: Humanoid robot node graph (sensors, control, AI)

### 3. Building Your First ROS 2 Package (600 words)
- Workspace setup: `mkdir -p ~/ros2_ws/src`
- Package creation: `ros2 pkg create`
- Publisher node: IMU data simulator
- Subscriber node: Data logger
- Build and run: `colcon build`, `ros2 run`
- **Code Example**: Complete publisher/subscriber pair

### 4. Launch Files and Parameters (400 words)
- Python launch file structure
- Loading parameters from YAML
- Remapping topics and namespaces
- **Code Example**: Multi-node launch with parameters

### 5. URDF for Humanoid Robots (500 words)
- Link and joint definitions
- Visual and collision geometries
- Inertial properties for physics simulation
- Joint types: revolute, prismatic, fixed
- **Code Example**: Humanoid torso-head-arm URDF
- Validation: `check_urdf` and RViz2 visualization

### 6. Connecting AI Agents via rclpy (400 words)
- Node lifecycle and callbacks
- Subscribing to sensors, publishing commands
- Timer-based control loops
- Integration pattern: AI decision → ROS 2 action
- **Code Example**: Simple reactive controller

### 7. Preparing for Simulation (200 words)
- Workspace structure for Gazebo integration
- Package dependencies for simulation
- Preview: Module 2 Digital Twin

### 8. Summary and Exercises (100 words)
- Key concepts recap
- 3 hands-on exercises for practice
- Resources for further learning

## Diagrams Required

1. **ROS 2 Architecture Overview**: Nodes, topics, services in abstract
2. **Humanoid Robot Node Graph**: Specific nodes for IMU, camera, joint control, AI planner
3. **URDF Link Hierarchy**: Visual tree of humanoid robot structure
4. **rclpy Integration Pattern**: Data flow from sensor → AI → actuator

## Code Examples Required

1. **IMU Publisher Node** (`imu_publisher.py`): Publishes simulated IMU data
2. **Data Subscriber Node** (`data_subscriber.py`): Logs received sensor data
3. **Launch File** (`humanoid_bringup.launch.py`): Starts multiple nodes with params
4. **Humanoid URDF** (`humanoid_base.urdf`): Torso, head, one arm with joints
5. **AI Controller Node** (`ai_controller.py`): Receives sensors, publishes commands

## Success Criteria

### Reader Outcomes

- **SC-001**: Reader can create ROS 2 workspace and build packages within 30 minutes
- **SC-002**: Reader can explain node/topic/service/action differences without reference
- **SC-003**: Reader's URDF loads in RViz2 without errors
- **SC-004**: Reader can trace data flow through node graph diagram
- **SC-005**: Reader's AI node successfully receives and publishes ROS 2 messages

### Content Quality

- **SC-006**: Word count between 2,000-3,000 words
- **SC-007**: Flesch-Kincaid grade level 10-12
- **SC-008**: All code examples execute without errors on fresh ROS 2 Humble install
- **SC-009**: Minimum 5 citations from authoritative ROS 2 sources
- **SC-010**: All diagrams follow standard ROS 2 visualization conventions

## Dependencies

- Ubuntu 22.04 LTS
- ROS 2 Humble Hawksbill
- Python 3.10+
- colcon build tools
- RViz2 for visualization
- (Optional) VS Code with ROS extension

## Out of Scope

- ROS 1 migration details
- Multi-machine ROS 2 setup
- Custom message type creation (covered in later modules)
- DDS vendor configuration
- Real-time kernel setup
- Hardware driver development

## Assumptions

- Reader has Python programming experience
- Reader has Linux command-line familiarity
- Reader has ROS 2 Humble installed (or follows installation appendix)
- Reader has 4GB+ RAM and 20GB+ disk space
