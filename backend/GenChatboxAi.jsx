import React, { useState } from 'react';
import './GenChatboxAi.css';

const GenChatboxAi = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [message, setMessage] = useState('');
  const [chatLog, setChatLog] = useState([
    { role: 'ai', text: 'Hi! I am SmartSpace AI. How can I help you with USDC payments today?' }
  ]);

  const toggleChat = () => setIsOpen(!isOpen);

  const handleSend = () => {
    if (!message.trim()) return;
    
    // Add user message
    setChatLog([...chatLog, { role: 'user', text: message }]);
    setMessage('');

    // Mock AI Response (Integrate your Gemini API call here)
    setTimeout(() => {
      setChatLog(prev => [...prev, { role: 'ai', text: 'That is a great question! Let me check that for you.' }]);
    }, 1000);
  };

  return (
    <div className={`chatbox-wrapper ${isOpen ? 'active' : ''}`}>
      {/* Floating Button */}
      <button className="chat-trigger" onClick={toggleChat}>
        {isOpen ? '✕' : '💬'}
      </button>

      {/* Chat Window */}
      {isOpen && (
        <div className="chat-window">
          <div className="chat-header">
            <h4>SmartSpace AI</h4>
          </div>
          <div className="chat-body">
            {chatLog.map((msg, i) => (
              <div key={i} className={`chat-bubble ${msg.role}`}>
                {msg.text}
              </div>
            ))}
          </div>
          <div className="chat-footer">
            <input 
              type="text" 
              value={message} 
              onChange={(e) => setMessage(e.target.value)}
              placeholder="Ask about APIs..." 
              onKeyPress={(e) => e.key === 'Enter' && handleSend()}
            />
            <button onClick={handleSend}>Send</button>
          </div>
        </div>
      )}
    </div>
  );
};

export default GenChatboxAi;