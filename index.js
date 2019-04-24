const express = require('express');
const pug = require('pug');
const search = require('./search').search;

const app = express();
const port = 8081;

app.use(express.static(__dirname + '/public'));
app.use('/js', express.static(__dirname + '/node_modules/bootstrap/dist/js'));
app.use('/css', express.static(__dirname + '/node_modules/bootstrap/dist/css'));
app.use('/js', express.static(__dirname + '/node_modules/jquery/dist'));
app.use('/js', express.static(__dirname + '/node_modules/popper.js/dist'));


var render = {
   search: pug.compileFile('templates/search.pug'),
   index: pug.compileFile('templates/index.pug')
};


// Routes
app.get("/", function(req, res) {
   res.send(render.index());
});

app.get("/search", function(req, res) {
   search(req.query.q, function(err, results) {
      res.send(render.search({
         results: results
      }));
   });
});




var server = app.listen(port, function () {
   var host = server.address().address
   var port = server.address().port

   console.log("App listening at http://%s:%s", host, port)
});

