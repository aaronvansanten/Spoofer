class Spoofer_API_Exception(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class Spoofer_Argument_Exception(Spoofer_API_Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
