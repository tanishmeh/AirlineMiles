const express = require('express');
const fs = require('fs');
const path = require('path');
const app = express();
const PORT = 3000;

app.use(express.static(path.join(__dirname, 'public')));

app.get('/flights', (req, res) => {
  res.sendFile(path.join(__dirname, 'AANonstop.json'));
});

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
