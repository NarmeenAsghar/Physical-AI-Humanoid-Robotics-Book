# Skill: digital-twin-visualization

## Purpose

Guide learners through Digital Twin concepts and visualization pipelines for humanoid robotics education. This skill bridges theoretical robotics models with real-time visual simulation using Unity and NVIDIA Omniverse platforms, enabling learners to see, test, and iterate on robot designs before physical deployment.

## Inputs

| Input | Type | Required | Description |
|-------|------|----------|-------------|
| `concept` | string | Yes | Digital Twin concept to teach (e.g., "synchronization", "sensor simulation", "physics fidelity") |
| `platform` | string | No | Target platform: `unity`, `omniverse`, or `comparison`. Default: `comparison` |
| `robot_type` | string | No | Robot context: `humanoid`, `mobile`, `manipulator`. Default: `humanoid` |
| `output_format` | string | No | Format: `explanation`, `pipeline_guide`, `tutorial`, `troubleshooting`. Default: `explanation` |
| `prior_knowledge` | string | No | Assumed background: `none`, `ros2`, `3d_modeling`. Default: `ros2` |

## Outputs

| Output | Description |
|--------|-------------|
| Conceptual explanation | Clear definition and relevance of Digital Twin concepts to robotics |
| Pipeline diagrams | Text-based flowcharts showing data flow between components |
| Platform-specific guides | Step-by-step instructions for Unity or Omniverse workflows |
| Configuration examples | Scene setup, connector configs, and synchronization parameters |
| Mapping tables | Robotics concepts mapped to platform-specific implementations |

## Constraints

### In Scope

- Digital Twin fundamentals: mirroring, synchronization, state management
- Unity Robotics Hub and ROS-TCP-Connector
- NVIDIA Omniverse Isaac Sim integration
- URDF/USD model import and conversion
- Sensor simulation: cameras, LiDAR, IMU, force/torque
- Physics engine configuration for realistic humanoid dynamics
- Real-time visualization of robot state and telemetry
- Recording and playback for analysis

### Out of Scope

- Game development features unrelated to robotics
- Photorealistic rendering optimization for film/media
- Cloud deployment of simulation environments
- Multi-user collaborative simulation
- Custom physics engine development
- AR/VR headset integration specifics

## Linked Documentation Paths

Content aligns with the following documentation structure:

```
docs/module-2-digital-twin/
├── index.md                        # Module overview and learning path
├── 01-digital-twin-concepts.md     # What is a Digital Twin, why it matters
├── 02-simulation-fundamentals.md   # Physics, time-stepping, determinism
├── 03-unity-setup.md               # Unity Hub, Robotics packages installation
├── 04-unity-ros-bridge.md          # ROS-TCP-Connector configuration
├── 05-omniverse-setup.md           # Omniverse Launcher, Isaac Sim installation
├── 06-omniverse-ros-bridge.md      # OmniGraph ROS2 bridge nodes
├── 07-urdf-to-usd.md               # Model conversion pipelines
├── 08-sensor-simulation.md         # Camera, LiDAR, IMU in simulation
├── 09-humanoid-rigging.md          # Joint hierarchies for bipedal robots
├── 10-state-synchronization.md     # Real-time mirroring strategies
├── 11-visualization-dashboards.md  # Telemetry display and debugging
├── 12-recording-playback.md        # Data capture for offline analysis
└── exercises/
    ├── exercise-01-unity-hello-robot.md
    ├── exercise-02-omniverse-import.md
    ├── exercise-03-sensor-visualization.md
    └── exercise-04-humanoid-walking.md
```

## Platform Concept Mapping

### Unity to Robotics Concepts

| Unity Concept | Robotics Equivalent | Documentation Reference |
|---------------|---------------------|------------------------|
| GameObject | Link (URDF) | `docs/module-2-digital-twin/03-unity-setup.md` |
| ArticulationBody | Joint with dynamics | `docs/module-2-digital-twin/09-humanoid-rigging.md` |
| ROS-TCP-Connector | ROS2 bridge | `docs/module-2-digital-twin/04-unity-ros-bridge.md` |
| Camera component | Vision sensor | `docs/module-2-digital-twin/08-sensor-simulation.md` |
| FixedUpdate | Control loop tick | `docs/module-2-digital-twin/02-simulation-fundamentals.md` |

### Omniverse to Robotics Concepts

| Omniverse Concept | Robotics Equivalent | Documentation Reference |
|-------------------|---------------------|------------------------|
| USD Prim | Link/Joint hierarchy | `docs/module-2-digital-twin/07-urdf-to-usd.md` |
| PhysX Articulation | Kinematic chain | `docs/module-2-digital-twin/09-humanoid-rigging.md` |
| OmniGraph | Dataflow programming | `docs/module-2-digital-twin/06-omniverse-ros-bridge.md` |
| Isaac Sim sensors | Synthetic data generation | `docs/module-2-digital-twin/08-sensor-simulation.md` |
| Action Graph | Event-driven control | `docs/module-2-digital-twin/10-state-synchronization.md` |

