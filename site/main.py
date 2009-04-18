import wsgiref.handlers
import urllib, cgi

from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.ext.webapp import template
from models import Script

class MainHandler(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        auth_save = self.request.cookies.get('auth_save', None)
        if auth_save:
            self.response.headers.add_header('Set-Cookie', 'auth_save=; expires=Wed, 11-Sep-1985 11:00:00 GMT')
            params = cgi.parse_qs(auth_save)
            script = Script(language=params['language'][0], code=params['code'][0])
            script.put()
            self.redirect('/view/%s' % script.name)
        else:
            if user:
                params = {'user': user, 'logout_url': users.create_logout_url("/")}
            else:
                params = {'user': user, 'login_url': users.create_login_url('/')}
            self.response.out.write(template.render('templates/main.html', params))

    def post(self):
        user = users.get_current_user()
        language = self.request.POST['language']
        code = self.request.POST['%s-code' % language]
        if user:
            script = Script(language=language, code=code)
            script.put()
            self.redirect('/view/%s' % script.name)
        else:
            auth_save = {'language': language, 'code': code}
            self.response.headers.add_header('Set-Cookie', 'auth_save=%s' % urllib.urlencode(auth_save))
            self.redirect(users.create_login_url("/"))

if __name__ == '__main__':
    wsgiref.handlers.CGIHandler().run(webapp.WSGIApplication([('/', MainHandler)], debug=True))
