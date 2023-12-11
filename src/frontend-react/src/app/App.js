import React, { useState } from 'react';
import { BrowserRouter as Router } from 'react-router-dom';
import {
  ThemeProvider,
  CssBaseline
} from '@material-ui/core';
import './App.css';
import { Button } from '@material-ui/core';
import Content from "../common/Content";
import Header from "../common/Header";
import Footer from "../common/Footer";
import Theme from "./Theme";
import ImageUploader from './imageUploader';
import ToneText from './ToneText';
import AudienceDropDown from './audienceDropDown';
import GenerateButton from './generateButton';
import axios from 'axios';
import CircularProgress from '@material-ui/core/CircularProgress';

const App = () => {
  // state to store data from each component
  const [inputValue, setInputValue] = useState('');
  const [uploadedImage, setUploadedImage] = useState(null);
  const [selectedAudience, setSelectedAudience] = useState('');
  const [generatedCaption, setGeneratedCaption] = useState('');
  const [loading, setLoading] = useState(false);
  // const [buttonText, setButtonText] = useState('Copy Caption');

  // function to handle tone submission
  const handleToneSubmit = (tone) => {
    // set tone
    setInputValue(tone);
  };

  // function to handle image upload
  const handleImageUpload = (image) => {
    // set image
    setUploadedImage(image);
  };

  // function to handle audience selection
  const handleAudienceSelect = (audience) => {
    // set audience
    setSelectedAudience(audience);
  };

  // function to send request to FastAPI
  const handleGenerateClick = () => {
    // create input
    const formData = new FormData();
    formData.append('image', uploadedImage);
    formData.append('tone', inputValue);
    formData.append('audience', selectedAudience);

    // start buffer icon
    setLoading(true);

    // send API request
    axios.post('/api/generate_caption', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
      .then(response => {
        setLoading(false);
        setGeneratedCaption(response.data.caption);
      })
      .catch(error => {
        setLoading(false);
        console.error('Error generating caption:', error.response.data);
      });
  };

  // function for copying caption
  // const handleCopyClick = () => {
  //   if (generatedCaption) {
  //     navigator.clipboard.writeText(generatedCaption)
  //       .then(() => {
  //         console.log('Caption copied to clipboard');
  //         setButtonText('Copied!');
  //       })
  //       .catch((error) => {
  //         console.error('Error copying to clipboard:', error);
  //       });
  //   } else {
  //     console.error('No generated caption to copy.');
  //   }
  // };



  // Build App
  let view = (
    <React.Fragment>
      <CssBaseline />
      <ThemeProvider theme={Theme}>
        <Router basename="/">
          <Header />
          <Content>
            {/* Use the ImageUploader component and pass the onImageUpload prop */}
            <ImageUploader onImageUpload={handleImageUpload} />
            {/* Tone text*/}
            <ToneText onToneSubmit={handleToneSubmit} />
            {/* Adding the audience dropdown */}
            <AudienceDropDown onSelectOption={handleAudienceSelect} />
            {/* Adding the generate button and passing the onGenerateClick prop */}
            {loading && <CircularProgress style={{ display: 'block', margin: '20px auto' }} />}
            <GenerateButton onClick={handleGenerateClick} />
            {generatedCaption && (
              <div style={{ textAlign: 'center', marginTop: '20px' }}>
                <p
                  style={{
                    fontSize: '25px',
                    fontWeight: 'bold',
                    fontFamily: "Roboto, Helvetica, Arial, sans-serif",
                    maxWidth: 600,
                    margin: '0 auto',
                  }}
                >
                  Generated Caption:<br /> {generatedCaption}
                </p>
                {/* <Button onClick={handleCopyClick} variant="contained" color="primary" style={{ marginTop: '10px' }}>
                  {buttonText}
                </Button> */}
              </div>
            )}
          </Content>
          <Footer />
        </Router>
      </ThemeProvider>
    </React.Fragment>
  );

  // Return View
  return view;
};

@app.get("/status")
async def get_api_status():
    return {
        "version": "2.1",
        // "tf_version": tf.__version__,
    }

export default App;