import React from 'react';
import { Code, Layout, Wrench, Sparkles, CheckCircle2, BookOpen } from 'lucide-react';

export default function Skills() {
  const programmingSkills = [
    { name: 'C', level: 'Basic Knowledge', note: 'Fundamentals & Syntax' },
    { name: 'C++', level: 'Basic Knowledge', note: 'OOP & Problem Solving' },
    { name: 'Java', level: 'Basic Knowledge', note: 'Object-Oriented Concepts' },
    { name: 'Python', level: 'Basic Knowledge', note: 'Scripting & Basics' },
  ];

  const frontendSkills = [
    { name: 'HTML5', level: 'Basics Known', note: 'Page Structure & Semantics' },
    { name: 'CSS3', level: 'Basics Known', note: 'Styling, Flexbox & Grid' },
    { name: 'JavaScript', level: 'Basics Known', note: 'DOM & Core Concepts' },
    { name: 'React.js', level: 'Currently Learning', note: 'Components & State' },
  ];

  const toolsAndPractices = [
    { name: 'Git & GitHub', level: 'Learning & Practicing', note: 'Version Control Basics' },
    { name: 'VS Code', level: 'Daily Driver', note: 'Code Editing & Extensions' },
    { name: 'Problem Solving', level: 'Active Practice', note: 'Logic & Algorithms' },
    { name: 'Command Line', level: 'Basics Known', note: 'Terminal Navigation' },
  ];

  return (
    <section id="skills" className="section">
      <div className="container">
        <div className="section-header">
          <div className="section-badge">
            <Wrench size={14} />
            <span>Technical Capabilities</span>
          </div>
          <h2 className="section-title">
            Skills &amp; <span className="gradient-text">Learning Journey</span>
          </h2>
          <p className="section-subtitle">
            An authentic view of the languages and frontend technologies I am building a foundation in.
          </p>
        </div>

        <div className="skills-container-grid">
          {/* Programming Languages */}
          <div className="glass-card skill-group-card">
            <div className="skill-group-header">
              <div className="skill-group-icon" style={{ background: 'rgba(59, 130, 246, 0.15)', color: '#3b82f6' }}>
                <Code size={22} />
              </div>
              <div>
                <h3 className="skill-group-title">Programming Languages</h3>
                <span className="skill-group-caption">Core Logic &amp; Foundations</span>
              </div>
            </div>

            <p className="skill-group-desc">
              Strong interest in fundamental computer science problem-solving using structured and object-oriented languages.
            </p>

            <div className="skill-list">
              {programmingSkills.map((skill, idx) => (
                <div key={idx} className="skill-item">
                  <div className="skill-item-info">
                    <span className="skill-item-name">{skill.name}</span>
                    <span className="skill-level-pill foundational">{skill.level}</span>
                  </div>
                  <span className="skill-item-note">{skill.note}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Frontend Development */}
          <div className="glass-card skill-group-card frontend-featured">
            <div className="skill-group-header">
              <div className="skill-group-icon" style={{ background: 'rgba(6, 182, 212, 0.15)', color: '#06b6d4' }}>
                <Layout size={22} />
              </div>
              <div>
                <h3 className="skill-group-title">Frontend Development</h3>
                <span className="skill-group-caption">Web Basics &amp; UI</span>
              </div>
            </div>

            <div className="learning-alert-badge">
              <Sparkles size={14} color="#38bdf8" />
              <span>Currently learning and actively improving my frontend skills</span>
            </div>

            <div className="skill-list">
              {frontendSkills.map((skill, idx) => (
                <div key={idx} className="skill-item">
                  <div className="skill-item-info">
                    <span className="skill-item-name">{skill.name}</span>
                    <span className={`skill-level-pill ${skill.level === 'Currently Learning' ? 'learning' : 'basics'}`}>
                      {skill.level}
                    </span>
                  </div>
                  <span className="skill-item-note">{skill.note}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Tools & Practices */}
          <div className="glass-card skill-group-card">
            <div className="skill-group-header">
              <div className="skill-group-icon" style={{ background: 'rgba(139, 92, 246, 0.15)', color: '#8b5cf6' }}>
                <BookOpen size={22} />
              </div>
              <div>
                <h3 className="skill-group-title">Tools &amp; Learning</h3>
                <span className="skill-group-caption">Developer Workflow</span>
              </div>
            </div>

            <p className="skill-group-desc">
              Practicing with standard development tools and adopting modern workflow habits.
            </p>

            <div className="skill-list">
              {toolsAndPractices.map((tool, idx) => (
                <div key={idx} className="skill-item">
                  <div className="skill-item-info">
                    <span className="skill-item-name">{tool.name}</span>
                    <span className="skill-level-pill tools">{tool.level}</span>
                  </div>
                  <span className="skill-item-note">{tool.note}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
