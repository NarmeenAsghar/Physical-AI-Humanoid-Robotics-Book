# Module Specification: Digital Twin — Gazebo + Unity Simulation

**Parent Feature**: `001-physical-ai-humanoid-book`
**Module**: 2 of 5
**Created**: 2025-12-16
**Status**: Draft
**Word Target**: 2,000–3,000 words
**Prerequisites**: Module 1 (ROS 2, URDF basics)

## Overview

This module teaches students to create digital twins of humanoid robots using Gazebo for physics simulation and Unity for high-fidelity visualization. Students learn to simulate sensors (LiDAR, depth cameras, IMU), physics (rigid body dynamics, collisions), and integrate simulation environments with ROS 2 for real-time testing before hardware deployment.

## User Scenarios & Testing

### User Story 1 - Spawn Humanoid in Gazebo (Priority: P1)

A robotics student wants to see their URDF humanoid robot in a physics-enabled simulation. They load their robot from Module 1 into Gazebo and observe it responding to gravity and collisions.

**Why this priority**: Gazebo is the primary simulation environment for ROS 2 robotics. Students need physics simulation before adding sensors or control.

**Independent Test**: Student spawns humanoid in Gazebo world, robot falls under gravity, and joints respond to physics.

**Acceptance Scenarios**:

1. **Given** a valid URDF from Module 1, **When** student launches Gazebo with spawn command, **Then** humanoid appears in the simulation world
2. **Given** a spawned robot, **When** simulation runs, **Then** robot responds to gravity (falls if unsupported, stands if balanced)
3. **Given** physics-enabled world, **When** robot contacts ground plane, **Then** collision is detected and robot doesn't fall through

---

### User Story 2 - Configure Sensor Simulation (Priority: P2)

A developer needs simulated sensor data to test perception algorithms without hardware. They add LiDAR, depth camera, and IMU plugins to their robot and receive sensor data on ROS 2 topics.

**Why this priority**: Sensor simulation enables perception pipeline development. Required for SLAM/navigation in Module 3.

**Independent Test**: Student runs `ros2 topic echo` and sees realistic sensor data streams from simulated sensors.

**Acceptance Scenarios**:

1. **Given** Gazebo with humanoid, **When** student adds LiDAR plugin, **Then** `/scan` topic publishes LaserScan messages
2. **Given** depth camera plugin configured, **When** simulation runs, **Then** `/depth/image_raw` contains depth data matching scene geometry
3. **Given** IMU plugin attached, **When** robot moves, **Then** `/imu/data` reflects acceleration and orientation changes
4. **Given** all sensors publishing, **When** student visualizes in RViz2, **Then** sensor data overlays correctly on robot model

---

### User Story 3 - Understand Physics Simulation (Priority: P3)

A researcher wants to understand how Gazebo simulates humanoid dynamics for locomotion research. They learn about rigid body dynamics, joint controllers, and collision handling.

**Why this priority**: Physics understanding is essential for realistic simulation and Sim2Real transfer.

**Independent Test**: Student can explain simulation parameters and tune physics for stable humanoid standing.

**Acceptance Scenarios**:

1. **Given** physics documentation, **When** student reads simulation concepts, **Then** they can explain time step, solver iterations, and contact parameters
2. **Given** unstable robot behavior, **When** student adjusts inertia/friction, **Then** simulation becomes more stable
3. **Given** joint effort controllers, **When** student sends position commands, **Then** joints move with appropriate dynamics

---

### User Story 4 - Unity Visualization Integration (Priority: P4)

A developer wants high-fidelity rendering for human-robot interaction demos. They connect Unity to ROS 2 and visualize the Gazebo simulation with photorealistic graphics.

**Why this priority**: Unity provides superior visualization for demos, training data generation, and HRI research. Differentiates from basic Gazebo rendering.

**Independent Test**: Student sees Unity rendering updated in real-time based on Gazebo simulation state.

**Acceptance Scenarios**:

