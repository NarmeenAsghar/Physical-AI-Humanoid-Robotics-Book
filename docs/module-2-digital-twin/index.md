---
sidebar_position: 1
title: "Module 2: Digital Twin with Gazebo"
description: Creating physics-enabled simulations for humanoid robots using Gazebo
---

# Module 2: Digital Twin with Gazebo

## Learning Objectives

By the end of this module, you will be able to:

- Explain the role of digital twins in Physical AI development
- Launch Gazebo simulations with humanoid robots
- Configure physics parameters for stable simulation
- Set up simulated sensors (LiDAR, depth camera, IMU)
- Integrate simulation data with ROS 2 for perception testing

## Prerequisites

- Completed Module 1 (ROS 2 fundamentals, URDF)
- Working ROS 2 Humble workspace
- Gazebo Harmonic installed (see [Installation Guide](/appendices/installation))

---

## Why Simulation Matters for Physical AI

Training Physical AI systems on real hardware is expensive, slow, and dangerous. A humanoid robot learning to walk will fall thousands of times—each fall risks mechanical damage and requires manual reset. Simulation solves this problem by providing an unlimited, safe environment for experimentation.

A **digital twin** is a virtual replica of a physical system that mirrors its behavior in real-time. For humanoid robotics, the digital twin includes the robot's kinematic structure, dynamic properties, sensors, and environment. Changes in the physical robot update the twin; experiments in simulation inform physical deployment.

The Simulation-to-Real (Sim2Real) pipeline has become central to modern robotics research. Systems like Boston Dynamics' Atlas and Tesla's Optimus rely heavily on simulation for policy training before hardware deployment (Tobin et al., 2017). The key insight: simulation fidelity determines transfer success.

This module focuses on **Gazebo**, the standard open-source simulator for ROS 2 robotics. Gazebo provides physics simulation, sensor modeling, and seamless ROS 2 integration—everything needed to develop and test humanoid control before touching real hardware.

---

## Gazebo Architecture

Gazebo operates as a client-server system with plugin-based extensibility:

```
┌──────────────────────────────────────────────────────────────┐
│                      GAZEBO ARCHITECTURE                     │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────────┐      ┌─────────────────┐               │
│  │  Gazebo Server  │◄────►│  Gazebo Client  │               │
│  │  (gzserver)     │      │  (gzclient/GUI) │               │
│  └────────┬────────┘      └─────────────────┘               │
│           │                                                  │
│           ▼                                                  │
│  ┌─────────────────────────────────────────┐                │
│  │            Physics Engine               │                │
│  │  (DART, ODE, Bullet, Simbody)          │                │
│  └─────────────────────────────────────────┘                │
│           │                                                  │
│           ▼                                                  │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐│
│  │ Sensor Plugins  │  │ Model Plugins   │  │ World Plugins││
│  │ (LiDAR, Camera) │  │ (Controllers)   │  │ (Physics)    ││
│  └────────┬────────┘  └────────┬────────┘  └──────────────┘│
│           │                    │                            │
│           ▼                    ▼                            │
│  ┌─────────────────────────────────────────┐                │
│  │         ROS 2 Bridge (gz_ros2_control)  │                │
│  └─────────────────────────────────────────┘                │
│           │                                                  │
│           ▼                                                  │
│       ROS 2 Topics: /scan, /depth, /imu, /joint_states      │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

**Key Components**:

- **Gazebo Server**: Runs physics simulation, sensor updates, and plugin execution
- **Physics Engine**: Calculates rigid body dynamics, collisions, and constraints (DART recommended for humanoids)
- **Sensor Plugins**: Generate simulated sensor data matching real hardware specifications
- **ROS 2 Bridge**: Publishes simulation data to standard ROS 2 topics

The simulation loop executes at fixed time steps (default 1ms). Each step: (1) apply forces, (2) solve physics constraints, (3) update state, (4) check collisions, (5) publish sensor data.

---

## From URDF to SDF

While URDF describes robot structure, **SDF (Simulation Description Format)** provides additional features required for simulation:

| Feature | URDF | SDF |
|---------|------|-----|
| Robot structure | ✓ | ✓ |
| Sensor definitions | Limited | Full support |
| Physics plugins | No | Yes |
| World description | No | Yes |
| Multiple robots | No | Yes |
| Closed-loop chains | No | Yes |

Gazebo automatically converts URDF to SDF at load time, but manual enhancement enables advanced features.

### Enhanced SDF with Gazebo Plugins

```xml
<?xml version="1.0"?>
<sdf version="1.8">
  <world name="humanoid_world">

    <!-- Physics configuration -->
    <physics type="dart">
      <max_step_size>0.001</max_step_size>
      <real_time_factor>1.0</real_time_factor>
      <dart>
        <collision_detector>fcl</collision_detector>
      </dart>
    </physics>

    <!-- Lighting -->
    <light type="directional" name="sun">
      <cast_shadows>true</cast_shadows>
      <pose>0 0 10 0 0 0</pose>
      <diffuse>0.8 0.8 0.8 1</diffuse>
    </light>

    <!-- Ground plane -->
    <model name="ground_plane">
      <static>true</static>
      <link name="link">
        <collision name="collision">
          <geometry><plane><normal>0 0 1</normal></plane></geometry>
          <surface>
            <friction>
              <ode><mu>100</mu><mu2>50</mu2></ode>
            </friction>
          </surface>
        </collision>
        <visual name="visual">
          <geometry><plane><normal>0 0 1</normal><size>100 100</size></plane></geometry>
        </visual>
      </link>
    </model>

    <!-- Include humanoid robot -->
    <include>
      <uri>model://humanoid_base</uri>
      <pose>0 0 1.0 0 0 0</pose>
    </include>

  </world>
