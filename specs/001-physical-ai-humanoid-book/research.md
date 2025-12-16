# Research: Physical AI & Humanoid Robotics Book

**Feature**: `001-physical-ai-humanoid-book`
**Date**: 2025-12-16
**Phase**: 0 (Research)

## Overview

This document consolidates research findings for the Physical AI & Humanoid Robotics technical book. All technical decisions are documented with rationale and alternatives considered.

## Technology Decisions

### 1. ROS 2 Version Selection

**Decision**: ROS 2 Humble Hawksbill (LTS) as primary, Iron as secondary

**Rationale**:
- Humble is the current LTS release (support until 2027)
- Widest hardware and package compatibility
- Most documentation and community support available
- Iron offers newer features but shorter support window

**Alternatives Considered**:
| Option | Pros | Cons | Rejected Because |
|--------|------|------|------------------|
| ROS 2 Iron only | Latest features | Shorter support, less tested | Readers need stable LTS |
| ROS 2 Rolling | Bleeding edge | Unstable, breaking changes | Not suitable for educational content |
| ROS 1 Noetic | Legacy support | EOL 2025, no future | Deprecated, not recommended |

**Sources**:
- ROS 2 Releases: https://docs.ros.org/en/rolling/Releases.html
- REP-2000: ROS 2 Version Policy

---

### 2. Simulation Environment Strategy

**Decision**: Gazebo Harmonic (primary), NVIDIA Isaac Sim (advanced), Unity (visualization)

**Rationale**:
- Gazebo is open-source, well-integrated with ROS 2, and accessible
- Isaac Sim provides photorealistic rendering and GPU-accelerated perception
- Unity fills the high-fidelity visualization gap with broader tooling
- Progressive complexity matches pedagogical goals

**Alternatives Considered**:
| Option | Pros | Cons | Rejected Because |
|--------|------|------|------------------|
| Gazebo only | Simple, open-source | Limited photorealism | Insufficient for advanced perception |
| Isaac Sim only | Most capable | Requires RTX GPU, steep learning curve | Not accessible to all readers |
| Webots | Cross-platform | Less ROS 2 integration | Not industry standard |
| CoppeliaSim | Flexible | Complex licensing, less ROS 2 | Industry prefers Gazebo/Isaac |

**Sources**:
- Gazebo Sim Documentation: https://gazebosim.org/docs
- NVIDIA Isaac Sim: https://developer.nvidia.com/isaac-sim
- Koenig, N., & Howard, A. (2004). Design and use paradigms for Gazebo. IEEE IROS.

---

### 3. Humanoid Robot Model

**Decision**: Generic humanoid URDF created from scratch (simplified)

**Rationale**:
- Avoids licensing issues with commercial robot models
- Readers understand robot description from fundamentals
- Can be customized for teaching purposes
- Matches common humanoid structure (torso, head, arms, legs)

**Alternatives Considered**:
| Option | Pros | Cons | Rejected Because |
|--------|------|------|------------------|
| NAO robot model | Well-documented | Proprietary, licensing unclear | Legal concerns |
| Pepper model | Popular platform | Complex, proprietary | Not freely available |
| Atlas (Boston Dynamics) | Impressive demos | Proprietary, no public URDF | Not accessible |
| Custom from scratch | Full control, educational | More work | Selected approach |

**Sources**:
- URDF Specification: https://wiki.ros.org/urdf
- ROS 2 URDF Tutorial: https://docs.ros.org/en/humble/Tutorials/Intermediate/URDF/

---

### 4. LLM Integration Approach

**Decision**: Multi-provider support (OpenAI API, Anthropic API, local Ollama/Qwen)

**Rationale**:
- No single LLM provider lock-in
- Readers can use API they have access to
- Local options for privacy/offline scenarios
- Demonstrates abstraction pattern for robotics

**Alternatives Considered**:
| Option | Pros | Cons | Rejected Because |
|--------|------|------|------------------|
| OpenAI only | Most capable, well-documented | Vendor lock-in, cost | Not accessible to all |
| Local only (Ollama) | Free, private | Less capable, resource intensive | Limits VLA quality |
| Anthropic only | Strong reasoning | Less common in robotics | Limited ecosystem |
| Multi-provider | Flexibility, accessibility | More code complexity | Accepted trade-off |

**Sources**:
- OpenAI API Documentation: https://platform.openai.com/docs
- Ollama: https://ollama.ai/
- LangChain for abstraction: https://langchain.com/

---

### 5. Speech Recognition

**Decision**: OpenAI Whisper (API and local models)

**Rationale**:
- State-of-the-art accuracy for speech recognition
- Open-source models available for local deployment
- API option for convenience
- Well-documented Python integration

**Alternatives Considered**:
| Option | Pros | Cons | Rejected Because |
|--------|------|------|------------------|
| Google Speech-to-Text | High accuracy | API cost, no local option | Vendor lock-in |
| Mozilla DeepSpeech | Open-source | Deprecated, lower accuracy | No longer maintained |
| Azure Speech | Enterprise features | Cost, complexity | Overkill for educational use |
| Whisper | Open + API, accurate | Requires decent hardware locally | Best balance |

**Sources**:
- Radford, A., et al. (2022). Robust Speech Recognition via Large-Scale Weak Supervision. OpenAI.
- Whisper GitHub: https://github.com/openai/whisper

---

### 6. Navigation Stack

**Decision**: Nav2 (ROS 2 Navigation)

**Rationale**:
- Standard ROS 2 navigation stack
- Well-documented with extensive tutorials
- Supports multiple planners and controllers
- Active development and community

