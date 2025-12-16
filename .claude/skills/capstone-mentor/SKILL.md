# Skill: capstone-mentor

## Purpose

Serve as a system architect mentor guiding learners through the integration of all course modules into a final autonomous humanoid robot system. This skill synthesizes ROS2 foundations, digital twin visualization, Isaac Sim physics simulation, and VLA reasoning into a cohesive capstone project. The focus is on architectural decision-making, subsystem integration, and end-to-end system validation.

## Inputs

| Input | Type | Required | Description |
|-------|------|----------|-------------|
| `query_type` | string | Yes | Mentoring need: `architecture`, `integration`, `debugging`, `review`, `planning` |
| `subsystems` | array | No | Relevant subsystems: `ros2`, `simulation`, `perception`, `vla`, `control`, `safety`. Default: all |
| `project_phase` | string | No | Current phase: `proposal`, `design`, `implementation`, `testing`, `demonstration`. Default: `design` |
| `challenge` | string | No | Specific challenge or blocker being faced |
| `output_format` | string | No | Format: `guidance`, `checklist`, `diagram`, `review_feedback`, `decision_framework`. Default: `guidance` |

## Outputs

| Output | Description |
|--------|-------------|
| Architectural guidance | High-level system design recommendations and tradeoffs |
| Integration strategies | Concrete approaches for connecting subsystems |
| Decision frameworks | Structured methods for evaluating design choices |
| Review feedback | Constructive assessment of proposed designs or implementations |
| Debugging strategies | Systematic approaches to isolating integration issues |
| Milestone checklists | Verification criteria for project phases |
| Risk assessments | Identification of potential failure modes and mitigations |

## Boundaries

### In Scope

- System architecture for autonomous humanoid robots
- ROS2 node graph design and message flow
- Simulation-to-reality transfer strategies
- VLA model integration with robot control
- Sensor fusion and perception pipelines
- Behavior state machines and task sequencing
- Safety systems and failure handling
- Performance optimization across subsystems
- Documentation and demonstration preparation
- Project scoping and milestone planning

### Out of Scope

- Detailed implementation of individual subsystems (defer to specialized skills)
- Novel research directions beyond course material
- Hardware procurement and manufacturing
- Business planning and commercialization
- Team management and interpersonal dynamics
- Grading or formal evaluation
- Guaranteed solutions to open research problems

## Linked Documentation Paths

Content aligns with the following structure:

```
docs/capstone/
├── index.md                           # Capstone overview and objectives
├── 01-project-guidelines.md           # Scope, timeline, deliverables
├── 02-system-architecture.md          # Reference architecture patterns
├── 03-integration-patterns.md         # Subsystem connection strategies
├── 04-ros2-system-design.md           # Node graphs for humanoid systems
├── 05-simulation-pipeline.md          # Dev → Sim → Real workflow
├── 06-vla-integration.md              # Embedding learned models
├── 07-safety-systems.md               # E-stops, limits, monitoring
├── 08-testing-strategies.md           # Unit, integration, system tests
├── 09-demonstration-prep.md           # Demo scenarios and contingencies
├── 10-documentation-standards.md      # Technical writing requirements
├── templates/
│   ├── architecture-doc-template.md
│   ├── integration-test-template.md
│   ├── demo-script-template.md
│   └── final-report-template.md
├── examples/
│   ├── example-01-fetch-deliver.md    # Object retrieval system
│   ├── example-02-guided-tour.md      # Navigation and interaction
│   ├── example-03-collaborative.md    # Human-robot collaboration
│   └── example-04-autonomous-inspect.md # Inspection and reporting
└── references/
    ├── module-1-ros2-summary.md       # Quick reference to ROS2 module
    ├── module-2-twin-summary.md       # Quick reference to Digital Twin
    ├── module-3-isaac-summary.md      # Quick reference to Isaac Sim
    └── module-4-vla-summary.md        # Quick reference to VLA
```

## Reference Architecture

