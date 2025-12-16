# Skill: isaac-sim-guidance

## Purpose

Provide comprehensive guidance on NVIDIA Isaac Sim for humanoid robotics simulation. This skill covers physics configuration, sensor modeling, control system integration, and simulation workflows tailored for educational robotics. Learners gain hands-on understanding of high-fidelity simulation as a foundation for real-world robot deployment.

## Inputs

| Input | Type | Required | Description |
|-------|------|----------|-------------|
| `topic` | string | Yes | Isaac Sim topic (e.g., "physics scene", "articulation", "domain randomization") |
| `task_type` | string | No | Task category: `setup`, `configuration`, `scripting`, `debugging`, `optimization`. Default: `configuration` |
| `robot_context` | string | No | Robot type: `humanoid`, `quadruped`, `manipulator`, `mobile_base`. Default: `humanoid` |
| `output_format` | string | No | Format: `explanation`, `step_by_step`, `code_snippet`, `checklist`. Default: `explanation` |
| `experience_level` | string | No | Learner level: `beginner`, `intermediate`, `advanced`. Default: `intermediate` |

## Outputs

| Output | Description |
|--------|-------------|
| Conceptual explanations | Physics and simulation principles mapped to Isaac Sim implementations |
| Setup procedures | Installation, licensing, and environment configuration steps |
| Code examples | Python scripts using `omni.isaac` APIs with annotations |
| Configuration guides | USD schema, PhysX parameters, and OmniGraph node setups |
| Debugging strategies | Diagnostic approaches for common simulation issues |
| Performance recommendations | Settings tuned for educational hardware constraints |

## Limits

### In Scope

- Isaac Sim installation and workspace setup
- PhysX articulation configuration for humanoid robots
- Sensor simulation: RGB cameras, depth, LiDAR, IMU, force/torque, contact
- Joint control: position, velocity, effort modes
- Domain randomization for sim-to-real transfer
- ROS2 bridge via OmniGraph
- Python scripting with `omni.isaac.core` and `omni.isaac.kit`
- Reinforcement learning environments with `omni.isaac.gym`
- USD scene composition and organization
- Headless simulation for training workloads

### Out of Scope

- Omniverse Enterprise deployment and licensing
- Multi-GPU cluster configuration
- Custom PhysX plugin development
- Omniverse Nucleus server administration
- Real-time ray tracing optimization for film quality
- Automotive or industrial automation workflows
- Isaac ROS (separate from Isaac Sim)
- Fleet management and cloud orchestration

## Linked Documentation Paths

Content aligns with the following structure:

```
docs/module-3-isaac/
├── index.md                          # Module overview and prerequisites
├── 01-isaac-sim-overview.md          # Platform architecture and capabilities
├── 02-installation.md                # System requirements, installation steps
├── 03-interface-tour.md              # UI panels, viewports, and navigation
├── 04-usd-fundamentals.md            # Universal Scene Description basics
├── 05-physics-scene-setup.md         # PhysX scene, gravity, time stepping
├── 06-articulations.md               # Joint types, drives, and humanoid chains
├── 07-humanoid-import.md             # URDF/MJCF to USD conversion
├── 08-joint-control.md               # Position, velocity, and torque control
├── 09-sensors/
│   ├── index.md                      # Sensor overview
│   ├── cameras.md                    # RGB, depth, segmentation
│   ├── lidar.md                      # Rotating and solid-state LiDAR
│   ├── imu.md                        # Inertial measurement units
│   └── contact-force.md              # Contact reporters and F/T sensors
├── 10-omnigraph-basics.md            # Visual scripting fundamentals
├── 11-ros2-integration.md            # OmniGraph ROS2 bridge nodes
├── 12-python-scripting.md            # Standalone and extension scripts
├── 13-domain-randomization.md        # Sim-to-real transfer techniques
├── 14-reinforcement-learning.md      # Isaac Gym environments
├── 15-headless-simulation.md         # Training without GUI
├── 16-performance-tuning.md          # FPS, physics substeps, GPU utilization
└── exercises/
    ├── exercise-01-first-scene.md
    ├── exercise-02-humanoid-standing.md
    ├── exercise-03-sensor-data.md
    ├── exercise-04-walking-policy.md
    └── exercise-05-domain-rand.md
```

## Physics Configuration Reference

### PhysX Scene Parameters

