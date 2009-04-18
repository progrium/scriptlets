// handler for SHTTPD/Mongoose (http://code.google.com/p/mongoose/)

var IO = require("io").IO,
    File = require("file").File,
    HashP = require("hashp").HashP;

var SHTTPD = exports.SHTTPD = exports.Handler = function() {}

SHTTPD.run = function(app, options) {
    var options = options || {},
        port = options["port"] || 8080,
        shttpd = options["shttpd"] || net.http.server.shttpd;
        
    var server = new shttpd.Server(port);
    
    server.registerURI(
    	"/*",
    	function (request) {
    	    SHTTPD.process(app, request, shttpd);
    	}
    );

    print("Jack is starting up using SHTTPD on port " + port);
        
    while (true) {
        server.processRequests();
    }
}

// Apparently no way to enumerate ENV or headers so we have to check against a list of common ones for now. Sigh.

SHTTPD.ENV_KEYS = [
    "SERVER_SOFTWARE", "SERVER_NAME", "GATEWAY_INTERFACE", "SERVER_PROTOCOL",
    "SERVER_PORT", "REQUEST_METHOD", "PATH_INFO", "PATH_TRANSLATED", "SCRIPT_NAME",
    "QUERY_STRING", "REMOTE_HOST", "REMOTE_ADDR", "AUTH_TYPE", "REMOTE_USER", "REMOTE_IDENT",
    "CONTENT_TYPE", "CONTENT_LENGTH", "HTTP_ACCEPT", "HTTP_USER_AGENT",
    "REQUEST_URI"
];
    
SHTTPD.HEADER_KEYS = [
    "Accept", "Accept-Charset", "Accept-Encoding", "Accept-Language", "Accept-Ranges",
    "Authorization", "Cache-Control", "Connection", "Cookie", "Content-Type", "Date",
    "Expect", "Host", "If-Match", "If-Modified-Since", "If-None-Match", "If-Range",
    "If-Unmodified-Since", "Max-Forwards", "Pragma", "Proxy-Authorization", "Range",
    "Referer", "TE", "Upgrade", "User-Agent", "Via", "Warn"
];

SHTTPD.process = function(app, request, shttpd) {
    try {
        var env = {};
    
        var key, value;
    
        SHTTPD.ENV_KEYS.forEach(function(key) {
            if (value = request.getEnv(key))
                env[key] = value;
        });
    
        SHTTPD.HEADER_KEYS.forEach(function(key) {
            if (value = request.getHeader(key)) {
                key = key.replace(/-/g, "_").toUpperCase();
                if (!key.match(/(CONTENT_TYPE|CONTENT_LENGTH)/i))
                    key = "HTTP_" + key;
                env[key] = value;
            }
        });

        var hostComponents = env["HTTP_HOST"].split(":")
        if (env["SERVER_NAME"] === undefined && hostComponents[0])
            env["SERVER_NAME"] = hostComponents[0];
        if (env["SERVER_PORT"] === undefined && hostComponents[1])
            env["SERVER_PORT"] = hostComponents[1];
        
        if (env["QUERY_STRING"] === undefined)
            env["QUERY_STRING"] = "";
        
        if (env["PATH_INFO"] === undefined)
            env["PATH_INFO"] = env["REQUEST_URI"];
            
        if (env["HTTP_VERSION"] === undefined)
            env["HTTP_VERSION"] = env["SERVER_PROTOCOL"] || "HTTP/1.1";
            
        if (env["CONTENT_LENGTH"] === undefined)
            env["CONTENT_LENGTH"] = "0";
            
        if (env["CONTENT_TYPE"] === undefined)
            env["CONTENT_TYPE"] = "text/plain";
        
        env["jack.version"]         = [0,1];
        env["jack.input"]           = null; // FIXME
        env["jack.errors"]          = system.stderr;
        env["jack.multithread"]     = false;
        env["jack.multiprocess"]    = true;
        env["jack.run_once"]        = false;
        env["jack.url_scheme"]      = "http"; // FIXME
    
        // call the app
        var result = app(env),
            status = result[0], headers = result[1], body = result[2];
    
        // FIXME: can't set the response status or headers?!
        
        // set the status
        //response.status(status);
    
        // set the headers
        //response.header(headers);
    
        // output the body
        body.forEach(function(string) {
            request.print(string);
        });
        
    } catch (e) {
        print("Exception! " + e);
    } finally {
        request.setFlags(shttpd.END_OF_OUTPUT);
    }
}
