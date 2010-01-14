import wsgiref.handlers
import urllib, cgi

from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.api import urlfetch
from google.appengine.ext.webapp import template
from models import Script, Version

class NewHandler(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            logout_url = users.create_logout_url('/')
        else:
            login_url = users.create_login_url('/')
        self.response.out.write(template.render('templates/new.html', locals()))

    def post(self):
        user = users.get_current_user()
        body = self.request.get('script')
        if body:
            script = Script()
            script.put()
            version = Version(script=script, body=body)
            version.put()
            script.latest_version = version
            script.put()
            self.redirect('/%s' % script.id)
        else:
            self.redirect('/new')

def script_routing(f):
    def wrap(self):
        parts = self.request.path.split('/')[1:]
        if parts[-1] == '':
            parts.pop()
        if '.' in parts[-1]:
            part, ext = parts[-1].split('.')
            parts[-1] = part
        else:
            ext = None
        script = Script.all().filter('id =', parts[0]).get()
        version = None
        if script:
            if len(parts) > 1:
                if parts[1] == 'latest':
                    return self.redirect('/%s/%s' % (script.id, script.latest_version.id))
                else:
                    version = script.version_set.filter('id =', parts[1]).get()
            else:
                version = script.latest_version
        if not version:
            self.not_found()
        elif self.should_run():
            self.run(script, version)
        elif ext == 'js':
            self.response.headers['Content-Type'] = 'text/javascript'
            self.response.out.write(version.body)
        else:
            user = users.get_current_user()
            if script.private and script.user.key() != user.key():
                return self.not_authorized()
            f(self, script, version, user)
    return wrap

class ScriptHandler(webapp.RequestHandler):
    def run(self, script, version):
        self.response.out.write(urlfetch.fetch(
            url='http://eval.progrium.com',
            payload=urllib.urlencode({'script': script.latest_version.body}),
            method='POST',
            deadline=10).content)
    
    def should_run(self):
        return self.request.host.startswith('run.') or self.request.path.split('/')[-1] == 'run'
    
    def not_found(self):
        self.error(404)
        self.response.out.write(template.render('templates/not_found.html', locals()))
        
    def not_authorized(self):
        self.error(403)
        self.response.out.write(template.render('templates/not_authorized.html', locals()))
        
    @script_routing
    def get(self, script, version, user=None):
        if not script.user:
            if user:
                script.user = user
                script.put()
            else:
                self.redirect(users.create_login_url('/%s' % script_id))
        self.response.out.write(template.render('templates/script.html', locals()))
    
    @script_routing
    def post(self, script, version, user=None):
        if script.user.key() != user.key():
            return self.not_authorized()
        version = Version(script=script, body=self.request.get('script'))
        version.put()
        script.latest_version = version
        script.put()
        self.redirect('/%s' % script.id)

class RootHandler(webapp.RequestHandler):
    def get(self):
        self.redirect('/new')

def main():
    application = webapp.WSGIApplication([
        ('/', RootHandler),
        ('/new', NewHandler),
        ('/.*', ScriptHandler),
        ], debug=True)
    wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
    main()