| Parameter | Typical Value | Humanoid Consideration |
|-----------|---------------|------------------------|
| `timeStepsPerSecond` | 120-500 | Higher for stable contact |
| `gravityDirection` | (0, 0, -1) | Z-up convention |
| `gravityMagnitude` | 9.81 | Earth standard |
| `enableGPUDynamics` | True | Required for articulations |
| `enableCCD` | True | Prevents foot tunneling |
| `solverPositionIterations` | 16-32 | Higher for joint stability |
| `solverVelocityIterations` | 8-16 | Reduces jitter |

### Articulation Drive Modes

| Mode | Use Case | API Reference |
|------|----------|---------------|
| Position | Joint angle tracking | `ArticulationAction.joint_positions` |
| Velocity | Wheeled joints, continuous rotation | `ArticulationAction.joint_velocities` |
| Effort | Torque control, compliant motion | `ArticulationAction.joint_efforts` |

Reference: `docs/module-3-isaac/08-joint-control.md`

## Instructional Guidelines

1. **Prerequisites explicit**: State required knowledge (USD basics, Python, ROS2) before each topic.
2. **Hardware-aware**: Note GPU memory requirements; provide fallback settings for consumer hardware.
3. **Determinism emphasis**: Explain fixed time stepping for reproducible training results.
4. **Safety in simulation**: Teach joint limits and collision detection before control.
5. **Iterative complexity**: Start with static scenes, add physics, then control, then learning.
6. **Script portability**: Provide both standalone scripts and extension-based examples.

## Example Usage

### Example 1: Physics scene setup

**Input:**
```
topic: "physics scene"
task_type: "setup"
robot_context: "humanoid"
output_format: "step_by_step"
```

**Output:**
```markdown
## Setting Up a Physics Scene for Humanoid Simulation

### Prerequisites
- Isaac Sim installed and licensed
- Completed: docs/module-3-isaac/02-installation.md

### Step 1: Create New Stage

File → New Stage
Save as: `humanoid_physics_scene.usd`

### Step 2: Add Physics Scene Prim

```python
from pxr import UsdPhysics, Gf

stage = omni.usd.get_context().get_stage()

# Create physics scene
scene_path = "/World/PhysicsScene"
scene = UsdPhysics.Scene.Define(stage, scene_path)

# Configure gravity
scene.CreateGravityDirectionAttr(Gf.Vec3f(0, 0, -1))
scene.CreateGravityMagnitudeAttr(9.81)
```

### Step 3: Configure PhysX Settings

Window → Simulation → Physics Settings

| Setting | Value |
|---------|-------|
| Time Steps Per Second | 200 |
| Solver Position Iterations | 24 |
| Solver Velocity Iterations | 8 |
| Enable GPU Dynamics | True |
| Broadphase Type | GPU |

### Step 4: Add Ground Plane

Create → Physics → Ground Plane

Properties:
- Collision enabled
- Static friction: 0.8 (rubber-like for humanoid feet)
- Dynamic friction: 0.6

### Step 5: Validate Setup

Press Play and verify:
- [ ] No warnings in Console
- [ ] Gravity direction indicator visible
- [ ] FPS stable at target rate

### Common Errors

| Error | Solution |
|-------|----------|
| "GPU dynamics requires GPU" | Enable in Physics Settings |
| "Articulation explosion" | Increase solver iterations |
| "Low FPS" | Reduce time steps or scene complexity |

### Reference
Full details: docs/module-3-isaac/05-physics-scene-setup.md
```

### Example 2: Humanoid joint control

**Input:**
```
topic: "joint control"
task_type: "scripting"
robot_context: "humanoid"
output_format: "code_snippet"
```

**Output:**
```markdown
## Humanoid Joint Control Script

### Overview
Control humanoid joints using position targets with the Articulation API.

### Prerequisites
- Humanoid USD imported: docs/module-3-isaac/07-humanoid-import.md
- Physics scene configured: docs/module-3-isaac/05-physics-scene-setup.md

### Code: Position Control for Standing Pose

File: `scripts/humanoid_stand.py`

```python
from omni.isaac.core import World
from omni.isaac.core.articulations import Articulation
import numpy as np

# Initialize simulation world
world = World(stage_units_in_meters=1.0)
world.scene.add_default_ground_plane()

# Load humanoid articulation
humanoid_prim_path = "/World/Humanoid"
humanoid = world.scene.add(
    Articulation(
        prim_path=humanoid_prim_path,
        name="humanoid"
    )
)

# Reset world to initialize articulation
world.reset()

