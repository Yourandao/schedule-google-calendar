from flask import Flask
from components.controller import Controller

flask_app = Flask(__name__)

controller = Controller()

flask_app.add_url_rule('/', 'index', lambda: controller.home())
flask_app.add_url_rule('/please', 'parsed', lambda: controller.parse())
flask_app.run(port=5001, debug=True)