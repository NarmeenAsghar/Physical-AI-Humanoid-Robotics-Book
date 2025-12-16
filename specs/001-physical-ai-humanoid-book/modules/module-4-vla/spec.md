# Module Specification: Vision-Language-Action (VLA) — Embodied AI Control

**Parent Feature**: `001-physical-ai-humanoid-book`
**Module**: 4 of 5
**Created**: 2025-12-16
**Status**: Draft
**Word Target**: 2,000–3,000 words
**Prerequisites**: Module 1 (ROS 2), Module 2 (Simulation), Module 3 (Perception/Navigation)

## Overview

This module teaches students to build Vision-Language-Action (VLA) systems that enable natural language control of humanoid robots. Students learn to integrate speech recognition (OpenAI Whisper), cognitive planning with LLMs (GPT/Qwen), and ROS 2 action execution to create robots that understand spoken commands, reason about tasks, and execute physical actions autonomously.

## User Scenarios & Testing

### User Story 1 - Implement Voice Command Recognition (Priority: P1)

A developer wants their humanoid to respond to voice commands. They integrate OpenAI Whisper for speech-to-text and publish transcriptions to ROS 2 topics in real-time.

**Why this priority**: Voice input is the user interface for VLA systems. Without reliable speech recognition, the entire pipeline cannot function.

**Independent Test**: Student speaks commands and sees accurate transcriptions published to ROS 2 topic.

**Acceptance Scenarios**:

1. **Given** Whisper model loaded, **When** student speaks "pick up the red cup", **Then** transcription appears on `/speech/text` topic within 2 seconds
2. **Given** continuous listening mode, **When** multiple commands are spoken, **Then** each is transcribed and published sequentially
3. **Given** noisy environment simulation, **When** clear command is spoken, **Then** transcription accuracy remains above 90%
4. **Given** ROS 2 node running, **When** no speech detected, **Then** node remains responsive without false positives

---

### User Story 2 - Build LLM Cognitive Planner (Priority: P2)

A researcher wants the robot to understand commands and generate action plans. They connect an LLM (GPT-4, Claude, or Qwen) to interpret natural language and output structured ROS 2 action sequences.

**Why this priority**: The LLM transforms human intent into robot-executable plans. This is the "brain" of the VLA system.

**Independent Test**: Student sends natural language command and receives valid action sequence as structured output.

**Acceptance Scenarios**:

1. **Given** LLM API configured, **When** "navigate to the kitchen" is sent, **Then** planner returns Nav2 goal coordinates
2. **Given** complex command "pick up the cup and bring it to me", **When** processed, **Then** planner outputs sequence: [detect_object, navigate_to_object, grasp, navigate_to_user, release]
3. **Given** ambiguous command, **When** processed, **Then** planner requests clarification or makes reasonable assumption
4. **Given** infeasible command, **When** processed, **Then** planner returns error with explanation

---

### User Story 3 - Execute ROS 2 Action Sequences (Priority: P3)

An engineer wants the planned actions to execute on the robot. They implement an action executor that translates LLM output into ROS 2 action client calls, handling feedback and errors.

**Why this priority**: Execution bridges planning to physical action. Without reliable execution, plans remain theoretical.

**Independent Test**: Student triggers action sequence and observes humanoid performing the planned movements in simulation.

**Acceptance Scenarios**:

1. **Given** action sequence from planner, **When** executor receives it, **Then** each action is called via ROS 2 action client
2. **Given** navigation action, **When** executed, **Then** humanoid moves to target position using Nav2
3. **Given** manipulation action, **When** executed, **Then** arm controller receives joint commands
4. **Given** action failure, **When** detected, **Then** executor reports error and attempts recovery or escalates

---

### User Story 4 - Integrate Vision for Object Detection (Priority: P4)

A developer wants the robot to identify objects mentioned in commands. They integrate computer vision with the VLA pipeline to detect, locate, and track objects in the scene.

**Why this priority**: Vision grounds language in the physical world. "The red cup" must map to actual object coordinates.

**Independent Test**: Student says "pick up the red cup" and system correctly identifies and localizes the cup in the scene.

**Acceptance Scenarios**:

