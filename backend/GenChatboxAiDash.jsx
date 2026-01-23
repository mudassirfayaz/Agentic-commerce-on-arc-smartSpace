import { useState } from 'react';
import './GenChatboxAiDash.css';

const GenChatboxAiDash = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    { text: "Hello! How can I help with your projects today?", isBot: true }
  ]);
  const [input, setInput] = useState('');

  const handleSend = (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    setMessages([...messages, { text: input, isBot: false }]);
    setInput('');
    
    // Simulate AI response
    setTimeout(() => {
      setMessages(prev => [...prev, { 
        text: "I'm processing that request for you. Would you like to check your USDC usage?", 
        isBot: true 
      }]);
    }, 1000);
  };

  return (
    <div className={`dash-chat-container ${isOpen ? 'open' : ''}`}>
      {!isOpen && (
        <button className="chat-launcher" onClick={() => setIsOpen(true)}>
          <span className="launcher-icon">💬</span>
          <span className="launcher-text">Ask AI</span>
        </button>
      )}

      {isOpen && (
        <div className="dash-chat-window">
          <div className="chat-header">
            <div className="header-info">
              <div className="bot-status"></div>
              <h3>SmartSpace AI</h3>
            </div>
            <button className="close-btn" onClick={() => setIsOpen(false)}>×</button>
          </div>

          <div className="chat-messages">
            {messages.map((msg, i) => (
              <div key={i} className={`msg-bubble ${msg.isBot ? 'bot' : 'user'}`}>
                {msg.text}
              </div>
            ))}
          </div>

          <form className="chat-input-area" onSubmit={handleSend}>
            <input 
              type="text" 
              placeholder="Type a message..." 
              value={input}
              onChange={(e) => setInput(e.target.value)}
            />
            <button type="submit" className="send-btn">Send</button>
          </form>
        </div>
      )}
    </div>
  );
};

export default GenChatboxAiDash;