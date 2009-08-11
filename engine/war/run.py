import sys
import base64

from webob import Request, Response

def handler(environ, start_response):
    start_response("200 OK", [ ('content-type', 'text/html') ])
    req = Request(environ)
    response_text = "Hello %s!" % req.GET.get('name', '')
    return [response_text]
