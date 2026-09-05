import React from 'react';
import { Award, Trophy, Code, Laptop, FileCheck, Sparkles, PlusCircle } from 'lucide-react';

export default function Achievements() {
  const achievementCategories = [
    {
      icon: <Trophy size={22} color="#fbbf24" />,
      title: 'Hackathons',
      status: 'Ready for updates',
      desc: 'Participating in inter-college and online hackathons to build collaborative solutions under time constraints.',
    },
    {
      icon: <Code size={22} color="#3b82f6" />,
      title: 'Coding Events',
      status: 'Ready for updates',
      desc: 'Engaging in programming contests and problem-solving events to strengthen algorithmic thinking.',
    },
    {
      icon: <Laptop size={22} color="#06b6d4" />,
      title: 'Workshops & Seminars',
      status: 'Ready for updates',
      desc: 'Attending technical workshops on emerging computer science tools, frameworks, and modern technologies.',
    },
    {
      icon: <FileCheck size={22} color="#10b981" />,
      title: 'Certifications',
      status: 'Ready for updates',
      desc: 'Pursuing structured technical courses and certifications across programming and web development.',
    },
  ];

  return (
    <section id="achievements" className="section">
      <div className="container">
        <div className="section-header">
          <div className="section-badge">
            <Award size={14} />
            <span>Milestones &amp; Events</span>
          </div>
          <h2 className="section-title">
            Achievements &amp; <span className="gradient-text">Activities</span>
          </h2>
          <p className="section-subtitle">
            A dedicated space to track participations, coding events, workshops, and verified credentials.
          </p>
        </div>

        <div className="achievements-container-grid">
          {achievementCategories.map((cat, idx) => (
            <div key={idx} className="glass-card achievement-category-card">
              <div className="achievement-cat-header">
                <div className="achievement-cat-icon">{cat.icon}</div>
                <span className="achievement-status-tag">{cat.status}</span>
              </div>
              <h3 className="achievement-cat-title">{cat.title}</h3>
              <p className="achievement-cat-desc">{cat.desc}</p>
            </div>
          ))}
        </div>

        {/* Section info box */}
        <div className="achievements-note glass-card">
          <Sparkles size={18} color="#38bdf8" />
          <span>
            Events and accomplishments will be highlighted here as I participate in hackathons, workshops, and earn new technical certifications.
          </span>
        </div>
      </div>
    </section>
  );
}
