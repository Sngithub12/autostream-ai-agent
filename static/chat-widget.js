// AutoStream Chat Widget
(function() {
  const WIDGET_ID = 'autostream-chat-widget';
  const API_URL = window.AUTOSTREAM_API_URL || 'http://localhost:8000';
  
  function initWidget() {
    // Create widget container
    const container = document.getElementById(WIDGET_ID);
    if (!container) return;
    
    const html = `
      <div class="autostream-chat">
        <div class="chat-header">
          <h3>AutoStream AI Agent</h3>
          <button class="close-btn">×</button>
        </div>
        <div class="chat-messages" id="chat-messages"></div>
        <div class="chat-input-area">
          <input type="text" id="user-message" placeholder="Ask me anything...">
          <button id="send-btn">Send</button>
        </div>
      </div>
    `;
    
    container.innerHTML = html;
    
    // Add styles
    const style = document.createElement('style');
    style.textContent = `
      .autostream-chat {
        width: 100%;
        max-width: 400px;
        height: 500px;
        display: flex;
        flex-direction: column;
        border: 1px solid #ddd;
        border-radius: 8px;
        background: white;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      }
      .chat-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 15px;
        border-radius: 8px 8px 0 0;
        display: flex;
        justify-content: space-between;
        align-items: center;
      }
      .chat-header h3 {
        margin: 0;
        font-size: 16px;
      }
      .close-btn {
        background: none;
        border: none;
        color: white;
        font-size: 24px;
        cursor: pointer;
      }
      .chat-messages {
        flex: 1;
        overflow-y: auto;
        padding: 15px;
        display: flex;
        flex-direction: column;
        gap: 10px;
      }
      .message {
        padding: 10px 15px;
        border-radius: 8px;
        max-width: 80%;
        word-wrap: break-word;
      }
      .message.user {
        align-self: flex-end;
        background: #667eea;
        color: white;
      }
      .message.bot {
        align-self: flex-start;
        background: #f0f0f0;
        color: #333;
      }
      .chat-input-area {
        border-top: 1px solid #ddd;
        padding: 15px;
        display: flex;
        gap: 10px;
      }
      .chat-input-area input {
        flex: 1;
        border: 1px solid #ddd;
        border-radius: 4px;
        padding: 10px;
        font-size: 14px;
      }
      .chat-input-area button {
        background: #667eea;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 10px 20px;
        cursor: pointer;
        font-weight: bold;
      }
      .chat-input-area button:hover {
        background: #764ba2;
      }
    `;
    document.head.appendChild(style);
    
    // Event listeners
    document.getElementById('send-btn').addEventListener('click', sendMessage);
    document.getElementById('user-message').addEventListener('keypress', (e) => {
      if (e.key === 'Enter') sendMessage();
    });
    document.querySelector('.close-btn').addEventListener('click', () => {
      container.style.display = 'none';
    });
  }
  
  async function sendMessage() {
    const input = document.getElementById('user-message');
    const message = input.value.trim();
    if (!message) return;
    
    // Add user message to chat
    addMessage(message, 'user');
    input.value = '';
    
    try {
      const response = await fetch(`${API_URL}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: getUserId(),
          message: message,
          channel: 'web'
        })
      });
      
      const data = await response.json();
      addMessage(data.response, 'bot');
    } catch (error) {
      addMessage('Sorry, there was an error. Please try again.', 'bot');
    }
  }
  
  function addMessage(text, sender) {
    const messagesDiv = document.getElementById('chat-messages');
    const msgElement = document.createElement('div');
    msgElement.className = `message ${sender}`;
    msgElement.textContent = text;
    messagesDiv.appendChild(msgElement);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
  }
  
  function getUserId() {
    let userId = localStorage.getItem('autostream_user_id');
    if (!userId) {
      userId = 'user_' + Date.now();
      localStorage.setItem('autostream_user_id', userId);
    }
    return userId;
  }
  
  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initWidget);
  } else {
    initWidget();
  }
})();
