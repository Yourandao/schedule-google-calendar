from components.google_processor import GoogleProcessor

class Controller:
    def home(self):
        return 'murr'

    def parse(self, name):
        proc = GoogleProcessor(name)
        proc.parse_and_push()

        return 'OK'