## Instructional Guidelines

1. **Platform-agnostic first**: Teach the Digital Twin concept before platform specifics.
2. **Visual pipeline documentation**: Describe data flow as source → transform → destination.
3. **Configuration over code**: Prefer declarative setup; show code only when necessary.
4. **Humanoid focus**: Use bipedal robot examples; reference joint counts and balance challenges.
5. **Performance awareness**: Note computational costs of physics fidelity and sensor simulation.
6. **Bidirectional emphasis**: Digital Twins read from AND write to physical systems.

## Example Requests

### Example 1: Explain Digital Twin synchronization

**Input:**
```
concept: "state synchronization"
platform: "comparison"
robot_type: "humanoid"
output_format: "explanation"
```

**Output:**
```markdown
## State Synchronization in Digital Twins

### Definition
State synchronization maintains correspondence between a physical robot and its virtual counterpart. For humanoid robots, this includes 20-40+ joint positions, velocities, and torques updated at 100-1000 Hz.

### Synchronization Patterns

| Pattern | Direction | Use Case | Latency Tolerance |
|---------|-----------|----------|-------------------|
| Shadow mode | Physical → Virtual | Monitoring, analysis | <100ms |
| Predictive mode | Virtual → Physical | Motion planning | <10ms |
| Bidirectional | Both | Teleoperation | <5ms |

### Unity Implementation
- ROS-TCP-Connector subscribes to `/joint_states`
- ArticulationBody.SetJointPositions() applies state each FixedUpdate
- Reference: docs/module-2-digital-twin/04-unity-ros-bridge.md

### Omniverse Implementation
- OmniGraph ROS2 Subscriber node receives `/joint_states`
- Articulation Controller applies joint targets
- Reference: docs/module-2-digital-twin/06-omniverse-ros-bridge.md

### Humanoid-Specific Considerations
- Balance feedback requires <10ms round-trip
- Foot contact states must sync with ground truth
- Center of mass visualization aids debugging

### Next Steps
See: docs/module-2-digital-twin/10-state-synchronization.md
```

### Example 2: Guide sensor simulation setup

**Input:**
```
concept: "sensor simulation"
platform: "omniverse"
robot_type: "humanoid"
output_format: "pipeline_guide"
```

**Output:**
```markdown
## Sensor Simulation Pipeline: Omniverse Isaac Sim

### Pipeline Overview

```
[Physical Sensor Specs]
        ↓
[USD Sensor Prim Creation]
        ↓
[Isaac Sim Sensor Extension]
        ↓
[OmniGraph Processing]
        ↓
[ROS2 Topic Publication]
        ↓
[Downstream Perception Nodes]
```

### Step 1: Define Sensor Specifications

File: `sensors/humanoid_sensors.yaml`

```yaml
head_camera:
  type: rgb_camera
  resolution: [640, 480]
  fov_degrees: 90
  update_rate_hz: 30
  ros_topic: /head_camera/image_raw

chest_imu:
  type: imu
  update_rate_hz: 200
  noise_density: 0.001
  ros_topic: /chest_imu/data
```

### Step 2: Create Sensor Prims

Path in USD: `/World/Humanoid/head/camera_link/RGBCamera`

Isaac Sim menu: Create → Isaac → Sensors → Camera

### Step 3: Configure OmniGraph

Nodes required:
1. Isaac Read Camera → outputs render product
2. Isaac Create Render Product → creates viewport
3. ROS2 Camera Helper → publishes to ROS2 topic

### Step 4: Verify Publication

```bash
ros2 topic hz /head_camera/image_raw
# Expected: ~30 Hz

ros2 topic echo /chest_imu/data --once
# Verify quaternion orientation and linear acceleration
```

### Common Issues

| Symptom | Cause | Solution |
|---------|-------|----------|
| 0 Hz on topic | OmniGraph not playing | Press Play in Isaac Sim |
| Black image | Camera inside geometry | Check camera transform |
| IMU drift | Missing noise model | Add realistic noise parameters |

### Reference Documentation
- Sensor setup: docs/module-2-digital-twin/08-sensor-simulation.md
- OmniGraph basics: docs/module-2-digital-twin/06-omniverse-ros-bridge.md
```

### Example 3: Tutorial for URDF to USD conversion

**Input:**
```
concept: "model conversion"
platform: "omniverse"
robot_type: "humanoid"
output_format: "tutorial"
```