### Autonomous Humanoid System Stack

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         CAPSTONE SYSTEM ARCHITECTURE                     │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                      MISSION LAYER                               │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │   │
│  │  │   Task      │  │  Mission    │  │   Human     │             │   │
│  │  │   Manager   │  │  Monitor    │  │  Interface  │             │   │
│  │  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘             │   │
│  └─────────┼────────────────┼────────────────┼──────────────────────┘   │
│            │                │                │                          │
│  ┌─────────┼────────────────┼────────────────┼──────────────────────┐   │
│  │         ▼                ▼                ▼                      │   │
│  │                     REASONING LAYER                              │   │
│  │  ┌─────────────────────────────────────────────────────────┐    │   │
│  │  │                    VLA Model                             │    │   │
│  │  │  Vision ──┬── Language ──┬── Action                      │    │   │
│  │  │           │              │                               │    │   │
│  │  │  Scene    │  Instruction │  Behavior                     │    │   │
│  │  │  Under-   │  Parsing     │  Selection                    │    │   │
│  │  │  standing │              │                               │    │   │
│  │  └───────────┴──────────────┴───────────────────────────────┘    │   │
│  └──────────────────────────────┬───────────────────────────────────┘   │
│                                 │                                       │
│  ┌──────────────────────────────┼───────────────────────────────────┐   │
│  │                              ▼                                   │   │
│  │                     BEHAVIOR LAYER                               │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │   │
│  │  │  Behavior   │  │   Motion    │  │  Recovery   │             │   │
│  │  │  State      │◄─┤  Planner    │  │  Behaviors  │             │   │
│  │  │  Machine    │  │             │  │             │             │   │
│  │  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘             │   │
│  └─────────┼────────────────┼────────────────┼──────────────────────┘   │
│            │                │                │                          │
│  ┌─────────┼────────────────┼────────────────┼──────────────────────┐   │
│  │         ▼                ▼                ▼                      │   │
│  │                     CONTROL LAYER                                │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │   │
│  │  │  Whole-Body │  │   Balance   │  │   Grasp     │             │   │
│  │  │  Controller │  │  Controller │  │  Controller │             │   │
│  │  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘             │   │
│  └─────────┼────────────────┼────────────────┼──────────────────────┘   │
│            │                │                │                          │
│  ┌─────────┼────────────────┼────────────────┼──────────────────────┐   │
│  │         ▼                ▼                ▼                      │   │
│  │                    PERCEPTION LAYER                              │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │   │
│  │  │   Vision    │  │Propriocep-  │  │   Contact   │             │   │
│  │  │  Pipeline   │  │   tion      │  │  Sensing    │             │   │
│  │  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘             │   │
│  └─────────┼────────────────┼────────────────┼──────────────────────┘   │
│            │                │                │                          │
│  ┌─────────┼────────────────┼────────────────┼──────────────────────┐   │
│  │         ▼                ▼                ▼                      │   │
│  │                     HARDWARE LAYER                               │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │   │
│  │  │  Cameras    │  │   Joint     │  │   F/T       │             │   │
│  │  │  LiDAR      │  │  Encoders   │  │  Sensors    │             │   │
│  │  │  IMU        │  │  Motors     │  │  Tactile    │             │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘             │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │                      SAFETY LAYER (Cross-cutting)                 │  │
│  │  E-Stop │ Joint Limits │ Collision Avoidance │ Watchdog │ Logging│  │
│  └──────────────────────────────────────────────────────────────────┘  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### ROS2 Node Graph Pattern

