class Router:

    def __init__(self):
        self.route = {}

    def get(self, path, handler):
        self.route[("GET", path)] = handler

    def post(self, path, handler):
        self.route[('POST', path)] = handler

    def match(self, method, path):
        return self.route[(method, path)]


