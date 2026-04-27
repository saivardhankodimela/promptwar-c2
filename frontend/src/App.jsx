import React, { useState, useRef } from 'react';
import Hero from './components/Hero';
import ChatInterface from './components/ChatInterface';
import ProcessMap from './components/ProcessMap';
import { AnimatePresence } from 'framer-motion';

const App = () => {
  const [isChatOpen, setIsChatOpen] = useState(false);
  const processRef = useRef(null);

  const scrollToProcess = () => {
    processRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <div style={{ backgroundColor: '#141414', minHeight: '100vh', width: '100%' }}>
      {/* Unified Navbar */}
      <nav style={{ 
        position: 'fixed', 
        top: 0, 
        width: '100%', 
        padding: '20px 4%', 
        background: 'rgba(20, 20, 20, 0.95)',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        zIndex: 100,
        borderBottom: '1px solid #333'
      }}>
        <div style={{ fontSize: '1.8rem', fontWeight: 900, letterSpacing: '-1px', color: 'white' }}>
          ELECTION <span style={{ color: '#E50914' }}>GUIDE</span>
        </div>
        <button 
          onClick={() => setIsChatOpen(true)}
          style={{ background: '#E50914', border: 'none', color: 'white', padding: '10px 24px', borderRadius: '4px', fontWeight: 'bold', cursor: 'pointer', fontSize: '0.9rem' }}
        >
          CHAT WITH GUIDE
        </button>
      </nav>

      {/* Hero: The Vision */}
      <Hero onChat={() => setIsChatOpen(true)} onViewProcess={scrollToProcess} />
      
      {/* The 8-Step Lifecycle Roadmap */}
      <div ref={processRef}>
        <ProcessMap onChat={() => setIsChatOpen(true)} />
      </div>

      {/* The Master Agent Interface Modal */}
      <AnimatePresence>
        {isChatOpen && <ChatInterface isOpen={isChatOpen} onClose={() => setIsChatOpen(false)} />}
      </AnimatePresence>

      <footer style={{ padding: '60px 4%', backgroundColor: '#000', color: '#444', fontSize: '0.8rem', textAlign: 'center' }}>
        <p style={{ marginBottom: '0.5rem', color: '#888' }}>ELECTION GUIDE - YOUR DEMOCRACY COMPANION</p>
        <p>© 2026 Powered by Vertex AI Mumbai (asia-south1)</p>
      </footer>
    </div>
  );
};

export default App;
