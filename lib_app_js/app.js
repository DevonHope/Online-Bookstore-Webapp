//const db = require('../db');
const express = require('express');
const requestModule = require('request');
const { Pool, Client } = require('pg');
//const connectionString = 'postgres://postgres:popeey@localhost:5432/Bookstore';
/*
const client = new Client({
  connectionString:connectionString
});*/
const pool = new Pool({
  user: "postgres",
  host: "localhost",
  database: "Bookstore",
  schema: "allops",
  password: "popeey",
  port: "5432"
});
const client = new Client({
  user: "postgres",
  host: "localhost",
  database: "Bookstore",
  schema: "allops",
  password: "popeey",
  port: "5432"
});

/*
client.connect();
console.log(client);
client.query()
//http://127.0.0.1:49957/?key=31710029-138c-43b6-8976-d9f8a0d7d78d
*/
var app = express();
app.use(express.static(__dirname + '/static'));
app.set('port',process.env.PORT || 4000);
app.set('view engine', 'ejs');

app.get('/',(request,response) => {
  response.sendFile(__dirname + '/html/index.html');
});

app.get('/showSignUp',(request,response) => {
  response.sendFile(__dirname + '/html/signup.html');
});

app.get('/showSearch', function(req,res) {
  console.log(req);
  //pool.query(req, )
});

app.get('/newBooks',function(req,res) {

    client.connect(function(err){
        if(err)
            throw err;

        var query = "select * from allops.book";

        client.query(query,function(err,result){
            if(err)
                throw err;
            else {
                 res.render('book.ejs', { book: result });
            }
        });
    });
});

app.get('/allbooks', function (req, res, next) {
  pool.query("select * from allops.book",(err, res) => {
    console.log(res.rows[0]);
  });
  /*
  client.query('SELECT * FROM allops.user', [1], function(err, result){
    if(err){
      console.log(err);
      res.status(400).send(err);
    }
    console.log(result)
    res.status(200).send(result.rows);
  });*/
});

app.listen(4000, function() {
  console.log('Server is running on port 4000');
});
