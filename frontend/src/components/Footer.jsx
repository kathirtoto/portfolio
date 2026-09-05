import React from 'react';
import { ArrowUp, Terminal, Mail, Phone } from 'lucide-react';

const LinkedinIcon = ({ size = 16 }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="currentColor">
    <path d="M19 3a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h14m-.5 15.5v-5.3a3.26 3.26 0 0 0-3.26-3.26c-.85 0-1.84.52-2.28 1.3v-1.11h-2.79v8.37h2.79v-4.93c0-.77.62-1.4 1.39-1.4a1.4 1.4 0 0 1 1.4 1.4v4.93h2.75M6.88 8.56a1.68 1.68 0 0 0 1.68-1.68c0-.93-.75-1.69-1.68-1.69a1.69 1.69 0 0 0-1.69 1.69c0 .93.76 1.68 1.69 1.68m1.39 9.94v-8.37H5.5v8.37h2.77z"/>
  </svg>
);

export default function Footer() {
  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <footer className="footer">
      <div className="container footer-inner">
        <div className="footer-left">
          <div className="footer-brand">
            <div className="brand-icon">
              <Terminal size={15} />
            </div>
            <span className="footer-brand-name">Kathiresan K</span>
          </div>
          <p className="footer-tagline">
            Computer Science &amp; Engineering Student • Rajalakshmi Engineering College
          </p>
          <div className="footer-copy">
            &copy; {new Date().getFullYear()} Kathiresan K. All Rights Reserved.
          </div>
        </div>

        <div className="footer-right">
          <div className="footer-links-group" style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
            <a
              href="https://www.linkedin.com/in/kathiresan-toto-327564364/"
              target="_blank"
              rel="noopener noreferrer"
              className="social-icon-link"
              title="LinkedIn Profile"
              aria-label="LinkedIn"
              style={{ width: '34px', height: '34px' }}
            >
              <LinkedinIcon size={16} />
            </a>
            <a
              href="mailto:kathiresantoto@gmail.com"
              className="social-icon-link"
              title="Email"
              aria-label="Email"
              style={{ width: '34px', height: '34px' }}
            >
              <Mail size={16} />
            </a>
            <a
              href="tel:9566741512"
              className="social-icon-link"
              title="Phone"
              aria-label="Phone"
              style={{ width: '34px', height: '34px' }}
            >
              <Phone size={15} />
            </a>
          </div>

          <button
            onClick={scrollToTop}
            className="btn btn-secondary scroll-top-btn"
            aria-label="Scroll back to top"
            title="Back to Top"
          >
            <ArrowUp size={16} />
          </button>
        </div>
      </div>
    </footer>
  );
}
