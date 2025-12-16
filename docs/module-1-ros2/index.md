---
sidebar_position: 1
title: "Module 1: ROS 2 — The Robotic Nervous System"
description: Understanding ROS 2 architecture and communication primitives for humanoid robots
---

# Module 1: ROS 2 — The Robotic Nervous System

## Learning Objectives

By the end of this module, you will be able to:

- Explain the role of ROS 2 as middleware for robotic systems
- Distinguish between nodes, topics, services, and actions
- Design communication patterns appropriate for different robotic tasks
- Trace data flow through a humanoid robot's ROS 2 node graph
- Create basic ROS 2 packages with Python nodes

## Prerequisites

- Python programming experience (functions, classes, callbacks)
- Basic Linux command-line proficiency
- ROS 2 Humble installed on Ubuntu 22.04 (see [Installation Guide](/appendices/installation))

---

## Why Robots Need a Nervous System

A humanoid robot is not a single program—it is a distributed system. Cameras capture images at 30 frames per second. IMUs report orientation at 100 Hz. Joint encoders stream position data from dozens of actuators. Meanwhile, perception algorithms identify objects, planners compute trajectories, and controllers generate motor commands. How do all these components communicate?

The human nervous system provides an apt analogy. Sensory neurons transmit signals from receptors to the brain. The brain processes information and generates motor commands. Motor neurons carry those commands to muscles. The system operates through standardized signaling protocols that allow billions of neurons to coordinate seamlessly.

ROS 2 (Robot Operating System 2) serves as the nervous system for robots. It provides standardized communication protocols that enable independent software components—called **nodes**—to exchange data reliably. A camera driver node publishes images. A perception node subscribes to images and publishes detected objects. A planner node subscribes to objects and publishes trajectories. Each component operates independently yet integrates into a coherent system.

### Why ROS 2 Over ROS 1?

ROS 1, introduced in 2007, revolutionized robotics research by providing reusable libraries and tools. However, its architecture assumed a single robot operating in a research lab with reliable networking. ROS 2, released in 2017, addresses limitations that emerged as robots moved into production environments (Macenski et al., 2022):

| Feature | ROS 1 | ROS 2 |
|---------|-------|-------|
| Communication | Custom TCP/UDP | DDS (industry standard) |
| Real-time support | Limited | Native support |
| Security | None built-in | DDS Security |
| Multi-robot | Complex | First-class support |
| Platforms | Linux only | Linux, Windows, macOS |
| Lifecycle | Ad-hoc | Managed node lifecycle |

For humanoid robots that must operate reliably in dynamic environments, ROS 2's improvements in real-time performance, security, and multi-platform support make it the clear choice for new development.

---

## ROS 2 Architecture Deep Dive

ROS 2's architecture centers on four communication primitives: **nodes**, **topics**, **services**, and **actions**. Understanding when to use each is fundamental to designing effective robot software.

### Nodes: The Computational Units

A **node** is an executable that performs computation within the ROS 2 system. Each node should have a single, well-defined purpose: one node for camera processing, another for path planning, another for motor control. This modular design enables:

- **Fault isolation**: A crashed perception node doesn't bring down motor control
- **Reusability**: The same camera driver works across different robots
- **Distributed computing**: Nodes can run on different machines
- **Independent development**: Teams can develop nodes in parallel

Nodes communicate through the other three primitives. A well-designed ROS 2 system consists of many small nodes rather than a few monolithic programs.

### Topics: Asynchronous Data Streams

**Topics** implement the publish-subscribe pattern for asynchronous communication. A publisher node sends messages to a named topic. Any number of subscriber nodes can receive those messages. Publishers and subscribers are decoupled—neither knows about the other's existence.

```
┌─────────────┐         /camera/image         ┌─────────────────┐
│ Camera Node │ ──────────────────────────────▶│ Perception Node │
└─────────────┘     (sensor_msgs/Image)       └─────────────────┘
                            │
                            │
                            ▼
                    ┌───────────────┐
                    │ Logger Node   │
                    └───────────────┘
```

