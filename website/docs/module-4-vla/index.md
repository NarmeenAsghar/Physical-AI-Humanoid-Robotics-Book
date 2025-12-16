---
sidebar_position: 1
title: "Module 4: Vision-Language-Action Robotics"
description: Building robots that understand natural language and act in the physical world
---

# Module 4: Vision-Language-Action Robotics

## Learning Objectives

By the end of this module, you will be able to:

- Explain the Vision-Language-Action (VLA) paradigm for embodied AI
- Integrate speech recognition for voice-commanded robots
- Build LLM-based cognitive planners that generate action sequences
- Execute planned actions through ROS 2 action clients
- Ground language references in visual perception
- Deploy an end-to-end VLA pipeline on a humanoid robot

## Prerequisites

- Completed Modules 1-3 (ROS 2, simulation, perception)
- Python 3.10+ with async programming familiarity
- API access to OpenAI, Anthropic, or local LLM (Ollama)
- Microphone for voice input (or audio files for testing)

---

## What is Vision-Language-Action?

Vision-Language-Action (VLA) represents the convergence of three AI capabilities into unified robotic systems: **seeing** the world through cameras and sensors, **understanding** natural language commands, and **acting** through physical manipulation and navigation.

```
┌─────────────────────────────────────────────────────────────────┐
│                    VLA ARCHITECTURE                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────────┐  │
│  │  Voice  │───►│ Whisper │───►│  LLM    │───►│  Action     │  │
│  │  Input  │    │  (STT)  │    │ Planner │    │  Executor   │  │
│  └─────────┘    └─────────┘    └────┬────┘    └──────┬──────┘  │
│                                     │                │         │
│                                     ▼                ▼         │
│                              ┌─────────────┐  ┌───────────┐   │
│                              │   Object    │  │  ROS 2    │   │
│                              │  Grounding  │  │  Actions  │   │
│                              └──────┬──────┘  └─────┬─────┘   │
│                                     │               │         │
│  ┌─────────┐    ┌─────────┐        │               │         │
│  │ Camera  │───►│ Vision  │────────┘               │         │
│  │  RGB-D  │    │   AI    │                        ▼         │
│  └─────────┘    └─────────┘                 ┌───────────┐    │
│                                             │ Humanoid  │    │
│                                             │  Robot    │    │
│                                             └───────────┘    │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

Traditional robots require explicit programming for every task. VLA systems understand intent from natural language—"pick up the red cup and bring it to me"—and autonomously plan and execute the necessary actions. This paradigm shift, enabled by large language models, represents the frontier of Physical AI research (Brohan et al., 2023).

---

## Speech Recognition with Whisper

OpenAI's Whisper provides state-of-the-art speech recognition that converts spoken commands into text. For robotics, we need real-time transcription published to ROS 2 topics.

### Whisper Model Options

| Model | Size | Speed | Accuracy | Use Case |
|-------|------|-------|----------|----------|
| tiny | 39M | Fastest | Good | Edge devices, real-time |
| base | 74M | Fast | Better | Balanced performance |
| small | 244M | Medium | High | Desktop, quality focus |
| large-v3 | 1.5B | Slow | Best | Offline processing |

### Whisper ROS 2 Node

```python
#!/usr/bin/env python3
"""whisper_node.py - Speech-to-text ROS 2 node using OpenAI Whisper."""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import whisper
import sounddevice as sd
import numpy as np
import queue
import threading

