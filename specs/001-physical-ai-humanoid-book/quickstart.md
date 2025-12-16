# Quickstart: Physical AI & Humanoid Robotics Book

**Feature**: `001-physical-ai-humanoid-book`
**Date**: 2025-12-16
**Audience**: Readers/Students

## Welcome

This quickstart guide helps you set up your development environment and navigate the Physical AI & Humanoid Robotics book effectively.

## Prerequisites

Before starting, ensure you have:

### Required Knowledge
- [ ] Intermediate Python programming (functions, classes, async)
- [ ] Basic Linux command line proficiency
- [ ] Understanding of coordinate systems and transforms
- [ ] Familiarity with version control (Git)

### Hardware Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| CPU | 4 cores, 2.5 GHz | 8+ cores, 3.0+ GHz |
| RAM | 16 GB | 32 GB |
| GPU | Integrated | NVIDIA RTX 3060+ |
| Storage | 50 GB free | 100 GB SSD |
| OS | Ubuntu 22.04 LTS | Ubuntu 22.04 LTS |

> **Note**: Modules 1-2 work without a dedicated GPU. Module 3 (NVIDIA Isaac) requires an RTX GPU or cloud access.

## Environment Setup

### Step 1: Install Ubuntu 22.04

Options:
- **Native installation** (recommended for best performance)
- **WSL2 on Windows 11** (works for Modules 1-2)
- **Virtual Machine** (VMware/VirtualBox with 3D acceleration)

### Step 2: Install ROS 2 Humble

```bash
# Set locale
sudo apt update && sudo apt install locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8

# Setup sources
sudo apt install software-properties-common
sudo add-apt-repository universe
sudo apt update && sudo apt install curl -y
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

# Install ROS 2
sudo apt update
sudo apt install ros-humble-desktop ros-humble-ros-base ros-dev-tools

# Source ROS 2
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

**Verify installation:**
```bash
ros2 --version
# Expected: ros2 0.X.X
```

### Step 3: Create ROS 2 Workspace

```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws
colcon build
echo "source ~/ros2_ws/install/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

### Step 4: Install Gazebo (Module 2)

```bash
# Install Gazebo Harmonic
sudo apt install gazebo
sudo apt install ros-humble-ros-gz

# Verify
gz sim --version
```

### Step 5: Install NVIDIA Isaac (Module 3, Optional)

**Requirements**: NVIDIA RTX GPU, Driver 525+

1. Install NVIDIA Container Toolkit:
```bash
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
sudo apt update
sudo apt install -y nvidia-container-toolkit
```

2. Pull Isaac Sim container:
```bash
docker pull nvcr.io/nvidia/isaac-sim:2023.1.1
```

Or install via Omniverse Launcher from [NVIDIA Developer](https://developer.nvidia.com/isaac-sim).

### Step 6: Install Python Dependencies

```bash
pip install --upgrade pip
pip install \
    openai \
    anthropic \
    openai-whisper \
    torch \
    transformers \
    numpy \
    scipy \
    matplotlib
```

## Book Navigation

### Reading Path

```
Start Here
    │
    ▼
┌─────────────────────────────────────┐
│ Introduction to Physical AI          │
└─────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────┐
│ Module 1: ROS 2 (Required)          │  ← Everyone starts here
│ - Architecture                       │
│ - First Package                      │
│ - URDF for Humanoids                │
│ - AI Integration                     │
└─────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────┐
│ Module 2: Digital Twin              │  ← Requires Module 1
│ - Gazebo Fundamentals               │
│ - Sensor Simulation                 │
│ - Unity Integration                 │
└─────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────┐
│ Module 3: NVIDIA Isaac              │  ← Requires RTX GPU
│ - Isaac Sim                         │     or cloud access
│ - Perception (VSLAM)                │
│ - Navigation (Nav2)                 │
│ - Sim2Real                          │
└─────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────┐
│ Module 4: Vision-Language-Action    │  ← Requires LLM API
│ - Whisper Speech Recognition        │
│ - LLM Cognitive Planning            │
│ - Action Execution                  │
│ - Vision Grounding                  │
└─────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────┐
│ Capstone: Autonomous Humanoid       │  ← Integrates all modules
│ - Full System Integration           │
│ - Demo: Voice-to-Action             │
└─────────────────────────────────────┘
```

### Alternative Paths

**Path A: No GPU Available**
- Complete Modules 1-2 locally
- Use cloud GPU (AWS g4dn.xlarge) for Module 3
- Continue with Module 4 and Capstone

**Path B: Focus on VLA Only**
- Complete Module 1 (required foundation)
- Skim Module 2-3 concepts
- Deep dive into Module 4

**Path C: Academic Course (13 weeks)**
- Weeks 1-3: Module 1
- Weeks 4-6: Module 2
- Weeks 7-9: Module 3
- Weeks 10-12: Module 4
- Week 13: Capstone

## Verification Checklist

Before starting each module, verify your setup:

### Module 1 Ready
```bash
# These should all succeed
ros2 --version
ros2 run demo_nodes_cpp talker &
ros2 run demo_nodes_cpp listener
# You should see messages being exchanged
```

### Module 2 Ready
```bash
gz sim --version
ros2 launch ros_gz_sim gz_sim.launch.py
# Gazebo should open
```

### Module 3 Ready
```bash
nvidia-smi  # Should show your GPU
# Isaac Sim should launch via Omniverse or Docker
```

### Module 4 Ready
```python
# Test Whisper
import whisper
model = whisper.load_model("base")
print("Whisper ready!")

# Test LLM API (replace with your API)
import openai
# or: import anthropic
print("LLM API configured!")
```

## Getting Help

### Common Issues

| Problem | Solution |
|---------|----------|
| `ros2: command not found` | Source ROS 2: `source /opt/ros/humble/setup.bash` |
| Gazebo won't start | Check `DISPLAY` environment variable |
| Isaac Sim crashes | Verify GPU driver version (≥525) |
| Whisper out of memory | Use smaller model: `whisper.load_model("tiny")` |
| LLM API rate limit | Implement caching or use local model |

### Resources

- ROS 2 Documentation: https://docs.ros.org/en/humble/
- Gazebo Tutorials: https://gazebosim.org/docs
- NVIDIA Isaac: https://developer.nvidia.com/isaac-sim
- OpenAI Whisper: https://github.com/openai/whisper

## Next Steps

1. **Read the Introduction** to understand Physical AI concepts
2. **Complete Module 1** to establish your ROS 2 foundation
3. **Build the humanoid URDF** as your first hands-on project
4. **Progress through modules** following the reading path

Welcome to the world of Physical AI and Humanoid Robotics!