1. **Given** ROS-Unity bridge installed, **When** student subscribes to joint states, **Then** Unity robot mirrors Gazebo robot pose
2. **Given** synchronized simulation, **When** Gazebo physics updates, **Then** Unity visualization reflects changes in real-time
3. **Given** Unity scene, **When** student adds lighting/materials, **Then** humanoid renders with photorealistic quality

---

### Edge Cases

- What if Gazebo crashes on spawn? Include URDF validation checklist and common fixes
- How to handle slow simulation (real-time factor < 1.0)? Document optimization strategies
- What if Unity-ROS bridge has latency? Provide sync troubleshooting guide
- How to debug sensor data that looks wrong? Include visualization and sanity check procedures
- What happens with invalid collision meshes? Document mesh simplification requirements

## Requirements

### Content Requirements

- **CR-001**: Chapter MUST explain Gazebo architecture and simulation loop
- **CR-002**: Chapter MUST cover URDF to SDF conversion and differences
- **CR-003**: Chapter MUST include sensor plugin configuration for LiDAR, depth camera, and IMU
- **CR-004**: Chapter MUST explain rigid body dynamics, collisions, and contact physics
- **CR-005**: Chapter MUST introduce Unity-ROS integration for visualization
- **CR-006**: Chapter MUST provide complete example of humanoid in Gazebo with all sensors

### Technical Requirements

- **TR-001**: All examples MUST run on Ubuntu 22.04 with ROS 2 Humble and Gazebo Harmonic (or Fortress)
- **TR-002**: Sensor plugins MUST use official Gazebo plugins (not deprecated ROS 1 plugins)
- **TR-003**: Unity examples MUST use ROS-TCP-Connector or ros2-for-unity
- **TR-004**: All launch files MUST follow ROS 2 Python launch format
- **TR-005**: Physics parameters MUST be documented with recommended values for humanoids

### Citation Requirements

- **CIT-001**: Chapter MUST cite official Gazebo documentation
- **CIT-002**: Chapter MUST reference at least 5 authoritative sources
- **CIT-003**: Sources SHOULD include peer-reviewed papers on robot simulation or digital twins
- **CIT-004**: All citations MUST follow APA 7th edition format

### Key Entities

- **Gazebo**: Open-source robotics simulator with physics engine, sensor simulation, and ROS 2 integration
- **SDF (Simulation Description Format)**: XML format for Gazebo worlds and models, more expressive than URDF
- **Digital Twin**: Virtual replica of physical robot synchronized with real-world state
- **Physics Engine**: Software component calculating rigid body dynamics, collisions, and constraints
- **Sensor Plugin**: Gazebo module that simulates sensor behavior and publishes data to ROS 2
- **ROS-Unity Bridge**: Middleware connecting Unity visualization to ROS 2 message system
- **Real-Time Factor**: Ratio of simulation time to wall-clock time (1.0 = real-time)

## Chapter Outline

### 1. Introduction to Digital Twins (250 words)
- What is a digital twin and why it matters for Physical AI
- Simulation-to-Real (Sim2Real) pipeline overview
- Gazebo vs Unity: complementary roles

### 2. Gazebo Fundamentals (400 words)
- Gazebo architecture: server, client, plugins
- Simulation loop and time stepping
- World files and model spawning
- **Diagram**: Gazebo architecture with ROS 2 integration

### 3. From URDF to SDF (300 words)
- URDF limitations for simulation
- SDF additional features (sensors, plugins, physics)
- Automatic conversion and manual enhancement
- **Code Example**: Enhanced SDF with Gazebo-specific tags

### 4. Physics Simulation Deep Dive (400 words)
- Rigid body dynamics fundamentals
- Collision detection and contact physics
- Joint types and controllers in Gazebo
- Tuning parameters for stable humanoid simulation
- **Diagram**: Physics simulation pipeline

### 5. Sensor Simulation (500 words)
- LiDAR plugin configuration and parameters
- Depth camera (RGBD) simulation
- IMU plugin with noise models
- Connecting sensors to ROS 2 topics
- **Code Example**: Complete sensor configuration in SDF
- **Diagram**: Sensor data pipeline from Gazebo to ROS 2

