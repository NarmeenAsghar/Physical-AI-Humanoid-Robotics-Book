---
sidebar_position: 3
title: "Hardware and Lab Infrastructure"
description: Workstation, edge computing, and robot lab requirements for Physical AI development
---

# Hardware and Lab Infrastructure for Physical AI

Physical AI development requires computational infrastructure spanning three tiers: **workstations** for simulation and training, **edge devices** for real-time robot AI, and **robot platforms** for physical experimentation. This appendix provides specifications and cost considerations for building a complete Physical AI lab.

---

## Digital Twin Workstation Requirements

The simulation workstation runs Isaac Sim, Gazebo, and AI training workloads. GPU performance is the primary bottleneck—ray-traced rendering and neural network training both demand significant graphics compute.

### Minimum Specifications

| Component | Minimum | Recommended | Justification |
|-----------|---------|-------------|---------------|
| **GPU** | RTX 3070 (8GB) | RTX 4080 (16GB) | Isaac Sim requires RTX; 16GB enables larger scenes |
| **CPU** | AMD Ryzen 7 / Intel i7 | AMD Ryzen 9 / Intel i9 | Physics simulation is CPU-bound; 8+ cores recommended |
| **RAM** | 32 GB | 64 GB | Large USD scenes and ML training require memory headroom |
| **Storage** | 512 GB NVMe | 1 TB NVMe + 2 TB HDD | Isaac Sim assets are large; fast storage improves load times |
| **OS** | Ubuntu 22.04 LTS | Ubuntu 22.04 LTS | ROS 2 Humble and Isaac Sim have best Linux support |

### GPU Selection Guide

| GPU | VRAM | Isaac Sim | ML Training | Price (2024) |
|-----|------|-----------|-------------|--------------|
| RTX 3070 | 8 GB | Basic scenes | Small models | ~$500 |
| RTX 4070 Ti | 12 GB | Medium scenes | Medium models | ~$800 |
| RTX 4080 | 16 GB | Complex scenes | Large models | ~$1,200 |
| RTX 4090 | 24 GB | Production | Full training | ~$2,000 |
| RTX A6000 | 48 GB | Enterprise | Research-scale | ~$4,500 |

**Recommendation**: For learning and development, RTX 4070 Ti provides the best value. For research labs running multiple parallel simulations, RTX 4090 or A6000 justify the investment.

### Why These Specifications?

**GPU (16GB+ VRAM)**: Isaac Sim's RTX ray tracing consumes 6-8 GB for basic scenes. Adding neural network inference (VSLAM, object detection) and domain randomization requires additional headroom. Under 12 GB leads to frequent out-of-memory errors.

**CPU (8+ cores)**: Gazebo physics runs on CPU. Humanoid robots with 20+ joints at 1000 Hz simulation require substantial single-threaded performance. Multi-core enables parallel ROS 2 node execution.

**RAM (64 GB)**: Large USD scenes can exceed 20 GB. Running Isaac Sim alongside RViz2, multiple terminals, and development tools requires 40+ GB for comfortable operation.

---

## Edge AI Kits

Edge devices run perception and control on the physical robot. NVIDIA Jetson provides the standard platform for ROS 2 robotics with GPU-accelerated AI.

### Jetson Platform Comparison

| Platform | AI Performance | Power | RAM | Use Case | Price |
|----------|---------------|-------|-----|----------|-------|
| Jetson Orin Nano | 40 TOPS | 7-15W | 8 GB | Basic perception, learning | ~$250 |
| Jetson Orin NX | 100 TOPS | 10-25W | 16 GB | Full VSLAM + navigation | ~$600 |
| Jetson AGX Orin | 275 TOPS | 15-60W | 32-64 GB | Complete AI stack + RL | ~$2,000 |

**Recommendation**: Jetson Orin NX offers the best balance for humanoid robots—sufficient for Isaac ROS VSLAM, Nav2, and object detection while maintaining reasonable power consumption.

### Sensor Kit Components

A complete edge AI kit includes:

| Component | Purpose | Example | Price |
|-----------|---------|---------|-------|
| **Stereo Camera** | Depth perception, VSLAM | Intel RealSense D435i | ~$300 |
| **RGB Camera** | Object detection, tracking | Logitech C920 / IMX477 | ~$50-100 |
| **IMU** | Orientation, motion | BNO055 / ICM-20948 | ~$30-50 |
| **LiDAR** | Obstacle detection, mapping | RPLiDAR A1/A2 | ~$100-400 |
| **Microphone Array** | Voice commands | ReSpeaker Mic Array | ~$80 |
| **Speaker** | Audio feedback | USB speaker | ~$20 |

**Complete Edge Kit Cost**: ~$800-1,500 (Jetson Orin NX + sensors)

---

## Robot Lab Options

Physical robot platforms range from affordable learning kits to research-grade humanoids. Choose based on learning goals and budget.

### Tier 1: Proxy Lab (Simulation-First)

**No physical robot required.** All development occurs in simulation with transfer-ready code.

| Component | Purpose | Cost |
|-----------|---------|------|
| Workstation | Isaac Sim, Gazebo | $2,000-4,000 |
| Edge Kit (optional) | Testing Isaac ROS | $800-1,500 |
| **Total** | | **$2,000-5,500** |

**Advantages**: Lowest cost, safest iteration, unlimited experimentation
**Limitations**: No Sim2Real validation, misses physical intuition

### Tier 2: Mini Humanoid Lab

Small humanoid platforms provide real hardware experience at accessible cost.

| Platform | DOF | Height | Features | Price |
|----------|-----|--------|----------|-------|
| Unitree G1 | 23 | 127 cm | Walking, manipulation | ~$16,000 |
| Fourier GR-1 | 32 | 165 cm | Full humanoid | ~$100,000 |
| Open-source (InMoov) | Variable | Custom | DIY, educational | ~$2,000-5,000 |

**Mini Lab Configuration**:

| Component | Cost |
|-----------|------|
| Mini humanoid (Unitree G1 or similar) | $16,000-25,000 |
| Workstation | $3,000 |
| Edge kit (Jetson + sensors) | $1,200 |
| Safety equipment (mats, barriers) | $500 |
| **Total** | **$20,000-30,000** |

### Tier 3: Premium Research Lab

Full-scale humanoid platforms for advanced research.

| Platform | DOF | Capabilities | Price |
|----------|-----|--------------|-------|
| Boston Dynamics Atlas | 28 | Parkour, manipulation | Not for sale |
| Agility Digit | 16 | Walking, carrying | ~$150,000 |
| Tesla Optimus | TBD | General purpose | ~$20,000 (target) |
| Figure 01 | 42 | Full manipulation | ~$200,000+ |

**Premium Lab Configuration**:

| Component | Cost |
|-----------|------|
| Research humanoid | $150,000-500,000 |
| High-end workstations (2x) | $10,000 |
| Motion capture system | $20,000-100,000 |
| Force plates, instrumentation | $15,000 |
| Safety infrastructure | $5,000 |
| **Total** | **$200,000-630,000** |

---

## Cloud vs On-Premises Comparison

Large-scale training and multi-user labs face build-vs-buy decisions.

### Cloud-Native Lab

| Provider | Service | Use Case | Cost Model |
|----------|---------|----------|------------|
| AWS | EC2 G5 instances | Isaac Sim, training | ~$3-8/hour |
| NVIDIA NGC | Omniverse Cloud | Collaborative simulation | Per-seat licensing |
| Google Cloud | A100 instances | Large-scale RL training | ~$10-30/hour |

**Advantages**:
- No capital expenditure
- Instant scaling for large training runs
- Multi-region collaboration

**Disadvantages**:
- Ongoing costs accumulate
- Network latency impacts real-time simulation
- Data transfer costs for large assets

### On-Premises Lab

