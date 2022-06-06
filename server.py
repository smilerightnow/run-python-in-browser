from bottle import route, run, template, request, response
import bottle, json, sys, traceback
from io import StringIO
from contextlib import redirect_stdout

@route('/run', method=["OPTIONS", "POST"])
def index():
	if request.method == "OPTIONS":
		response.set_header('Access-Control-Allow-Origin', "*")
		response.set_header("Access-Control-Allow-Headers", "*")
		response.set_header("Access-Control-Allow-Methods", "*")
	else:
		response.set_header('Access-Control-Allow-Origin', "*")
		body = json.loads(request.body.getvalue())
		
		f = StringIO()
		sys.stdout = f
		try:
			exec(body["python"])
		except Exception as e:
			print(traceback.format_exc())
		s = f.getvalue()

		return {"result": s}

class StripPathMiddleware(object):
  def __init__(self, app):
    self.app = app
  def __call__(self, e, h):
    e['PATH_INFO'] = e['PATH_INFO'].rstrip('/')
    return self.app(e,h)

app = bottle.app()
myapp = StripPathMiddleware(app)
bottle.run(app=myapp, host="localhost", port=8080)
