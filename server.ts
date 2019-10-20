import express from 'express';

const app = express();

app.get('/heartbeat', (req, res) => {
  res.send('I am good')
})

app.get('reddit-redirect', (req, res) => {
  res.send('OAuth worked')
})

app.listen(3333);
