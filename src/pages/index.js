import React from 'react';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';

export default function Home() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Hello from ${siteConfig.title}`}
      description="Physical AI Humanoid Robotics Textbook">
      <main>
        <div className="container margin-vert--xl">
          <div className="row">
            <div className="col col--6 col--offset-3">
              <h1 className="hero__title">{siteConfig.title}</h1>
              <p className="hero__subtitle">{siteConfig.tagline}</p>
              <div className="margin-vert--lg">
                <a
                  className="button button--primary button--lg"
                  href="/docs/intro">
                  Get Started
                </a>
              </div>
            </div>
          </div>
        </div>
      </main>
    </Layout>
  );
}