1. **Given** RGB camera stream, **When** "detect red cup" is requested, **Then** bounding box and centroid are returned
2. **Given** depth camera data, **When** object detected, **Then** 3D position in robot frame is calculated
3. **Given** multiple similar objects, **When** color/attribute specified, **Then** correct object is selected
4. **Given** object not visible, **When** detection requested, **Then** system reports "object not found" gracefully

---

### User Story 5 - Complete End-to-End VLA Pipeline (Priority: P5)

A student wants to demonstrate full VLA capability. They run the complete pipeline: voice command → transcription → LLM planning → vision grounding → action execution, observing the humanoid complete a spoken task.

**Why this priority**: End-to-end integration proves the system works. Prepares directly for Capstone.

**Independent Test**: Student speaks "go to the table and pick up the bottle" and humanoid completes the entire task autonomously.

**Acceptance Scenarios**:

1. **Given** all modules integrated, **When** voice command is spoken, **Then** humanoid completes task within reasonable time
2. **Given** pipeline running, **When** new command arrives mid-task, **Then** system queues or handles interruption gracefully
3. **Given** task completion, **When** finished, **Then** system confirms success via speech synthesis or ROS 2 feedback
4. **Given** pipeline failure at any stage, **When** error occurs, **Then** user receives informative feedback

---

### Edge Cases

- What if Whisper API has latency or rate limits? Provide local Whisper model option and caching
- How to handle LLM hallucinations in planning? Implement action validation and feasibility checks
- What if object detection fails? Include fallback behaviors and user clarification prompts
- How to handle interrupted commands? Define command queue and interruption policy
- What if network connectivity is lost? Document offline fallback modes where possible

## Requirements

### Content Requirements

- **CR-001**: Chapter MUST introduce VLA architecture and its role in Physical AI
- **CR-002**: Chapter MUST cover Whisper integration for speech-to-text with ROS 2
- **CR-003**: Chapter MUST explain LLM-based cognitive planning with structured output
- **CR-004**: Chapter MUST demonstrate ROS 2 action execution from LLM plans
- **CR-005**: Chapter MUST integrate vision for object detection and grounding
- **CR-006**: Chapter MUST provide complete end-to-end VLA pipeline example
- **CR-007**: Chapter MUST discuss error handling and graceful degradation

### Technical Requirements

- **TR-001**: All examples MUST run on Ubuntu 22.04 with ROS 2 Humble
- **TR-002**: Whisper integration MUST support both API and local model options
- **TR-003**: LLM integration MUST work with OpenAI API, Anthropic API, or local models (Ollama/Qwen)
- **TR-004**: Action execution MUST use standard ROS 2 action client patterns
- **TR-005**: Vision integration MUST use ROS 2 image transport and standard message types

### Citation Requirements

- **CIT-001**: Chapter MUST cite foundational VLA/embodied AI research papers
- **CIT-002**: Chapter MUST reference at least 5 authoritative sources
- **CIT-003**: Sources SHOULD include peer-reviewed papers on LLM+robotics integration
- **CIT-004**: All citations MUST follow APA 7th edition format

### Key Entities

- **VLA (Vision-Language-Action)**: Architecture combining visual perception, language understanding, and physical action
- **Speech-to-Text**: Conversion of spoken audio to text (Whisper)
- **Cognitive Planner**: LLM component that interprets commands and generates action plans
- **Action Sequence**: Ordered list of robot actions to accomplish a task
- **Object Grounding**: Mapping language references ("the red cup") to physical objects with coordinates
- **Action Client**: ROS 2 component that sends goals and receives feedback from action servers
- **Prompt Engineering**: Designing LLM prompts to produce reliable, structured robot commands

## Chapter Outline

### 1. Introduction to Vision-Language-Action (300 words)
- What is VLA and why it matters for Physical AI
- The perception-reasoning-action loop
- From chatbots to embodied agents
- **Diagram**: VLA architecture overview

### 2. Speech Recognition with Whisper (400 words)
- OpenAI Whisper overview and model sizes
- API vs local model deployment
- ROS 2 integration: audio capture to text topic
- Handling streaming and real-time transcription
- **Code Example**: Whisper ROS 2 node (`whisper_node.py`)
- **Diagram**: Speech-to-text pipeline

### 3. Cognitive Planning with LLMs (450 words)
- LLMs as robot task planners
- Prompt engineering for structured output
- JSON/YAML action schemas
- Handling ambiguity and clarification
- Multi-step reasoning for complex tasks
- **Code Example**: LLM planner node (`cognitive_planner.py`)
- **Diagram**: LLM planning architecture

