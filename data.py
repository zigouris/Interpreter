class Data:
    def __init__(self):
        self.variables = {}

    def read(self, id):
        if id in self.variables:
            return self.variables[id]
        else:
            raise KeyError(f"Variable '{id}' does not exist.")

    def read_all(self):
        return self.variables

    def write(self, variable, expression):
        variable_name = variable.value
        self.variables[variable_name] = expression
        print(self.variables)