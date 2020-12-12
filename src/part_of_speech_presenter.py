class PartOfSpeechPresenter:
    def __init__(self, view):
        self.view = view

    def nothing(self):
        self.view.print()

    def show_properties(self, param, param1):
        self.view.print("хлопець")
        pass

