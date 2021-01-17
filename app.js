const express = require("express");
const bodyParser = require("body-parser");
const path = require('path');
const env = require("dotenv");
const ejs = require("ejs");


const http = require("http");
const app = express();

// get environment variables from .env file (use process.env to access)
env.config();
const port = process.env.PORT || 8080;

app.use(express.static(path.join(__dirname, 'public')));
app.use(bodyParser.urlencoded({extended: false}));
app.use(bodyParser.json());



// no longer need to specify .ejs file extension
app.set("view engine", "ejs");
app.set('views', path.join(__dirname, 'views'));


app.get('/main', function(req, res){
    // var info = dropbase.get(req.session.username);
  res.render("main.ejs", {info: info});
});

app.get('/', function(req, res){
  res.render("signup.ejs");
});

app.post('/checklogin', function(req, res){
  res.redirect('/main');
});


//app.listen(port, () => console.log(`Server listening on port ${port}`));
app.listen(port);