class WhisperNode(Node):
    def __init__(self):
        super().__init__('whisper_node')

        # Parameters
        self.declare_parameter('model_size', 'base')
        self.declare_parameter('sample_rate', 16000)
        self.declare_parameter('chunk_duration', 3.0)

        model_size = self.get_parameter('model_size').value
        self.sample_rate = self.get_parameter('sample_rate').value
        self.chunk_duration = self.get_parameter('chunk_duration').value

        # Load Whisper model
        self.get_logger().info(f'Loading Whisper model: {model_size}')
        self.model = whisper.load_model(model_size)

        # Publisher for transcriptions
        self.text_pub = self.create_publisher(String, '/speech/text', 10)

        # Audio queue and recording thread
        self.audio_queue = queue.Queue()
        self.recording = True

        # Start audio capture thread
        self.audio_thread = threading.Thread(target=self._capture_audio)
        self.audio_thread.start()

        # Timer for processing audio chunks
        self.create_timer(self.chunk_duration, self._process_audio)

        self.get_logger().info('Whisper node ready - listening for speech')

    def _capture_audio(self):
        """Continuously capture audio from microphone."""
        def callback(indata, frames, time, status):
            if status:
                self.get_logger().warn(f'Audio status: {status}')
            self.audio_queue.put(indata.copy())

        with sd.InputStream(samplerate=self.sample_rate, channels=1,
                           callback=callback, blocksize=int(self.sample_rate * 0.1)):
            while self.recording:
                sd.sleep(100)

    def _process_audio(self):
        """Process accumulated audio and transcribe."""
        if self.audio_queue.empty():
            return

        # Collect audio chunks
        chunks = []
        while not self.audio_queue.empty():
            chunks.append(self.audio_queue.get())

        if not chunks:
            return

        # Combine and normalize audio
        audio = np.concatenate(chunks).flatten()
        audio = audio.astype(np.float32)

        # Transcribe with Whisper
        result = self.model.transcribe(audio, language='en')
        text = result['text'].strip()

        if text and len(text) > 2:  # Filter noise
            msg = String()
            msg.data = text
            self.text_pub.publish(msg)
            self.get_logger().info(f'Transcribed: "{text}"')

    def destroy_node(self):
        self.recording = False
        self.audio_thread.join()
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    node = WhisperNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

---

## Cognitive Planning with LLMs

The cognitive planner transforms natural language commands into structured action sequences. Large language models excel at this task when given proper prompts and output schemas.

### Prompt Engineering for Robotics

The key to reliable LLM planning is constraining outputs to valid robot actions:

```python
SYSTEM_PROMPT = """You are a robot task planner. Given a natural language command,
output a JSON array of actions the humanoid robot should execute.

Available actions:
- {"action": "navigate", "target": "<location_name or x,y coordinates>"}
- {"action": "detect_object", "object": "<object description>"}
- {"action": "pick", "object": "<object_id from detection>"}
- {"action": "place", "location": "<location description>"}
- {"action": "speak", "text": "<response to user>"}

Rules:
1. Always detect objects before picking them
2. Navigate to objects before picking
3. Output only valid JSON array
4. If command is unclear, use "speak" to ask for clarification

Example:
Command: "Pick up the red cup from the table"
Output: [
  {"action": "navigate", "target": "table"},
  {"action": "detect_object", "object": "red cup"},
  {"action": "pick", "object": "detected_object_0"},
  {"action": "speak", "text": "I have picked up the red cup"}
]"""
```

### Cognitive Planner Node

