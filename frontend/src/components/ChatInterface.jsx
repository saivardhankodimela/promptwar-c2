import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { motion, AnimatePresence } from 'framer-motion';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

const ChatInterface = ({ isOpen, onClose }) => {
  const [messages, setMessages] = useState([
    { text: "Hi! I'm voter.ai, your personal Election Guide. I'm here to help you understand how our democracy works in simple steps.\n\nFrom getting your ID to seeing a new government formed, I've got you covered. What would you like to ask?", isBot: true }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Accessibility: Keyboard Focus Trap & Escape Key
  useEffect(() => {
    if (!isOpen) return;

    const handleKeyDown = (e) => {
      if (e.key === 'Escape') onClose();
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, onClose]);

  useEffect(() => {
    if (isOpen) {
      inputRef.current?.focus();
    }
  }, [isOpen]);

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;
    
    const userMsg = input;
    setMessages(prev => [...prev, { text: userMsg, isBot: false }]);
    setInput('');
    setIsLoading(true);

    try {
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
      role="dialog"
      aria-modal="true"
      aria-labelledby="chat-heading"
      initial={{ opacity: 0, scale: 0.98, y: 10 }}
      animate={{ opacity: 1, scale: 1, y: 0 }}
      exit={{ opacity: 0, scale: 0.98, y: 10 }}
      className="chat-window"
    >
      <header className="chat-header">
        <h2 id="chat-heading" style={{ margin: 0, fontSize: '1.1rem', fontWeight: 800, color: 'white' }}>
          voter.<span>ai</span> | ELECTION GUIDE
        </h2>
        <button 
          onClick={onClose} 
          aria-label="Close Chat"
          className="close-button"
          style={{ background: 'none', border: 'none', color: '#888', fontSize: '1.2rem', cursor: 'pointer', padding: '5px' }}
        >
          ✕
        </button>
      </header>

      <section 
        className="chat-body"
        role="log"
        aria-live="polite"
        aria-label="Chat messages"
        aria-atomic="false"
      >
        {messages.map((m, i) => (
          <motion.div 
            key={i} 
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className={m.isBot ? "message-bot" : "message-user"}
            role="article"
          >
            {m.isBot ? (
              <div className="markdown-content">
                <ReactMarkdown remarkPlugins={[remarkGfm]}>
                  {m.text}
                </ReactMarkdown>
              </div>
            ) : (
              m.text
            )}
          </motion.div>
        ))}
        {isLoading && (
          <div className="message-bot" style={{ fontStyle: 'italic', opacity: 0.7 }}>
            voter.ai is thinking...
          </div>
        )}
        <div ref={messagesEndRef} />
      </section>

      <footer className="chat-input-area">
        <input 
          ref={inputRef}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSend()}
          placeholder="Ask about voter IDs, dates, or process..."
          aria-label="Type your question"
          className="input-field"
          disabled={isLoading}
        />
        <button 
          onClick={handleSend}
          className="send-button"
          aria-label="Send message"
          disabled={isLoading || !input.trim()}
        >
          {isLoading ? '...' : 'SEND'}
        </button>
      </footer>
    </motion.div>
  );
};

export default ChatInterface;
