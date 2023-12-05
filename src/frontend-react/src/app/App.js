// // import React from 'react';
// // import { BrowserRouter as Router } from 'react-router-dom';
// // import {
// //   ThemeProvider,
// //   CssBaseline
// // } from '@material-ui/core';
// // import './App.css';
// // import Content from "../common/Content";
// // import Header from "../common/Header";
// // import Footer from "../common/Footer";
// // import Theme from "./Theme";
// // import ImageUploader from './imageUploader';
// // import imageUploader from "../components/imageUploader"

// // // import AppRoutes from "./AppRoutes";
// // // import DataService from '../services/DataService';


// // const App = (props) => {

// //   console.log("================================== App ======================================");

// //   // // Init Data Service
// //   // DataService.Init();
// //   const handleImageUpload = (image) => {
// //     // Here you can perform any logic related to image upload
// //     console.log("Image uploaded:", image);

// //     // You can call the necessary functions to send the image to your backend
// //     // For simplicity, let's assume there's a function `sendImageToBackend` in DataService
// //     // DataService.sendImageToBackend(image);
// //   };

// //   // Build App
// //   let view = (
// //     <React.Fragment>
// //       <CssBaseline />
// //       <ThemeProvider theme={Theme}>
// //         <Router basename="/">
// //           <Header></Header>
// //           <Content>
// //             {/* Use the ImageUploader component */}
// //             <ImageUploader onImageUpload={handleImageUpload} />
// //             <imageUploader />


// //           </Content>
// //           <Footer></Footer>
// //         </Router>
// //       </ThemeProvider>
// //     </React.Fragment>
// //   )

// //   // Return View
// //   return view
// // }

// // export default App;



// // import React from 'react';
// // import { BrowserRouter as Router } from 'react-router-dom';
// // import {
// //   ThemeProvider,
// //   CssBaseline
// // } from '@material-ui/core';
// // import './App.css';
// // import Content from "../common/Content";
// // import Header from "../common/Header";
// // import Footer from "../common/Footer";
// // import Theme from "./Theme";
// // import ImageUploader from './imageUploader';
// // import ToneText from './ToneText';
// // import AudienceDropDown from './audienceDropDown';


// // const App = () => {
// //   console.log("================================== App ======================================");

// //   const handleImageUpload = (image) => {
// //     // Here you can perform any logic related to image upload
// //     console.log("Image uploaded:", image);

// //     // You can call the necessary functions to send the image to your backend
// //     // For simplicity, let's assume there's a function `sendImageToBackend` in DataService
// //     // DataService.sendImageToBackend(image);
// //   };

// //   // Build App
// //   let view = (
// //     <React.Fragment>
// //       <CssBaseline />
// //       <ThemeProvider theme={Theme}>
// //         <Router basename="/">
// //           <Header />
// //           <Content>
// //             {/* Use the ImageUploader component and pass the onImageUpload prop */}
// //             <ImageUploader onImageUpload={handleImageUpload} />
// //             {/* Tone text*/}
// //             <ToneText />
// //             {/* Adding the audience dropdown */}
// //             <AudienceDropDown />
// //           </Content>
// //           <Footer />
// //         </Router>
// //       </ThemeProvider>
// //     </React.Fragment>
// //   )

// //   // Return View
// //   return view
// // }

// // export default App;

// // App.js

// import React, { useState } from 'react';
// import { BrowserRouter as Router } from 'react-router-dom';
// import {
//   ThemeProvider,
//   CssBaseline
// } from '@material-ui/core';
// import './App.css';
// import Content from "../common/Content";
// import Header from "../common/Header";
// import Footer from "../common/Footer";
// import Theme from "./Theme";
// import ImageUploader from './imageUploader';
// import ToneText from './ToneText';
// import AudienceDropDown from './audienceDropDown';