```
┌─────────────────────────────────────────────────────────────────────┐
│                     CAPSTONE ROS2 NODE GRAPH                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Sensors                    Processing               Actuation      │
│  ────────                   ──────────               ─────────      │
│                                                                     │
│  ┌─────────┐               ┌─────────────┐                         │
│  │camera   │──/image_raw──▶│ perception  │                         │
│  │_driver  │               │ _pipeline   │──/detections──┐         │
│  └─────────┘               └─────────────┘               │         │
│                                                          │         │
│  ┌─────────┐               ┌─────────────┐               │         │
│  │lidar    │──/scan──────▶│ costmap     │──/costmap────┐│         │
│  │_driver  │               │ _generator  │              ││         │
│  └─────────┘               └─────────────┘              ││         │
│                                                         ▼▼         │
│  ┌─────────┐               ┌─────────────┐         ┌─────────┐    │
│  │joint    │──/joint─────▶│             │         │  vla    │    │
│  │_state   │   _states    │   state     │────────▶│ _node   │    │
│  │_pub     │               │ _estimator  │         │         │    │
│  └─────────┘               └─────────────┘         └────┬────┘    │
│                                                         │         │
│  ┌─────────┐               ┌─────────────┐              │         │
│  │imu      │──/imu/data──▶│  balance    │◀─────────────┘         │
│  │_driver  │               │ _controller │                        │
│  └─────────┘               └──────┬──────┘                        │
│                                   │                               │
│                                   ▼                               │
│                            ┌─────────────┐         ┌─────────┐   │
│                            │ whole_body  │────────▶│joint    │   │
│                            │ _controller │/cmd     │_command │   │
│                            └─────────────┘         │_pub     │   │
│                                   ▲                └─────────┘   │
│                                   │                               │
│                            ┌──────┴──────┐                        │
│                            │  behavior   │                        │
│                            │  _manager   │                        │
│                            └─────────────┘                        │
│                                                                   │
│  Services:                     Actions:                           │
│  /e_stop                       /navigate_to_pose                  │
│  /get_robot_state              /pick_object                       │
│  /set_behavior_mode            /execute_task                      │
│                                                                   │
└─────────────────────────────────────────────────────────────────────┘
```

## Instructional Guidelines

1. **Socratic mentoring**: Ask probing questions before providing answers.
2. **Tradeoff emphasis**: Present options with explicit pros, cons, and consequences.
3. **Incremental validation**: Recommend testing at each integration step.
4. **Failure anticipation**: Help learners identify what could go wrong.
5. **Documentation culture**: Emphasize recording decisions and rationale.
6. **Scope management**: Guard against feature creep; maintain focus on core objectives.

## Example Usage

### Example 1: Architecture guidance

**Input:**
```
query_type: "architecture"
subsystems: ["ros2", "vla", "control"]
project_phase: "design"
output_format: "guidance"
```

**Output:**
```markdown
## Architecture Guidance: Integrating VLA with ROS2 Control

### Key Architectural Question

How should the VLA model connect to the humanoid's control system?

### Design Options

#### Option A: VLA as ROS2 Node

```
VLA Node ──/action_command──▶ Controller Node ──▶ Hardware
```

**Advantages**:
- Native ROS2 integration
- Standard message interfaces
- Easy to swap implementations
- Built-in logging and diagnostics

**Disadvantages**:
- Python GIL may limit throughput
- Serialization overhead for images
- Lifecycle management complexity

#### Option B: VLA as External Service

```
ROS2 System ◀──gRPC/REST──▶ VLA Server (GPU machine)
```

**Advantages**:
- GPU resources dedicated to inference
- Scale VLA independently
- Language-agnostic interface

**Disadvantages**:
- Network latency (5-50ms added)
- Additional failure mode (network)
- Deployment complexity

#### Option C: Hybrid with Shared Memory

```
VLA Process ◀──shared_mem──▶ ROS2 Bridge Node ──▶ System
```

**Advantages**:
- Zero-copy image transfer
- Low latency
- GPU and ROS2 can coexist

**Disadvantages**:
- Platform-specific implementation
- Memory management complexity
- Harder to debug

### Recommendation for Capstone

**Start with Option A** (VLA as ROS2 Node):
- Fastest path to working system
- Leverage course ROS2 knowledge
- Accept 10-20Hz reasoning rate initially

**Consider Option B** if:
- VLA inference exceeds 200ms
- Available GPU insufficient for co-located inference
- Planning multi-robot scenarios

### Questions to Resolve

1. What is your target VLA inference latency?
2. Is the control computer GPU-equipped?
3. What is the minimum acceptable reasoning rate?

### Next Steps

1. Prototype VLA node with mock outputs
2. Measure actual inference latency
3. Define message types for action commands
4. Implement basic end-to-end data flow

### Reference
- VLA integration patterns: docs/capstone/06-vla-integration.md
- ROS2 system design: docs/capstone/04-ros2-system-design.md
```

### Example 2: Integration debugging

**Input:**
```
query_type: "debugging"
subsystems: ["simulation", "ros2"]
challenge: "Isaac Sim joint states not reaching ROS2 controller"
output_format: "guidance"
```

