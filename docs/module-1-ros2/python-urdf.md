---
sidebar_position: 2
title: "ROS 2 Python, URDF, and Humanoid Models"
description: Building ROS 2 packages with Python and creating humanoid robot descriptions
---

# ROS 2 Python, URDF, and Humanoid Models

This section transitions from concepts to practice. You will create ROS 2 packages using Python, configure systems with launch files, and build robot descriptions using URDF—the foundation for simulation in later modules.

## Building Your First ROS 2 Package

ROS 2 organizes code into **packages**—self-contained units with source code, configuration, and dependencies. A well-structured workspace enables reproducible builds across machines.

### Workspace Setup

Create a workspace following ROS 2 conventions:

```bash
# Create workspace structure
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws

# Create your first package
ros2 pkg create --build-type ament_python humanoid_sensors \
    --dependencies rclpy sensor_msgs geometry_msgs

# Build the workspace
colcon build --symlink-install
source install/setup.bash
```

The `--symlink-install` flag enables rapid iteration by linking source files rather than copying them—changes take effect without rebuilding.

### IMU Publisher Node

Inertial Measurement Units (IMUs) provide orientation and acceleration data critical for humanoid balance. The following node publishes simulated IMU readings:

```python
#!/usr/bin/env python3
"""imu_publisher.py - Publishes simulated IMU data for humanoid robot."""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu
from builtin_interfaces.msg import Time
import math

class IMUPublisher(Node):
    def __init__(self):
        super().__init__('imu_publisher')

        # Declare and get parameters
        self.declare_parameter('publish_rate', 100.0)
        self.declare_parameter('frame_id', 'imu_link')

        rate = self.get_parameter('publish_rate').value
        self.frame_id = self.get_parameter('frame_id').value

        # Create publisher with QoS for sensor data
        self.publisher = self.create_publisher(Imu, '/imu/data', 10)

        # Timer for periodic publishing
        self.timer = self.create_timer(1.0 / rate, self.publish_imu)
        self.t = 0.0

        self.get_logger().info(f'IMU Publisher started at {rate} Hz')

    def publish_imu(self):
        msg = Imu()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = self.frame_id

        # Simulated orientation (quaternion)
        msg.orientation.w = math.cos(self.t * 0.1)
        msg.orientation.x = 0.0
        msg.orientation.y = 0.0
        msg.orientation.z = math.sin(self.t * 0.1)

        # Simulated angular velocity
        msg.angular_velocity.x = 0.01 * math.sin(self.t)
        msg.angular_velocity.y = 0.01 * math.cos(self.t)
        msg.angular_velocity.z = 0.0

        # Simulated linear acceleration (gravity + movement)
        msg.linear_acceleration.x = 0.1 * math.sin(self.t * 0.5)
        msg.linear_acceleration.y = 0.0
        msg.linear_acceleration.z = 9.81  # Gravity

        self.publisher.publish(msg)
        self.t += 0.01

def main(args=None):
    rclpy.init(args=args)
    node = IMUPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

**Expected output** when running `ros2 topic echo /imu/data`:

```
header:
  stamp:
    sec: 1702747200
    nanosec: 123456789
  frame_id: imu_link
orientation:
  x: 0.0
  y: 0.0
  z: 0.099833
  w: 0.995004
angular_velocity:
  x: 0.008414
  y: 0.005403
  z: 0.0
linear_acceleration:
  x: 0.047942
  y: 0.0
  z: 9.81
```

### Sensor Data Subscriber

A subscriber node processes incoming sensor data—essential for logging, monitoring, or feeding AI systems:

```python
#!/usr/bin/env python3
"""data_subscriber.py - Subscribes to sensor data and logs readings."""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu, LaserScan, Image

class SensorSubscriber(Node):
    def __init__(self):
        super().__init__('sensor_subscriber')

        # Subscribe to IMU
        self.imu_sub = self.create_subscription(
            Imu, '/imu/data', self.imu_callback, 10)

        # Subscribe to LiDAR (when available)
        self.lidar_sub = self.create_subscription(
            LaserScan, '/scan', self.lidar_callback, 10)

        self.get_logger().info('Sensor Subscriber initialized')

    def imu_callback(self, msg):
        # Extract orientation as Euler angles for logging
        q = msg.orientation
        self.get_logger().info(
            f'IMU: orientation_w={q.w:.3f}, accel_z={msg.linear_acceleration.z:.2f}')

    def lidar_callback(self, msg):
        # Log range statistics
        valid_ranges = [r for r in msg.ranges if msg.range_min < r < msg.range_max]
        if valid_ranges:
            self.get_logger().info(
                f'LiDAR: {len(valid_ranges)} valid readings, '
                f'min={min(valid_ranges):.2f}m, max={max(valid_ranges):.2f}m')

def main(args=None):
    rclpy.init(args=args)
    node = SensorSubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

---

## Launch Files and Parameters

