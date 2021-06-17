class NotFoundGame(Exception):
    def __init__(self, text):
        self.txt = text


class NotFoundBoard(Exception):
    def __init__(self, text):
        self.txt = text


class BoardAlreadyExist(Exception):
    def __init__(self, text):
        self.txt = text
