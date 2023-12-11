// component for the generate caption button

import React from 'react';
import Button from '@material-ui/core/Button';

const GenerateButton = ({ onClick }) => {
  return (
    <div style={{ marginTop: '20px', textAlign: 'center' }}>
      <Button
        variant="contained"
        color="primary"
        onClick={onClick}
        style={{
          fontFamily: "Roboto, Helvetica, Arial, sans-serif",
          fontSize: '18px',
          padding: '10px',
        }}
      >
        Generate caption
      </Button>
    </div>
  );
};

export default GenerateButton;