### 6. Unity for High-Fidelity Visualization (350 words)
- Unity-ROS integration options
- Setting up ROS-TCP-Connector
- Importing robot models to Unity
- Real-time pose synchronization
- **Code Example**: Unity C# subscriber for joint states

### 7. Complete Digital Twin Workflow (300 words)
- Launching Gazebo simulation with sensors
- Visualizing in RViz2 and Unity simultaneously
- Recording and playback with rosbag2
- **Code Example**: Launch file for complete digital twin

### 8. Preparing for NVIDIA Isaac (150 words)
- Limitations of Gazebo for advanced perception
- Preview: Isaac Sim photorealism and synthetic data
- Module 3 connection

### 9. Summary and Exercises (100 words)
- Key concepts recap
- 3 hands-on exercises
- Resources for further learning

## Diagrams Required

1. **Gazebo Architecture**: Server, client, plugins, ROS 2 bridge
2. **Physics Simulation Pipeline**: Forces → Solver → State update → Collision response
3. **Sensor Data Pipeline**: Gazebo sensor → Plugin → ROS 2 topic → Subscriber
4. **Digital Twin Architecture**: Physical robot ↔ Gazebo simulation ↔ Unity visualization
5. **Humanoid Sensor Placement**: Visual showing LiDAR, cameras, IMU positions on robot

## Code Examples Required

1. **Gazebo World File** (`humanoid_world.sdf`): World with ground plane, lighting, physics config
2. **Sensor SDF** (`humanoid_sensors.sdf`): Robot model with LiDAR, depth camera, IMU plugins
3. **Launch File** (`gazebo_bringup.launch.py`): Spawns world and robot with all sensors
4. **Unity Subscriber** (`JointStateSubscriber.cs`): C# script receiving ROS 2 joint states
5. **Complete Launch** (`digital_twin.launch.py`): Full simulation with RViz2 visualization

## Success Criteria

### Reader Outcomes

- **SC-001**: Reader can spawn humanoid in Gazebo within 15 minutes of starting module
- **SC-002**: Reader can configure all three sensor types (LiDAR, depth, IMU) and see data in RViz2
- **SC-003**: Reader can explain physics parameters and their effect on simulation stability
- **SC-004**: Reader can set up Unity-ROS bridge and see synchronized visualization
- **SC-005**: Reader can run complete digital twin workflow with recording/playback

### Content Quality

- **SC-006**: Word count between 2,000-3,000 words
- **SC-007**: Flesch-Kincaid grade level 10-12
- **SC-008**: All examples execute without errors on fresh ROS 2 Humble + Gazebo Harmonic install
- **SC-009**: Minimum 5 citations from authoritative simulation/robotics sources
- **SC-010**: All diagrams clearly illustrate data flow and architecture

## Dependencies

- Module 1 completion (URDF, ROS 2 basics)
- Ubuntu 22.04 LTS
- ROS 2 Humble Hawksbill
- Gazebo Harmonic (or Fortress for compatibility)
- Unity 2022.3 LTS (for visualization section)
- ROS-TCP-Connector package
- GPU recommended for Unity visualization

## Out of Scope

- Gazebo Classic (deprecated) — focus on new Gazebo (Ignition lineage)
- Custom plugin development (beyond configuration)
- Unity physics simulation (use Gazebo for physics)
- Photorealistic rendering in Gazebo (covered in Isaac Sim, Module 3)
- Multi-robot simulation
- Cloud-based simulation deployment

## Assumptions

- Reader completed Module 1 with working ROS 2 workspace and URDF
- Reader has basic familiarity with 3D graphics concepts
- Reader has sufficient GPU for Unity visualization (integrated GPU acceptable)
- Gazebo Harmonic is compatible with reader's ROS 2 installation
- Unity Hub and Unity Editor can be installed on reader's system