```python
#!/usr/bin/env python3
"""cognitive_planner.py - LLM-based task planner for humanoid robot."""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from std_srvs.srv import Trigger
import json
import openai  # or anthropic, ollama

class CognitivePlanner(Node):
    def __init__(self):
        super().__init__('cognitive_planner')

        # Parameters
        self.declare_parameter('llm_provider', 'openai')  # openai, anthropic, ollama
        self.declare_parameter('model', 'gpt-4')
        self.declare_parameter('api_key', '')

        self.provider = self.get_parameter('llm_provider').value
        self.model = self.get_parameter('model').value

        # Initialize LLM client
        self._init_llm_client()

        # Subscribe to speech transcriptions
        self.create_subscription(String, '/speech/text', self._on_command, 10)

        # Publisher for action plans
        self.plan_pub = self.create_publisher(String, '/planner/actions', 10)

        self.get_logger().info(f'Cognitive planner ready with {self.provider}/{self.model}')

    def _init_llm_client(self):
        """Initialize the appropriate LLM client."""
        api_key = self.get_parameter('api_key').value
        if self.provider == 'openai':
            openai.api_key = api_key
            self.client = openai
        # Add other providers as needed

    def _on_command(self, msg):
        """Process incoming voice command."""
        command = msg.data
        self.get_logger().info(f'Planning for command: "{command}"')

        try:
            actions = self._generate_plan(command)

            # Publish action plan
            plan_msg = String()
            plan_msg.data = json.dumps(actions)
            self.plan_pub.publish(plan_msg)

            self.get_logger().info(f'Generated plan: {len(actions)} actions')

        except Exception as e:
            self.get_logger().error(f'Planning failed: {e}')

    def _generate_plan(self, command):
        """Call LLM to generate action plan."""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": command}
            ],
            temperature=0.1,  # Low temperature for consistent output
            response_format={"type": "json_object"}
        )

        # Parse JSON response
        content = response.choices[0].message.content
        plan = json.loads(content)

        # Validate actions
        return self._validate_plan(plan.get('actions', plan))

    def _validate_plan(self, actions):
        """Validate that all actions are executable."""
        valid_actions = ['navigate', 'detect_object', 'pick', 'place', 'speak']
        validated = []

        for action in actions:
            if action.get('action') in valid_actions:
                validated.append(action)
            else:
                self.get_logger().warn(f'Skipping invalid action: {action}')

        return validated

def main(args=None):
    rclpy.init(args=args)
    node = CognitivePlanner()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

---

## ROS 2 Action Execution

The action executor translates LLM-generated plans into ROS 2 action client calls, managing the execution lifecycle with feedback and error handling.

```python
#!/usr/bin/env python3
"""action_executor.py - Executes action sequences on humanoid robot."""

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from std_msgs.msg import String
from nav2_msgs.action import NavigateToPose
from geometry_msgs.msg import PoseStamped
import json

class ActionExecutor(Node):
    def __init__(self):
        super().__init__('action_executor')

        # Action clients
        self.nav_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')

        # Subscribe to action plans
        self.create_subscription(String, '/planner/actions', self._execute_plan, 10)

        # Status publisher
        self.status_pub = self.create_publisher(String, '/executor/status', 10)

        self.get_logger().info('Action executor ready')

    async def _execute_plan(self, msg):
        """Execute a sequence of actions."""
        actions = json.loads(msg.data)

        for i, action in enumerate(actions):
            self.get_logger().info(f'Executing action {i+1}/{len(actions)}: {action["action"]}')

            success = await self._execute_action(action)

            if not success:
                self._publish_status(f'Failed at action {i+1}: {action["action"]}')
                return

        self._publish_status('Plan completed successfully')

    async def _execute_action(self, action):
        """Execute a single action."""
        action_type = action['action']

        if action_type == 'navigate':
            return await self._navigate(action['target'])
        elif action_type == 'detect_object':
            return await self._detect_object(action['object'])
        elif action_type == 'pick':
            return await self._pick_object(action['object'])
        elif action_type == 'place':
            return await self._place_object(action['location'])
        elif action_type == 'speak':
            return self._speak(action['text'])

        return False

    async def _navigate(self, target):
        """Send navigation goal to Nav2."""
        goal = NavigateToPose.Goal()
        goal.pose = self._parse_target(target)

        self.nav_client.wait_for_server()
        result = await self.nav_client.send_goal_async(goal)

        return result.accepted

    def _publish_status(self, status):
        """Publish execution status."""
        msg = String()
        msg.data = status
        self.status_pub.publish(msg)
```

---

## Vision Integration for Object Grounding

Language references like "the red cup" must map to physical objects with 3D coordinates. Object grounding combines detection with depth sensing.

```
┌─────────────────────────────────────────────────────────────────┐
│                OBJECT GROUNDING PIPELINE                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────┐    ┌─────────────┐    ┌─────────────────────────┐ │
│  │  RGB    │───►│   Object    │───►│  Bounding Boxes         │ │
│  │ Camera  │    │  Detector   │    │  + Class Labels         │ │
│  └─────────┘    │  (YOLO)     │    └───────────┬─────────────┘ │
│                 └─────────────┘                │               │
│                                                ▼               │
│  ┌─────────┐                        ┌─────────────────────────┐│
│  │  Depth  │───────────────────────►│  3D Position            ││
│  │ Camera  │                        │  Calculation            ││
│  └─────────┘                        └───────────┬─────────────┘│
│                                                 │               │
│  ┌─────────┐                                    ▼               │
│  │Language │    ┌─────────────┐    ┌─────────────────────────┐ │
│  │Reference│───►│  Attribute  │───►│  Matched Object         │ │
│  │"red cup"│    │  Matching   │    │  with 3D Pose           │ │
│  └─────────┘    └─────────────┘    └─────────────────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

