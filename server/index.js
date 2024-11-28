const express = require('express');
const multer = require('multer');
const { isEyeOpen } = require('../isEyeOpen');

const app = express();

// Set up multer storage options
const storage = multer.memoryStorage(); // Store file in memory as a binary buffer
const upload = multer({ storage });

// Define a route to handle the POST request with form-data
app.post('/isEyesOpen', upload.single('image'), (req, res) => {
  // The uploaded file will be available in req.file
  if (!req.file) {
    return res.status(400).send('No file uploaded');
  }

  // To read the binary data
  const imageBinary = req.file.buffer;

  isEyeOpen(imageBinary, 0.23)
    .then((result) => {
      res.send(`Are the eyes open? ${result}`);
    })
    .catch((error) => {
      res.status(500).send(error.message);
    });
});

app.listen(3000, () => {
  console.log('Server is running on port 3000');
});
