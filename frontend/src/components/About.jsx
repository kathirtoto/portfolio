import React from 'react';
import { User, Code2, GraduationCap, Compass, Lightbulb, Target } from 'lucide-react';

export default function About() {
  const highlights = [
    {
      icon: <GraduationCap size={22} color="#3b82f6" />,
      title: 'CSE Student',
      desc: 'Pursuing Computer Science and Engineering at Rajalakshmi Engineering College.',
    },
    {
      icon: <Code2 size={22} color="#06b6d4" />,
      title: 'Programming Foundations',
      desc: 'Gaining strong basics in C, C++, Java, and Python logic building.',
    },
    {
      icon: <Compass size={22} color="#8b5cf6" />,
      title: 'Frontend Explorer',
      desc: 'Practicing HTML, CSS, JavaScript, and diving into modern React.js interfaces.',
    },
    {
      icon: <Target size={22} color="#10b981" />,
      title: 'Growth-Minded',
      desc: 'Focused on consistent hands-on learning, problem solving, and building projects.',
    },
  ];

  return (
    <section id="about" className="section">
      <div className="container">
        <div className="section-header">
          <div className="section-badge">
            <User size={14} />
            <span>About Me</span>
          </div>
          <h2 className="section-title">
            Passionate About <span className="gradient-text">Software &amp; Learning</span>
          </h2>
          <p className="section-subtitle">
            An enthusiastic Computer Science student eager to understand core concepts and build practical solutions.
          </p>
        </div>

        <div className="about-grid">
          {/* Left bio column */}
          <div className="about-text-card glass-card">
            <h3 className="about-heading">Hello! I'm Kathiresan K</h3>
            <p className="about-lead">
              I am a Computer Science and Engineering student at <strong>Rajalakshmi Engineering College</strong>.
              I have basic knowledge of <strong>C, C++, Java, and Python</strong>. I also know the basics of
              <strong> HTML, CSS, and JavaScript</strong> and I am currently improving my frontend development
              skills and learning new technologies.
            </p>
            <p>
              My goal is to cultivate a solid understanding of software development by writing clean code,
              practicing algorithmic problem solving, and exploring how modern web applications come together.
              I enjoy turning concepts learned in coursework into functional, hands-on projects.
            </p>
            <p>
              I am continuously working towards sharpening my technical capabilities and looking forward to
              collaborating on exciting developer projects and expanding my toolkit.
            </p>
          </div>

          {/* Right highlight cards */}
          <div className="about-highlights-grid">
            {highlights.map((item, idx) => (
              <div key={idx} className="glass-card highlight-card">
                <div className="highlight-icon-wrapper">{item.icon}</div>
                <h4 className="highlight-title">{item.title}</h4>
                <p className="highlight-desc">{item.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
