---
sidebar_position: 1
title: "Capstone: The Autonomous Humanoid Robot"
description: Integrating all modules into a voice-commanded autonomous humanoid system
---

# Capstone: The Autonomous Humanoid Robot

The capstone project integrates everything you've learned—ROS 2 architecture, digital twin simulation, GPU-accelerated perception, and vision-language-action pipelines—into a complete autonomous humanoid system. By the end, your robot will receive voice commands, plan task sequences, navigate environments, perceive objects, and perform manipulation.

## Reference Scenario

**Voice Command**: *"Go to the table, pick up the bottle, and place it on the shelf."*

This single sentence triggers a cascade of AI systems working in concert:

1. **Speech Recognition**: Whisper converts audio to text
2. **Cognitive Planning**: LLM decomposes command into action sequence
3. **Navigation**: Nav2 plans path to table, avoiding obstacles
4. **Perception**: Vision system detects and localizes the bottle
5. **Manipulation**: Arm controller executes grasp
6. **Navigation**: Robot carries object to shelf
7. **Manipulation**: Arm places object at target location
8. **Feedback**: System announces task completion

---

## System Architecture

The autonomous humanoid operates through coordinated ROS 2 nodes spanning six subsystems:

```
┌─────────────────────────────────────────────────────────────────┐
│                 AUTONOMOUS HUMANOID ARCHITECTURE                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    VOICE INTERFACE                       │   │
│  │  ┌─────────────┐         ┌─────────────────────────┐    │   │
│  │  │   Whisper   │────────►│  /speech/text           │    │   │
│  │  │   Node      │         │  (std_msgs/String)      │    │   │
│  │  └─────────────┘         └───────────┬─────────────┘    │   │
│  └──────────────────────────────────────┼──────────────────┘   │
│                                         ▼                       │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                  COGNITIVE LAYER                         │   │
│  │  ┌─────────────┐         ┌─────────────────────────┐    │   │
│  │  │    LLM      │────────►│  /task/plan             │    │   │
│  │  │   Planner   │         │  (TaskPlan msg)         │    │   │
│  │  └─────────────┘         └───────────┬─────────────┘    │   │
│  └──────────────────────────────────────┼──────────────────┘   │
│                                         ▼                       │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                  EXECUTION LAYER                         │   │
│  │  ┌─────────────────────────────────────────────────┐    │   │
│  │  │              Task Executor                       │    │   │
│  │  │         (State Machine / Behavior Tree)          │    │   │
│  │  └───────┬─────────────┬─────────────┬─────────────┘    │   │
│  └──────────┼─────────────┼─────────────┼──────────────────┘   │
│             ▼             ▼             ▼                       │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐               │
│  │ Navigation  │ │ Perception  │ │Manipulation │               │
│  │   (Nav2)    │ │(Isaac ROS)  │ │  (MoveIt2)  │               │
│  └──────┬──────┘ └──────┬──────┘ └──────┬──────┘               │
│         └───────────────┼───────────────┘                       │
│                         ▼                                       │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                 SIMULATION LAYER                         │   │
│  │              Gazebo / Isaac Sim                          │   │
│  │         (Physics, Sensors, Rendering)                    │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### ROS 2 Interface Map

| Interface | Type | Message/Service | Purpose |
|-----------|------|-----------------|---------|
| `/speech/text` | Topic | std_msgs/String | Transcribed voice commands |
| `/task/plan` | Topic | custom/TaskPlan | Action sequence from LLM |
| `/task/status` | Topic | std_msgs/String | Current execution state |
| `/navigate_to_pose` | Action | NavigateToPose | Navigation goals |
| `/perception/detect` | Service | DetectObject | Object detection requests |
| `/arm/pick` | Action | PickObject | Grasp execution |
| `/arm/place` | Action | PlaceObject | Place execution |

---

## Data and Control Flow

### Voice to Plan

When the user speaks, data flows through the cognitive pipeline:

```python
# 1. Whisper transcription
audio_input → whisper_node → "/speech/text": "Go to the table..."

# 2. LLM planning (cognitive_planner receives text)
{
  "command": "Go to the table, pick up the bottle, place it on shelf",
  "actions": [
    {"type": "navigate", "target": "table"},
    {"type": "detect", "object": "bottle"},
    {"type": "pick", "object_id": "detected_0"},
    {"type": "navigate", "target": "shelf"},
    {"type": "place", "location": "shelf_surface"}
  ]
}
```

### Plan to Execution

The task executor processes each action sequentially:

```python
#!/usr/bin/env python3
"""task_executor.py - State machine executing planned actions."""

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from nav2_msgs.action import NavigateToPose
from std_msgs.msg import String
import json
from enum import Enum, auto

