from flask import Flask
from components.controller import Controller

flask_app = Flask(__name__)

controller = Controller()

flask_app.add_url_rule('/', 'index', lambda: controller.home())
flask_app.add_url_rule('/calendar/<name>', 'parsed', lambda name: controller.parse(name))

if __name__ == '__main__':
    flask_app.run(port=5001)