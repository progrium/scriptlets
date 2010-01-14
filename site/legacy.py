import wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.api import urlfetch
import urllib

LEGACY_URL = "http://1.latest.scriptletsapp.appspot.com"

class LegacyAdaptor(webapp.RequestHandler):
    def get(self):
        self.redirect('%s%s' % (LEGACY_URL, self.request.path))
    
    def post(self):
        payload = dict(self.request.POST)
        headers = dict(self.request.headers)
        self.response.out.write(urlfetch.fetch(
                    url='%s%s' % (LEGACY_URL, self.request.path),
                    payload=urllib.urlencode(payload) if len(payload) else None,
                    method=self.request.method,
                    headers=headers,
                    deadline=10).content)
    
def main():
    application = webapp.WSGIApplication([
        ('/view/.*', LegacyAdaptor),
        ('/code/.*', LegacyAdaptor),
        ('/run/.*', LegacyAdaptor),
        ], debug=True)
    wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
    main()