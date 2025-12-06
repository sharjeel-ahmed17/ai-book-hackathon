---
sidebar_position: 1
---

# Physical AI Edge Kit Setup

This guide will help you set up the Physical AI Edge Kit hardware for the Physical AI Humanoid Robotics course.

## Prerequisites

- Physical AI Edge Kit hardware
- Power supply for the hardware
- Network connection (Ethernet or Wi-Fi)
- Computer for initial setup and development
- SSH client (e.g., PuTTY on Windows, or built-in ssh on macOS/Linux)

## Installation Steps

### 1. Unpack and Inspect Hardware

1. Carefully unpack the Physical AI Edge Kit
2. Verify all components are present:
   - Edge computing device (e.g., NVIDIA Jetson)
   - Robot platform or robotic components
   - Power cables and adapters
   - Network cables (if applicable)

### 2. Physical Setup

1. Place the Edge Kit in a well-ventilated area
2. Connect the power supply to the device
3. Connect network cables if using Ethernet
4. Power on the device and wait for boot sequence to complete

### 3. Network Configuration

1. Connect to the same network as your development computer
2. Find the device IP address:
   - Check your router's connected devices list
   - Or connect a monitor and keyboard to the device to check network settings
   - Or use network scanning tools like `nmap`

### 4. Initial Connection

Connect to the device via SSH:

```bash
ssh username@device-ip-address
# Default credentials are typically provided with your kit
```

### 5. Install ROS 2

The Edge Kit may come with ROS 2 pre-installed. If not, install ROS 2 Humble Hawksbill:

```bash
# Update package lists
sudo apt update

# Install ROS 2 Humble
sudo apt install software-properties-common
sudo add-apt-repository universe
sudo apt update
sudo apt install ros-humble-desktop
```

### 6. Install Additional Dependencies

```bash
# Install Python packages
pip3 install numpy scipy matplotlib

# Install robot-specific packages
sudo apt install ros-humble-ros2-control ros-humble-ros2-controllers
```

### 7. Clone Course Repository

```bash
git clone https://github.com/sharjeel-ahmed17/ai-book-hackathon.git
cd ai-book-hackathon
```

### 8. Configure Robot Interface

Configure the robot-specific interfaces and drivers:

```bash
# Source ROS 2 environment
source /opt/ros/humble/setup.bash

# Build robot-specific packages (if provided with the kit)
colcon build
source install/setup.bash
```

## Validation Steps

1. Verify ROS 2 installation:
   ```bash
   ros2 --version
   ```

2. Check robot connectivity:
   ```bash
   # List available ROS 2 nodes
   ros2 node list
   ```

3. Test basic robot functionality (commands may vary based on your specific robot):
   ```bash
   # Publish test commands to robot
   ros2 topic pub /cmd_vel geometry_msgs/Twist "{linear: {x: 0.1}, angular: {z: 0.1}}"
   ```

## Troubleshooting

### Common Issues

- **Cannot connect via SSH**: Verify IP address and network connectivity
- **ROS 2 not found**: Ensure you've sourced the ROS 2 setup script
- **Robot not responding**: Check hardware connections and power status

## Next Steps

Once your Physical AI Edge Kit is set up, proceed to the [Foundations section](../../textbook/foundations/intro.md) of the textbook.