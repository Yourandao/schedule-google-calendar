from flask import Flask
import sys
from components.controller import Controller

flask_app = Flask(__name__)

controller = Controller()

flask_app.add_url_rule('/', 'index', lambda: controller.home())
flask_app.add_url_rule('/calendar/<name>', 'parsed', lambda name: controller.parse(name))

if __name__ == '__main__':
    print('starting server', file=sys.stderr)
    flask_app.run(debug=False, host='0.0.0.0')