Topics are ideal for:
- **Sensor data**: Continuous streams of images, laser scans, IMU readings
- **State information**: Robot pose, joint positions, battery level
- **Commands**: Velocity commands, trajectory waypoints

Each topic has a **message type** that defines its data structure. ROS 2 provides standard message types (`sensor_msgs/Image`, `geometry_msgs/Twist`) and supports custom types for application-specific data.

**Quality of Service (QoS)** policies control reliability and performance:
- **Reliable**: Guarantees delivery (use for commands)
- **Best effort**: Accepts message loss (use for high-frequency sensors)
- **History depth**: How many messages to buffer

### Services: Synchronous Request-Response

**Services** implement synchronous communication where a client sends a request and waits for a response. Unlike topics, services involve exactly two parties and block until completion.

```
┌─────────────┐      /get_map (Request)       ┌─────────────┐
│ Planner     │ ─────────────────────────────▶│ Map Server  │
│ Node        │                               │ Node        │
│             │◀───────────────────────────── │             │
└─────────────┘      /get_map (Response)      └─────────────┘
```

Services are ideal for:
- **Configuration queries**: "What is the current map?"
- **One-shot computations**: "Compute inverse kinematics for this pose"
- **State changes**: "Enable motor power"

Avoid services for continuous data—the blocking nature creates bottlenecks. If you need frequent queries, consider publishing the data on a topic instead.

### Actions: Long-Running Tasks with Feedback

**Actions** handle long-running tasks that need progress feedback and cancellation support. An action client sends a goal to an action server. The server executes the task, periodically sending feedback, and eventually returns a result.

```
┌─────────────┐                              ┌─────────────────┐
│ Task        │ ── Goal: Navigate to (3,4) ──▶│ Navigation      │
│ Manager     │                              │ Action Server   │
│             │◀── Feedback: 50% complete ── │                 │
│             │◀── Feedback: 75% complete ── │                 │
│             │◀── Result: Succeeded ─────── │                 │
└─────────────┘                              └─────────────────┘
```

Actions are ideal for:
- **Navigation**: Move to a goal position
- **Manipulation**: Pick up an object
- **Behaviors**: Execute a multi-step task

The three-part structure (goal, feedback, result) and cancellation support make actions essential for robot behaviors that take significant time.

---

## Humanoid Robot Node Graph

A humanoid robot requires coordinating dozens of components. The following diagram illustrates a typical node graph architecture:

```
                        ┌─────────────────────────────────────────┐
                        │           PERCEPTION LAYER              │
                        │  ┌─────────┐  ┌─────────┐  ┌─────────┐ │
                        │  │ Camera  │  │ Depth   │  │  IMU    │ │
                        │  │ Driver  │  │ Driver  │  │ Driver  │ │
                        │  └────┬────┘  └────┬────┘  └────┬────┘ │
                        │       │            │            │       │
                        │       ▼            ▼            ▼       │
                        │    /image      /depth       /imu/data   │
                        └───────┼────────────┼────────────┼───────┘
                                │            │            │
                        ┌───────▼────────────▼────────────▼───────┐
                        │           PROCESSING LAYER              │
                        │  ┌─────────────┐  ┌─────────────────┐   │
                        │  │  Object     │  │  State          │   │
                        │  │  Detection  │  │  Estimation     │   │
                        │  └──────┬──────┘  └────────┬────────┘   │
                        │         │                  │            │
                        │         ▼                  ▼            │
                        │    /detected_objects   /robot_state     │
                        └─────────┼──────────────────┼────────────┘
                                  │                  │
                        ┌─────────▼──────────────────▼────────────┐
                        │           PLANNING LAYER                │
                        │  ┌─────────────┐  ┌─────────────────┐   │
                        │  │  Motion     │  │  AI Cognitive   │   │
                        │  │  Planner    │  │  Planner        │   │
                        │  └──────┬──────┘  └────────┬────────┘   │
                        │         │                  │            │
                        │         ▼                  ▼            │
                        │    /trajectory        /task_plan        │
                        └─────────┼──────────────────┼────────────┘
                                  │                  │
                        ┌─────────▼──────────────────▼────────────┐
                        │           CONTROL LAYER                 │
                        │  ┌─────────────────────────────────┐    │
                        │  │       Joint Controllers         │    │
                        │  │   (head, arms, torso, legs)     │    │
                        │  └──────────────┬──────────────────┘    │
                        │                 │                       │
                        │                 ▼                       │
                        │          /joint_commands                │
                        └─────────────────┼───────────────────────┘
                                          │
                                          ▼
                                    ┌───────────┐
                                    │  Hardware │
                                    │  Interface│
                                    └───────────┘
```