class TaskState(Enum):
    IDLE = auto()
    PLANNING = auto()
    NAVIGATING = auto()
    PERCEIVING = auto()
    PICKING = auto()
    PLACING = auto()
    COMPLETE = auto()
    FAILED = auto()

class TaskExecutor(Node):
    def __init__(self):
        super().__init__('task_executor')

        # State management
        self.state = TaskState.IDLE
        self.current_plan = []
        self.action_index = 0

        # Action clients
        self.nav_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')

        # Subscribers
        self.create_subscription(String, '/task/plan', self._on_plan, 10)

        # Publishers
        self.status_pub = self.create_publisher(String, '/task/status', 10)

        self.get_logger().info('Task Executor ready')

    def _on_plan(self, msg):
        """Receive new task plan from cognitive planner."""
        plan = json.loads(msg.data)
        self.current_plan = plan.get('actions', [])
        self.action_index = 0
        self._execute_next_action()

    def _execute_next_action(self):
        """Execute the next action in the plan."""
        if self.action_index >= len(self.current_plan):
            self._complete_task()
            return

        action = self.current_plan[self.action_index]
        action_type = action['type']

        self._publish_status(f"Executing: {action_type}")

        if action_type == 'navigate':
            self._execute_navigation(action)
        elif action_type == 'detect':
            self._execute_detection(action)
        elif action_type == 'pick':
            self._execute_pick(action)
        elif action_type == 'place':
            self._execute_place(action)

    def _execute_navigation(self, action):
        """Send navigation goal to Nav2."""
        self.state = TaskState.NAVIGATING
        goal = NavigateToPose.Goal()
        goal.pose = self._lookup_location(action['target'])

        future = self.nav_client.send_goal_async(goal)
        future.add_done_callback(self._on_nav_complete)

    def _on_nav_complete(self, future):
        """Handle navigation completion."""
        result = future.result()
        if result.status == 4:  # SUCCEEDED
            self.action_index += 1
            self._execute_next_action()
        else:
            self._handle_failure("Navigation failed")

    def _complete_task(self):
        """Mark task as complete."""
        self.state = TaskState.COMPLETE
        self._publish_status("Task completed successfully")

    def _handle_failure(self, reason):
        """Handle action failure with recovery attempt."""
        self.state = TaskState.FAILED
        self._publish_status(f"Task failed: {reason}")
        # Attempt recovery or notify user

    def _publish_status(self, status):
        """Publish current execution status."""
        msg = String()
        msg.data = status
        self.status_pub.publish(msg)
        self.get_logger().info(status)
```

---

## Failure Handling and Recovery

Robust systems anticipate and handle failures at every stage:

### Failure Taxonomy

| Stage | Failure Mode | Detection | Recovery Strategy |
|-------|--------------|-----------|-------------------|
| Speech | Transcription error | Low confidence score | Request repeat |
| Planning | Invalid action | Schema validation | Re-prompt LLM |
| Navigation | Path blocked | Nav2 timeout | Replan or report |
| Perception | Object not found | Empty detection | Search behavior |
| Manipulation | Grasp failed | Force feedback | Retry with offset |

### Feedback Loop Architecture

```
┌────────────────────────────────────────────────────────────┐
│                    FEEDBACK LOOP                           │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  Action Request ──► Execution ──► Result                   │
│        ▲                              │                    │
│        │                              ▼                    │
│        │                        ┌──────────┐               │
│        │                        │ Success? │               │
│        │                        └────┬─────┘               │
│        │                   Yes ──────┴────── No            │
│        │                    │                │             │
│        │                    ▼                ▼             │
│        │              Next Action      ┌──────────┐        │
│        │                               │ Retry?   │        │
│        │                               └────┬─────┘        │
│        │                          Yes ──────┴────── No     │
│        │                           │                │      │
│        └───────────────────────────┘                ▼      │
│                                              Report Failure │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

---

## Master Launch File

