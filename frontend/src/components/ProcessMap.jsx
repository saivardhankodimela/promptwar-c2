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
    <div style={{ padding: '4rem 4%', backgroundColor: '#141414', borderTop: '1px solid #222' }}>
      <h2 style={{ fontSize: '2.2rem', fontWeight: 900, marginBottom: '3rem', textAlign: 'center' }}>
        The Full Election <span style={{ color: '#E50914' }}>Lifecycle</span>
      </h2>
      
      {/* 8-Step Grid */}
      <div style={{ 
        display: 'grid', 
        gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', 
        gap: '15px',
        marginBottom: '4rem'
      }}>
        {steps.map((step, i) => (
          <motion.div 
            key={i}
            whileHover={{ y: -5, backgroundColor: '#1f1f1f' }}
            style={{
              backgroundColor: '#181818',
              padding: '1.5rem',
              borderRadius: '8px',
              borderLeft: '4px solid #E50914',
              textAlign: 'center',
              boxShadow: '0 4px 15px rgba(0,0,0,0.3)',
              transition: 'background-color 0.3s'
            }}
          >
            <h3 style={{ marginBottom: '0.5rem', color: '#E50914', fontSize: '1.1rem' }}>{step.title}</h3>
            <p style={{ color: '#b3b3b3', fontSize: '0.85rem' }}>{step.desc}</p>
          </motion.div>
        ))}
      </div>

      {/* Primary Chat CTA at the Bottom of Process */}
      <div style={{ textAlign: 'center', padding: '2rem', backgroundColor: '#181818', borderRadius: '12px', border: '1px dashed #333' }}>
        <h3 style={{ marginBottom: '1rem', fontSize: '1.5rem' }}>Have questions about any of these steps?</h3>
        <p style={{ color: '#b3b3b3', marginBottom: '2rem' }}>Our AI Guide is ready to explain the counting rules, EVM security protocols, or registration steps.</p>
        <button 
          className="btn-netflix" 
          onClick={onChat}
          style={{ fontSize: '1.2rem', padding: '16px 40px', margin: '0 auto' }}
        >
          <span>💬</span> Chat with Election Guide
        </button>
      </div>
    </div>
  );
};

export default ProcessMap;
