import React from 'react';
import { motion } from 'framer-motion';

const ProcessMap = ({ onChat }) => {
  const steps = [
    { title: "1. Register", desc: "Get on the voter list." },
    { title: "2. Verify", desc: "Confirm your details." },
    { title: "3. Research", desc: "Know your candidates." },
    { title: "4. Vote", desc: "Cast your ballot at the booth." },
    { title: "5. EVM Security", desc: "Collection & safe storage." },
    { title: "6. Counting", desc: "Official tallying of votes." },
    { title: "7. Results", desc: "Declaration of the winners." },
    { title: "8. Formation", desc: "Government takes the oath." }
  ];

  return (
    <section className="process-section" aria-labelledby="process-heading">
      <h2 id="process-heading">
        The Full Election <span>Lifecycle</span>
      </h2>
      
      {/* 8-Step Grid */}
      <div className="process-grid">
        {steps.map((step, i) => (
          <motion.div 
            key={i}
            whileHover={{ y: -5 }}
            className="process-card"
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