### 4. ROS 2 Action Execution (400 words)
- ROS 2 actions review (from Module 1)
- Action executor design pattern
- Translating LLM output to action goals
- Feedback handling and progress monitoring
- Error recovery strategies
- **Code Example**: Action executor node (`action_executor.py`)

### 5. Vision Integration for Object Grounding (350 words)
- Object detection in ROS 2 (YOLO, GroundingDINO, or similar)
- Depth-based 3D localization
- Connecting language references to detected objects
- Multi-modal fusion: vision + language
- **Code Example**: Object grounding service (`object_grounder.py`)
- **Diagram**: Vision grounding pipeline

### 6. Complete VLA Pipeline (350 words)
- Integrating all components
- Launch file for full pipeline
- Demo scenario: voice-commanded pick-and-place
- Performance considerations and optimization
- **Code Example**: Complete launch file (`vla_pipeline.launch.py`)
- **Diagram**: End-to-end data flow

### 7. Preparing for Capstone (150 words)
- VLA as the cognitive core of autonomous humanoid
- Integration with navigation and manipulation
- Preview: Capstone autonomous humanoid

### 8. Summary and Exercises (100 words)
- Key concepts recap
- 3 hands-on exercises
- Resources for advanced VLA research

## Diagrams Required

1. **VLA Architecture Overview**: Voice → Whisper → LLM → Actions → Robot
2. **Speech-to-Text Pipeline**: Microphone → Audio → Whisper → Text → ROS 2 Topic
3. **LLM Planning Architecture**: Text command → Prompt → LLM → JSON actions → Validator
4. **Vision Grounding Pipeline**: Camera → Detection → Depth → 3D coordinates → Object reference
5. **End-to-End Data Flow**: Complete pipeline from voice to robot motion

## Code Examples Required

1. **Whisper ROS 2 Node** (`whisper_node.py`): Captures audio, transcribes, publishes to topic
2. **Cognitive Planner** (`cognitive_planner.py`): Receives text, calls LLM API, outputs action JSON
3. **Action Executor** (`action_executor.py`): Parses actions, calls ROS 2 action clients
4. **Object Grounder** (`object_grounder.py`): Detects objects, returns 3D positions
5. **VLA Launch File** (`vla_pipeline.launch.py`): Launches complete pipeline with parameters

## Success Criteria

### Reader Outcomes

- **SC-001**: Reader can run Whisper node and see transcriptions within 30 minutes
- **SC-002**: Reader can configure LLM planner to generate valid action sequences
- **SC-003**: Reader can execute planned actions on simulated humanoid
- **SC-004**: Reader can detect and localize objects mentioned in voice commands
- **SC-005**: Reader can run complete VLA pipeline from voice to robot action

### Content Quality

- **SC-006**: Word count between 2,000-3,000 words
- **SC-007**: Flesch-Kincaid grade level 10-12
- **SC-008**: All examples execute without errors on ROS 2 Humble
- **SC-009**: Minimum 5 citations from authoritative VLA/embodied AI sources
- **SC-010**: All diagrams clearly illustrate multi-modal data flow

## Dependencies

- Module 1 completion (ROS 2 actions, topics)
- Module 2 completion (simulation environment)
- Module 3 completion (perception, navigation)
- Ubuntu 22.04 LTS
- ROS 2 Humble Hawksbill
- Python 3.10+ with async support
- OpenAI API key (or Anthropic/local alternative)
- Whisper model (API or local: whisper-base minimum)
- Object detection model (YOLO, GroundingDINO, or equivalent)
- Microphone for voice input (or audio file simulation)

## Out of Scope

- LLM training or fine-tuning
- Deep NLP theory beyond practical application
- Custom speech recognition model training
- Advanced manipulation planning (grasp synthesis)
- Multi-agent coordination
- Real-time hard constraints (soft real-time acceptable)
- Non-English language support (English only for examples)

## Assumptions

- Reader completed Modules 1-3 with working simulation environment
- Reader has API access to at least one LLM provider (or can run local models)
- Reader has basic understanding of async programming in Python
- Reader has microphone or can use pre-recorded audio for testing
- Network connectivity available for API calls (local alternatives documented)
- Simulation environment from Module 2/3 available for testing
