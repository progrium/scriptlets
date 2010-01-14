import time
from google.appengine.ext import db

def baseN(num,b=62,numerals="0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"): 
    return ((num == 0) and  "0" ) or (baseN(num // b, b).lstrip("0") + numerals[num % b])

class Script(db.Model):
    user = db.UserProperty(auto_current_user_add=True)
    id = db.StringProperty(required=True)
    name = db.StringProperty()
    private = db.BooleanProperty(default=False)
    latest_version = db.ReferenceProperty()
    
    created  = db.DateTimeProperty(auto_now_add=True)
    edited   = db.DateTimeProperty()
    executed = db.DateTimeProperty()
    run_count = db.IntegerProperty(default=0)

    # Legacy fields
    name = db.StringProperty()
    code = db.TextProperty()    
    language = db.StringProperty()
    
    def __init__(self, *args, **kwargs):
        kwargs['id'] = kwargs.get('id', baseN(abs(hash(time.time()))))
        super(Script, self).__init__(*args, **kwargs)

class Version(db.Model):
    script = db.ReferenceProperty(Script)
    id = db.StringProperty(required=True)
    body = db.TextProperty()   
    
    created  = db.DateTimeProperty(auto_now_add=True) 
    executed = db.DateTimeProperty()
    run_count = db.IntegerProperty(default=0)
    
    def __init__(self, *args, **kwargs):
        kwargs['id'] = kwargs.get('id', str(abs(hash(time.time()))))
        super(Version, self).__init__(*args, **kwargs)