---
sidebar_position: 1
---

# Digital Twin Workstation Setup

This guide will help you set up a local development environment with digital twin capabilities for the Physical AI Humanoid Robotics course.

## Prerequisites

- Windows 10/11, macOS, or Linux
- At least 16GB RAM (32GB recommended)
- NVIDIA GPU with CUDA support (optional but recommended)
- At least 100GB free disk space
- Git installed
- Python 3.8 or higher

## Installation Steps

### 1. Install Git and Python

Make sure Git and Python are installed on your system:

```bash
git --version
python3 --version
```

### 2. Install ROS 2 Humble Hawksbill

Follow the official ROS 2 installation guide for your operating system:
- [ROS 2 Humble Installation Guide](https://docs.ros.org/en/humble/Installation.html)

### 3. Install NVIDIA Isaac Sim

1. Download Isaac Sim from the [NVIDIA Developer website](https://developer.nvidia.com/isaac-sim)
2. Follow the installation instructions for your platform
3. Verify the installation by launching Isaac Sim

### 4. Install Additional Dependencies

```bash
# Create a Python virtual environment
python3 -m venv isaac-sim-env
source isaac-sim-env/bin/activate  # On Windows: isaac-sim-env\Scripts\activate

# Install Python dependencies
pip install numpy scipy matplotlib
```

### 5. Clone Course Repository

```bash
git clone https://github.com/sharjeel-ahmed17/ai-book-hackathon.git
cd ai-book-hackathon
```

### 6. Install Docusaurus Dependencies

```bash
npm install
```

## Validation Steps

1. Verify ROS 2 installation:
   ```bash
   source /opt/ros/humble/setup.bash  # Adjust path as needed
   ros2 --version
   ```

2. Verify Isaac Sim installation:
   - Launch Isaac Sim and ensure it starts without errors

3. Test Docusaurus:
   ```bash
   npm start
   ```
   The textbook should be accessible at http://localhost:3000

## Troubleshooting

### Common Issues

- **Isaac Sim won't start**: Ensure your GPU drivers are up to date and CUDA is properly installed
- **ROS 2 commands not found**: Make sure you sourced the ROS 2 setup script
- **Docusaurus fails to start**: Check that Node.js and npm are properly installed

## Next Steps

Once your Digital Twin Workstation is set up, proceed to the [Foundations section](../../textbook/foundations/intro.md) of the textbook.