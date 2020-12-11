class ViewMock:
    def __init__(self):
        self.console_log = ""
        pass

    def print(self, message=""):
        self.console_log += message

    def get(self):
        return self.console_log

    def clean(self):
        self.console_log = ""
