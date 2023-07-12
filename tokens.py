class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return str(self.value)

class Integer(Token):
    def __init__(self, value):
        super().__init__("INT", value)

class Float(Token):
    def __init__(self, value):
        super().__init__("FLT", value)

class Operator(Token):
    def __init__(self, value):
        super().__init__("OPERATOR", value)

class Identifier(Token):
    def __init__(self, value):
        super().__init__("ID", value)

class String(Token):
    def __init__(self, value):
        super().__init__("STR", value)