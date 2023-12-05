// import React, { useState } from 'react';

// const ToneButton = () => {
//   const [inputValue, setInputValue] = useState('');
//   const [errorMessage, setErrorMessage] = useState('');

//   const handleInputChange = (event) => {
//     const inputText = event.target.value.trim();
//     setInputValue(inputText);
//     setErrorMessage('');
//   };

//   const handleButtonClick = () => {
//     // Validate if the input contains only one word
//     if (inputValue === '' || inputValue.split(' ').length > 1) {
//       setErrorMessage('Please enter only one word to specify your tone!');
//     } else {
//       // Perform your desired action with the one-word input
//       console.log('Entered word:', inputValue);
//       // Add your logic here, e.g., sending the word to the backend or performing some action
//     }
//   };

//   return (
//     <div style={{ marginTop: '20px', textAlign: 'center' }}>
//       <input
//         type="text"
//         value={inputValue}
//         onChange={handleInputChange}
//         placeholder="Specify a tone"
//       />
//       <button onClick={handleButtonClick}>Submit</button>
//       {errorMessage && <p style={{ color: 'red' }}>{errorMessage}</p>}
//     </div>
//   );
// };

// export default ToneButton;
// import React, { useState } from 'react';

// const ToneButton = ({ onToneSubmit }) => {
//   const [inputValue, setInputValue] = useState('');
//   const [errorMessage, setErrorMessage] = useState('');

//   const handleInputChange = (event) => {
//     const inputText = event.target.value.trim();
//     setInputValue(inputText);
//     setErrorMessage('');
//   };

//   const handleButtonClick = () => {
//     if (inputValue === '' || inputValue.split(' ').length > 1) {
//       setErrorMessage('Please enter only one word to specify your tone!');
//     } else {
//       console.log('Entered word:', inputValue);
//       onToneSubmit(inputValue); // Pass the selected tone to the parent component
//     }
//   };

//   return (
//     <div style={{ marginTop: '20px', textAlign: 'center' }}>
//       <input
//         type="text"
//         value={inputValue}
//         onChange={handleInputChange}
//         placeholder="Specify a tone"
//       />
//       <button onClick={handleButtonClick}>Submit</button>
//       {errorMessage && <p style={{ color: 'red' }}>{errorMessage}</p>}
//     </div>
//   );
// };

// export default ToneButton;



// import React, { useState } from 'react';

// const ToneText = () => {
//   const [inputValue, setInputValue] = useState('');
//   const [errorMessage, setErrorMessage] = useState('');

//   const handleInputChange = (event) => {
//     const inputText = event.target.value.trim();
//     setInputValue(inputText);
//     setErrorMessage('');
//   };

//   const handleInputBlur = () => {
//     // Validate if the input contains only one word
//     if (inputValue === '' || inputValue.split(' ').length > 1) {
//       setErrorMessage('Please enter only one word to specify your tone!');
//     }
//   };

//   const handleInputKeyPress = (event) => {
//     // Prevent the input from accepting spaces
//     if (event.key === ' ') {
//       event.preventDefault();
//     }
//   };

//   return (
//     <div style={{ marginTop: '20px', textAlign: 'center' }}>
//       <input
//         type="text"
//         value={inputValue}
//         onChange={handleInputChange}
//         onBlur={handleInputBlur}
//         onKeyPress={handleInputKeyPress}
//         placeholder="Specify a tone"
//         style={{ fontFamily: "Roboto, Helvetica, Arial, sans-serif" }}
//       />
//       {errorMessage && <p style={{ color: 'red' }}>{errorMessage}</p>}
//     </div>
//   );
// };

// export default ToneText;

import React, { useState } from 'react';

const ToneText = ({ onToneSubmit }) => {
  const [inputValue, setInputValue] = useState('');
  const [errorMessage, setErrorMessage] = useState('');

  const handleInputChange = (event) => {
    const inputText = event.target.value.trim();
    setInputValue(inputText);
    setErrorMessage('');
  };

  const handleInputBlur = () => {
    // Validate if the input contains only one word
    if (inputValue === '' || inputValue.split(' ').length > 1) {
      setErrorMessage('Please enter only one word to specify your tone!');
    }
  };

  const handleInputKeyPress = (event) => {
    // Prevent the input from accepting spaces
    if (event.key === ' ') {
      event.preventDefault();
    }
  };

  const handleButtonClick = () => {
    if (inputValue === '' || inputValue.split(' ').length > 1) {
      setErrorMessage('Please enter only one word to specify your tone!');
    } else {
      console.log('Entered word:', inputValue);
      onToneSubmit(inputValue); // Pass the selected tone to the parent component
    }
  };

  return (
    <div style={{ marginTop: '20px', textAlign: 'center' }}>
      <input
        type="text"
        value={inputValue}
        onChange={handleInputChange}
        onBlur={handleInputBlur}
        onKeyPress={handleInputKeyPress}
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