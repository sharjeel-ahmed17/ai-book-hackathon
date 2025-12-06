---
sidebar_position: 1
---

# Cloud-Native Environment Setup

This guide will help you set up a cloud-based development environment for the Physical AI Humanoid Robotics course.

## Prerequisites

- Cloud provider account (AWS, Azure, or GCP)
- Sufficient compute resources (GPU-enabled instances recommended)
- SSH key pair for secure access
- Basic understanding of cloud computing concepts

## Installation Steps

### 1. Choose Cloud Provider and Instance Type

Select a cloud provider and appropriate instance type:

- **AWS**: Use EC2 instances like p3 or g4dn for GPU acceleration
- **Azure**: Use VMs like NCv3 or NDv2 series for GPU acceleration
- **GCP**: Use Compute Engine with GPUs attached

Recommended specifications:
- At least 8 vCPUs
- 32GB+ RAM
- NVIDIA T4 or better GPU (for Isaac Sim)
- 100GB+ SSD storage

### 2. Launch Cloud Instance

1. Create a new virtual machine instance with your chosen specifications
2. Configure security groups/firewall rules to allow:
   - SSH access (port 22)
   - HTTP access (port 80) if needed
   - HTTPS access (port 443)
3. Attach your SSH key for secure access
4. Launch the instance

### 3. Connect to Your Instance

Connect via SSH:

```bash
ssh -i your-private-key.pem ubuntu@your-instance-ip
# Adjust username based on your instance OS (ubuntu, centos, etc.)
```

### 4. Update System and Install Dependencies

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install essential tools
sudo apt install -y git curl wget build-essential cmake
sudo apt install -y python3 python3-pip python3-venv
```

### 5. Install Docker (Optional but Recommended)

```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
sudo usermod -aG docker $USER

# Log out and back in for group changes to take effect
```

### 6. Install ROS 2

Install ROS 2 Humble Hawksbill:

```bash
# Add ROS 2 repository
sudo apt update && sudo apt install -y software-properties-common
sudo add-apt-repository universe
sudo apt update

# Install ROS 2 packages
sudo apt install -y ros-humble-desktop
sudo apt install -y python3-rosdep python3-rosinstall python3-rosinstall-generator python3-wstool build-essential
```

### 7. Install NVIDIA Container Toolkit (for GPU acceleration)

If using GPU-enabled instances:

```bash
# Add NVIDIA package repositories
wget -O /tmp/nvidia-ml.deb http://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-ubuntu2004.pin
sudo mv /tmp/nvidia-ml.deb /etc/apt/preferences.d/cuda-repository-pin-600
sudo apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/7fa2af80.pub
sudo add-apt-repository "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/ /"

# Install NVIDIA Container Toolkit
sudo apt update
sudo apt install -y nvidia-container-toolkit
sudo systemctl restart docker
```

### 8. Clone Course Repository

```bash
git clone https://github.com/sharjeel-ahmed17/ai-book-hackathon.git
cd ai-book-hackathon
```

### 9. Install Docusaurus Dependencies

```bash
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs
npm install
```

## Validation Steps

1. Verify ROS 2 installation:
   ```bash
   source /opt/ros/humble/setup.bash
   ros2 --version
   ```

2. Check GPU availability (if using GPU instance):
   ```bash
   nvidia-smi
   ```

3. Test Docusaurus:
   ```bash
   npm start
   ```
   The textbook should be accessible at http://your-instance-public-ip:3000

## Troubleshooting

### Common Issues

- **Instance not accessible**: Check security group settings and ensure ports are open
- **GPU not detected**: Verify NVIDIA drivers are properly installed
- **Docker permission errors**: Log out and back in after adding user to docker group

## Cost Management

- Monitor your cloud usage to avoid unexpected charges
- Consider using spot instances for cost savings during development
- Shut down instances when not in use

## Next Steps

Once your Cloud-Native Environment is set up, proceed to the [Foundations section](../../textbook/foundations/intro.md) of the textbook.