```python
#!/usr/bin/env python3
"""capstone.launch.py - Launch complete autonomous humanoid system."""

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, GroupAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node, PushRosNamespace
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    # Package directories
    sim_pkg = get_package_share_directory('humanoid_sim')
    vla_pkg = get_package_share_directory('humanoid_vla')
    nav_pkg = get_package_share_directory('humanoid_nav')

    # Simulation (Gazebo or Isaac Sim)
    simulation = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(sim_pkg, 'launch', 'gazebo_bringup.launch.py')
        )
    )

    # Navigation stack
    navigation = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(nav_pkg, 'launch', 'nav2_bringup.launch.py')
        ),
        launch_arguments={'use_sim_time': 'true'}.items()
    )

    # Voice interface
    whisper = Node(
        package='humanoid_vla',
        executable='whisper_node',
        name='whisper',
        parameters=[{'model_size': 'base'}]
    )

    # Cognitive planner
    planner = Node(
        package='humanoid_vla',
        executable='cognitive_planner',
        name='cognitive_planner',
        parameters=[{'llm_provider': 'openai', 'model': 'gpt-4'}]
    )

    # Task executor
    executor = Node(
        package='humanoid_capstone',
        executable='task_executor',
        name='task_executor'
    )

    # Perception
    perception = Node(
        package='humanoid_perception',
        executable='object_detector',
        name='object_detector'
    )

    # System monitor
    monitor = Node(
        package='humanoid_capstone',
        executable='system_monitor',
        name='system_monitor'
    )

    return LaunchDescription([
        simulation,
        navigation,
        whisper,
        planner,
        executor,
        perception,
        monitor
    ])
```

---

## Demo Walkthrough

### Step 1: Launch the System

```bash
# Terminal 1: Launch capstone
ros2 launch humanoid_capstone capstone.launch.py

# Terminal 2: Monitor status
ros2 topic echo /task/status
```

### Step 2: Issue Voice Command

Speak into the microphone: *"Go to the table, pick up the bottle, and place it on the shelf."*

### Step 3: Observe Execution

Watch the terminal output:

```
[whisper_node] Transcribed: "Go to the table, pick up the bottle..."
[cognitive_planner] Generated plan with 5 actions
[task_executor] Executing: navigate to table
[task_executor] Navigation complete
[task_executor] Executing: detect bottle
[object_detector] Detected: bottle at (1.2, 0.5, 0.8)
[task_executor] Executing: pick bottle
[task_executor] Grasp successful
[task_executor] Executing: navigate to shelf
[task_executor] Navigation complete
[task_executor] Executing: place on shelf
[task_executor] Place successful
[task_executor] Task completed successfully
```

### Step 4: Verify in RViz2

Visualize the complete execution:
- Navigation path (green line)
- Object detection markers (bounding boxes)
- Robot pose and joint states
- Sensor data streams

---

## Exercises

1. **Multi-Object Task**: Modify the system to handle "Pick up the cup and the bottle, then place them both on the counter." Extend the task executor to manage multiple objects in sequence.

2. **Error Recovery**: Introduce a simulated failure (block navigation path mid-execution). Implement and test recovery behavior that replans around obstacles.

3. **Natural Interaction**: Add speech synthesis feedback so the robot announces its intentions and progress. The robot should say "I'm heading to the table" before navigating.

---

## Summary

The capstone demonstrates the complete Physical AI pipeline:

- **Voice Interface** captures natural language commands via Whisper
- **Cognitive Planning** with LLMs transforms intent into action sequences
- **Task Execution** coordinates navigation, perception, and manipulation
- **Failure Handling** ensures robust operation with recovery strategies
- **Feedback Loops** provide visibility and enable debugging

You have built a voice-controlled autonomous humanoid robot—the embodiment of Physical AI principles.

---

## References

Ahn, M., Brohan, A., Brown, N., Chebotar, Y., Cortes, O., David, B., ... & Zeng, A. (2022). Do as I can, not as I say: Grounding language in robotic affordances. *arXiv preprint arXiv:2204.01691*.

Colledanchise, M., & Ögren, P. (2018). Behavior trees in robotics and AI: An introduction. *CRC Press*.

Macenski, S., Foote, T., Gerkey, B., Lalancette, C., & Woodall, W. (2022). Robot Operating System 2: Design, architecture, and uses in the wild. *Science Robotics*, 7(66), eabm6074.

Chitta, S., Sucan, I., & Cousins, S. (2012). MoveIt! *IEEE Robotics & Automation Magazine*, 19(1), 18-19.

Brohan, A., Brown, N., Carbajal, J., Chebotar, Y., Chen, X., Choromanski, K., ... & Zitkovich, B. (2023). RT-2: Vision-language-action models transfer web knowledge to robotic control. *arXiv preprint arXiv:2307.15818*.
