class Data:
    def __init__(self):
        self.variables = {}

    def write(self, variable, value):
        self.variables[variable.value] = value

    def read(self, variable_name):
        return self.variables.get(variable_name, None)
