from flask import Flask, Blueprintvalidators

app = Flask(__name__)

class Redprint(object):
    def __init__(self, name):
        self.name = name
        self.mound = []

    def route(self, rule, **options):
        def deco(f):
            self.mound.append((f, rule, options))
            return f
        return deco

    def register(self, bp, url_prefix):
        for f, rule, options in self.mound:
            endpoint = options.pop('endpoint', None)
            bp.add_url_rule(url_prefix + rule,  endpoint, f, **options)


book_api = Redprint('book')
bp_v1 = Blueprint('v1', __name__)
book_api.register(bp_v1, url_prefix='book')
app.register_blueprint(bp_v1)


if __name__ == '__main__':
    app.run()
