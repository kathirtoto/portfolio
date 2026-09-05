import React, { useState } from 'react';
import { ArrowDown, Mail, Phone, GraduationCap } from 'lucide-react';

const LinkedinIcon = ({ size = 20 }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="currentColor">
    <path d="M19 3a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h14m-.5 15.5v-5.3a3.26 3.26 0 0 0-3.26-3.26c-.85 0-1.84.52-2.28 1.3v-1.11h-2.79v8.37h2.79v-4.93c0-.77.62-1.4 1.39-1.4a1.4 1.4 0 0 1 1.4 1.4v4.93h2.75M6.88 8.56a1.68 1.68 0 0 0 1.68-1.68c0-.93-.75-1.69-1.68-1.69a1.69 1.69 0 0 0-1.69 1.69c0 .93.76 1.68 1.69 1.68m1.39 9.94v-8.37H5.5v8.37h2.77z"/>
  </svg>
);

const GithubIcon = ({ size = 20 }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M15 22v-4a4.8 4.8 0 0 0-1-3.5c3 0 6-2 6-5.5.08-1.25-.27-2.48-1-3.5.28-1.15.28-2.35 0-3.5 0 0-1 0-3 1.5-2.64-.5-5.36-.5-8 0C6 2 5 2 5 2c-.3 1.15-.3 2.35 0 3.5A5.403 5.403 0 0 0 4 9c0 3.5 3 5.5 6 5.5-.39.49-.68 1.05-.85 1.65-.17.6-.22 1.23-.15 1.85v4" />
    <path d="M9 18c-4.51 2-5-2-7-2" />
  </svg>
);

export default function Hero() {
  const [imageError, setImageError] = useState(false);

  return (
    <section id="hero" className="hero">
      <div className="container">
        <div className="hero-grid">
          {/* Left Hero Details */}
          <div className="hero-content">
            <div className="hero-badge">
              <span className="pulse-dot"></span>
              <span>Computer Science Engineering Student</span>
            </div>

            <h1 className="hero-title">
              Hi, I'm <span className="gradient-text">Kathiresan K</span>
            </h1>

            <div className="hero-college-tag">
              <GraduationCap size={18} className="hero-college-icon" />
              <span>Rajalakshmi Engineering College</span>
            </div>

            <p className="hero-desc">
              Computer Science Engineering student at Rajalakshmi Engineering College with a
              foundation in C, C++, Java, Python and frontend development. Currently learning
              and building my skills through hands-on practice.
            </p>

            <div className="hero-actions">
              <a href="#skills" className="btn btn-primary">
                <span>View My Skills</span>
                <ArrowDown size={18} />
              </a>
              <a href="#contact" className="btn btn-secondary">
                <span>Contact Me</span>
                <Mail size={18} />
              </a>
            </div>

            <div className="hero-socials">
              <a
                href="https://www.linkedin.com/in/kathiresan-toto-327564364/"
                target="_blank"
                rel="noopener noreferrer"
                className="social-icon-link linkedin-link"
                title="LinkedIn Profile: Kathiresan K"
                aria-label="Kathiresan's LinkedIn Profile"
              >
                <LinkedinIcon size={19} />
              </a>
              <a
                href="mailto:kathiresantoto@gmail.com"
                className="social-icon-link"
                title="Email: kathiresantoto@gmail.com"
                aria-label="Email Kathiresan"
              >
                <Mail size={20} />
              </a>
              <a
                href="tel:9566741512"
                className="social-icon-link"
                title="Phone: 9566741512"
                aria-label="Call Kathiresan"
              >
                <Phone size={19} />
              </a>
              <a
                href="https://github.com"
                target="_blank"
                rel="noopener noreferrer"
                className="social-icon-link"
                title="GitHub Profile"
                aria-label="GitHub Profile"
              >
                <GithubIcon size={20} />
              </a>
            </div>
          </div>

          {/* Right Hero Visual / Clean Circular Photo Avatar */}
          <div className="hero-visual">
            <div className="hero-avatar-card">
              <div className="avatar-circle-wrapper">
                {!imageError ? (
                  <img
                    src="/assets/profile.jpg"
                    alt="Kathiresan K"
                    className="avatar-img"
                    onError={() => setImageError(true)}
                  />
                ) : (
                  <div className="avatar-fallback">
                    <span className="avatar-initials">K</span>
                    <span className="avatar-role-hint">Kathiresan K</span>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