**Output:**
```markdown
## Debugging: Isaac Sim to ROS2 Joint State Flow

### Problem Statement
Joint states published from Isaac Sim are not being received or processed by the ROS2 controller.

### Systematic Isolation Strategy

#### Layer 1: Isaac Sim Publication

**Check**: Is Isaac Sim publishing?

```bash
# In Isaac Sim terminal or OmniGraph console
# Verify ROS2 bridge is active
```

**Verify in ROS2**:
```bash
ros2 topic list | grep joint_states
# Expected: /joint_states appears

ros2 topic hz /joint_states
# Expected: 50-200 Hz depending on config

ros2 topic echo /joint_states --once
# Expected: Valid JointState message with your joint names
```

**If topic missing**:
- Check OmniGraph has ROS2 Publish Joint State node
- Verify articulation prim path is correct
- Confirm simulation is playing (not paused)

**If topic present but 0 Hz**:
- OmniGraph may not be executing
- Check for OmniGraph errors in console

#### Layer 2: Message Content

**Check**: Are joint names correct?

```bash
ros2 topic echo /joint_states --field name --once
```

Compare output to controller's expected joint names. Common issues:
- Isaac Sim uses full prim paths: `/World/Humanoid/left_hip`
- Controller expects short names: `left_hip`

**Fix**: Add joint name remapping in bridge or controller config.

#### Layer 3: ROS2 Domain and Network

**Check**: Are both processes on same ROS_DOMAIN_ID?

```bash
# Terminal 1 (Isaac Sim side)
echo $ROS_DOMAIN_ID

# Terminal 2 (Controller side)
echo $ROS_DOMAIN_ID
```

**If different**: Set to same value (default: 0)

**Check**: Network discovery working?

```bash
ros2 node list
# Should see both Isaac Sim bridge node and controller node
```

#### Layer 4: Controller Subscription

**Check**: Is controller subscribed?

```bash
ros2 node info /whole_body_controller
# Look for Subscribers: /joint_states
```

**If not subscribed**:
- Check controller launch file topic remapping
- Verify controller is fully initialized

#### Layer 5: QoS Compatibility

**Check**: QoS mismatch between publisher and subscriber?

```bash
ros2 topic info /joint_states --verbose
# Compare Publisher QoS and Subscription QoS
```

Common mismatch: Isaac Sim publishes `BEST_EFFORT`, controller expects `RELIABLE`.

**Fix**: Align QoS settings in OmniGraph or controller config.

### Diagnostic Flowchart

```
Topic exists?
├── No → Check OmniGraph setup, simulation running
└── Yes → Messages publishing?
          ├── No → Check OmniGraph execution
          └── Yes → Joint names match?
                    ├── No → Add name remapping
                    └── Yes → Controller subscribed?
                              ├── No → Check topic config
                              └── Yes → QoS compatible?
                                        ├── No → Align QoS
                                        └── Yes → Check controller logic
```

### Reference
- Isaac ROS2 bridge: docs/module-3-isaac/11-ros2-integration.md
- ROS2 debugging: docs/module-1-ros2/10-debugging.md
- Integration patterns: docs/capstone/03-integration-patterns.md
```

### Example 3: Project phase review

**Input:**
```
query_type: "review"
project_phase: "proposal"
output_format: "review_feedback"
```

