const express = require("express");
const bodyParser = require("body-parser");
const path = require('path');
const env = require("dotenv");
const ejs = require("ejs");
const request = require("request");


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


app.get('/main', function(req, res) {
    const select = "title,acronym,status,conditionsabbrev,interventionabbrev,phases,location,distance,time,url,inclusioncrit,exclusioncrit,age,contactname,contactphone,contactaddress,contactemail,enrollment,longitude,latitude";
    const gender = req.query.gender || 'in.(Male,All)';
    const age = req.query.age || 'phfts.{Adult}';
    const conditions = req.query.conditions || 'neq.null';
    const phases = req.query.phases || 'neq.null';
    console.log(select, gender);
    const url = 'https://query.dropbase.io/guFdPgANE2WEhqhVw4kCeP/cc?select=' + select + '&gender=' + gender + '&age=' + age + '&conditionsabbrev=' + conditions + '&phases=' + phases + '&order=distance.nullsfirst' + '&limit=300';
    console.log("URL: " + url);
    request({
        url: url,
        headers: {
            'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhYmFzZUlkIjoiZ3VGZFBnQU5FMldFaHFoVnc0a0NlUCIsImFjY2Vzc1Blcm0iOiJmdWxsIiwidG9rZW5JZCI6IkhGWElmWGIwRmhDNUpETVhsbVNUeDNMb0lxN3RlZGM3VUN2Z3A0NVd1clZRbUpmdFhGWm5YN1JsNDNFZTVWNDEiLCJpYXQiOjE2MTA4NTIyODIsImV4cCI6MTYxMTAyNTA4MiwiaXNzIjoiZHJvcGJhc2UuaW8iLCJzdWIiOiJCQkJkRmZ4b3hpeEtBM1d2RFhaYTVlIn0.osNKNhoSDyYieDCRFZwg7vExKY6vfvHNuvO-62UejWY'
        },
        rejectUnauthorized: false
    }, function (err, response, body) {
        if (err) {
            console.log(err);
        } else {
            console.log("Response " + response.statusCode);
            console.log(JSON.parse(body));
            const clinics = JSON.parse(body);
            res.render("main.ejs", {studies: clinics});
        }
    });
  
});

app.get('/', function(req, res){
  res.render("login.ejs");
});

app.get('/signup', function(req,res){
    res.render("signup.ejs")
});


app.post('/checklogin', function(req, res){
  res.redirect('/main');
});


//app.listen(port, () => console.log(`Server listening on port ${port}`));
app.listen(port);