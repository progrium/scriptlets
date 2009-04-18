import wsgiref.handlers
from django.utils import simplejson
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from models import Script

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
            self.response.out.write(script.run(self.request))
        else:
            self.redirect('/')


if __name__ == '__main__':
    wsgiref.handlers.CGIHandler().run(webapp.WSGIApplication([('/view/.*', ViewHandler),('/run/.*', RunHandler)], debug=True))
