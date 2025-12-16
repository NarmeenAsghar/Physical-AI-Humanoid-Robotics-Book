# Skill: ros2-teaching

## Purpose

Provide structured, step-by-step instruction on ROS2 (Robot Operating System 2) concepts for learners progressing from beginner to intermediate levels. This skill supports the Docusaurus-based robotics book by generating educational content, explanations, and code examples aligned with the curriculum.

## Inputs

| Input | Type | Required | Description |
|-------|------|----------|-------------|
| `topic` | string | Yes | The ROS2 concept to teach (e.g., "nodes", "topics", "services", "URDF") |
| `level` | string | No | Learner level: `beginner` or `intermediate`. Default: `beginner` |
| `context` | string | No | Additional context such as prior knowledge or specific use case |
| `output_format` | string | No | Desired format: `explanation`, `code_example`, `exercise`, `full_lesson`. Default: `explanation` |

## Outputs

| Output | Description |
|--------|-------------|
| Structured explanation | Clear, sequential breakdown of the requested ROS2 concept |
| Code examples | Python code snippets with inline comments explaining each component |
| Exercises | Practice problems with expected outcomes |
| Documentation references | Explicit paths to relevant docs in the book |

## Boundaries

### In Scope

- ROS2 Humble and later distributions
- Python-based node development
- Core concepts: nodes, topics, publishers, subscribers, services, actions, parameters
- URDF and robot description files
- Launch files and configuration
- Basic debugging with `ros2` CLI tools
- Integration with simulation concepts referenced in other modules

### Out of Scope

- ROS1 legacy systems
- C++ node development (unless explicitly requested for comparison)
- Advanced middleware configuration (DDS tuning)
- Hardware driver development
- Production deployment and DevOps

## Linked Documentation Paths

All content aligns with and references the following documentation structure:

```
docs/module-1-ros2/
├── index.md                    # Module overview and learning objectives
├── 01-introduction.md          # What is ROS2, history, ecosystem
├── 02-installation.md          # Setup instructions for Ubuntu/Windows
├── 03-nodes-and-executors.md   # Creating and running nodes
├── 04-topics.md                # Publishers and subscribers
├── 05-services.md              # Request-response communication
├── 06-actions.md               # Long-running tasks with feedback
├── 07-parameters.md            # Runtime configuration
├── 08-urdf-basics.md           # Robot description format
├── 09-launch-files.md          # Multi-node orchestration
├── 10-debugging.md             # CLI tools and troubleshooting
└── exercises/                  # Hands-on practice files
    ├── exercise-01-first-node.md
    ├── exercise-02-pub-sub.md
    └── exercise-03-service-client.md
```

## Instructional Guidelines

1. **Sequential progression**: Build concepts incrementally. Never assume knowledge not yet covered.
2. **Code-first learning**: Provide working code examples before abstract explanations.
3. **Explicit file paths**: Always reference where code or configuration belongs in a ROS2 workspace.
4. **Terminal commands**: Include exact commands learners should run, with expected output.
5. **Error anticipation**: Address common mistakes and their solutions proactively.
6. **No conversational filler**: Deliver direct, technical instruction without pleasantries.

## Example Usage

### Example 1: Teach a concept

**Input:**
```
topic: "topics"
level: "beginner"
output_format: "full_lesson"
```

**Output structure:**
```markdown
## Topics in ROS2

### Learning Objectives
- Understand the publish-subscribe communication pattern
- Create a publisher node in Python
- Create a subscriber node in Python
- Use ros2 topic CLI commands for inspection

### Concept Overview
[Sequential explanation of topics as a communication mechanism]

### Code Example: Publisher Node

File: `~/ros2_ws/src/my_package/my_package/publisher_node.py`

[Annotated Python code]

### Code Example: Subscriber Node

File: `~/ros2_ws/src/my_package/my_package/subscriber_node.py`

[Annotated Python code]

### Running the Examples
[Terminal commands with expected output]

### Common Errors
[Table of errors and solutions]

### Next Steps
See: docs/module-1-ros2/05-services.md
```

### Example 2: Generate an exercise

**Input:**
```
topic: "services"
level: "intermediate"
output_format: "exercise"
```

**Output structure:**
```markdown
## Exercise: Custom Service for Robot State Query

### Objective
Create a service that returns the current state of a simulated robot.

### Requirements
1. Define a custom service type in `srv/GetRobotState.srv`
2. Implement a service server that tracks robot state
3. Implement a client that queries state on demand

### Starter Code
[Partial implementation with TODO markers]

### Acceptance Criteria
- Service responds within 100ms
- Client handles service unavailability gracefully
- State includes: position (x, y, z), battery_level, operational_status

### Solution Reference
See: docs/module-1-ros2/exercises/exercise-03-service-client.md
```

### Example 3: Explain URDF

**Input:**
```
topic: "URDF"
level: "beginner"
output_format: "explanation"
```

**Output structure:**
```markdown
## URDF: Unified Robot Description Format

### What URDF Defines
URDF is an XML specification that describes:
- Links: rigid bodies with visual, collision, and inertial properties
- Joints: connections between links with type, axis, and limits

### Minimal URDF Structure

File: `~/ros2_ws/src/my_robot_description/urdf/robot.urdf`

[XML code with annotations]

### Visualization Command
ros2 launch urdf_tutorial display.launch.py model:=robot.urdf

### Related Documentation
- Full URDF reference: docs/module-1-ros2/08-urdf-basics.md
- Visualization in simulation: docs/module-2-digital-twin/
```

## Integration Notes

This skill coordinates with:
- `digital-twin-visualization`: URDF models connect to simulation visualization
- `isaac-sim-guidance`: ROS2 nodes interface with Isaac Sim environments
- `capstone-mentor`: ROS2 competency is prerequisite for capstone projects

## Version

- Skill version: 1.0.0
- Target ROS2 distribution: Humble Hawksbill (LTS)
- Last updated: 2025-01-15
