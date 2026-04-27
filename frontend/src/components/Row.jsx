import React from 'react';
import { motion } from 'framer-motion';

const Row = ({ title, cards }) => {
  return (
    <div style={{ padding: '2rem 4%', overflow: 'visible' }}>
      <h2 style={{ fontSize: '1.5rem', fontWeight: 700, marginBottom: '1rem', color: '#e5e5e5' }}>{title}</h2>
      <div style={{ display: 'flex', gap: '10px', overflowX: 'auto', paddingBottom: '1rem', scrollbarWidth: 'none' }}>
        {cards.map((card, idx) => (
          <motion.div
            key={idx}
            whileHover={{ scale: 1.1, zIndex: 10 }}
            style={{
              flex: '0 0 240px',
              height: '135px',
              backgroundColor: '#181818',
              borderRadius: '4px',
              cursor: 'pointer',
              backgroundImage: `url(${card.image})`,
              backgroundSize: 'cover',
              backgroundPosition: 'center',
              position: 'relative',
              boxShadow: '0 4px 15px rgba(0,0,0,0.5)'
            }}
          >
            <div style={{
              position: 'absolute',
              bottom: 0,
              left: 0,
              right: 0,
              padding: '10px',
              background: 'linear-gradient(transparent, rgba(0,0,0,0.9))',
              fontSize: '0.8rem',
              fontWeight: 'bold'
            }}>
              {card.title}
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
};

export default Row;