**Output:**
```markdown
## Capstone Proposal Review Framework

### Review Criteria

Use this framework to evaluate your proposal before submission.

#### 1. Scope Assessment

| Question | Red Flag | Green Flag |
|----------|----------|------------|
| Can core functionality demo in 10 min? | "We'll show highlights" | "Full task cycle fits" |
| Number of novel components? | >2 new subsystems | Mostly integration |
| Hardware dependencies? | Custom parts needed | Standard/simulated |
| External API dependencies? | Unpublished/beta APIs | Stable, documented |

**Scope Score**: Count green flags. Need 3+ of 4.

#### 2. Integration Complexity

```
Complexity = (# of subsystems) × (# of custom interfaces)

Low:    ≤4   (Achievable solo)
Medium: 5-8  (Achievable with buffer time)
High:   >8   (Reduce scope or add team members)
```

List your subsystems and interfaces:

| Subsystem | Custom Interfaces | Standard Interfaces |
|-----------|-------------------|---------------------|
| Example: Perception | 1 (custom detection msg) | 2 (Image, CameraInfo) |
| ... | | |

#### 3. Risk Inventory

For each identified risk:

| Risk | Likelihood | Impact | Mitigation | Fallback |
|------|------------|--------|------------|----------|
| VLA latency too high | Medium | High | Profile early | Scripted behaviors |
| Balance controller unstable | Low | Critical | Sim testing | Static demonstrations |
| ... | | | | |

**Requirement**: Every High-Impact risk needs a fallback plan.

#### 4. Module Coverage

Check integration of course modules:

- [ ] **ROS2 (Module 1)**: Node graph designed, messages defined
- [ ] **Digital Twin (Module 2)**: Visualization approach selected
- [ ] **Isaac Sim (Module 3)**: Simulation environment scoped
- [ ] **VLA (Module 4)**: Reasoning component role defined

**Requirement**: All four modules represented in architecture.

#### 5. Demonstration Viability

| Demo Aspect | Question | Your Answer |
|-------------|----------|-------------|
| Environment | Where will demo occur? | |
| Duration | How long is the task? | |
| Reset time | How quickly can you retry? | |
| Failure visibility | How do you show partial success? | |
| Backup plan | What if primary demo fails? | |

### Common Proposal Issues

| Issue | Symptom | Remedy |
|-------|---------|--------|
| Scope creep | "And then we'll also..." | Define explicit non-goals |
| Vague success criteria | "Robot will navigate well" | Quantify: "reach goal within 1m" |
| Missing integration | Subsystems listed, not connected | Draw data flow diagram |
| No fallback | Single path to success | Add graceful degradation |
| Hardware assumption | "Assuming we get the arm" | Simulation-first approach |

### Proposal Checklist

Before submitting:

- [ ] Problem statement is one paragraph
- [ ] Success criteria are measurable
- [ ] Architecture diagram shows all data flows
- [ ] Each subsystem has owner/responsibility
- [ ] Timeline has milestones, not dates
- [ ] Risks have mitigations AND fallbacks
- [ ] Demo scenario is scripted
- [ ] All four course modules appear

### Reference
- Project guidelines: docs/capstone/01-project-guidelines.md
- Architecture template: docs/capstone/templates/architecture-doc-template.md
```

### Example 4: Milestone planning

**Input:**
```
query_type: "planning"
project_phase: "implementation"
subsystems: ["ros2", "simulation", "perception", "vla", "control"]
output_format: "checklist"
```

**Output:**
```markdown
## Implementation Milestone Checklist

### Milestone Structure

Implementation proceeds in integration waves. Each milestone produces a demonstrable capability.

---

### Milestone 1: Foundation

**Goal**: Basic ROS2 system with simulated robot responding to commands.

#### Deliverables

- [ ] ROS2 workspace compiles without errors
- [ ] Launch file starts all core nodes
- [ ] Isaac Sim loads humanoid model
- [ ] Joint states flow: Isaac Sim → ROS2 (verify with `ros2 topic echo`)
- [ ] Joint commands flow: ROS2 → Isaac Sim (verify robot moves)
- [ ] Basic teleoperation works (keyboard/joystick → motion)

#### Validation Test
```bash
# Start system
ros2 launch capstone_bringup simulation.launch.py

# Verify data flow
ros2 topic hz /joint_states  # Should show ~100Hz
ros2 topic pub /joint_command std_msgs/Float64MultiArray "data: [0.1, 0, 0, ...]" --once
# Robot should move in simulation
```

#### Exit Criteria
- [ ] Can command robot to move to 3 different poses
- [ ] Joint state latency < 20ms
- [ ] No error messages in any terminal

---

### Milestone 2: Perception Pipeline

**Goal**: Robot perceives environment and publishes semantic information.

#### Deliverables

- [ ] Camera node publishes images from simulation
- [ ] Perception node processes images
- [ ] Object detections published as typed messages
- [ ] Detections visualized in RViz or simulation
- [ ] False positive rate acceptable for task

#### Validation Test
```bash
# With simulation running
ros2 topic echo /detections --once
# Should show detected objects with positions

# Place known object in scene
# Verify detection appears within 500ms
```

#### Exit Criteria
- [ ] Target objects detected at >80% recall
- [ ] Position error < 10cm at 1m distance
- [ ] Processing rate ≥ 5Hz

---

### Milestone 3: VLA Integration

**Goal**: Language instructions produce robot intentions.

#### Deliverables

- [ ] VLA node loads model successfully
- [ ] Node subscribes to camera and instruction topics
- [ ] Node publishes action intentions
- [ ] Basic instruction → action mapping works
- [ ] Latency measured and documented

#### Validation Test
```bash
# Publish test instruction
ros2 topic pub /instruction std_msgs/String "data: 'pick up the cup'" --once

# Verify action output
ros2 topic echo /vla_action --once
# Should show action type and parameters
```

#### Exit Criteria
- [ ] 5 test instructions produce correct action types
- [ ] Inference latency < 500ms
- [ ] No crashes on malformed input

---

### Milestone 4: Behavior Execution

**Goal**: Robot executes complete behaviors from VLA outputs.

#### Deliverables

- [ ] Behavior state machine implemented
- [ ] State machine receives VLA actions
- [ ] Motion planner generates trajectories
- [ ] Whole-body controller executes motions
- [ ] Basic task completes in simulation

#### Validation Test
```bash
# Issue task command
ros2 action send_goal /execute_task capstone_msgs/action/ExecuteTask \
  "{instruction: 'wave hello'}"

# Observe robot complete waving motion
# Action should return success
```

#### Exit Criteria
- [ ] 3 distinct behaviors execute correctly
- [ ] Behaviors recoverable from pause
- [ ] Error states handled gracefully

---

### Milestone 5: Safety Systems

**Goal**: Robot operates within safe bounds under all conditions.

#### Deliverables

- [ ] E-stop service implemented and tested
- [ ] Joint limits enforced in controller
- [ ] Collision avoidance active
- [ ] Watchdog detects and handles node failures
- [ ] All safety events logged

#### Validation Test
```bash
# Trigger e-stop during motion
ros2 service call /e_stop std_srvs/srv/Trigger

# Robot should stop within 100ms
# Verify log entry created

# Command motion beyond joint limit
# Verify command is rejected, not executed
```

#### Exit Criteria
- [ ] E-stop halts robot in <100ms
- [ ] Joint limits never exceeded
- [ ] System recovers from single node crash

---

### Milestone 6: End-to-End Demonstration

**Goal**: Complete task from instruction to execution.

#### Deliverables

- [ ] Demo scenario scripted and rehearsed
- [ ] Nominal path works 3 consecutive times
- [ ] At least one failure mode has recovery
- [ ] Demo can reset in <2 minutes
- [ ] Backup demonstration prepared

#### Validation Test
```
Full demonstration dry run:
1. System cold start
2. Issue instruction verbally or via interface
3. Robot perceives, reasons, acts
4. Task completes successfully
5. Reset and repeat
```

#### Exit Criteria
- [ ] Demo succeeds 3/5 attempts
- [ ] Total demo time < 10 minutes
- [ ] Graceful handling of at least one failure type

---

### Progress Tracking

| Milestone | Target Week | Status | Blockers |
|-----------|-------------|--------|----------|
| 1. Foundation | Week 2 | | |
| 2. Perception | Week 4 | | |
| 3. VLA Integration | Week 6 | | |
| 4. Behavior Execution | Week 8 | | |
| 5. Safety Systems | Week 9 | | |
| 6. End-to-End Demo | Week 10 | | |

### Reference
- Testing strategies: docs/capstone/08-testing-strategies.md
- Demo preparation: docs/capstone/09-demonstration-prep.md
```

## Integration Notes

This skill synthesizes knowledge from all prior modules:

- **ros2-teaching**: Foundation for all inter-process communication and system design
- **digital-twin-visualization**: Visualization and debugging of integrated system
- **isaac-sim-guidance**: Physics simulation for safe development and testing
- **vla-reasoning**: High-level reasoning that drives robot behavior

The capstone mentor ensures these components work together as a coherent system rather than isolated demonstrations.

## Mentoring Principles

1. **Guide, don't solve**: Provide frameworks for decision-making, not decisions
2. **Celebrate incremental progress**: Each working integration is an achievement
3. **Normalize failure**: Integration bugs are learning opportunities
4. **Maintain perspective**: A working simple system beats a broken complex one
5. **Document decisions**: Future-you will thank present-you

## Version

- Skill version: 1.0.0
- Assumes completion of Modules 1-4
- Last updated: 2025-01-15
