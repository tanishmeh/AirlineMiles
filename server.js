const express = require('express');
const {exec} = require('child_process');
const fs = require('fs');
const cors = require('cors');
const path = require('path');
const app = express();
const PORT = 3000;

const venvPath = '/Users/tanishmehta/Desktop/Projects/AirlineMiles/venv/bin/python';

// Use express.json() to parse JSON bodies into JS objects
app.use(express.json());

// Use cors to allow cross-origin requests
app.use(cors());

app.use(express.static(path.join(__dirname, 'public')));

app.use(express.urlencoded({ extended: true }));

app.post('/AAOneWayFINAL', (req, res) => {
  const { from, to, date1, date2 } = req.body;
  exec(`${venvPath} AAOneWayFINAL.py ${from} ${to} ${date1} ${date2}`, (error, stdout, stderr) => {
    if (error) {
      console.error(`exec error: ${error}`);
      res.status(500).json({ message: "Error executing script" });
      return;
    }
    console.log(`stdout: ${stdout}`);
    console.error(`stderr: ${stderr}`);
  });
  console.log('Data received and Python script executed.');
  res.json({ message: "Data received and Python script executed." });
});

app.get('/flights', (req, res) => {
  const filePath = path.join(__dirname, 'AANonstop.json');

  function checkFileExistsAndNotEmpty() {
    fs.access(filePath, fs.constants.F_OK, (err) => {
      if (err) {
        // File does not exist yet, wait for a bit then check again
        console.log('File not found. Waiting...');
        setTimeout(checkFileExistsAndNotEmpty, 1000); // Check again after 1 second
      } else {
        // File exists, now check if it's not empty
        fs.stat(filePath, (err, stats) => {
          if (err) {
            console.log('Error getting file stats.');
            res.status(500).send('Error checking file');
          } else if (stats.size === 0) {
            // File is empty, wait for a bit then check again
            console.log('File is empty. Waiting...');
            setTimeout(checkFileExistsAndNotEmpty, 1000); // Check again after 1 second
          } else {
            // File exists and is not empty, send it in the response
            res.sendFile(filePath);
          }
        });
      }
    });
  }
  checkFileExistsAndNotEmpty();
});

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
