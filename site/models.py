import time
import urllib
import base64
from google.appengine.ext import db
from google.appengine.api import urlfetch

def baseN(num,b,numerals="0123456789abcdefghijklmnopqrstuvwxyz"): 
    return ((num == 0) and  "0" ) or (baseN(num // b, b).lstrip("0") + numerals[num % b])
    
language_engines = {
    'php': 'http://scriptlets-engine.appspot.com/run.php',
    'javascript': 'http://scriptlets-engine.appspot.com/javascript/',
    'python': 'http://scriptlets-python.appspot.com/python/',
}


class Script(db.Model):
    name = db.StringProperty(required=True)
    code = db.TextProperty(required=True)
    language = db.StringProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    updated = db.DateTimeProperty(auto_now=True)
    user = db.UserProperty(auto_current_user_add=True)
    
    def __init__(self, *args, **kwargs):
        kwargs['name'] = kwargs.get('name', baseN(abs(hash(time.time())), 36))
        super(Script, self).__init__(*args, **kwargs)
        
    def run(self, request):
        payload = dict(request.POST)
        headers = dict(request.headers)
        headers['Run-Code'] = base64.b64encode(self.code)
        return urlfetch.fetch(
                    url='%s?%s' % (language_engines[self.language], request.query_string),
                    payload=urllib.urlencode(payload) if len(payload) else None,
                    method=request.method,
                    headers=headers).content