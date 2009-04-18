var Request = require("./request").Request;

// FIXME: add to Array
var includes = function(arr, obj) {
    for (var i = 0, l = arr.length; i < l; i++) {
        if (arr[i] === obj) return true;    
    }
}

/**
 * Provides Rails-style HTTP method overriding via the _method parameter or X-HTTP-METHOD-OVERRIDE header
 * http://code.google.com/apis/gdata/docs/2.0/basics.html#UpdatingEntry
 */
var MethodOverride = exports.MethodOverride = function(app) {
    return function(env) {
        if (env["REQUEST_METHOD"] == "POST") {
            var request = new Request(env),
                method = request.POST(MethodOverride.METHOD_OVERRIDE_PARAM_KEY) || env[MethodOverride.HTTP_METHOD_OVERRIDE_HEADER];
            if (method && includes(MethodOverride.HTTP_METHODS, method.toUpperCase())) {
                env["jack.methodoverride.original_method"] = env["REQUEST_METHOD"];
                env["REQUEST_METHOD"] = method.toUpperCase();
            }
        }
        return app(env);
    }
}

MethodOverride.HTTP_METHODS = ["GET", "HEAD", "PUT", "POST", "DELETE", "OPTIONS"];
MethodOverride.METHOD_OVERRIDE_PARAM_KEY = "_method";
MethodOverride.HTTP_METHOD_OVERRIDE_HEADER = "HTTP_X_HTTP_METHOD_OVERRIDE";
