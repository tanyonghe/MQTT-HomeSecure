var express = require('express');
var app = express();

app.use(express.static('public'));

app.get('/', function (req, res) {
  res.sendfile('index.html');
});

app.get('/formSubmission', function (req, res) {
  if (req.query.uname === 'admin' && req.query.psw === 'cs3103rocks') {
    res.redirect('dashboard.html');
  } else {
    res.redirect('index.html');
  }
});

app.listen(3000, function(){
  console.log("Listening on port 3000!")
});