#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#




import wsgiref.handlers
import sys

from google.appengine.ext import webapp

class MainHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write('<form method="post"><textarea name="_code"></textarea><input type="submit" /></form>')
    
    def post(self):
        code = self.request.params['_code'].replace("\r\n", "\n") + "\n"
        code = "from google.appengine.api.urlfetch import fetch\n%s" % code
        compiled = compile(code, '<string>', 'exec')
        old_stderr, old_stdout = sys.stderr, sys.stdout
        try:
            sys.stderr, sys.stdout = self.response.out, self.response.out
            exec compiled in {'req': self.request, 'resp': self.response}
        finally:
            sys.stderr, sys.stdout = old_stderr, old_stdout
        


def main():
    application = webapp.WSGIApplication([('/python/', MainHandler)],
                                       debug=True)
    wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
    main()