Launch files orchestrate multiple nodes, set parameters, and configure namespaces. ROS 2 uses Python for launch files, providing programmatic flexibility.

### Multi-Node Launch File

```python
#!/usr/bin/env python3
"""humanoid_bringup.launch.py - Launch humanoid sensor nodes."""

from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    # Declare launch arguments
    rate_arg = DeclareLaunchArgument(
        'imu_rate',
        default_value='100.0',
        description='IMU publish rate in Hz'
    )

    # IMU Publisher node
    imu_node = Node(
        package='humanoid_sensors',
        executable='imu_publisher',
        name='imu_publisher',
        parameters=[{
            'publish_rate': LaunchConfiguration('imu_rate'),
            'frame_id': 'torso_imu_link'
        }],
        output='screen'
    )

    # Sensor Subscriber node
    subscriber_node = Node(
        package='humanoid_sensors',
        executable='data_subscriber',
        name='sensor_monitor',
        output='screen'
    )

    return LaunchDescription([
        rate_arg,
        imu_node,
        subscriber_node
    ])
```

**Launch with custom parameters:**

```bash
ros2 launch humanoid_sensors humanoid_bringup.launch.py imu_rate:=50.0
```

### Parameter Configuration with YAML

For complex configurations, use YAML files:

```yaml
# config/humanoid_params.yaml
humanoid_sensors:
  imu_publisher:
    ros__parameters:
      publish_rate: 100.0
      frame_id: torso_imu_link
      noise_stddev: 0.01

  sensor_monitor:
    ros__parameters:
      log_level: info
      buffer_size: 100
```

Load in launch file:

```python
from ament_index_python.packages import get_package_share_directory
import os

config = os.path.join(
    get_package_share_directory('humanoid_sensors'),
    'config',
    'humanoid_params.yaml'
)

node = Node(
    package='humanoid_sensors',
    executable='imu_publisher',
    parameters=[config]
)
```

---

## URDF for Humanoid Robots

The **Unified Robot Description Format (URDF)** defines a robot's physical structure—links (rigid bodies), joints (connections), and properties for visualization and physics simulation.

### URDF Structure

A URDF file consists of:

- **Links**: Rigid bodies with visual geometry, collision geometry, and inertial properties
- **Joints**: Connections between links defining motion constraints
- **Materials**: Visual appearance (colors, textures)

### Humanoid URDF Example

The following URDF defines a humanoid torso, head, and right arm:

```xml
<?xml version="1.0"?>
<robot name="humanoid_base">

  <!-- Base link (torso) -->
  <link name="torso_link">
    <visual>
      <geometry>
        <box size="0.4 0.3 0.6"/>
      </geometry>
      <material name="gray">
        <color rgba="0.5 0.5 0.5 1.0"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <box size="0.4 0.3 0.6"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="15.0"/>
      <inertia ixx="0.5" ixy="0" ixz="0" iyy="0.4" iyz="0" izz="0.3"/>
    </inertial>
  </link>

  <!-- Head -->
  <link name="head_link">
    <visual>
      <geometry>
        <sphere radius="0.12"/>
      </geometry>
      <material name="skin">
        <color rgba="0.9 0.75 0.65 1.0"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <sphere radius="0.12"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="4.0"/>
      <inertia ixx="0.02" ixy="0" ixz="0" iyy="0.02" iyz="0" izz="0.02"/>
    </inertial>
  </link>

  <!-- Neck joint (pan-tilt) -->
  <joint name="neck_pan" type="revolute">
    <parent link="torso_link"/>
    <child link="head_link"/>
    <origin xyz="0 0 0.4" rpy="0 0 0"/>
    <axis xyz="0 0 1"/>
    <limit lower="-1.57" upper="1.57" effort="10" velocity="1.0"/>
  </joint>

  <!-- Right shoulder link -->
  <link name="right_upper_arm">
    <visual>
      <origin xyz="0 0 -0.15"/>
      <geometry>
        <cylinder radius="0.05" length="0.3"/>
      </geometry>
      <material name="gray"/>
    </visual>
    <collision>
      <origin xyz="0 0 -0.15"/>
      <geometry>
        <cylinder radius="0.05" length="0.3"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="2.0"/>
      <origin xyz="0 0 -0.15"/>
      <inertia ixx="0.02" ixy="0" ixz="0" iyy="0.02" iyz="0" izz="0.005"/>
    </inertial>
  </link>

  <!-- Right shoulder joint -->
  <joint name="right_shoulder_pitch" type="revolute">
    <parent link="torso_link"/>
    <child link="right_upper_arm"/>
    <origin xyz="-0.22 0 0.25" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="-3.14" upper="1.57" effort="50" velocity="2.0"/>
  </joint>

  <!-- IMU sensor link -->
  <link name="imu_link">
    <visual>
      <geometry>
        <box size="0.02 0.02 0.01"/>
      </geometry>
      <material name="blue">
        <color rgba="0 0 1 1"/>
      </material>
    </visual>
  </link>

  <joint name="imu_joint" type="fixed">
    <parent link="torso_link"/>
    <child link="imu_link"/>
    <origin xyz="0 0 0.2" rpy="0 0 0"/>
  </joint>

  <!-- Camera link -->
  <link name="camera_link">
    <visual>
      <geometry>
        <box size="0.03 0.08 0.02"/>
      </geometry>
      <material name="black">
        <color rgba="0.1 0.1 0.1 1"/>
      </material>
    </visual>
  </link>

  <joint name="camera_joint" type="fixed">
    <parent link="head_link"/>
    <child link="camera_link"/>
    <origin xyz="0.1 0 0" rpy="0 0 0"/>
  </joint>

</robot>
```