# Get joint information
num_joints = humanoid.num_dof
joint_names = humanoid.dof_names
print(f"Humanoid has {num_joints} joints: {joint_names}")

# Define standing pose (example: 28-DOF humanoid)
standing_pose = np.zeros(num_joints)

# Adjust key joints for natural standing
joint_indices = {name: i for i, name in enumerate(joint_names)}

# Slight knee bend for stability
if "left_knee" in joint_indices:
    standing_pose[joint_indices["left_knee"]] = 0.1  # radians
if "right_knee" in joint_indices:
    standing_pose[joint_indices["right_knee"]] = 0.1

# Apply position targets
humanoid.set_joint_position_targets(standing_pose)

# Configure joint drives (stiffness and damping)
stiffness = np.full(num_joints, 1000.0)  # N*m/rad
damping = np.full(num_joints, 100.0)     # N*m*s/rad

humanoid.set_gains(kps=stiffness, kds=damping)

# Run simulation loop
for i in range(1000):
    world.step(render=True)

    # Read current joint positions
    current_positions = humanoid.get_joint_positions()

    if i % 100 == 0:
        error = np.abs(standing_pose - current_positions).mean()
        print(f"Step {i}: Mean position error = {error:.4f} rad")

print("Standing pose achieved.")
```

### Key API Methods

| Method | Purpose |
|--------|---------|
| `get_joint_positions()` | Read current joint angles |
| `set_joint_position_targets()` | Set desired positions |
| `set_joint_velocity_targets()` | Set desired velocities |
| `set_joint_efforts()` | Apply direct torques |
| `set_gains(kps, kds)` | Configure PD controller |

### Tuning Guidelines

| Robot Mass | Stiffness Range | Damping Range |
|------------|-----------------|---------------|
| < 20 kg | 100-500 | 10-50 |
| 20-80 kg | 500-2000 | 50-200 |
| > 80 kg | 2000-5000 | 200-500 |

### Reference
Full control guide: docs/module-3-isaac/08-joint-control.md
```

### Example 3: Sensor configuration

**Input:**
```
topic: "IMU sensor"
task_type: "configuration"
robot_context: "humanoid"
output_format: "checklist"
```

**Output:**
```markdown
## IMU Sensor Configuration Checklist

### Purpose
Add an IMU to a humanoid's pelvis for orientation and acceleration feedback.

### Prerequisites
- [ ] Humanoid articulation loaded
- [ ] Physics scene running at ≥200 Hz

### Configuration Steps

#### 1. Create IMU Prim
- [ ] Navigate to pelvis link in Stage panel
- [ ] Create → Isaac → Sensors → IMU Sensor
- [ ] Position at center of mass of pelvis

#### 2. Set Sensor Properties

| Property | Value | Notes |
|----------|-------|-------|
| Enabled | True | |
| Sensor Period | 0.005 | 200 Hz output |
| Linear Acceleration Filter Cutoff | 50 | Hz, noise reduction |
| Angular Velocity Filter Cutoff | 50 | Hz |

#### 3. Configure Noise Model (Optional)

For realistic sim-to-real transfer:
- [ ] Angular velocity noise density: 0.0002 rad/s/√Hz
- [ ] Linear acceleration noise density: 0.002 m/s²/√Hz
- [ ] Gyroscope bias instability: 0.0001 rad/s
- [ ] Accelerometer bias instability: 0.0002 m/s²

Reference: docs/module-3-isaac/09-sensors/imu.md

#### 4. Connect to OmniGraph

- [ ] Create Action Graph
- [ ] Add node: Isaac Read IMU
- [ ] Connect IMU prim path
- [ ] Add node: ROS2 Publish Imu
- [ ] Set topic: `/humanoid/pelvis_imu`
- [ ] Set frame_id: `pelvis_link`

#### 5. Verify Output

```bash
# Check topic exists
ros2 topic list | grep imu

# Verify data
ros2 topic echo /humanoid/pelvis_imu --once

# Check rate
ros2 topic hz /humanoid/pelvis_imu
# Expected: ~200 Hz
```

#### 6. Validation Tests

- [ ] Robot stationary: linear acceleration ≈ (0, 0, 9.81)
- [ ] Robot tilted 45°: orientation quaternion changes appropriately
- [ ] Robot moving: angular velocity non-zero during rotation

### Common Issues

| Symptom | Check |
|---------|-------|
| All zeros | Is simulation playing? |
| Wrong frame | Verify prim path in Read IMU node |
| Excessive noise | Reduce noise parameters |
| Delayed data | Check OmniGraph execution order |

### Reference Documentation
- IMU setup: docs/module-3-isaac/09-sensors/imu.md
- OmniGraph ROS2: docs/module-3-isaac/11-ros2-integration.md
```