**Data Flow Example: "Look at detected object"**

1. Camera driver publishes image to `/image` (topic, 30 Hz)
2. Object detection subscribes to `/image`, publishes to `/detected_objects` (topic)
3. AI planner subscribes to `/detected_objects`, decides to look at object
4. AI planner calls motion planner service to compute head trajectory
5. Motion planner publishes trajectory to `/trajectory` (topic)
6. Joint controller subscribes to `/trajectory`, publishes to `/joint_commands`
7. Hardware interface executes joint commands

This layered architecture separates concerns: perception nodes don't know about control, planners don't know about hardware. Changes to one layer don't require changes to others.

---

## Choosing the Right Communication Pattern

When designing a ROS 2 system, selecting the appropriate primitive for each interaction is crucial:

| Use Case | Primitive | Rationale |
|----------|-----------|-----------|
| Sensor data stream | Topic | Continuous, multiple consumers |
| Motor commands | Topic | Continuous, best-effort OK |
| Get current map | Service | One-shot query, needs response |
| Set parameter | Service | Configuration change |
| Navigate to goal | Action | Long-running, needs feedback |
| Pick up object | Action | Multi-step, cancellable |
| Emergency stop | Topic + Service | Broadcast + confirmation |

> **Key Insight**: Topics flow continuously like rivers. Services are like phone calls—you wait for an answer. Actions are like hiring a contractor—they work on your task and report progress.

---

## Summary

ROS 2 provides the communication infrastructure that enables humanoid robots to function as integrated systems. The key concepts are:

- **Nodes** are independent processes with single responsibilities
- **Topics** enable asynchronous publish-subscribe for continuous data
- **Services** provide synchronous request-response for queries and commands
- **Actions** manage long-running tasks with feedback and cancellation
- **QoS policies** control reliability and performance tradeoffs

The layered architecture—perception, processing, planning, control—separates concerns and enables modular development. In the next section, we'll put these concepts into practice by building our first ROS 2 package.

---

## Exercises

1. **Diagram Exercise**: Draw a node graph for a humanoid robot that tracks a person and follows them. Identify which communications should be topics, services, or actions.

2. **Design Exercise**: You need to implement a "wave hello" behavior. The robot should raise its arm, wave three times, and lower its arm. Which ROS 2 primitive would you use? Why?

3. **Analysis Exercise**: A robot's camera node publishes at 30 Hz, but the perception node can only process 10 frames per second. What QoS settings would prevent the perception node from falling behind?

---

## References

Macenski, S., Foote, T., Gerkey, B., Lalancette, C., & Woodall, W. (2022). Robot Operating System 2: Design, architecture, and uses in the wild. *Science Robotics*, 7(66), eabm6074. https://doi.org/10.1126/scirobotics.abm6074

Open Robotics. (2023). *ROS 2 Documentation: Humble Hawksbill*. https://docs.ros.org/en/humble/

Quigley, M., Conley, K., Gerkey, B., Faust, J., Foote, T., Leibs, J., ... & Ng, A. Y. (2009). ROS: An open-source robot operating system. In *ICRA Workshop on Open Source Software* (Vol. 3, No. 3.2, p. 5).

OMG. (2015). *Data Distribution Service (DDS) Specification, Version 1.4*. Object Management Group. https://www.omg.org/spec/DDS/