### Joint Types

| Type | Degrees of Freedom | Use Case |
|------|-------------------|----------|
| `revolute` | 1 (rotation with limits) | Elbows, knees, neck |
| `continuous` | 1 (unlimited rotation) | Wheels |
| `prismatic` | 1 (linear translation) | Linear actuators |
| `fixed` | 0 | Sensor mounts, rigid attachments |
| `floating` | 6 | Free-floating base |

### Validating URDF

Always validate before use:

```bash
# Install URDF tools
sudo apt install liburdfdom-tools

# Check URDF syntax
check_urdf humanoid_base.urdf

# Visualize in RViz2
ros2 launch urdf_tutorial display.launch.py model:=humanoid_base.urdf
```

**Expected validation output:**

```
robot name is: humanoid_base
---------- Successfully Parsed XML ---------------
root Link: torso_link has 3 child(ren)
    child(1):  head_link
    child(2):  right_upper_arm
    child(3):  imu_link
```

---

## Publishing Sensor Data

Humanoid robots integrate multiple sensor modalities. Here are patterns for common sensors:

### Camera Data Pipeline

```python
# In a camera node
from sensor_msgs.msg import Image, CameraInfo
from cv_bridge import CvBridge

self.image_pub = self.create_publisher(Image, '/camera/image_raw', 10)
self.info_pub = self.create_publisher(CameraInfo, '/camera/camera_info', 10)
self.bridge = CvBridge()

def publish_image(self, cv_image):
    msg = self.bridge.cv2_to_imgmsg(cv_image, encoding='bgr8')
    msg.header.stamp = self.get_clock().now().to_msg()
    msg.header.frame_id = 'camera_link'
    self.image_pub.publish(msg)
```

### LiDAR Data Pattern

```python
from sensor_msgs.msg import LaserScan
import math

def publish_scan(self):
    msg = LaserScan()
    msg.header.stamp = self.get_clock().now().to_msg()
    msg.header.frame_id = 'lidar_link'
    msg.angle_min = -math.pi
    msg.angle_max = math.pi
    msg.angle_increment = math.pi / 180  # 1 degree
    msg.range_min = 0.1
    msg.range_max = 10.0
    msg.ranges = [...]  # 360 range readings
    self.scan_pub.publish(msg)
```

---

## Exercises

1. **Package Creation**: Create a new ROS 2 package called `humanoid_control` that subscribes to `/imu/data` and publishes a `geometry_msgs/Twist` message to `/cmd_vel` when the robot tilts beyond 10 degrees.

2. **URDF Extension**: Extend the humanoid URDF to include a left arm mirroring the right arm. Add a `left_shoulder_pitch` joint and `left_upper_arm` link. Validate with `check_urdf`.

3. **Launch Configuration**: Create a launch file that starts your IMU publisher, control node, and RViz2 visualization simultaneously. Use a YAML parameter file to configure all nodes.

---

## Summary

This section covered practical ROS 2 development skills:

- **Package creation** with `ros2 pkg create` and `colcon build`
- **Python nodes** using rclpy for publishers and subscribers
- **Launch files** for multi-node orchestration with parameters
- **URDF** for defining humanoid robot structure with links, joints, and sensors
- **Sensor patterns** for IMU, camera, and LiDAR data

These foundations prepare you for Module 2, where you will bring this URDF to life in physics simulation with Gazebo.

---

## References

Thomas, D., Woodall, W., & Fernandez, E. (2014). Next-generation ROS: Building on DDS. In *ROSCon 2014*. Open Robotics.

Open Robotics. (2023). *Creating a ROS 2 package*. ROS 2 Documentation. https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Creating-Your-First-ROS2-Package.html

Open Robotics. (2023). *URDF tutorials*. ROS 2 Documentation. https://docs.ros.org/en/humble/Tutorials/Intermediate/URDF/URDF-Main.html

Quigley, M., Gerkey, B., & Smart, W. D. (2015). *Programming Robots with ROS: A Practical Introduction to the Robot Operating System*. O'Reilly Media.

Metta, G., Fitzpatrick, P., & Natale, L. (2006). YARP: Yet another robot platform. *International Journal of Advanced Robotic Systems*, 3(1), 43-48.
