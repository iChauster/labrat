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
    var select = req.query.select || "title";
    var gender = req.query.gender || 'in.(Male)';
    var acronym = req.query.acronym || '';
    var conditions = req.query.conditions || [];
    // var status = req.query.status || ;
    // var age = req.query.age || ;
    console.log(select, gender);
    request({
        url: 'https://query.dropbase.io/guFdPgANE2WEhqhVw4kCeP/labrat?select=' + select + '&gender=' + gender + '&acronym&interventions&location&distance',
        headers: {
            'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhYmFzZUlkIjoiZ3VGZFBnQU5FMldFaHFoVnc0a0NlUCIsImFjY2Vzc1Blcm0iOiJmdWxsIiwidG9rZW5JZCI6IkhGWElmWGIwRmhDNUpETVhsbVNUeDNMb0lxN3RlZGM3VUN2Z3A0NVd1clZRbUpmdFhGWm5YN1JsNDNFZTVWNDEiLCJpYXQiOjE2MTA4NTIyODIsImV4cCI6MTYxMTAyNTA4MiwiaXNzIjoiZHJvcGJhc2UuaW8iLCJzdWIiOiJCQkJkRmZ4b3hpeEtBM1d2RFhaYTVlIn0.osNKNhoSDyYieDCRFZwg7vExKY6vfvHNuvO-62UejWY'
        },
        rejectUnauthorized: false
    }, function (err, response, body) {
        if (err) {
            console.log(err);
        } else {
            console.log("Response " + response);
            console.log(JSON.parse(body));
            res.render("main.ejs");
        }
    });
  
});

app.get('/', function(req, res){
  res.render("signup.ejs");
});

app.post('/checklogin', function(req, res){
  res.redirect('/main?select=title&gender=in.(Male)');
});


//app.listen(port, () => console.log(`Server listening on port ${port}`));
app.listen(port);