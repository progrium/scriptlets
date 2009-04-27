import time
from google.appengine.ext import db

def baseN(num,b,numerals="0123456789abcdefghijklmnopqrstuvwxyz"): 
    return ((num == 0) and  "0" ) or (baseN(num // b, b).lstrip("0") + numerals[num % b])


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
