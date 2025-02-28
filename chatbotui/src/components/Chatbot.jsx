import React, { useState, useEffect } from 'react';
import brain from '../assets/icon.png'
import './style.css';

const initialQuestions = [
  '!info',
  '!commands',
  '!links'
];

class Chatbox {
    constructor() {
      this.args = {
        openButton: document.querySelector('.chatbox__button'),
        chatBox: document.querySelector('.chatbox__support'),
        sendButton: document.querySelector('.send__button')
      };
  
      this.state = false;
      this.messages = [];
    }
  
    display() {
      const { openButton, chatBox, sendButton } = this.args;
  
      openButton.addEventListener('click', () => this.toggleState(chatBox));
  
      sendButton.addEventListener('click', () => this.onSendButton(chatBox));
  
      const node = chatBox.querySelector('input');
      node.addEventListener('keyup', ({ key }) => {
        if (key === 'Enter') {
          this.onSendButton(chatBox);
        }
      });
    }
  
    toggleState(chatbox) {
      this.state = !this.state;
  
      // Show or hide the box
      if (this.state) {
        chatbox.classList.add('chatbox--active');
      } else {
        chatbox.classList.remove('chatbox--active');
      }
    }
  
    onSendButton(chatbox) {
      const textField = chatbox.querySelector('input');
      const text1 = textField.value;
      if (text1 === '') {
          return;
      }
  
      const msg1 = { name: 'User', message: text1 };
      this.messages.push(msg1);
  
      // Show typing indicator
      const typingIndicator = { name: 'Sam', message: 'Typing...' };
      this.messages.push(typingIndicator);
      this.updateChatText(chatbox);
  
      setTimeout(() => {
          // Simulate the chatbot response with a delay
          fetch('https://chatbot-ebx8.onrender.com/predict', {
              method: 'POST',
              body: JSON.stringify({ message: text1 }),
              mode: 'cors',
              headers: {
                  'Content-Type': 'application/json'
              },
          })
          .then(r => r.json())
          .then(r => {
              // Remove the typing indicator
              const typingIndex = this.messages.findIndex(msg => msg.message === 'Typing...');
              if (typingIndex !== -1) {
                  this.messages.splice(typingIndex, 1);
              }
  
              const msg2 = { name: 'Sam', message: r.answer };
              this.messages.push(msg2);
              this.updateChatText(chatbox);
              textField.value = '';
          })
          .catch((error) => {
              console.error('Error:', error);
              this.updateChatText(chatbox);
              textField.value = '';
          });
      }, 800); // Adjust the delay time as needed
  }
  
    updateChatText(chatbox) {
      let html = '';
      this.messages.slice().reverse().forEach(function(item, index) {
        if (item.name === 'Sam') {
          html += '<div class="messages__item messages__item--visitor">' + item.message + '</div>';
        } else {
          html += '<div class="messages__item messages__item--operator">' + item.message + '</div>';
        }
      });
  
      const chatmessage = chatbox.querySelector('.chatbox__messages');
      chatmessage.innerHTML = html;
    }
  }
  
function Chatbot() {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [showOptions, setShowOptions] = useState(true);
  const [questions] = useState(initialQuestions);
  const [clickedQuestions, setClickedQuestions] = useState([]);

  useEffect(() => {
    const chatbox = new Chatbox(setMessages);
    chatbox.display();

    // Cleanup function if needed
    return () => {
      // Cleanup logic here if needed
    };
  }, []);

  const handleSendButton = () => {
    if (inputValue.trim() !== '') {
      const newMessage = {
        name: 'User',
        message: inputValue
      };
      setMessages([...messages, newMessage]);
      setInputValue('');
      setShowOptions(true);
    }
  };

  const handleInputChange = (event) => {
    setInputValue(event.target.value);
  };

  const handleQuestionClick = (question) => {
    setInputValue(question);
    setShowOptions(false);
    setClickedQuestions([...clickedQuestions, question]);
  };

  const handleRefreshOptions = () => {
    setClickedQuestions([]);
    setShowOptions(true);
  };

  const handleKeyDown = (event) => {
    if (event.key === 'Enter') {
      setShowOptions(true);
    }
  };

  useEffect(() => {
    if (clickedQuestions.length === questions.length) {
      setShowOptions(false);
    }
  }, [clickedQuestions, questions]);

  return (
    <div className="container hidden md:block font-sans">
      <div className="chatbox">
        <div className="chatbox__support">
          <div className="chatbox__header">
            <div className="chatbox__image--header">
              <img className='chatbot__icon--inside' src={brain} alt="chatbox icon" />
            </div>
            <div className="chatbox__content--header">
              <h4 className="chatbox__heading--header">Chat support 👇</h4>
              <p className="chatbox__description--header">Hi, My name is Sam. How can I help you?</p>
            </div>
          </div>
          {showOptions && clickedQuestions.length === questions.length && (
            <div className="chatbox__refresh-button">
              <button className="chatbox__refresh-button" onClick={handleRefreshOptions}>
                Refresh options
              </button>
            </div>
          )}
          {showOptions && (
            <div className="chatbox__options">
              {questions.map((question, index) => {
                if (clickedQuestions.includes(question)) {
                  return null;
                }
                return (
                  <div key={index} className="chatbox__option-line">
                    <button
                      className="chatbox__option-button"
                      onClick={() => handleQuestionClick(question)}
                    >
                      {question}
                    </button>
                  </div>
                );
              })}
            </div>
          )}
          <div className="chatbox__messages">
            {messages.map((message, index) => (
              <div className="message" key={index}>
                <div className="message__text">{message.message}</div>
              </div>
            ))}
          </div>
          <div className="chatbox__footer">
            <input
              type="text"
              placeholder="Write a message..."
              value={inputValue}
              onChange={handleInputChange}
              onKeyDown={handleKeyDown}
            />
            <button className="chatbox__send--footer send__button" onClick={handleSendButton}>
              Send
            </button>
          </div>
        </div>
        <div className="chatbox__button">
          <button className='chatbot__icon--outside'>
            <img src={brain} alt="chatbox icon" />
          </button>
        </div>
      </div>
    </div>
  );
}

export default Chatbot;
