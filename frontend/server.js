// server.js
const { createServer } = require('http');  // Change 'https' to 'http'
const { parse } = require('url');
const next = require('next');

const dev = process.env.NODE_ENV !== 'production';
const app = next({ dev });
const handle = app.getRequestHandler();


//app.prepare().then(() => {

  //const port = 3001;
  //createServer((req, res) => {  
    //const parsedUrl = parse(req.url, true);
    //handle(req, res, parsedUrl);
  //}).listen(port, (err) => {
    //if (err) throw err;
    //console.log(`> Server running on http://localhost:${port}`);  
  //});
//});

app.prepare().then(() => {
  const port = 3001;
  const host = "127.0.0.1"
  createServer((req, res) => {  
    const parsedUrl = parse(req.url, true);
    handle(req, res, parsedUrl);
  }).listen(port, host, (err) => {
    if (err) throw err;
    console.log(`> Server running on http://${host}:${port}`);  
  });
});
