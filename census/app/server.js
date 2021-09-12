'use strict';
const express = require('express');
var bodyParser = require('body-parser');
const config = require('./server/config').config;
const Connection = require('./server/config').Connection;
const utility = require('./server/utility');
const attributes = require('./server/attributes');
const auth = require('./server/auth');
// Constants
const PORT = 8080;
const HOST = '0.0.0.0';

// App
const app = express();
app.use(express.static("./client/public"))
app.use(bodyParser.json())
app.use(bodyParser.urlencoded({
  extended: true
}))
let db;

async function main(){
  console.log("test")
  db = await Connection();
}



app.get('/test', async (req, res) => {
  res.send('no i chuj');
  const reso = await utility.validate_email("test@test.pl")
});

app.post('/api/census/auth', auth.authenticateJWT ,async (req,res)=>{
  res.send("Działa, Alles gut")
  console.log(Connection())
})

app.post('/api/census/login', auth.login);

app.post('/api/census/attrib/add', auth.authenticateJWT, attributes.add)

app.listen(PORT, HOST);
console.log(`Running on http://${HOST}:${PORT}`);

main();