// const processImage = async (image) => {
//   try {
//     // Implement your image processing logic here
//     // For example, you might want to convert the image to base64
//     const base64Image = await convertImageToBase64(image);
//     return base64Image;
//   } catch (error) {
//     console.error('Error processing image:', error);
//     return null;
//   }
// };

// const convertImageToBase64 = (image) => {
//   return new Promise((resolve, reject) => {
//     const reader = new FileReader();
//     reader.onloadend = () => {
//       resolve(reader.result.split(',')[1]);
//     };
//     reader.onerror = (error) => {
//       reject(error);
//     };
//     reader.readAsDataURL(image);
//   });
// };

// const App = () => {
//   const [selectedAudience, setSelectedAudience] = useState('');
//   const [uploadedImage, setUploadedImage] = useState(null);
//   const [submittedTone, setSubmittedTone] = useState('');

//   // const handleImageUpload = async (image) => {
//   //   try {
//   //     // Process the image and obtain the tone and audience values
//   //     const processedImage = await processImage(image);

//   //     // Call the FastAPI endpoint to generate the caption
//   //     const response = await fetch('http://localhost:9000/generate_caption/', {
//   //       method: 'POST',
//   //       headers: {
//   //         'Content-Type': 'application/json',
//   //         'Accept': 'application/json',
//   //       },
//   //       body: JSON.stringify({
//   //         image: processedImage,
//   //         tone: submittedTone,
//   //         audience: selectedAudience,
//   //       }),
//   //     });

//   //     if (response.ok) {
//   //       const result = await response.json();
//   //       console.log('Caption:', result.caption);
//   //       // Update your React state or UI with the obtained caption
//   //     } else {
//   //       console.error('Failed to generate caption');
//   //     }
//   //   } catch (error) {
//   //     console.error('Error during image upload:', error);
//   //   }
//   // };

//   const handleImageUpload = async (image) => {
//     try {
//       // Process the image and obtain the tone and audience values
//       const processedImage = await processImage(image);

//       // Set the uploaded image in the state
//       setUploadedImage(URL.createObjectURL(image));

//       // Call the FastAPI endpoint to generate the caption
//       const response = await fetch('http://localhost:9000/generate_caption/', {
//         method: 'POST',
//         headers: {
//           'Content-Type': 'application/json',
//           'Accept': 'application/json',
//         },
//         body: JSON.stringify({
//           image: processedImage,
//           tone: submittedTone,
//           audience: selectedAudience,
//         }),
//       });

//       if (response.ok) {
//         const result = await response.json();
//         console.log('Caption:', result.caption);
//         // Update your React state or UI with the obtained caption
//       } else {
//         console.error('Failed to generate caption');
//       }
//     } catch (error) {
//       console.error('Error during image upload:', error);
//     }
//   };

//   const handleToneSubmit = (tone) => {
//     // Store the submitted tone in the state
//     setSubmittedTone(tone);
//   };

//   return (
//     <React.Fragment>
//       <CssBaseline />
//       <ThemeProvider theme={Theme}>
//         <Router basename="/">
//           <Header />
//           <Content>
//             {/* Display the uploaded image */}
//             {uploadedImage && (
//               <img src={uploadedImage} alt="Uploaded" style={{ maxWidth: '100%' }} />
//             )}

//             <ImageUploader onImageUpload={handleImageUpload} />
//             <ToneText onToneSubmit={handleToneSubmit} />
//             <AudienceDropDown onSelectOption={setSelectedAudience} />
//           </Content>
//           <Footer />
//         </Router>
//       </ThemeProvider>
//     </React.Fragment>
//   );
// }

// export default App;

// import React, { useState } from 'react';
// import { BrowserRouter as Router } from 'react-router-dom';
// import { ThemeProvider, CssBaseline } from '@material-ui/core';
// import './App.css';
// import Content from "../common/Content";
// import Header from "../common/Header";
// import Footer from "../common/Footer";
// import Theme from "./Theme";
// import ImageUploader from './imageUploader';
// import ToneText from './ToneText';
// import AudienceDropDown from './audienceDropDown';

