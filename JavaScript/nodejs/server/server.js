var http = require('http');  // HTTP library
var fs = require('fs');  // File system library
var url = require('url');  // URL library

var dt = require('./datetime.js');

http.createServer(function(req, res) {

    const u = url.parse(req.url, true);
    console.log(`Request URL: ${req.url}, path: ${u.pathname}`);

    if (u.pathname === '/') {
        console.log('Reading index.html');
        fs.readFile('index.html', function(err, data) {
            res.statusCode = 200;
            res.writeHead(200, {'Content-Type': 'text/html'});
            res.write(data);
            return res.end();
        });
    } else if (u.pathname === '/number') {
        const value = u.query['value'];
        console.log(`Received value: ${value}`);
        res.statusCode = 200;
        res.writeHead(200, {'Content-Type': 'application/json'});
        const result = {
            result: 2*value
        };
        return res.end(JSON.stringify(result));
    }
  
}).listen(8080);