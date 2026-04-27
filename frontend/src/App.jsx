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
    <div className="app-container">
      {/* Unified Navbar */}
      <nav className="header" role="navigation" aria-label="Main Navigation">
        <div className="brand" aria-label="voter.ai">
          voter.<span>ai</span>
        </div>
        <button 
          onClick={() => setIsChatOpen(true)}
          className="send-button"
          aria-label="Start chat with election guide"
          style={{ padding: '8px 20px', fontSize: '0.9rem' }}
        >
          CHAT WITH GUIDE
        </button>
      </nav>

      <main>
        {/* Hero: The Vision */}
        <Hero onChat={() => setIsChatOpen(true)} onViewProcess={scrollToProcess} />
        
        {/* The 8-Step Lifecycle Roadmap */}
        <div ref={processRef} id="process-section">
          <ProcessMap onChat={() => setIsChatOpen(true)} />
        </div>
      </main>

      {/* The Master Agent Interface Modal */}
      <AnimatePresence>
        {isChatOpen && (
          <ChatInterface 
            isOpen={isChatOpen} 
            onClose={() => setIsChatOpen(false)} 
          />
        )}
      </AnimatePresence>

      <footer className="main-footer">
        <p>ELECTION GUIDE - YOUR DEMOCRACY COMPANION</p>
        <p>© 2026 Powered by Vertex AI</p>
      </footer>
    </div>
  );
};

export default App;