// const App = () => {
//   const [selectedAudience, setSelectedAudience] = useState('');
//   const [submittedTone, setSubmittedTone] = useState('');

//   const handleImageUpload = async (image) => {
//     try {
//       const processedImage = await processImage(image);

//       const response = await fetch('http://localhost:9000/generate_caption/', {
//         method: 'POST',
//         headers: {
//           'Content-Type': 'application/json',
//           'Accept': 'application/json',
//         },
//         body: JSON.stringify({
//           image: processedImage,
//           tone: submittedTone,
//           audience: selectedAudience,
//         }),
//       });

//       if (response.ok) {
//         const result = await response.json();
//         console.log('Caption:', result.caption);
//         // Update your React state or UI with the obtained caption
//       } else {
//         console.error('Failed to generate caption');
//       }
//     } catch (error) {
//       console.error('Error during image upload:', error);
//     }
//   };

//   const handleToneSubmit = (tone) => {
//     setSubmittedTone(tone);
//   };

//   return (
//     <React.Fragment>
//       <CssBaseline />
//       <ThemeProvider theme={Theme}>
//         <Router basename="/">
//           <Header />
//           <Content>
//             <ImageUploader onImageUpload={handleImageUpload} />
//             <ToneText onToneSubmit={handleToneSubmit} />
//             <AudienceDropDown onSelectOption={setSelectedAudience} />
//           </Content>
//           <Footer />
//         </Router>
//       </ThemeProvider>
//     </React.Fragment>
//   );
// };

// const processImage = async (image) => {
//   try {
//     const base64Image = await convertImageToBase64(image);
//     return base64Image;
//   } catch (error) {
//     console.error('Error processing image:', error);
//     return null;
//   }
// };

// const convertImageToBase64 = (image) => {
//   return new Promise((resolve, reject) => {
//     const reader = new FileReader();
//     reader.onloadend = () => {
//       resolve(reader.result.split(',')[1]);
//     };
//     reader.onerror = (error) => {
//       reject(error);
//     };
//     reader.readAsDataURL(image);
//   });
// };

// export default App;
import React, { useState } from 'react';
import { BrowserRouter as Router } from 'react-router-dom';
import { ThemeProvider, CssBaseline } from '@material-ui/core';
import './App.css';
import Content from "../common/Content";
import Header from "../common/Header";
import Footer from "../common/Footer";
import Theme from "./Theme";
import ImageUploader from './imageUploader';
import ToneText from './ToneText';
import AudienceDropDown from './audienceDropDown';

const App = () => {
  const [selectedAudience, setSelectedAudience] = useState('');
  const [submittedTone, setSubmittedTone] = useState('');

  const handleImageUpload = async (image) => {
    try {
      const response = await fetch('http://localhost:9000/generate_caption/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        body: JSON.stringify({
          image: image,  // Directly use the image without processing
          tone: submittedTone,
          audience: selectedAudience,
        }),
      });

      if (response.ok) {
        const result = await response.json();
        console.log('Caption:', result.caption);
        // Update your React state or UI with the obtained caption
      } else {
        console.error('Failed to generate caption');
      }
    } catch (error) {
      console.error('Error during image upload:', error);
    }
  };

  const handleToneSubmit = (tone) => {
    setSubmittedTone(tone);
  };

  return (
    <React.Fragment>
      <CssBaseline />
      <ThemeProvider theme={Theme}>
        <Router basename="/">
          <Header />
          <Content>
            <ImageUploader onImageUpload={handleImageUpload} />
            <ToneText onToneSubmit={handleToneSubmit} />
            <AudienceDropDown onSelectOption={setSelectedAudience} />
          </Content>
          <Footer />
        </Router>
      </ThemeProvider>
    </React.Fragment>
  );
};

export default App;
