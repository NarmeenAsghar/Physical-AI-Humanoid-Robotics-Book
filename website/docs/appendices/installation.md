---
sidebar_position: 1
title: "Installation Guide"
description: Complete setup instructions for ROS 2, Gazebo, and NVIDIA Isaac Sim
---

# Installation Guide

This guide provides step-by-step instructions for setting up the development environment required for Physical AI and humanoid robotics development. Follow the sections relevant to your current module.

---

## System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **OS** | Ubuntu 22.04 LTS | Ubuntu 22.04 LTS |
| **CPU** | Intel i7 / AMD Ryzen 7 | Intel i9 / AMD Ryzen 9 |
| **RAM** | 16 GB | 32-64 GB |
| **GPU** | GTX 1070 (Gazebo only) | RTX 3080+ (Isaac Sim) |
| **Storage** | 100 GB free | 250+ GB SSD |

> **Note**: Isaac Sim requires an NVIDIA RTX GPU. Modules 1-2 can be completed with any modern GPU.

---

## ROS 2 Humble Installation (Module 1)

ROS 2 Humble Hawksbill is the recommended LTS distribution for this curriculum.

### Set Locale

```bash
locale  # check for UTF-8

sudo apt update && sudo apt install locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8
```

### Setup Sources

```bash
# Enable Ubuntu Universe repository
sudo apt install software-properties-common
sudo add-apt-repository universe

# Add ROS 2 GPG key
sudo apt update && sudo apt install curl -y
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg

# Add repository to sources list
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
```

### Install ROS 2 Packages

```bash
sudo apt update
sudo apt upgrade

# Desktop install (recommended) - includes RViz, demos, tutorials
sudo apt install ros-humble-desktop

# Development tools
sudo apt install ros-dev-tools
```

### Environment Setup

```bash
# Add to ~/.bashrc
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

### Verify Installation

```bash
# Terminal 1: Run talker
ros2 run demo_nodes_cpp talker

# Terminal 2: Run listener
ros2 run demo_nodes_cpp listener
```

You should see the talker publishing messages and the listener receiving them.

### Additional ROS 2 Packages

```bash
# Packages used in this curriculum
sudo apt install ros-humble-joint-state-publisher-gui
sudo apt install ros-humble-xacro
sudo apt install ros-humble-robot-state-publisher
sudo apt install ros-humble-tf2-tools
```

---

## Gazebo Harmonic Installation (Module 2)

Gazebo (formerly Ignition Gazebo) provides physics simulation for digital twins.

### Install Gazebo Harmonic

```bash
# Install dependencies
sudo apt-get update
sudo apt-get install lsb-release wget gnupg

# Add Gazebo repository
sudo wget https://packages.osrfoundation.org/gazebo.gpg -O /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] http://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/gazebo-stable.list > /dev/null

# Install Gazebo Harmonic
sudo apt-get update
sudo apt-get install gz-harmonic
```

### Install ROS 2-Gazebo Bridge

```bash
# Install ros_gz packages for ROS 2 Humble
sudo apt install ros-humble-ros-gz
```

### Verify Installation

```bash
# Launch Gazebo with a sample world
gz sim shapes.sdf
```

You should see the Gazebo GUI with geometric shapes.

### Test ROS 2 Bridge

```bash
# Terminal 1: Launch Gazebo
gz sim -r shapes.sdf

# Terminal 2: List Gazebo topics
gz topic -l