</sdf>
```

---

## Physics Simulation for Humanoids

Humanoid robots present unique physics challenges: bipedal balance requires precise contact modeling, high degree-of-freedom chains demand efficient solvers, and joint compliance affects stability.

### Critical Physics Parameters

| Parameter | Description | Humanoid Recommendation |
|-----------|-------------|------------------------|
| `max_step_size` | Simulation time step | 0.001s (1ms) |
| `solver_iterations` | Constraint solver passes | 50-100 |
| `friction_mu` | Coulomb friction coefficient | 0.8-1.0 (rubber on concrete) |
| `contact_stiffness` | Contact spring constant | 1e6-1e8 N/m |
| `contact_damping` | Contact damping coefficient | 1e3-1e5 Ns/m |

### Rigid Body Dynamics

Gazebo solves Newton-Euler equations for each link:

```
F = ma          (linear motion)
τ = Iα          (angular motion)
```

For stable humanoid simulation:

1. **Inertia tensors** must be physically realistic—use CAD-derived values or estimate from geometry
2. **Mass distribution** affects center of mass—critical for balance
3. **Joint limits** prevent hyperextension—match hardware specifications
4. **Damping** reduces oscillation—add to all revolute joints

### Collision Configuration

```xml
<collision name="foot_collision">
  <geometry>
    <box><size>0.25 0.15 0.05</size></box>
  </geometry>
  <surface>
    <contact>
      <ode>
        <kp>1e7</kp>           <!-- Contact stiffness -->
        <kd>1e4</kd>           <!-- Contact damping -->
        <min_depth>0.001</min_depth>
      </ode>
    </contact>
    <friction>
      <ode>
        <mu>0.9</mu>           <!-- Primary friction -->
        <mu2>0.9</mu2>         <!-- Secondary friction -->
      </ode>
    </friction>
  </surface>
</collision>
```

---

## Simulated Sensors

Gazebo's sensor plugins generate realistic data streams that match real hardware characteristics, including noise models and update rates.

### LiDAR Configuration

```xml
<sensor name="lidar" type="gpu_lidar">
  <pose>0 0 0.5 0 0 0</pose>
  <topic>/scan</topic>
  <update_rate>10</update_rate>
  <lidar>
    <scan>
      <horizontal>
        <samples>360</samples>
        <resolution>1</resolution>
        <min_angle>-3.14159</min_angle>
        <max_angle>3.14159</max_angle>
      </horizontal>
    </scan>
    <range>
      <min>0.1</min>
      <max>10.0</max>
      <resolution>0.01</resolution>
    </range>
    <noise>
      <type>gaussian</type>
      <mean>0.0</mean>
      <stddev>0.01</stddev>
    </noise>
  </lidar>
</sensor>
```

### Depth Camera (RGB-D)

```xml
<sensor name="depth_camera" type="depth_camera">
  <pose>0.1 0 0.4 0 0 0</pose>
  <update_rate>30</update_rate>
  <camera>
    <horizontal_fov>1.047</horizontal_fov>
    <image>
      <width>640</width>
      <height>480</height>
      <format>R8G8B8</format>
    </image>
    <clip>
      <near>0.1</near>
      <far>10.0</far>
    </clip>
  </camera>
