class Error:
    def __init__(self, name, info):
        self.name = name
        self.info = info

    def get_name(self):
        return self.name

    def get_info(self):
        return self.info

    def __repr__(self):
        return f'Error: <{self.get_name()}> {self.get_info()}'