**Output:**
```markdown
## Tutorial: Converting Humanoid URDF to USD for Omniverse

### Prerequisites
- Completed: docs/module-1-ros2/08-urdf-basics.md
- URDF file validated with `check_urdf`
- Omniverse Isaac Sim installed

### Learning Objectives
- Convert URDF to USD using Isaac Sim importer
- Resolve mesh path references
- Configure physics properties for humanoid dynamics
- Validate joint limits and collision geometry

### Input Files

```
~/ros2_ws/src/humanoid_description/
├── urdf/
│   └── humanoid.urdf
├── meshes/
│   ├── visual/
│   │   ├── torso.obj
│   │   ├── left_thigh.obj
│   │   └── ...
│   └── collision/
│       ├── torso_collision.obj
│       └── ...
```

### Step 1: Launch URDF Importer

Isaac Sim menu: Isaac Utils → URDF Importer

### Step 2: Configure Import Settings

| Setting | Value | Rationale |
|---------|-------|-----------|
| Fix Base Link | False | Humanoid must be free-floating |
| Self Collision | True | Limbs must not interpenetrate |
| Create Physics Scene | True | Required for simulation |
| Joint Drive Type | Position | Standard for joint control |

### Step 3: Execute Import

Input path: `~/ros2_ws/src/humanoid_description/urdf/humanoid.urdf`
Output path: `omniverse://localhost/Projects/humanoid/humanoid.usd`

### Step 4: Post-Import Validation

Check in Stage panel:
- [ ] All links present under `/World/humanoid`
- [ ] Joint count matches URDF (e.g., 28 joints)
- [ ] Visual meshes render correctly
- [ ] Collision meshes visible in Physics Debug

### Step 5: Physics Tuning

For stable humanoid simulation, adjust:

```python
# In Script Editor
from pxr import UsdPhysics

stage = omni.usd.get_context().get_stage()
scene = UsdPhysics.Scene.Get(stage, "/physicsScene")
scene.GetGravityDirectionAttr().Set((0, 0, -1))
scene.GetGravityMagnitudeAttr().Set(9.81)
```

### Expected Result
USD file with:
- Articulation root at pelvis/base_link
- Properly configured joint drives
- Collision geometry for contact simulation

### Troubleshooting

| Issue | Solution |
|-------|----------|
| Missing meshes | Use absolute paths or copy meshes to USD directory |
| Robot falls through ground | Add ground plane with collision |
| Joints at wrong limits | Edit joint properties in Property panel |

### Next Steps
- Add sensors: docs/module-2-digital-twin/08-sensor-simulation.md
- Connect to ROS2: docs/module-2-digital-twin/06-omniverse-ros-bridge.md
```

### Example 4: Troubleshooting visualization issues

**Input:**
```
concept: "visualization debugging"
platform: "unity"
robot_type: "humanoid"
output_format: "troubleshooting"
```

**Output:**
```markdown
## Troubleshooting: Unity Humanoid Visualization

### Diagnostic Checklist

Run through these checks in order:

#### 1. ROS Connection Status

```csharp
// Check in Unity Console
// Should see: "ROS connection established"
```

If not connected:
```bash
# Terminal 1: Start ROS TCP endpoint
ros2 run ros_tcp_endpoint default_server_endpoint --ros-args -p ROS_IP:=0.0.0.0

# Verify port
netstat -an | grep 10000
```

#### 2. Topic Data Flow

```bash
# Verify joint states publishing
ros2 topic echo /joint_states --once

# Check message frequency
ros2 topic hz /joint_states
# Expected: 50-100 Hz for smooth visualization
```

#### 3. Joint Mapping Verification

| Symptom | Cause | Fix |
|---------|-------|-----|
| Robot in T-pose | No joint data received | Check topic subscription |
| Single joint moves | Mapping array mismatch | Verify joint name order |
| Jerky motion | Low publish rate | Increase controller rate |
| Opposite rotation | Axis sign mismatch | Negate joint value |

#### 4. ArticulationBody Configuration

Inspector checklist for root body:
- [ ] Immovable: False (humanoid must move)
- [ ] Use Gravity: True
- [ ] Collision Detection: Continuous Speculative

#### 5. Frame Rate vs Physics Rate

```
Unity Time Settings:
- Fixed Timestep: 0.005 (200 Hz physics)
- Maximum Allowed Timestep: 0.02

If visualization stutters:
- Reduce physics rate to 0.01 (100 Hz)
- Enable Interpolation on ArticulationBody
```

### Common Error Messages

| Error | Solution |
|-------|----------|
| "ArticulationBody not found" | Add ArticulationBody to root link |
| "Joint index out of range" | URDF joint count ≠ script array size |
| "NaN in joint position" | Check for divide-by-zero in transforms |

### Reference
Full setup guide: docs/module-2-digital-twin/04-unity-ros-bridge.md
```

## Integration Notes

This skill coordinates with:
- `ros2-teaching`: URDF models and joint state messages originate from ROS2 knowledge
- `isaac-sim-guidance`: Omniverse-specific deep dives extend this skill's Omniverse coverage
- `vla-reasoning`: Visualization supports understanding of vision-language-action model inputs
- `capstone-mentor`: Digital Twin competency required for simulation-based capstone projects

## Version

- Skill version: 1.0.0
- Supported platforms: Unity 2022.3 LTS, Omniverse Isaac Sim 2023.1+
- Last updated: 2025-01-15
