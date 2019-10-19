__package__ = None

class EventObject:
    def __init__(self, subject : str, location : str, time : str, color : int, date):
        self.subject = subject
        self.location = location
        self.time = time
        self.color = color
        self.date = date