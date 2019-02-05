import importlib
from werkzeug.exceptions import HTTPException, NotFound
from werkzeug.routing import Map
from werkzeug.wrappers import Request, Response

class Router:
    def __init__(self, url_map):
        self.request = None
        self.urls = Map(url_map)

    def dispatch_request(self, environ):
        self.request = Request(environ)
        urls = self.urls.bind_to_environ(self.request.environ)
        try:
            endpoint, values = urls.match()
            return self.call_endpoint(endpoint, **values)
        except NotFound as e:
            print(e)
            return self.error_404()
        except HTTPException as e:
            return e

    def parse_endpoint(self, endpoint):
        return endpoint.split('@')[0], endpoint.split('@')[-1]

    def call_endpoint(self, endpoint, **values):
        # Is this endpoint callable?
        if (callable(endpoint)):
            return Response(endpoint(self.request, **values))

        # Otherwise we probably have a controller and action
        try:
            controller, action = self.parse_endpoint(endpoint)
            module = importlib.import_module('controllers.' + controller)
        except ImportError as e:
            print("\n[ERROR]: Could not find controller - "+controller+"\n")
            return e

        try:
            return Response(getattr(module, action)(self.request, **values))
            
        except Exception as e:
            print("\n[ERROR]: No '"+action+"' method found in "+controller)
            return e

    def error_404(self):
        return Response('Error 404 - Page Not Found')
