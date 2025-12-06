// @ts-check
// `@type` JSDoc annotations allow IDEs and type checkers to autocomplete and validate types

/** @type {import('@docusaurus/types').DocusaurusConfig} */
module.exports = {
  title: 'Physical AI Humanoid Robotics Textbook',
  tagline: 'A comprehensive guide to Physical AI and Humanoid Robotics',
  url: 'https://your-project-name.vercel.app', // Replace with your actual Vercel URL after deployment
  baseUrl: '/',
  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',
  favicon: 'img/favicon.ico',
  organizationName: 'sharjeel-ahmed17', // Usually your GitHub org/user name.
  projectName: 'ai-book-hackathon', // Usually your repo name.

  presets: [
    [
      '@docusaurus/preset-classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: require.resolve('./sidebars.js'),
          // Please change this to your repo.
          editUrl: 'https://github.com/sharjeel-ahmed17/ai-book-hackathon/edit/main/',
        },
        blog: false, // Disable blog for textbook
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      navbar: {
        title: 'Physical AI Humanoid Robotics',
        logo: {
          alt: 'Robotics Logo',
          src: 'img/logo.svg',
        },
        items: [
          {
            type: 'doc',
            docId: 'textbook/intro',
            position: 'left',
            label: 'Textbook',
          },
          {
            href: 'https://github.com/sharjeel-ahmed17/ai-book-hackathon',
            label: 'GitHub',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Textbook',
            items: [
              {
                label: 'Foundations',
                to: '/docs/textbook/foundations/intro',
              },
              {
                label: 'ROS 2',
                to: '/docs/textbook/ros2/intro',
              },
              {
                label: 'Digital Twin',
                to: '/docs/textbook/digital-twin/intro',
              },
              {
                label: 'NVIDIA Isaac',
                to: '/docs/textbook/nvidia-isaac/intro',
              },
              {
                label: 'VLA & Humanoid',
                to: '/docs/textbook/vla-humanoid/intro',
              },
              {
                label: 'Capstone',
                to: '/docs/textbook/capstone/intro',
              },
            ],
          },
          {
            title: 'Community',
            items: [
              {
                label: 'GitHub',
                href: 'https://github.com/sharjeel-ahmed17/ai-book-hackathon',
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} Physical AI Humanoid Robotics Textbook. Built with Docusaurus.`,
      },
      prism: {
        theme: require('prism-react-renderer').themes.github,
        darkTheme: require('prism-react-renderer').themes.dracula,
        additionalLanguages: ['python', 'bash', 'docker', 'json'],
      },
    }),
};