import React, { useState } from 'react';

const AudienceDropDown = ({ onSelectOption }) => {
  const [selectedOption, setSelectedOption] = useState('');

  const handleOptionChange = (event) => {
    setSelectedOption(event.target.value);
    onSelectOption(event.target.value);
  };

  return (
    <div style={{ display: 'flex', justifyContent: 'center', marginTop: '20px' }}>
      <select
        value={selectedOption}
        onChange={handleOptionChange}
        style={{
          fontFamily: "Roboto, Helvetica, Arial, sans-serif",
          fontSize: '18px',
          padding: '10px',
        }}
      >
        <option value="">Select your audience</option>
        <option value="personal">Personal</option>
        <option value="promotional">Promotional</option>
        <option value="academic">Academic</option>
      </select>
    </div>
  );
};

export default AudienceDropDown;
