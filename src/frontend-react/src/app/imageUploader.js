// import React, { useCallback } from 'react';
// import { useDropzone } from 'react-dropzone';
// import { makeStyles, Paper, Typography } from '@material-ui/core';
// import axios from 'axios';

// const useStyles = makeStyles((theme) => ({
//   container: {
//     maxWidth: 600, // Set maximum width
//     margin: '0 auto', // Center the container
//   },
//   dropzone: {
//     display: 'flex',
//     flexDirection: 'column',
//     alignItems: 'center',
//     padding: theme.spacing(10),
//     borderWidth: 2,
//     borderRadius: 2,
//     marginTop: '20px',
//     borderColor: theme.palette.primary.main,
//     borderStyle: 'dashed',
//     backgroundColor: theme.palette.background.default,
//     color: theme.palette.text.primary,
//     outline: 'none',
//     transition: 'border .24s ease-in-out',
//     cursor: 'pointer',
//   },
// }));

// const ImageUploader = ({ onImageUpload }) => {
//   const classes = useStyles();

//   const onDrop = useCallback((acceptedFiles) => {
//     // Do something with the dropped files
//     if (acceptedFiles.length > 0) {
//       const image = acceptedFiles[0];
//       //const imgBase64 = await convertImageToBase64(file);
//       onImageUpload(image);
//     }
//   }, [onImageUpload]);

//   const { getRootProps, getInputProps, isDragActive } = useDropzone({
//     onDrop,
//     accept: 'image/*',
//   });

//   return (
//     <div className={classes.container}>
//       <div {...getRootProps()} className={classes.dropzone}>
//         <input {...getInputProps()} />
//         {isDragActive ? (
//           <Typography variant="h6">Drop the image here</Typography>
//         ) : (
//           <Typography variant="h6">Drag and drop an image here, or click to select one</Typography>
//         )}
//       </div>
//     </div>
//   );
// };

// export default ImageUploader;

// import React, { useCallback, useState } from 'react';
// import { useDropzone } from 'react-dropzone';
// import { makeStyles, Paper, Typography } from '@material-ui/core';
// import axios from 'axios';

// const useStyles = makeStyles((theme) => ({
//   container: {
//     maxWidth: 600, // Set maximum width
//     margin: '0 auto', // Center the container
//   },
//   dropzone: {
//     display: 'flex',
//     flexDirection: 'column',
//     alignItems: 'center',
//     padding: theme.spacing(10),
//     borderWidth: 2,
//     borderRadius: 2,
//     marginTop: '20px',
//     borderColor: theme.palette.primary.main,
//     borderStyle: 'dashed',
//     backgroundColor: theme.palette.background.default,
//     color: theme.palette.text.primary,
//     outline: 'none',
//     transition: 'border .24s ease-in-out',
//     cursor: 'pointer',
//   },
//   uploadedImage: {
//     maxWidth: '100%',
//     marginTop: theme.spacing(2),
//     borderRadius: theme.shape.borderRadius,
//   },
// }));

// const ImageUploader = ({ onImageUpload }) => {
//   const classes = useStyles();
//   const [uploadedImage, setUploadedImage] = useState(null);

//   const onDrop = useCallback(async (acceptedFiles) => {
//     // Do something with the dropped files
//     if (acceptedFiles.length > 0) {
//       const image = acceptedFiles[0];
//       //const imgBase64 = await convertImageToBase64(image);
//       setUploadedImage(image);
//       onImageUpload(image);
//     }
//   }, [onImageUpload]);

//   const { getRootProps, getInputProps, isDragActive } = useDropzone({
//     onDrop,
//     accept: 'image/*',
//   });

//   return (
//     <div className={classes.container}>
//       <div {...getRootProps()} className={classes.dropzone}>
//         <input {...getInputProps()} />
//         {uploadedImage ? (
//           <img src={uploadedImage} alt="Uploaded" className={classes.uploadedImage} />
//         ) : isDragActive ? (
//           <Typography variant="h6">Drop the image here</Typography>
//         ) : (
//           <Typography variant="h6">Drag and drop an image here, or click to select one</Typography>
//         )}
//       </div>
//     </div>
//   );
// };

// // const convertImageToBase64 = (image) => {
// //   return new Promise((resolve, reject) => {
// //     const reader = new FileReader();
// //     reader.onloadend = () => {
// //       resolve(reader.result.split(',')[1]);
// //     };
// //     reader.onerror = (error) => {
// //       reject(error);
// //     };
// //     reader.readAsDataURL(image);
// //   });
// // };

// export default ImageUploader;


// import React, { useCallback } from 'react';
// import { useDropzone } from 'react-dropzone';
// import { makeStyles, Paper, Typography } from '@material-ui/core';
// import axios from 'axios';

