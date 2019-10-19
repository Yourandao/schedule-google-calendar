from components.google_processor import GoogleProcessor

class Controller:
    def home(self):
        return 'murr'

    def parse(self):
        proc = GoogleProcessor('ilya')
        proc.parse_and_push()

        return 'pozhaluista'