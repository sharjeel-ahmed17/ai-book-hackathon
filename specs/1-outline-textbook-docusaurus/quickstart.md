# Quickstart Guide: Physical AI Humanoid Robotics Textbook

## Overview
This guide will help you get started with the Physical AI Humanoid Robotics textbook project. The textbook supports a 13-week training program for industry engineers with Python knowledge, covering Physical AI, ROS 2, Digital Twin workflows, NVIDIA Isaac, and VLA models with humanoid robotics.

## Prerequisites
- Git installed on your system
- Node.js (version 18 or higher)
- npm or yarn package manager
- Python knowledge (required for the target audience)

## Setting up the Development Environment

### 1. Clone the Repository
```bash
git clone https://github.com/your-org/physical-ai-humanoid-textbook.git
cd physical-ai-humanoid-textbook
```

### 2. Install Docusaurus Dependencies
```bash
npm install
# or
yarn install
```

### 3. Start the Development Server
```bash
npm run start
# or
yarn start
```

This will start the Docusaurus development server and open the textbook in your browser at http://localhost:3000.

## Textbook Structure
The textbook is organized according to the 13-week curriculum:

1. **Weeks 1-2**: Foundations of Physical AI
2. **Weeks 3-5**: ROS 2
3. **Weeks 6-7**: Digital Twin workflows
4. **Weeks 8-10**: NVIDIA Isaac
5. **Weeks 11-13**: VLA models and humanoid robotics
6. **Capstone**: Build an autonomous humanoid pipeline

## Platform Setup Options
Learners can choose from three platform setups:
- Digital Twin workstation
- Physical AI Edge Kit
- Cloud-native environment

Each option has specific setup guides in the textbook.

## Contributing Content
To add or modify content:

1. Navigate to the appropriate section in the `docs/` directory
2. Edit the Markdown files following Docusaurus conventions
3. Add code examples with proper syntax highlighting
4. Include diagrams where helpful for understanding
5. Test your changes locally before submitting

## Building for Production
To build the static site for deployment:

```bash
npm run build
# or
yarn build
```

The built site will be in the `build/` directory and can be deployed to GitHub Pages.

## Deployment
The textbook is deployed via GitHub Pages. After merging changes to the main branch, the site will automatically update.

## Getting Help
- Check the troubleshooting sections in each platform setup guide
- Review the FAQ section in the textbook
- Submit issues for content corrections or suggestions