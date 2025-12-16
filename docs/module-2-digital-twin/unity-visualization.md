---
sidebar_position: 2
title: "Unity and High-Fidelity Digital Twins"
description: Photorealistic visualization and human-robot interaction with Unity
---

# Unity and High-Fidelity Digital Twins

While Gazebo excels at physics simulation, its rendering capabilities are limited. Unity fills this gap by providing photorealistic visualization, advanced lighting, and the graphical fidelity needed for human-robot interaction research and demonstration.

## Why Unity for Robotics?

Gazebo and Unity serve complementary roles in the digital twin ecosystem:

| Capability | Gazebo | Unity |
|------------|--------|-------|
| Physics accuracy | ✓✓✓ | ✓ |
| Rendering quality | ✓ | ✓✓✓ |
| Sensor simulation | ✓✓✓ | ✓✓ |
| Real-time performance | ✓✓ | ✓✓✓ |
| VR/AR support | Limited | Native |
| Asset ecosystem | Robotics-focused | Massive |

The typical workflow: **Gazebo handles physics truth** while **Unity provides visualization**. Robot state flows from Gazebo through ROS 2 to Unity, which renders the scene with high-fidelity graphics.

### Use Cases for Unity in Physical AI

**1. Synthetic Data Generation**

Training perception models requires massive labeled datasets. Unity's configurable lighting, materials, and camera parameters enable domain randomization—generating millions of synthetic training images with automatic ground truth labels (Tobin et al., 2017).

**2. Human-Robot Interaction Studies**

Studying how humans interact with robots requires realistic visualization. Unity's animation systems, facial expressions, and body language enable believable humanoid representations for HRI experiments.

**3. Demonstration and Communication**

Stakeholder presentations, funding proposals, and public demonstrations benefit from Unity's cinematic quality. A photorealistic humanoid simulation communicates capabilities more effectively than wireframe visualization.

**4. VR Teleoperation Interfaces**

Unity's native VR support enables immersive teleoperation—operators can control humanoid robots through VR headsets with natural hand tracking, improving situational awareness and control precision.

---

## Architecture: Gazebo + Unity Integration

The integration architecture separates physics computation from rendering:

```
┌─────────────────────────────────────────────────────────────────┐
│                    DIGITAL TWIN ARCHITECTURE                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐         ROS 2          ┌─────────────────────┐│
│  │   Gazebo    │◄──────Topics──────────►│   Unity + ROS-TCP   ││
│  │  (Physics)  │                        │  (Visualization)    ││
│  └──────┬──────┘                        └──────────┬──────────┘│
│         │                                          │           │
│         ▼                                          ▼           │
│  ┌─────────────┐                        ┌─────────────────────┐│
│  │ /joint_states│                       │ Photorealistic      ││
│  │ /tf          │                       │ Rendering           ││
│  │ /sensor_data │                       │ + VR/AR Support     ││
│  └─────────────┘                        └─────────────────────┘│
│                                                                 │
│  Physical Truth ◄────────────────────────► Visual Fidelity     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Data Flow**:
1. Gazebo computes physics and publishes joint states to `/joint_states`
2. ROS 2 bridge transmits messages over TCP to Unity
3. Unity applies joint angles to the robot model
4. Unity renders the scene with advanced materials and lighting

---

## Unity-ROS Integration Options

Several approaches connect Unity to ROS 2:

### ROS-TCP-Connector (Recommended)

Unity Robotics Hub's official solution provides bidirectional communication:

```
Unity ◄──── TCP ────► ROS-TCP-Endpoint ◄──── ROS 2 ────► Gazebo
```

**Setup Steps**:
1. Install ROS-TCP-Endpoint package in your ROS 2 workspace
2. Import ROS-TCP-Connector into Unity via Package Manager
3. Configure endpoint IP and port in Unity
4. Create subscribers for robot state topics

### ros2-for-unity

Native ROS 2 client library compiled for Unity—no bridge process required:

```csharp
// Direct ROS 2 communication in Unity
using ROS2;

public class DirectSubscriber : MonoBehaviour
{
    private INode node;
    private ISubscription<sensor_msgs.msg.JointState> subscriber;

    void Start()
    {
        RCLdotnet.Init();
        node = RCLdotnet.CreateNode("unity_subscriber");
        subscriber = node.CreateSubscription<sensor_msgs.msg.JointState>(
            "/joint_states", msg => ApplyJointStates(msg));
    }
}
```

---

## Joint State Synchronization

The core integration task: applying ROS 2 joint states to Unity's articulated robot model.

### Unity C# Subscriber

```csharp
using UnityEngine;
using Unity.Robotics.ROSTCPConnector;
using RosMessageTypes.Sensor;
using System.Collections.Generic;

public class JointStateSubscriber : MonoBehaviour
{
    [SerializeField] private string topicName = "/joint_states";

    // Map joint names to Unity transforms
    private Dictionary<string, ArticulationBody> jointMap;

