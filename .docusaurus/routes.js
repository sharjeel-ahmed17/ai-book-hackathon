import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';

export default [
  {
    path: '/__docusaurus/debug',
    component: ComponentCreator('/__docusaurus/debug', '5ff'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/config',
    component: ComponentCreator('/__docusaurus/debug/config', '5ba'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/content',
    component: ComponentCreator('/__docusaurus/debug/content', 'a2b'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/globalData',
    component: ComponentCreator('/__docusaurus/debug/globalData', 'c3c'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/metadata',
    component: ComponentCreator('/__docusaurus/debug/metadata', '156'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/registry',
    component: ComponentCreator('/__docusaurus/debug/registry', '88c'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/routes',
    component: ComponentCreator('/__docusaurus/debug/routes', '000'),
    exact: true
  },
  {
    path: '/docs',
    component: ComponentCreator('/docs', '287'),
    routes: [
      {
        path: '/docs',
        component: ComponentCreator('/docs', '928'),
        routes: [
          {
            path: '/docs',
            component: ComponentCreator('/docs', 'dd1'),
            routes: [
              {
                path: '/docs/intro',
                component: ComponentCreator('/docs/intro', '853'),
                exact: true
              },
              {
                path: '/docs/setup-guides/cloud-native/setup',
                component: ComponentCreator('/docs/setup-guides/cloud-native/setup', 'a6e'),
                exact: true,
                sidebar: "textbookSidebar"
              },
              {
                path: '/docs/setup-guides/digital-twin-workstation/setup',
                component: ComponentCreator('/docs/setup-guides/digital-twin-workstation/setup', '229'),
                exact: true,
                sidebar: "textbookSidebar"
              },
              {
                path: '/docs/setup-guides/intro',
                component: ComponentCreator('/docs/setup-guides/intro', 'df0'),
                exact: true,
                sidebar: "textbookSidebar"
              },
              {
                path: '/docs/setup-guides/physical-ai-edge-kit/setup',
                component: ComponentCreator('/docs/setup-guides/physical-ai-edge-kit/setup', 'c39'),
                exact: true,
                sidebar: "textbookSidebar"
              },
              {
                path: '/docs/textbook/capstone/intro',
                component: ComponentCreator('/docs/textbook/capstone/intro', 'd62'),
                exact: true,
                sidebar: "textbookSidebar"
              },
              {
                path: '/docs/textbook/digital-twin/intro',
                component: ComponentCreator('/docs/textbook/digital-twin/intro', 'd0b'),
                exact: true,
                sidebar: "textbookSidebar"
              },
              {
                path: '/docs/textbook/foundations/intro',
                component: ComponentCreator('/docs/textbook/foundations/intro', 'cbe'),
                exact: true,
                sidebar: "textbookSidebar"
              },
              {
                path: '/docs/textbook/intro',
                component: ComponentCreator('/docs/textbook/intro', 'a48'),
                exact: true,
                sidebar: "textbookSidebar"
              },
              {
                path: '/docs/textbook/nvidia-isaac/intro',
                component: ComponentCreator('/docs/textbook/nvidia-isaac/intro', '70b'),
                exact: true,
                sidebar: "textbookSidebar"
              },
              {
                path: '/docs/textbook/ros2/intro',
                component: ComponentCreator('/docs/textbook/ros2/intro', '47d'),
                exact: true,
                sidebar: "textbookSidebar"
              },
              {
                path: '/docs/textbook/vla-humanoid/intro',
                component: ComponentCreator('/docs/textbook/vla-humanoid/intro', '3e0'),
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
