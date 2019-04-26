const express = require('express');
const pug = require('pug');
const client = require('./search');

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
app.get("/", function (req, res) {
  res.send(render.index());
});

app.get("/search", function (req, res) {
  var query = req.query.q;

  if (!query) {
    res.send(render.search());
    return;
  }

  var opt = {
    search: req.query.q,
    top: 20
  };

  if (req.query.asccooktime) {
    opt.orderby = "total_time asc";
    opt.filter = "total_time ne 0";
  }

  if (req.query.desccooktime) {
    opt.orderby = "total_time desc";
  }

  if (req.query.customcooktime) {
    opt.filter = "total_time lt " + req.query.desiredcooktime;
    opt.orderby = "total_time desc";
  }


  client.search('documentdb-index', opt, function (err, results) {
    if (err) {
      console.log(err);
      res.status(500);
      res.send("Invalid Query");
    } else {
      res.send(
        render.search({
          results: results,
          query: query
        })
      );
    }
  });

});




var server = app.listen(port, function () {
  var host = server.address().address
  var port = server.address().port

  console.log("App listening at http://%s:%s", host, port)
});

