import React from 'react';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import clsx from 'clsx';

import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <h1 className="hero__title">{siteConfig.title}</h1>
        <p className="hero__subtitle">{siteConfig.tagline}</p>
        <div className={styles.buttons}>
          <Link
            className="button button--secondary button--lg"
            to="/docs/textbook/intro">
            Get Started - 5 min ⏱️
          </Link>
        </div>
      </div>
    </header>
  );
}

const Card = ({ title, description, icon, to, color }) => (
  <div className={`col col--4 ${styles.featureCard}`}>
    <div className={clsx('card', styles.card, styles[color])}>
      <div className="card__body">
        <div className={styles.cardHeader}>
          <span className={styles.cardIcon}>{icon}</span>
          <h3 className="card__title">{title}</h3>
        </div>
        <p>{description}</p>
      </div>
      <div className="card__footer">
        <Link to={to} className={`button button--${color || 'primary'} button--block`}>
          Learn More
        </Link>
      </div>
    </div>
  </div>
);

function HomepageCards() {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          <Card
            title="Foundations of Physical AI"
            description="Weeks 1-2: Learn the fundamental concepts of Physical AI, embodied intelligence, and the intersection of AI and robotics."
            icon="🤖"
            to="/docs/textbook/foundations/intro"
            color="primary"
          />
          <Card
            title="ROS 2 Framework"
            description="Weeks 3-5: Master the Robot Operating System for building and controlling complex robotic applications."
            icon="🔧"
            to="/docs/textbook/ros2/intro"
            color="secondary"
          />
          <Card
            title="Digital Twin Workflows"
            description="Weeks 6-7: Create and manage digital twins for simulation, testing, and validation of robotic systems."
            icon="🔄"
            to="/docs/textbook/digital-twin/intro"
            color="info"
          />
        </div>

        <div className="row" style={{ marginTop: '20px' }}>
          <Card
            title="NVIDIA Isaac"
            description="Weeks 8-10: Leverage NVIDIA Isaac platform for accelerated robotics development and deployment."
            icon="⚡"
            to="/docs/textbook/nvidia-isaac/intro"
            color="success"
          />
          <Card
            title="VLA Models & Humanoid"
            description="Weeks 11-13: Explore Vision-Language-Action models and their application in humanoid robotics."
            icon="🦾"
            to="/docs/textbook/vla-humanoid/intro"
            color="warning"
          />
          <Card
            title="Capstone Project"
            description="Build an autonomous humanoid pipeline integrating all concepts learned throughout the curriculum."
            icon="🎓"
            to="/docs/textbook/capstone/intro"
            color="danger"
          />
        </div>
      </div>
    </section>
  );
}

function SetupGuides() {
  return (
    <section className={styles.setupSection}>
      <div className="container">
        <div className="text--center padding-horiz--md">
          <h2>Platform Setup Guides</h2>
          <p>Get your development environment ready with our comprehensive setup guides</p>
        </div>
        <div className="row">
          <div className="col col--4">
            <div className="card">
              <div className="card__body text--center">
                <h3>Workstation Setup</h3>
                <p>Digital Twin Workstation configuration</p>
              </div>
              <div className="card__footer">
                <Link to="/docs/setup-guides/digital-twin-workstation/setup" className="button button--primary button--block">
                  Setup Guide
                </Link>
              </div>
            </div>
          </div>
          <div className="col col--4">
            <div className="card">
              <div className="card__body text--center">
                <h3>Edge Kit Setup</h3>
                <p>Physical AI Edge Kit configuration</p>
              </div>
              <div className="card__footer">
                <Link to="/docs/setup-guides/physical-ai-edge-kit/setup" className="button button--secondary button--block">
                  Setup Guide
                </Link>
              </div>
            </div>
          </div>
          <div className="col col--4">
            <div className="card">
              <div className="card__body text--center">
                <h3>Cloud Setup</h3>
                <p>Cloud-Native Environment configuration</p>
              </div>
              <div className="card__footer">
                <Link to="/docs/setup-guides/cloud-native/setup" className="button button--info button--block">
                  Setup Guide
                </Link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

export default function Home() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Home - ${siteConfig.title}`}
      description="Physical AI Humanoid Robotics Textbook - A comprehensive guide to building intelligent humanoid robots">
      <HomepageHeader />
      <main>
        <HomepageCards />
        <SetupGuides />
      </main>
    </Layout>
  );
}