| Component | Cost | Lifetime |
|-----------|------|----------|
| Workstations (3x) | $12,000 | 4-5 years |
| Network infrastructure | $2,000 | 5+ years |
| UPS, cooling | $1,500 | 5+ years |
| **Total** | **$15,500** | |
| **Annual equivalent** | ~$3,500/year | |

**Advantages**:
- Predictable costs after initial investment
- Zero latency for real-time development
- Full data control

**Disadvantages**:
- Large upfront cost
- Maintenance responsibility
- Scaling requires hardware purchase

### Cost/Latency Decision Matrix

| Scenario | Recommendation | Rationale |
|----------|----------------|-----------|
| Learning/individual | On-prem workstation | Predictable cost, always available |
| Research team (5-10) | Hybrid (on-prem + cloud burst) | Daily work local, large runs in cloud |
| Large-scale RL training | Cloud | Thousands of parallel environments |
| Real-time robot testing | On-prem | Latency-critical |
| Multi-site collaboration | Cloud (NGC) | Shared simulation environments |

---

## Summary Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                 PHYSICAL AI LAB ARCHITECTURE                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              DEVELOPMENT TIER (Workstation)              │   │
│  │  • Isaac Sim / Gazebo simulation                        │   │
│  │  • AI model training and fine-tuning                    │   │
│  │  • Domain randomization, synthetic data                  │   │
│  │  GPU: RTX 4080+ | RAM: 64GB | Storage: 1TB NVMe         │   │
│  └──────────────────────────┬──────────────────────────────┘   │
│                             │ ROS 2 / Ethernet                  │
│                             ▼                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                EDGE TIER (Jetson Orin)                   │   │
│  │  • Real-time perception (VSLAM, detection)              │   │
│  │  • Navigation and control execution                      │   │
│  │  • Sensor fusion and inference                          │   │
│  │  Compute: 100 TOPS | RAM: 16GB | Power: 25W             │   │
│  └──────────────────────────┬──────────────────────────────┘   │
│                             │ CAN / Serial / Ethernet           │
│                             ▼                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              ROBOT TIER (Humanoid Platform)              │   │
│  │  • Joint actuators and sensors                          │   │
│  │  • Cameras, LiDAR, IMU, microphones                     │   │
│  │  • Physical interaction with environment                │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Quick Reference: Lab Configurations

| Lab Type | Workstation | Edge | Robot | Total Cost |
|----------|-------------|------|-------|------------|
| **Proxy (simulation)** | RTX 4070 Ti | Optional | None | $2,500-4,000 |
| **Learning** | RTX 4080 | Jetson Orin NX | DIY/Open-source | $5,000-10,000 |
| **Mini Humanoid** | RTX 4080 | Jetson Orin NX | Unitree G1 | $20,000-30,000 |
| **Research** | RTX 4090 / A6000 | Jetson AGX Orin | Research platform | $200,000+ |

---

## Recommendations by Audience

**Students/Hobbyists**: Start with Proxy Lab (simulation-only). Invest in a capable workstation with RTX 4070 Ti or better. Add Jetson Orin Nano later for edge AI experimentation.

**University Labs**: Mini Humanoid Lab provides real hardware experience. Budget $25,000-50,000 for complete setup including safety infrastructure.

**Research Institutions**: Premium Lab with motion capture and instrumentation. Plan for $300,000+ initial investment with ongoing maintenance budget.

**Industry R&D**: Hybrid cloud/on-prem with dedicated simulation clusters. Focus on Sim2Real pipeline efficiency rather than hardware diversity.

---

## References

NVIDIA. (2023). *Isaac Sim System Requirements*. https://docs.omniverse.nvidia.com/isaacsim/latest/installation/requirements.html

NVIDIA. (2023). *Jetson Modules Comparison*. https://developer.nvidia.com/embedded/jetson-modules

Open Robotics. (2023). *ROS 2 Hardware Recommendations*. https://docs.ros.org/en/humble/

Intel. (2023). *RealSense Depth Camera D435i Specifications*. https://www.intelrealsense.com/depth-camera-d435i/