The grounding service receives a language description, queries the object detector, filters by attributes (color, size, type), and returns the 3D position in the robot's coordinate frame.

---

## Complete VLA Pipeline

### Launch File

```python
#!/usr/bin/env python3
"""vla_pipeline.launch.py - Launch complete VLA system."""

from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        # Speech recognition
        Node(
            package='humanoid_vla',
            executable='whisper_node',
            name='whisper',
            parameters=[{'model_size': 'base'}],
            output='screen'
        ),

        # Cognitive planner
        Node(
            package='humanoid_vla',
            executable='cognitive_planner',
            name='planner',
            parameters=[{
                'llm_provider': 'openai',
                'model': 'gpt-4',
            }],
            output='screen'
        ),

        # Action executor
        Node(
            package='humanoid_vla',
            executable='action_executor',
            name='executor',
            output='screen'
        ),

        # Object detection
        Node(
            package='humanoid_vla',
            executable='object_detector',
            name='detector',
            output='screen'
        ),
    ])
```

### Demo: Voice-Commanded Pick-and-Place

```bash
# Terminal 1: Launch VLA pipeline
ros2 launch humanoid_vla vla_pipeline.launch.py

# Terminal 2: Monitor status
ros2 topic echo /executor/status

# Speak command into microphone:
# "Go to the table and pick up the red cup"
```

**Expected behavior**:
1. Whisper transcribes: "Go to the table and pick up the red cup"
2. LLM generates: `[navigate→table, detect→red cup, pick→object]`
3. Executor calls Nav2, then manipulation actions
4. Humanoid navigates to table, identifies cup, grasps it

---

## Exercises

1. **Whisper Integration**: Deploy the Whisper node with different model sizes. Compare transcription accuracy and latency for robotics commands. Document which model provides the best balance for real-time use.

2. **Prompt Engineering**: Modify the cognitive planner's system prompt to handle new action types (e.g., "wave hello", "look at person"). Test with voice commands and verify the LLM generates valid action sequences.

3. **End-to-End Demo**: Run the complete VLA pipeline in simulation. Issue three different voice commands and document the full execution trace from speech to robot action.

---

## Summary

Vision-Language-Action systems represent the integration of modern AI with physical robotics:

- **Whisper** converts voice commands to text in real-time
- **LLM planners** transform natural language into structured action sequences
- **Action executors** translate plans to ROS 2 action client calls
- **Object grounding** maps language references to physical coordinates
- **End-to-end pipelines** enable voice-commanded autonomous robots

The Capstone project builds on this foundation to create a fully autonomous humanoid that responds to natural language commands.

---

## References

Brohan, A., Brown, N., Carbajal, J., Chebotar, Y., Chen, X., Choromanski, K., ... & Zitkovich, B. (2023). RT-2: Vision-language-action models transfer web knowledge to robotic control. *arXiv preprint arXiv:2307.15818*.

Radford, A., Kim, J. W., Xu, T., Brockman, G., McLeavey, C., & Sutskever, I. (2023). Robust speech recognition via large-scale weak supervision. In *International Conference on Machine Learning* (pp. 28492-28518). PMLR.

Ahn, M., Brohan, A., Brown, N., Chebotar, Y., Cortes, O., David, B., ... & Zeng, A. (2022). Do as I can, not as I say: Grounding language in robotic affordances. *arXiv preprint arXiv:2204.01691*.

Liu, S., Zeng, Z., Ren, T., Li, F., Zhang, H., Yang, J., ... & Zhang, L. (2023). Grounding DINO: Marrying DINO with grounded pre-training for open-set object detection. *arXiv preprint arXiv:2303.05499*.

Driess, D., Xia, F., Sajjadi, M. S., Lynch, C., Chowdhery, A., Ichter, B., ... & Florence, P. (2023). PaLM-E: An embodied multimodal language model. *arXiv preprint arXiv:2303.03378*.
