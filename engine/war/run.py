import sys
import base64

from webob import Request, Response

def handler(environ, start_response):
    req = Request(environ)
    resp = Response()

    code = base64.b64decode(environ['HTTP_RUN_CODE']).replace("\r\n", "\n") + "\n"
    code = "from scriptlets.util import RestClient\n%s" % code
    compiled = compile(code, '<string>', 'exec')
    
    old_stderr, old_stdout = sys.stderr, sys.stdout
    sys.stderr, sys.stdout = resp, resp
    
    exec compiled in {'req': req, 'resp': resp}
    
    sys.stderr, sys.stdout = old_stderr, old_stdout
    return resp(environ, start_response)