// const useStyles = makeStyles((theme) => ({
//   dropzone: {
//     display: 'flex',
//     flexDirection: 'column',
//     alignItems: 'center',
//     padding: theme.spacing(2),
//     borderWidth: 2,
//     borderRadius: 2,
//     borderColor: theme.palette.primary.main,
//     borderStyle: 'dashed',
//     backgroundColor: theme.palette.background.default,
//     color: theme.palette.text.primary,
//     outline: 'none',
//     transition: 'border .24s ease-in-out',
//     cursor: 'pointer',
//     margin: '20px'
//   },
// }));

// const ImageUploader = ({ onImageUpload }) => {
//   const classes = useStyles();

//   const onDrop = useCallback(async (acceptedFiles) => {
//     // Do something with the dropped files
//     if (acceptedFiles.length > 0) {
//       const image = acceptedFiles[0];

//       // Convert the image to Base64
//       const imgBase64 = await convertImageToBase64(image);

//       // Call the API to get the caption
//       const caption = await sendImageToAPI(imgBase64);

//       // Pass the image and caption to the parent component
//       onImageUpload({ image, caption });
//     }
//   }, [onImageUpload]);

//   const { getRootProps, getInputProps, isDragActive } = useDropzone({
//     onDrop,
//     accept: 'image/*',
//   });

//   const convertImageToBase64 = (file) => {
//     return new Promise((resolve) => {
//       const reader = new FileReader();
//       reader.onloadend = () => {
//         resolve(reader.result.split(',')[1]);
//       };
//       reader.readAsDataURL(file);
//     });
//   };

//   const sendImageToAPI = async (imgBase64) => {
//     // Replace with the actual URL of your FastAPI server
//     const apiUrl = 'http://localhost:9000/generate_caption/';

//     try {
//       const response = await fetch(apiUrl, {
//         method: 'POST',
//         headers: {
//           'Content-Type': 'application/json',
//         },
//         body: JSON.stringify({ image: imgBase64 }),
//       });

//       if (response.ok) {
//         const result = await response.json();
//         return result.caption;
//       } else {
//         console.error('Error:', response.statusText);
//         return null;
//       }
//     } catch (error) {
//       console.error('Error:', error.message);
//       return null;
//     }
//   };

//   return (
//     <div {...getRootProps()} className={classes.dropzone}>
//       <input {...getInputProps()} />
//       {isDragActive ? (
//         <Typography variant="h6">Drop the image here</Typography>
//       ) : (
//         <Typography variant="h6">Drag and drop an image here, or click to select one</Typography>
//       )}
//     </div>
//   );
// };

// export default ImageUploader;

// dk
import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { makeStyles, Typography } from '@material-ui/core';

const useStyles = makeStyles((theme) => ({
  container: {
    maxWidth: 600, // Set maximum width
    margin: '0 auto', // Center the container
  },
  dropzone: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    padding: theme.spacing(10),
    borderWidth: 2,
    borderRadius: 2,
    marginTop: '20px',
    borderColor: theme.palette.primary.main,
    borderStyle: 'dashed',
    backgroundColor: theme.palette.background.default,
    color: theme.palette.text.primary,
    outline: 'none',
    transition: 'border .24s ease-in-out',
    cursor: 'pointer',
  },
  uploadedImage: {
    maxWidth: '100%',
    marginTop: theme.spacing(2),
    borderRadius: theme.shape.borderRadius,
  },
  centeredText: {
    textAlign: 'center',
  },
}));

const ImageUploader = ({ onImageUpload }) => {
  const classes = useStyles();
  const [uploadedImage, setUploadedImage] = useState(null);
  const [errorMessage, setErrorMessage] = useState('');

  const onDrop = useCallback((acceptedFiles) => {
    if (acceptedFiles.length > 0) {
      const image = acceptedFiles[0];

      // Check if the file type is JPEG
      if (image.type === 'image/jpeg') {
        setUploadedImage(URL.createObjectURL(image));
        onImageUpload(image);
        setErrorMessage('');
      } else {
        // Clear the uploaded image and display an error message for invalid file type
        setUploadedImage(null);
        onImageUpload(null);
        setErrorMessage('Invalid file type. Please upload a JPEG image.');
      }
    }
  }, [onImageUpload]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: 'image/jpeg',
  });

  return (
    <div className={`${classes.container} ${classes.centeredText}`}>
      <div {...getRootProps()} className={classes.dropzone}>
        <input {...getInputProps()} />
        {uploadedImage ? (
          <img src={uploadedImage} alt="Uploaded" className={classes.uploadedImage} />
        ) : isDragActive ? (
          <Typography variant="h6">Drop the JPEG image here</Typography>
        ) : (
          <>
            <Typography variant="h6">Drag and drop a JPEG image here, or click to select one</Typography>
            {errorMessage && <p style={{ color: 'red' }}>{errorMessage}</p>}
          </>
        )}
      </div>
    </div>
  );
};

export default ImageUploader;
