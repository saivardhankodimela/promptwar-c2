import React from 'react';
import { motion } from 'framer-motion';

const Hero = ({ onChat, onViewProcess }) => {
  return (
    <section className="hero-container" aria-labelledby="hero-title">
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        className="hero-content"
      >
        <h1 id="hero-title">
          voter.<span>ai</span> | <br /> ELECTION GUIDE
        </h1>
        <p className="hero-description">
          Confused about voting in India? I'm your dedicated AI guide for the 8-step election lifecycle. Get instant, verified answers on registration, myths, and your rights.
        </p>
        <div className="hero-actions">
          <button 
            className="send-button" 
            onClick={onChat}
            aria-label="Chat with election guide"
          >
            Chat with Guide
          </button>
          <button 
            className="btn-secondary" 
            onClick={onViewProcess}
            aria-label="View election process roadmap"
          >
            How it Works
          </button>
        </div>
      </motion.div>
    </section>
  );
};

export default Hero;