    void Start()
    {
        // Build joint mapping from robot hierarchy
        jointMap = new Dictionary<string, ArticulationBody>();
        foreach (var joint in GetComponentsInChildren<ArticulationBody>())
        {
            jointMap[joint.name] = joint;
        }

        // Subscribe to joint states
        ROSConnection.GetOrCreateInstance()
            .Subscribe<JointStateMsg>(topicName, OnJointStateReceived);
    }

    void OnJointStateReceived(JointStateMsg msg)
    {
        for (int i = 0; i < msg.name.Length; i++)
        {
            if (jointMap.TryGetValue(msg.name[i], out var joint))
            {
                // Convert radians to degrees for Unity
                float angle = (float)msg.position[i] * Mathf.Rad2Deg;

                var drive = joint.xDrive;
                drive.target = angle;
                joint.xDrive = drive;
            }
        }
    }
}
```

### Robot Import Workflow

1. **Export URDF** from your ROS 2 package
2. **Import to Unity** using URDF Importer package
3. **Configure ArticulationBody** components for physics
4. **Apply materials** and lighting for visual fidelity
5. **Attach subscriber** script to robot root

---

## Rendering for Realism

Unity's rendering pipeline enables photorealistic humanoid visualization:

### High Definition Render Pipeline (HDRP)

For maximum visual quality:
- Physically-based materials with subsurface scattering (skin)
- Ray-traced reflections and global illumination
- Volumetric lighting and fog
- High-quality anti-aliasing

### Universal Render Pipeline (URP)

For real-time performance on standard hardware:
- Optimized PBR materials
- Efficient shadow rendering
- Post-processing effects
- VR-ready performance

### Material Considerations for Humanoids

| Body Part | Material Type | Key Properties |
|-----------|---------------|----------------|
| Skin | Subsurface scattering | Scattering profile, thickness |
| Eyes | Refraction + reflection | Cornea IOR, iris texture |
| Clothing | Fabric shader | Weave pattern, translucency |
| Metal parts | PBR metallic | Roughness, reflectivity |

---

## Synthetic Data Generation

Unity enables creating training datasets for perception models:

```csharp
// Example: Capture labeled training images
public class SyntheticDataCapture : MonoBehaviour
{
    public Camera captureCamera;
    public int imageCount = 10000;

    IEnumerator CaptureDataset()
    {
        for (int i = 0; i < imageCount; i++)
        {
            // Randomize lighting
            RandomizeLighting();

            // Randomize camera pose
            RandomizeCameraPose();

            // Capture RGB image
            CaptureImage($"rgb_{i:D5}.png");

            // Capture segmentation mask (ground truth)
            CaptureSegmentation($"seg_{i:D5}.png");

            yield return null;
        }
    }
}
```

Domain randomization parameters:
- **Lighting**: Direction, intensity, color temperature
- **Materials**: Texture variations, roughness ranges
- **Camera**: Position, orientation, field of view
- **Distractors**: Background objects, occlusions

---

## Exercises

1. **Basic Integration**: Set up ROS-TCP-Connector between your Gazebo humanoid simulation and Unity. Verify that joint movements in Gazebo appear in Unity within 50ms latency.

2. **Material Enhancement**: Import your humanoid URDF to Unity and apply PBR materials to differentiate body parts. Add an environment with realistic lighting and capture screenshots comparing Gazebo vs Unity rendering.

3. **Data Generation**: Create a script that captures 100 images of the humanoid from random viewpoints. Include bounding box annotations for the robot in each frame. Verify annotations align with the rendered robot.

---

## Summary

Unity extends the digital twin beyond physics simulation:

- **Complementary roles**: Gazebo for physics truth, Unity for visual fidelity
- **ROS integration**: ROS-TCP-Connector or ros2-for-unity for communication
- **Joint synchronization**: Subscribe to `/joint_states` and apply to ArticulationBody
- **Rendering pipelines**: HDRP for quality, URP for performance
- **Synthetic data**: Domain randomization for perception training

The combination of Gazebo's accurate physics and Unity's photorealistic rendering creates a complete digital twin platform for Physical AI development.

---

## References

Unity Technologies. (2023). *Unity Robotics Hub*. https://github.com/Unity-Technologies/Unity-Robotics-Hub

Unity Technologies. (2023). *URDF Importer*. Unity Asset Store. https://github.com/Unity-Technologies/URDF-Importer

Tobin, J., Fong, R., Ray, A., Schneider, J., Zaremba, W., & Abbeel, P. (2017). Domain randomization for transferring deep neural networks from simulation to the real world. In *IEEE/RSJ International Conference on Intelligent Robots and Systems* (pp. 23-30).

Juliani, A., Berges, V. P., Teng, E., Cohen, A., Harper, J., Elion, C., ... & Lange, D. (2018). Unity: A general platform for intelligent agents. *arXiv preprint arXiv:1809.02627*.

Mittal, M., Yu, C., Yu, Q., Liu, J., Rudin, N., Hoeller, D., ... & Hutter, M. (2023). Orbit: A unified simulation framework for interactive robot learning environments. *IEEE Robotics and Automation Letters*, 8(6), 3740-3747.