# Terminal 3: Bridge a topic to ROS 2
ros2 run ros_gz_bridge parameter_bridge /clock@rosgraph_msgs/msg/Clock@gz.msgs.Clock
```

---

## NVIDIA Isaac Sim Installation (Module 3)

Isaac Sim provides photorealistic simulation with GPU acceleration.

### Prerequisites

1. **NVIDIA Driver**: Version 525.60.11 or later
2. **NVIDIA GPU**: RTX 2070 or better (RTX 3080+ recommended)
3. **CUDA**: 12.0 or later (installed with driver)

### Check NVIDIA Driver

```bash
nvidia-smi
# Should show driver version 525+ and GPU information
```

### Install Omniverse Launcher

1. Download the Omniverse Launcher from [NVIDIA Omniverse](https://www.nvidia.com/en-us/omniverse/download/)
2. Make executable and run:

```bash
chmod +x omniverse-launcher-linux.AppImage
./omniverse-launcher-linux.AppImage
```

3. Sign in with NVIDIA account (free)

### Install Isaac Sim

1. In Omniverse Launcher, go to **Exchange** tab
2. Search for "Isaac Sim"
3. Click **Install** (requires ~30 GB)
4. Wait for installation to complete

### Launch Isaac Sim

```bash
# Via Omniverse Launcher: Click "Launch" on Isaac Sim
# Or via command line:
~/.local/share/ov/pkg/isaac_sim-*/isaac-sim.sh
```

### Install Isaac ROS

```bash
# Create Isaac ROS workspace
mkdir -p ~/isaac_ros_ws/src
cd ~/isaac_ros_ws/src

# Clone Isaac ROS packages
git clone https://github.com/NVIDIA-ISAAC-ROS/isaac_ros_common.git
git clone https://github.com/NVIDIA-ISAAC-ROS/isaac_ros_visual_slam.git

# Build workspace
cd ~/isaac_ros_ws
colcon build --symlink-install
source install/setup.bash
```

### Verify Isaac Sim ROS 2 Bridge

1. Launch Isaac Sim
2. Open **Isaac Examples > ROS2 > Navigation**
3. Click **Play**
4. In terminal, verify ROS 2 topics:

```bash
ros2 topic list
# Should show camera, lidar, and other sensor topics
```

---

## Python Environment Setup

### Create Virtual Environment (Optional)

```bash
# Install virtualenv
sudo apt install python3-venv

# Create environment for ML packages
python3 -m venv ~/physical_ai_env
source ~/physical_ai_env/bin/activate

# Install common packages
pip install numpy scipy matplotlib
pip install torch torchvision  # For VLA module
pip install transformers       # For LLM integration
pip install openai-whisper     # For speech recognition
```

### ROS 2 Python Packages

```bash
# Ensure colcon and rosdep are available
pip install colcon-common-extensions
sudo apt install python3-rosdep
sudo rosdep init
rosdep update
```

---

## Verification Checklist

Use this checklist to verify your installation is complete:

### ROS 2 Humble
- [ ] `ros2 --version` shows "humble"
- [ ] `ros2 topic list` returns without error
- [ ] RViz2 launches: `rviz2`
- [ ] Demo nodes communicate (talker/listener)

### Gazebo Harmonic
- [ ] `gz sim --version` shows version info
- [ ] Gazebo GUI launches with shapes world
- [ ] ROS 2 bridge publishes clock topic

### Isaac Sim (Optional for Module 3)
- [ ] `nvidia-smi` shows driver 525+
- [ ] Omniverse Launcher installed
- [ ] Isaac Sim launches and renders
- [ ] ROS 2 bridge publishes sensor data

---

## Troubleshooting

### ROS 2 Command Not Found

```bash
# Ensure setup is sourced
source /opt/ros/humble/setup.bash

# Add to bashrc if not present
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
```

### Gazebo Crashes on Launch

```bash
# Check OpenGL support
glxinfo | grep "OpenGL version"

# Try software rendering
export LIBGL_ALWAYS_SOFTWARE=1
gz sim shapes.sdf
```

### Isaac Sim Performance Issues

1. Reduce viewport resolution in Preferences
2. Disable ray tracing: **Render Settings > Path Tracing > Off**
3. Close other GPU-intensive applications
4. Ensure sufficient VRAM (check with `nvidia-smi`)

### ROS 2-Gazebo Bridge Not Working

```bash
# Verify both systems are running
ros2 topic list
gz topic -l

# Check bridge is running
ros2 node list | grep bridge
```

---

## References

- [ROS 2 Humble Installation](https://docs.ros.org/en/humble/Installation.html)
- [Gazebo Harmonic Documentation](https://gazebosim.org/docs/harmonic)
- [NVIDIA Isaac Sim Documentation](https://docs.omniverse.nvidia.com/isaacsim/latest/)
- [Isaac ROS Getting Started](https://nvidia-isaac-ros.github.io/getting_started/)
