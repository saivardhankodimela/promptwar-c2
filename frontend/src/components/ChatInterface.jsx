import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { motion, AnimatePresence } from 'framer-motion';

const ChatInterface = ({ isOpen, onClose }) => {
  const [messages, setMessages] = useState([
    { text: "Hi! I'm voter.ai, your personal Election Guide. I'm here to help you understand how our democracy works in simple steps.\n\nFrom getting your ID to seeing a new government formed, I've got you covered. What would you like to ask?", isBot: true }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim()) return;
    
    const userMsg = input;
    setMessages(prev => [...prev, { text: userMsg, isBot: false }]);
    setInput('');
    setIsLoading(true);

    try {
      // Relative URL for Unified Container
      const response = await axios.post('/chat', {
        user_id: 'unified_user',
        query: userMsg
      });
      setMessages(prev => [...prev, { text: response.data.response, isBot: true, data: response.data }]);
    } catch (error) {
      setMessages(prev => [...prev, { text: "Oops! I'm having a little trouble connecting. Can you try again in a second?", isBot: true }]);
    } finally {
      setIsLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <motion.div 
      initial={{ opacity: 0, scale: 0.98, y: 10 }}
      animate={{ opacity: 1, scale: 1, y: 0 }}
      exit={{ opacity: 0, scale: 0.98, y: 10 }}
      style={{
        position: 'fixed',
        top: '5%',
        left: '5%',
        right: '5%',
        bottom: '5%',
        backgroundColor: '#111',
        zIndex: 1000,
        borderRadius: '12px',
        display: 'flex',
        flexDirection: 'column',
        boxShadow: '0 0 100px rgba(0,0,0,0.9)',
        border: '1px solid #E50914',
        overflow: 'hidden'
      }}
    >
      <div style={{ padding: '1.2rem 2rem', borderBottom: '1px solid #333', display: 'flex', justifyContent: 'space-between', alignItems: 'center', backgroundColor: '#181818' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <h2 style={{ fontSize: '1rem', fontWeight: 900, letterSpacing: '1px', color: 'white' }}>
            voter.<span style={{ color: '#E50914' }}>ai</span> | ELECTION GUIDE
          </h2>
        </div>
        <button onClick={onClose} style={{ background: 'none', border: 'none', color: '#666', fontSize: '1.4rem', cursor: 'pointer' }}>✕</button>
      </div>

      <div style={{ flex: 1, overflowY: 'auto', padding: '2rem', display: 'flex', flexDirection: 'column', gap: '1.2rem', backgroundColor: '#0c0c0c' }}>
        {messages.map((m, i) => (
          <div key={i} style={{ 
            alignSelf: m.isBot ? 'flex-start' : 'flex-end',
            maxWidth: '80%',
            backgroundColor: m.isBot ? '#1f1f1f' : '#E50914',
            padding: '14px 20px',
            borderRadius: '8px',
            lineHeight: 1.5,
            fontSize: '1rem',
            border: m.isBot ? '1px solid #333' : 'none',
            whiteSpace: 'pre-wrap',
            color: 'white'
          }}>
            {m.text}
          </div>
        ))}
        {isLoading && <div style={{ color: '#E50914', fontSize: '0.8rem', fontStyle: 'italic' }}>Thinking...</div>}
        <div ref={messagesEndRef} />
      </div>

      <div style={{ padding: '1.5rem 2rem', borderTop: '1px solid #333', display: 'flex', gap: '1rem', backgroundColor: '#181818' }}>
        <input 
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleSend()}
          placeholder="Ask me anything about elections!"
          style={{
            flex: 1,
            backgroundColor: '#0c0c0c',
            border: '1px solid #444',
            color: 'white',
            padding: '14px 20px',
            borderRadius: '6px',
            outline: 'none',
            fontSize: '1rem'
          }}
        />
        <button 
          onClick={handleSend}
          style={{ 
            backgroundColor: '#E50914', 
            color: 'white', 
            border: 'none', 
            padding: '0 30px', 
            borderRadius: '6px', 
            fontWeight: '900', 
            cursor: 'pointer'
          }}
        >
          SEND
        </button>
      </div>
    </motion.div>
  );
};

export default ChatInterface;
