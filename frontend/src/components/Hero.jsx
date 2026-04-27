import React from 'react';
import { motion } from 'framer-motion';

const Hero = ({ onChat, onViewProcess }) => {
  return (
    <div className="hero-container" style={{
      height: '70vh',
      width: '100%',
      position: 'relative',
      backgroundImage: 'linear-gradient(to bottom, rgba(0,0,0,0.5) 0%, #141414 100%), url("https://images.unsplash.com/photo-1540910419892-f7ef7173fdd4?q=80&w=2070&auto=format&fit=crop")',
      backgroundSize: 'cover',
      backgroundPosition: 'center',
      display: 'flex',
      alignItems: 'center',
      padding: '0 4%'
    }}>
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        className="hero-content"
      >
        <h1 style={{ fontSize: '3.5rem', fontWeight: 900, marginBottom: '1rem', textTransform: 'uppercase', letterSpacing: '-2px' }}>
          voter.<span style={{ color: '#E50914' }}>ai</span> | <br /> ELECTION GUIDE
        </h1>
        <p style={{ fontSize: '1.2rem', maxWidth: '550px', marginBottom: '2rem', color: '#e5e5e5', lineHeight: 1.4 }}>
          Confused about voting? I'm here to help. Get instant answers on registration, locations, and your rights in a simple chat.
        </p>
        <div style={{ display: 'flex', gap: '1rem' }}>
          <button className="btn-netflix" onClick={onChat} style={{ fontSize: '1.1rem', padding: '14px 28px' }}>
            <span>💬</span> Chat with Guide
          </button>
          <button className="btn-netflix btn-secondary" onClick={onViewProcess} style={{ fontSize: '1.1rem', padding: '14px 28px' }}>
            🗺️ How it Works
          </button>
        </div>
      </motion.div>
    </div>
  );
};

export default Hero;