</sensor>
```

### IMU Sensor

```xml
<sensor name="imu_sensor" type="imu">
  <pose>0 0 0.3 0 0 0</pose>
  <topic>/imu/data</topic>
  <update_rate>100</update_rate>
  <imu>
    <angular_velocity>
      <x><noise type="gaussian"><mean>0</mean><stddev>0.0001</stddev></noise></x>
      <y><noise type="gaussian"><mean>0</mean><stddev>0.0001</stddev></noise></y>
      <z><noise type="gaussian"><mean>0</mean><stddev>0.0001</stddev></noise></z>
    </angular_velocity>
    <linear_acceleration>
      <x><noise type="gaussian"><mean>0</mean><stddev>0.001</stddev></noise></x>
      <y><noise type="gaussian"><mean>0</mean><stddev>0.001</stddev></noise></y>
      <z><noise type="gaussian"><mean>0</mean><stddev>0.001</stddev></noise></z>
    </linear_acceleration>
  </imu>
</sensor>
```

---

## Simulation Workflow

### Launch File for Digital Twin

```python
#!/usr/bin/env python3
"""gazebo_bringup.launch.py - Launch humanoid simulation."""

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    pkg_share = get_package_share_directory('humanoid_sim')

    # Launch Gazebo with world file
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(get_package_share_directory('ros_gz_sim'),
                        'launch', 'gz_sim.launch.py')
        ]),
        launch_arguments={'gz_args': '-r humanoid_world.sdf'}.items()
    )

    # Spawn robot
    spawn_robot = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-name', 'humanoid',
            '-topic', 'robot_description',
            '-z', '1.0'
        ],
        output='screen'
    )

    # Bridge Gazebo topics to ROS 2
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/scan@sensor_msgs/msg/LaserScan@gz.msgs.LaserScan',
            '/imu/data@sensor_msgs/msg/Imu@gz.msgs.IMU',
            '/depth/image@sensor_msgs/msg/Image@gz.msgs.Image',
        ],
        output='screen'
    )

    # RViz2 visualization
    rviz = Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', os.path.join(pkg_share, 'config', 'humanoid.rviz')],
        output='screen'
    )

    return LaunchDescription([
        gazebo,
        spawn_robot,
        bridge,
        rviz
    ])
```

### Verification Commands

After launching, verify sensor data flows:

```bash
# Check available topics
ros2 topic list

# Verify IMU data (should show ~100 Hz)
ros2 topic hz /imu/data

# Echo LiDAR readings
ros2 topic echo /scan --once

# View simulation in RViz2
rviz2
```

**Expected output** from `ros2 topic hz /imu/data`:

```
average rate: 99.987
    min: 0.009s max: 0.011s std dev: 0.00043s window: 100
```

---

## Exercises

1. **Physics Tuning**: Modify the ground friction coefficient from 0.9 to 0.3 (icy surface). Observe how the humanoid's stability changes. Document the minimum friction required for stable standing.

2. **Sensor Integration**: Add a second LiDAR sensor to the humanoid's head. Configure it with 180° field of view facing forward. Verify data appears on a new topic `/head_scan`.

3. **Recording and Playback**: Use `ros2 bag record` to capture 30 seconds of sensor data while manually moving the robot. Play back the recording and visualize in RViz2 without running Gazebo.

---

## Summary

This module introduced digital twin concepts and practical Gazebo simulation:

- **Digital twins** enable safe, fast iteration for Physical AI development
- **Gazebo architecture** separates physics, rendering, and ROS 2 integration
- **SDF** extends URDF with simulation-specific features
- **Physics parameters** must be tuned for stable humanoid simulation
- **Sensor plugins** generate realistic LiDAR, depth, and IMU data

Module 3 introduces NVIDIA Isaac Sim for photorealistic rendering and advanced perception training—capabilities beyond Gazebo's scope.

---

## References

Koenig, N., & Howard, A. (2004). Design and use paradigms for Gazebo, an open-source multi-robot simulator. In *IEEE/RSJ International Conference on Intelligent Robots and Systems* (pp. 2149-2154).

Open Robotics. (2023). *Gazebo Sim Documentation*. https://gazebosim.org/docs

Todorov, E., Erez, T., & Tassa, Y. (2012). MuJoCo: A physics engine for model-based control. In *IEEE/RSJ International Conference on Intelligent Robots and Systems* (pp. 5026-5033).

Tobin, J., Fong, R., Ray, A., Schneider, J., Zaremba, W., & Abbeel, P. (2017). Domain randomization for transferring deep neural networks from simulation to the real world. In *IEEE/RSJ International Conference on Intelligent Robots and Systems* (pp. 23-30).

Open Dynamics Engine. (2023). *ODE User Guide*. https://ode.org/wiki/index.php/Manual
