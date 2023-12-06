// component for adding the tone text box

import React, { useState } from 'react';

const ToneText = ({ onToneSubmit }) => {
  const [inputValue, setInputValue] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  
  // trim input text
  const handleInputChange = (event) => {
    const inputText = event.target.value.trim();
    setInputValue(inputText);
    onToneSubmit(inputText);
    setErrorMessage('');
  };

  const handleInputBlur = () => {
    // only allow one word
    if (inputValue === '' || inputValue.split(' ').length > 1) {
      setErrorMessage('Please enter one word to specify your tone!');
    }
  };

  const handleInputKeyPress = (event) => {
    // prevent the input from accepting spaces
    if (event.key === ' ') {
      event.preventDefault();
    }
  };

  return (
    <div style={{ marginTop: '20px', textAlign: 'center' }}>
      <input
        type="text"
        value={inputValue}
        onChange={handleInputChange}
        onBlur={handleInputBlur}
        onKeyDown={handleInputKeyPress}
        placeholder="Specify a tone"
        style={{
          fontFamily: "Roboto, Helvetica, Arial, sans-serif",
          fontSize: '18px',
          padding: '10px',
        }}
      />
      {/* Remove the button */}
      {errorMessage && <p style={{ color: 'red' }}>{errorMessage}</p>}
    </div>
  );
};

export default ToneText;