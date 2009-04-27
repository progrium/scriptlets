import wsgiref.handlers
from django.utils import simplejson
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import urlfetch
from models import Script
import base64
import urllib

language_engines = {
    'php': 'http://scriptlets-engine.appspot.com/run.php',
    'javascript': 'http://scriptlets-engine.appspot.com/javascript/',
    'python': 'http://scriptlets-python.appspot.com/python/',
}

class ViewHandler(webapp.RequestHandler):
    def get(self):
        if self.request.path[-1] == '/':
            self.redirect(self.request.path[:-1])
        name = self.request.path.split('/')[-1]
        script = Script.all().filter('name =', name).get()
        if script:
            params = {'script':script, 'lines': script.code.count("\n"), 'run_url': self.request.url.replace('view', 'run')}
            user = users.get_current_user()
            if user:
                params['user'] = user
                params['logout_url'] = users.create_logout_url("/")
            else:
                params['user'] = user
                params['login_url'] = users.create_login_url('/')
            self.response.out.write(template.render('templates/view.html', params))
        else:
            self.redirect('/')

class CodeHandler(webapp.RequestHandler):
    def get(self):
        if self.request.path[-1] == '/':
            self.redirect(self.request.path[:-1])
        name = self.request.path.split('/')[-1]
        script = Script.all().filter('name =', name).get()
        self.response.out.write(base64.b64encode(script.code))

class RunHandler(webapp.RequestHandler):
    def get(self):
        if self.request.path[-1] == '/':
            self.redirect(self.request.path[:-1])
        self._run_script()

    def post(self):
        self._run_script()
        
    def _run_script(self):
        name = self.request.path.split('/')[-1]
        script = Script.all().filter('name =', name).get()
        if script:
            payload = dict(self.request.POST)
            headers = dict(self.request.headers)
            if headers.get('Content-Type'):
                del headers['Content-Type']
            headers['Run-Code'] = base64.b64encode(script.code)
            headers['Run-Code-URL'] = self.request.url.replace('run', 'code')
            self.response.out.write(urlfetch.fetch(
                        url='%s?%s' % (language_engines[script.language], self.request.query_string),
                        payload=urllib.urlencode(payload) if len(payload) else None,
                        method=self.request.method,
                        headers=headers).content)
        else:
            self.redirect('/')


if __name__ == '__main__':
    wsgiref.handlers.CGIHandler().run(webapp.WSGIApplication([
    ('/view/.*', ViewHandler),
    ('/code/.*', CodeHandler),
    ('/run/.*', RunHandler)], debug=True))
