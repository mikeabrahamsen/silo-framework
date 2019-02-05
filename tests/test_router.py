import unittest
from werkzeug.routing import Rule
from Silo.routing.route import Route


class TestRouteMethods(unittest.TestCase):

    def test_url_params_parsed_correctly(self):
        self.assertEqual(Route().parse_url('/url/{param}/test'), '/url/<param>/test')

    def test_define_get_route(self):
        self.route_matches_rule(
            Route().get('/url/{param}', 'test_controller@action'),
            Rule('/url/<param>', endpoint='test_controller@action', methods=['GET'])
        )

    def test_define_post_route(self):
        self.route_matches_rule(
            Route().post('/url/{param}', 'test_controller@action'),
            Rule('/url/<param>', endpoint='test_controller@action', methods=['POST'])
        )

    def route_matches_rule(self, route, rule):
        self.assertEqual(route.endpoint, rule.endpoint)
        self.assertEqual(route.methods, rule.methods)
