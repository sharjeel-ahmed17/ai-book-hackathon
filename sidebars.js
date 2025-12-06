/**
 * Creating an sidebar entry for the textbook structure following the 13-week curriculum:
 * - Weeks 1-2: Foundations of Physical AI
 * - Weeks 3-5: ROS 2
 * - Weeks 6-7: Digital Twin workflows
 * - Weeks 8-10: NVIDIA Isaac
 * - Weeks 11-13: VLA models and humanoid robotics
 * - Capstone: Build an autonomous humanoid pipeline
 */

module.exports = {
  textbookSidebar: [
    'textbook/intro',
    {
      type: 'category',
      label: 'Weeks 1-2: Foundations of Physical AI',
      items: [
        'textbook/foundations/intro',
      ],
    },
    {
      type: 'category',
      label: 'Weeks 3-5: ROS 2',
      items: [
        'textbook/ros2/intro',
      ],
    },
    {
      type: 'category',
      label: 'Weeks 6-7: Digital Twin Workflows',
      items: [
        'textbook/digital-twin/intro',
      ],
    },
    {
      type: 'category',
      label: 'Weeks 8-10: NVIDIA Isaac',
      items: [
        'textbook/nvidia-isaac/intro',
      ],
    },
    {
      type: 'category',
      label: 'Weeks 11-13: VLA Models and Humanoid Robotics',
      items: [
        'textbook/vla-humanoid/intro',
      ],
    },
    {
      type: 'category',
      label: 'Capstone: Autonomous Humanoid Pipeline',
      items: [
        'textbook/capstone/intro',
      ],
    },
    {
      type: 'category',
      label: 'Platform Setup Guides',
      items: [
        'setup-guides/intro',
        {
          type: 'category',
          label: 'Digital Twin Workstation',
          items: ['setup-guides/digital-twin-workstation/setup'],
        },
        {
          type: 'category',
          label: 'Physical AI Edge Kit',
          items: ['setup-guides/physical-ai-edge-kit/setup'],
        },
        {
          type: 'category',
          label: 'Cloud-Native Environment',
          items: ['setup-guides/cloud-native/setup'],
        },
      ],
    },
  ],
};