**Alternatives Considered**:
| Option | Pros | Cons | Rejected Because |
|--------|------|------|------------------|
| Custom navigation | Full control | Massive effort, error-prone | Not practical for book scope |
| move_base (ROS 1) | Mature | ROS 1 only, deprecated | Not ROS 2 compatible |
| Nav2 | Standard, maintained | Learning curve | Selected approach |

**Sources**:
- Nav2 Documentation: https://navigation.ros.org/
- Macenski, S., et al. (2020). The Marathon 2: A Navigation System. IEEE IROS.

---

### 7. Perception Pipeline

**Decision**: Isaac ROS for GPU-accelerated perception, fallback to CPU alternatives

**Rationale**:
- Isaac ROS provides hardware-accelerated VSLAM, stereo, segmentation
- Integrates with Isaac Sim for seamless simulation
- CPU fallbacks (ORB-SLAM3, OpenCV) for readers without RTX GPUs

**Alternatives Considered**:
| Option | Pros | Cons | Rejected Because |
|--------|------|------|------------------|
| OpenCV only | Universal, simple | Limited SLAM capabilities | Insufficient for humanoid |
| ORB-SLAM3 | Open-source, accurate | CPU-bound, complex setup | Not GPU-accelerated |
| Isaac ROS | GPU-accelerated, integrated | Requires NVIDIA GPU | Selected with fallbacks |

**Sources**:
- Isaac ROS: https://nvidia-isaac-ros.github.io/
- Mur-Artal, R., & Tardós, J. D. (2017). ORB-SLAM2. IEEE T-RO.

---

### 8. Docusaurus Configuration

**Decision**: Docusaurus 3.x with docs-only mode, GitHub Pages deployment

**Rationale**:
- Modern, React-based static site generator
- Excellent Markdown support with MDX
- Built-in versioning for future updates
- Simple GitHub Pages integration

**Alternatives Considered**:
| Option | Pros | Cons | Rejected Because |
|--------|------|------|------------------|
| GitBook | Simple, beautiful | Vendor lock-in, cost | Limited customization |
| MkDocs | Python-based, simple | Less feature-rich | Limited for complex books |
| Sphinx | Python standard | Complex theming | Not as modern |
| Docusaurus | Modern, flexible | Requires Node.js | Selected approach |

**Sources**:
- Docusaurus Documentation: https://docusaurus.io/docs

---

## Citation Research

### Core Textbooks

1. **Spong, M. W., Hutchinson, S., & Vidyasagar, M.** (2020). *Robot Modeling and Control* (2nd ed.). Wiley.
   - Primary reference for kinematics, dynamics, control

2. **Siciliano, B., et al.** (2010). *Robotics: Modelling, Planning and Control*. Springer.
   - Comprehensive robotics reference

3. **Thrun, S., Burgard, W., & Fox, D.** (2005). *Probabilistic Robotics*. MIT Press.
   - SLAM, localization, navigation foundations

4. **Craig, J. J.** (2005). *Introduction to Robotics: Mechanics and Control* (3rd ed.). Pearson.
   - Kinematics, Denavit-Hartenberg convention

### Key Papers

5. **Quigley, M., et al.** (2009). ROS: an open-source Robot Operating System. *ICRA Workshop*.
   - ROS foundational paper

6. **Macenski, S., et al.** (2023). From the desks of ROS maintainers: A survey of modern & capable mobile robotics. *arXiv*.
   - Nav2 and modern ROS 2 robotics

7. **Radford, A., et al.** (2022). Robust Speech Recognition via Large-Scale Weak Supervision. *OpenAI Technical Report*.
   - Whisper speech recognition

8. **Brohan, A., et al.** (2022). RT-1: Robotics Transformer for Real-World Control at Scale. *arXiv*.
   - Vision-Language-Action foundations

9. **Driess, D., et al.** (2023). PaLM-E: An Embodied Multimodal Language Model. *ICML*.
   - Embodied AI with language models

10. **Kajita, S., et al.** (2001). The 3D Linear Inverted Pendulum Mode: A simple modeling for a biped walking pattern generation. *IEEE IROS*.
    - Humanoid locomotion fundamentals

### Official Documentation (to cite as sources)

11. ROS 2 Documentation (Open Robotics)
12. Gazebo Sim Documentation (Open Robotics)
13. NVIDIA Isaac Sim User Guide (NVIDIA)
14. Nav2 Documentation (Open Robotics)
15. OpenAI API Documentation (OpenAI)

---

## Platform Requirements Research

### Minimum Hardware Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| CPU | 4 cores, 2.5 GHz | 8+ cores, 3.0+ GHz |
| RAM | 16 GB | 32 GB |
| GPU | Integrated (Gazebo only) | RTX 3060+ (Isaac Sim) |
| Storage | 50 GB free | 100 GB SSD |
| OS | Ubuntu 22.04 LTS | Ubuntu 22.04 LTS |

### Cloud Alternatives

| Provider | Instance | Cost (approx) | Use Case |
|----------|----------|---------------|----------|
| AWS | g4dn.xlarge | $0.50/hr | Isaac Sim, VSLAM |
| Azure | NC6 | $0.90/hr | Isaac Sim, VSLAM |
| NVIDIA NGC | Various | Free tier available | Isaac containers |

---

## Research Summary

All technical decisions have been made with:
- Educational accessibility as primary concern
- Industry-standard tools preferred
- Open-source options prioritized where possible
- Fallback options for resource-constrained readers
- Academic rigor through authoritative citations

**Phase 0 Status**: ✅ COMPLETE — All unknowns resolved, ready for Phase 1.
