//const db = require('../db');
const express = require('express');
const requestModule = require('request');
const router = express.Router();
const { Pool, Client } = require('pg');

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

var app = express();
app.use(express.static(__dirname + '/static'));
app.set('port',process.env.PORT || 4000);
app.set('view engine', 'pug');

/*
const data = {text: req.body.text, complete: false};
// SQL Query > Insert Data
client.query('INSERT INTO items(text, complete) values($1, $2)',
[data.text, data.complete]);
*/

app.get('/',(request,response) => {
  response.render('index');
});

app.get('/showSignUp',(request,response) => {
  response.sendFile(__dirname + '/html/signup.html');
});

app.get('/showSearch', function(req,res) {
  console.log(req);
  pool.connect(function(err){
      if(err){
          done();
          console.log(err);
          return res.status(500).json({succuss: false, data: err});
      }

      var query = "select * from allops.book where bk_name = [$1]";
      pool.query(query,function(err,result){
          if(err)
              throw err;
          else {
               res.render('search', { search: result });
          }
      });
  });
  //pool.query(req, )
});

app.get('/',function(req,res) {
    pool.connect(function(err){
        if(err){
            done();
            console.log(err);
            return res.status(500).json({succuss: false, data: err});
        }

        var query = "select * from allops.book";
        pool.query(query,function(err,result){
            if(err)
                throw err;
            else {
                 res.render('index', { books: result });
            }
        });
    });
});

app.get('/allbooks', function (req, res, next) {
  pool.query("select * from allops.book",(err, res) => {
    console.log(res.rows[0].bk_name);
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
/* DELETE*/
/*
router.delete('/api/v1/todos/:todo_id', (req, res, next) => {
  const results = [];
  // Grab data from the URL parameters
  const id = req.params.todo_id;
  // Get a Postgres client from the connection pool
  pg.connect(connectionString, (err, client, done) => {
    // Handle connection errors
    if(err) {
      done();
      console.log(err);
      return res.status(500).json({success: false, data: err});
    }
    // SQL Query > Delete Data
    client.query('DELETE FROM items WHERE id=($1)', [id]);
    // SQL Query > Select Data
    var query = client.query('SELECT * FROM items ORDER BY id ASC');
    // Stream results back one row at a time
    query.on('row', (row) => {
      results.push(row);
    });
    // After all data is returned, close connection and return results
    query.on('end', () => {
      done();
      return res.json(results);
    });
  });
});
*/
/* CREATE */
/*
router.post('/api/v1/todos', (req, res, next) => {
  const results = [];
  // Grab data from http request
  const data = {text: req.body.text, complete: false};
  // Get a Postgres client from the connection pool
  pg.connect(connectionString, (err, client, done) => {
    // Handle connection errors
    if(err) {
      done();
      console.log(err);
      return res.status(500).json({success: false, data: err});
    }
    // SQL Query > Insert Data
    client.query('INSERT INTO items(text, complete) values($1, $2)',
    [data.text, data.complete]);
    // SQL Query > Select Data
    const query = client.query('SELECT * FROM items ORDER BY id ASC');
    // Stream results back one row at a time
    query.on('row', (row) => {
      results.push(row);
    });
    // After all data is returned, close connection and return results
    query.on('end', () => {
      done();
      return res.json(results);
    });
  });
});
*/
/* READ */
/*
router.get('/api/v1/todos', (req, res, next) => {
  const results = [];
  // Get a Postgres client from the connection pool
  pg.connect(connectionString, (err, client, done) => {
    // Handle connection errors
    if(err) {
      done();
      console.log(err);
      return res.status(500).json({success: false, data: err});
    }
    // SQL Query > Select Data
    const query = client.query('SELECT * FROM items ORDER BY id ASC;');
    // Stream results back one row at a time
    query.on('row', (row) => {
      results.push(row);
    });
    // After all data is returned, close connection and return results
    query.on('end', () => {
      done();
      return res.json(results);
    });
  });
});
*/
/* UPDATE */
/*
router.put('/api/v1/todos/:todo_id', (req, res, next) => {
  const results = [];
  // Grab data from the URL parameters
  const id = req.params.todo_id;
  // Grab data from http request
  const data = {text: req.body.text, complete: req.body.complete};
  // Get a Postgres client from the connection pool
  pg.connect(connectionString, (err, client, done) => {
    // Handle connection errors
    if(err) {
      done();
      console.log(err);
      return res.status(500).json({success: false, data: err});
    }
    // SQL Query > Update Data
    client.query('UPDATE items SET text=($1), complete=($2) WHERE id=($3)',
    [data.text, data.complete, id]);
    // SQL Query > Select Data
    const query = client.query("SELECT * FROM items ORDER BY id ASC");
    // Stream results back one row at a time
    query.on('row', (row) => {
      results.push(row);
    });
    // After all data is returned, close connection and return results
    query.on('end', function() {
      done();
      return res.json(results);
    });
  });
});
*/
app.listen(4000, function() {
  console.log('Server is running on port 4000');
});
