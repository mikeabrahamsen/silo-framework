from werkzeug.routing import Rule

class Route:
    def get(self, url, action):
        return self.make_rule(url, action, methods=['GET'])

    def post(self, url, action):
        return self.make_rule(url, action, methods=['POST'])
        
    def parse_url(self, url):
        return url.replace('{', '<').replace('}', '>')

    def make_rule(self, url, action, **options):
        return Rule(self.parse_url(url), endpoint=action, **options)
