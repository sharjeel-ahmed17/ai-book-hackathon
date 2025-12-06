import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';

export default [
  {
    path: '/ai-book-hackathon/__docusaurus/debug',
    component: ComponentCreator('/ai-book-hackathon/__docusaurus/debug', '54a'),
    exact: true
  },
  {
    path: '/ai-book-hackathon/__docusaurus/debug/config',
    component: ComponentCreator('/ai-book-hackathon/__docusaurus/debug/config', '2b7'),
    exact: true
  },
  {
    path: '/ai-book-hackathon/__docusaurus/debug/content',
    component: ComponentCreator('/ai-book-hackathon/__docusaurus/debug/content', '162'),
    exact: true
  },
  {
    path: '/ai-book-hackathon/__docusaurus/debug/globalData',
    component: ComponentCreator('/ai-book-hackathon/__docusaurus/debug/globalData', '714'),
    exact: true
  },
  {
    path: '/ai-book-hackathon/__docusaurus/debug/metadata',
    component: ComponentCreator('/ai-book-hackathon/__docusaurus/debug/metadata', 'ec9'),
    exact: true
  },
  {
    path: '/ai-book-hackathon/__docusaurus/debug/registry',
    component: ComponentCreator('/ai-book-hackathon/__docusaurus/debug/registry', '4fc'),
    exact: true
  },
  {
    path: '/ai-book-hackathon/__docusaurus/debug/routes',
    component: ComponentCreator('/ai-book-hackathon/__docusaurus/debug/routes', '60e'),
    exact: true
  },
  {
    path: '/ai-book-hackathon/docs',
    component: ComponentCreator('/ai-book-hackathon/docs', '9bc'),
    routes: [
      {
        path: '/ai-book-hackathon/docs',
        component: ComponentCreator('/ai-book-hackathon/docs', 'b21'),
        routes: [
          {
            path: '/ai-book-hackathon/docs',
            component: ComponentCreator('/ai-book-hackathon/docs', 'e1b'),
            routes: [
              {
                path: '/ai-book-hackathon/docs/intro',
                component: ComponentCreator('/ai-book-hackathon/docs/intro', '642'),
                exact: true
              },
              {
                path: '/ai-book-hackathon/docs/setup-guides/cloud-native/setup',
                component: ComponentCreator('/ai-book-hackathon/docs/setup-guides/cloud-native/setup', 'c8d'),
                exact: true,
                sidebar: "textbookSidebar"
              },
              {
                path: '/ai-book-hackathon/docs/setup-guides/digital-twin-workstation/setup',
                component: ComponentCreator('/ai-book-hackathon/docs/setup-guides/digital-twin-workstation/setup', '063'),
                exact: true,
                sidebar: "textbookSidebar"
              },
              {
                path: '/ai-book-hackathon/docs/setup-guides/intro',
                component: ComponentCreator('/ai-book-hackathon/docs/setup-guides/intro', 'b9f'),
                exact: true,
                sidebar: "textbookSidebar"
              },
              {
                path: '/ai-book-hackathon/docs/setup-guides/physical-ai-edge-kit/setup',
                component: ComponentCreator('/ai-book-hackathon/docs/setup-guides/physical-ai-edge-kit/setup', 'b4e'),
                exact: true,
                sidebar: "textbookSidebar"
              },
              {
                path: '/ai-book-hackathon/docs/textbook/capstone/intro',
                component: ComponentCreator('/ai-book-hackathon/docs/textbook/capstone/intro', 'a72'),
                exact: true,
                sidebar: "textbookSidebar"
              },
              {
                path: '/ai-book-hackathon/docs/textbook/digital-twin/intro',
                component: ComponentCreator('/ai-book-hackathon/docs/textbook/digital-twin/intro', '36d'),
                exact: true,
                sidebar: "textbookSidebar"
              },
              {
                path: '/ai-book-hackathon/docs/textbook/foundations/intro',
                component: ComponentCreator('/ai-book-hackathon/docs/textbook/foundations/intro', '878'),
                exact: true,
                sidebar: "textbookSidebar"
              },
              {
                path: '/ai-book-hackathon/docs/textbook/intro',
                component: ComponentCreator('/ai-book-hackathon/docs/textbook/intro', '6e5'),
                exact: true,
                sidebar: "textbookSidebar"
              },
              {
                path: '/ai-book-hackathon/docs/textbook/nvidia-isaac/intro',
                component: ComponentCreator('/ai-book-hackathon/docs/textbook/nvidia-isaac/intro', 'dfd'),
                exact: true,
                sidebar: "textbookSidebar"
              },
              {
                path: '/ai-book-hackathon/docs/textbook/ros2/intro',
                component: ComponentCreator('/ai-book-hackathon/docs/textbook/ros2/intro', '963'),
                exact: true,
                sidebar: "textbookSidebar"
              },
              {
                path: '/ai-book-hackathon/docs/textbook/vla-humanoid/intro',
                component: ComponentCreator('/ai-book-hackathon/docs/textbook/vla-humanoid/intro', '108'),
                exact: true,
                sidebar: "textbookSidebar"
              }
            ]
          }
        ]
      }
    ]
  },
  {
    path: '*',
    component: ComponentCreator('*'),
  },
];
