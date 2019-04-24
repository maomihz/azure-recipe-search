const express = require('express');
const app = express();
const port = 3000;

app.use(express.static('public'))
 
 var server = app.listen(8081, function () {
    var host = server.address().address
    var port = server.address().port
    
    console.log("Example app listening at http://%s:%s", host, port)
 });

 //get the ingredients
 //send to azure search
 //show returned data