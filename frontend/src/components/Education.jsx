import React from 'react';
import { GraduationCap, Building2, BookOpen, Clock, Award, CheckCircle } from 'lucide-react';

export default function Education() {
  const courseworkFocus = [
    'Programming in C & C++',
    'Object-Oriented Programming (Java)',
    'Python Programming & Problem Solving',
    'Data Structures & Algorithms',
    'Database Management Systems',
    'Web Development Basics',
  ];

  return (
    <section id="education" className="section">
      <div className="container">
        <div className="section-header">
          <div className="section-badge">
            <GraduationCap size={14} />
            <span>Academic Background</span>
          </div>
          <h2 className="section-title">
            My <span className="gradient-text">Education</span>
          </h2>
          <p className="section-subtitle">
            Formal engineering foundation and coursework in computer science principles.
          </p>
        </div>

        <div className="education-wrapper">
          <div className="glass-card education-card">
            <div className="education-header">
              <div className="education-icon-box">
                <Building2 size={28} color="#3b82f6" />
              </div>
              <div className="education-title-group">
                <h3 className="education-degree">B.E. Computer Science and Engineering</h3>
                <h4 className="education-college">Rajalakshmi Engineering College</h4>
              </div>
              <div className="education-status-badge">
                <Clock size={14} />
                <span>Currently Studying</span>
              </div>
            </div>

            <div className="education-divider"></div>

            <div className="education-body">
              <div className="education-field-item">
                <span className="field-label">Department:</span>
                <span className="field-value">Department of Computer Science and Engineering</span>
              </div>
              <div className="education-field-item">
                <span className="field-label">Current Status:</span>
                <span className="field-value status-highlight">Undergraduate Student</span>
              </div>

              <div className="education-focus-section">
                <div className="focus-heading">
                  <BookOpen size={16} color="#06b6d4" />
                  <span>Key Coursework & Learning Focus</span>
                </div>
                <div className="coursework-tags">
                  {courseworkFocus.map((course, idx) => (
                    <div key={idx} className="course-tag">
                      <CheckCircle size={13} color="#3b82f6" />
                      <span>{course}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
