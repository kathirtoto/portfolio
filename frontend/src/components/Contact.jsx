import React, { useState } from 'react';
import { Mail, Phone, Send, MessageSquare, CheckCircle, AlertCircle, Loader2, GraduationCap, ExternalLink } from 'lucide-react';

const LinkedinIcon = ({ size = 20 }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="currentColor">
    <path d="M19 3a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h14m-.5 15.5v-5.3a3.26 3.26 0 0 0-3.26-3.26c-.85 0-1.84.52-2.28 1.3v-1.11h-2.79v8.37h2.79v-4.93c0-.77.62-1.4 1.39-1.4a1.4 1.4 0 0 1 1.4 1.4v4.93h2.75M6.88 8.56a1.68 1.68 0 0 0 1.68-1.68c0-.93-.75-1.69-1.68-1.69a1.69 1.69 0 0 0-1.69 1.69c0 .93.76 1.68 1.69 1.68m1.39 9.94v-8.37H5.5v8.37h2.77z"/>
  </svg>
);

export default function Contact({ onShowToast }) {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    message: '',
    _gotcha: '', // Honeypot field for anti-spam
  });

  const [loading, setLoading] = useState(false);
  const [buttonState, setButtonState] = useState('idle'); // 'idle' | 'sending' | 'sent'
  const [status, setStatus] = useState(null); // 'success' | 'error' | null
  const [statusMessage, setStatusMessage] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setButtonState('sending');
    setStatus(null);
    setStatusMessage('');

    try {
      const res = await fetch('/api/contact', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });

      const data = await res.json();

      if (res.ok && data.success) {
        setStatus('success');
        setStatusMessage(data.message || 'Your message has been sent successfully.');
        setButtonState('sent');
        // Reset form ONLY on success
        setFormData({ name: '', email: '', message: '', _gotcha: '' });

        if (onShowToast) {
          onShowToast('success', data.message || 'Your message has been sent successfully.');
        }

        // Return button to idle after 3.5s
        setTimeout(() => {
          setButtonState('idle');
        }, 3500);
      } else {
        setStatus('error');
        const errText = data.message || 'Unable to send your message right now.';
        setStatusMessage(errText);
        setButtonState('idle');
        // Note: We deliberately DO NOT reset form data on error so user can re-try
        if (onShowToast) {
          onShowToast('error', errText);
        }
      }
    } catch (err) {
      setStatus('error');
      const errText = 'Unable to send your message right now.';
      setStatusMessage(errText);
      setButtonState('idle');
      if (onShowToast) {
        onShowToast('error', errText);
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <section id="contact" className="section">
      <div className="container">
        <div className="section-header">
          <div className="section-badge">
            <MessageSquare size={14} />
            <span>Connect With Me</span>
          </div>
          <h2 className="section-title">
            Get In <span className="gradient-text">Touch</span>
          </h2>
          <p className="section-subtitle">
            Have a question, feedback, or want to connect? Send a message directly to my inbox.
          </p>
        </div>

        <div className="contact-grid">
          {/* Contact Details Left */}
          <div className="contact-info">
            <div className="glass-card contact-info-card">
              <div className="contact-info-icon" style={{ background: 'rgba(59, 130, 246, 0.15)', color: '#3b82f6' }}>
                <Mail size={22} />
              </div>
              <div>
                <div className="contact-info-title">Email Address</div>
                <a href="mailto:kathiresantoto@gmail.com" className="contact-info-value highlight-link">
                  kathiresantoto@gmail.com
                </a>
              </div>
            </div>

            <div className="glass-card contact-info-card">
              <div className="contact-info-icon" style={{ background: 'rgba(10, 102, 194, 0.18)', color: '#0a66c2' }}>
                <LinkedinIcon size={22} />
              </div>
              <div>
                <div className="contact-info-title">LinkedIn Profile</div>
                <a
                  href="https://www.linkedin.com/in/kathiresan-toto-327564364/"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="contact-info-value highlight-link"
                  style={{ display: 'inline-flex', alignItems: 'center', gap: '0.35rem' }}
                >
                  <span>Kathiresan K</span>
                  <ExternalLink size={14} />
                </a>
              </div>
            </div>

            <div className="glass-card contact-info-card">
              <div className="contact-info-icon" style={{ background: 'rgba(16, 185, 129, 0.15)', color: '#10b981' }}>
                <Phone size={22} />
              </div>
              <div>
                <div className="contact-info-title">Phone Number</div>
                <a href="tel:9566741512" className="contact-info-value highlight-link">
                  +91 9566741512
                </a>
              </div>
            </div>

            <div className="glass-card contact-info-card">
              <div className="contact-info-icon" style={{ background: 'rgba(6, 182, 212, 0.15)', color: '#06b6d4' }}>
                <GraduationCap size={22} />
              </div>
              <div>
                <div className="contact-info-title">Institution &amp; Department</div>
                <div className="contact-info-value">
                  Rajalakshmi Engineering College
                  <div style={{ fontSize: '0.85rem', color: '#94a3b8', marginTop: '2px' }}>
                    Department of Computer Science and Engineering
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Contact Form Right */}
          <div className="glass-card contact-form-card">
            <h3 className="form-heading">Send a Message</h3>
            <p className="form-subheading">
              Submissions are forwarded directly to <strong>kathiresantoto@gmail.com</strong>.
            </p>

            {status === 'success' && (
              <div className="form-feedback success">
                <CheckCircle size={18} />
                <span>{statusMessage}</span>
              </div>
            )}

            {status === 'error' && (
              <div className="form-feedback error">
                <AlertCircle size={18} />
                <span>{statusMessage}</span>
              </div>
            )}

            <form onSubmit={handleSubmit}>
              {/* Anti-spam Honeypot Field */}
              <input
                type="text"
                name="_gotcha"
                value={formData._gotcha}
                onChange={handleChange}
                style={{ display: 'none', position: 'absolute', left: '-9999px' }}
                tabIndex="-1"
                autoComplete="off"
              />

              <div className="form-group">
                <label className="form-label" htmlFor="name">
                  Name *
                </label>
                <input
                  id="name"
                  type="text"
                  name="name"
                  required
                  placeholder="Enter your name"
                  className="form-input"
                  value={formData.name}
                  onChange={handleChange}
                />
              </div>

              <div className="form-group">
                <label className="form-label" htmlFor="email">
                  Email *
                </label>
                <input
                  id="email"
                  type="email"
                  name="email"
                  required
                  placeholder="name@example.com"
                  className="form-input"
                  value={formData.email}
                  onChange={handleChange}
                />
              </div>

              <div className="form-group">
                <label className="form-label" htmlFor="message">
                  Message *
                </label>
                <textarea
                  id="message"
                  name="message"
                  required
                  rows="5"
                  placeholder="Type your message here..."
                  className="form-textarea"
                  value={formData.message}
                  onChange={handleChange}
                ></textarea>
              </div>

              <button
                type="submit"
                className="btn btn-primary submit-btn"
                disabled={loading}
              >
                {buttonState === 'sending' ? (
                  <>
                    <Loader2 size={18} className="animate-spin" />
                    <span>Sending...</span>
                  </>
                ) : buttonState === 'sent' ? (
                  <>
                    <CheckCircle size={18} />
                    <span>Message Sent</span>
                  </>
                ) : (
                  <>
                    <Send size={18} />
                    <span>Send Message</span>
                  </>
                )}
              </button>
            </form>
          </div>
        </div>
      </div>
    </section>
  );
}
