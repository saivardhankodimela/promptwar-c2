import React from 'react';
import { motion } from 'framer-motion';

const ProcessMap = ({ onChat }) => {
  const steps = [
    { title: "1. Electoral Roll", desc: "Preparation and verification of voter lists." },
    { title: "2. Announcement", desc: "Official schedule and Model Code of Conduct." },
    { title: "3. Nominations", desc: "Filing and scrutiny of candidate papers." },
    { title: "4. Campaigning", desc: "Political outreach and manifesto releases." },
    { title: "5. Polling Day", desc: "Secure voting via EVM and VVPAT." },
    { title: "6. EVM Security", desc: "Sealing and transport to strongrooms." },
    { title: "7. Counting", desc: "Tallying of votes and declaration of results." },
    { title: "8. Formation", desc: "Government formation and oath of office." }
  ];

  return (
    <section className="process-section" aria-labelledby="process-heading">
      <h2 id="process-heading">
        The Full Election <span>Lifecycle</span>
      </h2>
      <p style={{ textAlign: 'center', color: 'var(--text-gray)', marginTop: '-3rem', marginBottom: '4rem', fontSize: '1.2rem' }}>
        Master the 8-Step Journey of Indian Democracy
      </p>
      
      {/* 8-Step Grid */}
      <div className="process-grid">
        {steps.map((step, i) => (
          <motion.div 
            key={i}
            whileHover={{ y: -5 }}
            className="process-card"
            tabIndex="0"
            role="article"
            aria-label={`Step ${step.title}: ${step.desc}`}
          >
            <h3>{step.title}</h3>
            <p>{step.desc}</p>
          </motion.div>
        ))}
      </div>

      {/* Primary Chat CTA at the Bottom of Process */}
      <div className="process-cta">
        <h3>Have questions about any of these steps?</h3>
        <p>Our AI Guide is ready to explain the counting rules, EVM security protocols, or registration steps.</p>
        <button 
          className="send-button" 
          onClick={onChat}
          aria-label="Ask a question about the election process"
        >
          Chat with Election Guide
        </button>
      </div>
    </section>
  );
};

export default ProcessMap;