### Example 4: Domain randomization

**Input:**
```
topic: "domain randomization"
task_type: "configuration"
robot_context: "humanoid"
output_format: "explanation"
experience_level: "advanced"
```

**Output:**
```markdown
## Domain Randomization for Humanoid Sim-to-Real Transfer

### Concept
Domain randomization bridges the simulation-to-reality gap by training policies on varied simulation parameters. The policy learns features robust to physical variations it will encounter on real hardware.

### Randomization Categories for Humanoids

#### 1. Dynamics Randomization

| Parameter | Range | Impact |
|-----------|-------|--------|
| Link masses | ±15% | Balance sensitivity |
| Joint friction | 0.01-0.1 N·m | Motion smoothness |
| Joint damping | ±20% | Velocity tracking |
| Ground friction | 0.5-1.2 | Foot slip behavior |
| Motor strength | ±10% | Torque limits |

#### 2. Observation Noise

| Sensor | Noise Type | Magnitude |
|--------|------------|-----------|
| Joint position | Gaussian | σ = 0.01 rad |
| Joint velocity | Gaussian | σ = 0.1 rad/s |
| IMU orientation | Quaternion perturbation | 2° |
| IMU angular velocity | Gaussian | σ = 0.02 rad/s |

#### 3. Action Delays and Latency

| Parameter | Range | Real-World Analog |
|-----------|-------|-------------------|
| Action delay | 0-20 ms | Control loop latency |
| Observation delay | 0-10 ms | Sensor processing |

#### 4. External Perturbations

| Perturbation | Application | Purpose |
|--------------|-------------|---------|
| Random pushes | Torso, 50-200 N | Balance recovery |
| Terrain variation | Height ±5 cm | Foot placement adaptation |
| Payload variation | 0-5 kg | Mass distribution changes |

### Implementation with Isaac Sim

```python
from omni.isaac.core.utils.random import set_random_seed
from omni.isaac.core.prims import XFormPrim
import numpy as np

class HumanoidDomainRandomizer:
    def __init__(self, humanoid, seed=42):
        self.humanoid = humanoid
        set_random_seed(seed)

    def randomize_masses(self, variation=0.15):
        """Randomize link masses within ±variation."""
        for link in self.humanoid.get_links():
            original_mass = link.get_mass()
            scale = np.random.uniform(1 - variation, 1 + variation)
            link.set_mass(original_mass * scale)

    def randomize_friction(self, min_val=0.5, max_val=1.2):
        """Randomize ground contact friction."""
        friction = np.random.uniform(min_val, max_val)
        # Apply to ground plane material
        self.ground_material.set_dynamic_friction(friction)
        self.ground_material.set_static_friction(friction * 1.2)

    def apply_push(self, force_range=(50, 200)):
        """Apply random push to torso."""
        force_mag = np.random.uniform(*force_range)
        direction = np.random.randn(3)
        direction[2] = 0  # Horizontal only
        direction = direction / np.linalg.norm(direction)
        force = direction * force_mag
        self.humanoid.apply_force(force, link_name="torso")

    def on_reset(self):
        """Called at episode start."""
        self.randomize_masses()
        self.randomize_friction()
```

### Curriculum Strategy

| Training Phase | Randomization Level | Goal |
|----------------|---------------------|------|
| Phase 1 (0-25%) | None | Basic locomotion |
| Phase 2 (25-50%) | Low (±5%) | Refine gait |
| Phase 3 (50-75%) | Medium (±10%) | Robustness |
| Phase 4 (75-100%) | Full (±15%+) | Sim-to-real ready |

### Reference Documentation
- Domain randomization: docs/module-3-isaac/13-domain-randomization.md
- RL environments: docs/module-3-isaac/14-reinforcement-learning.md
```

## Integration Notes

This skill coordinates with:
- `ros2-teaching`: Joint state messages and control interfaces build on ROS2 knowledge
- `digital-twin-visualization`: Isaac Sim is primary Omniverse platform; concepts overlap
- `vla-reasoning`: Sensor simulation provides training data for vision-language-action models
- `capstone-mentor`: Isaac Sim proficiency enables simulation-validated capstone projects

## Version

- Skill version: 1.0.0
- Target Isaac Sim version: 2023.1.0+
- Last updated: 2025-01-15
