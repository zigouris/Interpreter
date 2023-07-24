from tokens import Token, Integer, Float, Operator, Identifier, String

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def move(self):
        self.pos += 1
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None

    def peek(self):
        next_pos = self.pos + 1
        if next_pos < len(self.text):
            return self.text[next_pos]
        else:
            return None

    def skip_whitespace(self):
        while self.current_char is not None and (self.current_char.isspace() or self.current_char == '\n'):
            self.move()

    def parse_number(self):
        result = ""
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.move()
        if self.current_char == ".":
            result += "."
            self.move()
            while self.current_char is not None and self.current_char.isdigit():
                result += self.current_char
                self.move()
        if result == ".":
            return Operator(".")
        if "." in result:
            return Float(float(result))
        return Integer(int(result))

    def parse_identifier(self):
        result = ""
        while (
            self.current_char is not None
            and (self.current_char.isalnum() or self.current_char == "_")
        ):
            result += self.current_char
            self.move()
        return result
    
    def parse_string(self):
        result = ""
        self.move()
        while self.current_char is not None and self.current_char != '"':
            result += self.current_char
            self.move()
        self.move()
        return String(result)

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return self.parse_number()

            if self.current_char.isalpha() or self.current_char == "_":
                identifier = self.parse_identifier()
                if identifier in ["int", "float"]:
                    return Token("TYPE", identifier)
                elif identifier == "print":
                    return Token("PRINT", identifier)
                elif identifier == "if":
                    return Token("IF", identifier)
                return Identifier(identifier)

            if self.current_char == "=":
                self.move()
                if self.current_char == "=":
                    self.move()
                    return Operator("==")
                else:
                    return Operator("=")

            if self.current_char == "+":
                self.move()
                return Operator("+")

            if self.current_char == "-":
                self.move()
                return Operator("-")

            if self.current_char == "*":
                self.move()
                return Operator("*")

            if self.current_char == "/":
                self.move()
                return Operator("/")

            if self.current_char == "%":
                self.move()
                return Operator("%")

            if self.current_char == "(":
                self.move()
                return Operator("(")

            if self.current_char == ")":
                self.move()
                return Operator(")")

            if self.current_char == ">":
                self.move()
                if self.current_char == "=":
                    self.move()
                    return Operator(">=")
                else:
                    return Operator(">")

            if self.current_char == "<":
                self.move()
                if self.current_char == "=":
                    self.move()
                    return Operator("<=")
                else:
                    return Operator("<")

            if self.current_char == "!":
                self.move()
                if self.current_char == "=":
                    self.move()
                    return Operator("!=")
                else:
                    raise Exception("Invalid operator")
                
            if self.current_char == "{":
                self.move()
                return Operator("{")
            
            if self.current_char == "}":
                self.move()
                return Operator("}")

            if self.current_char == '"':
                return self.parse_string()

        return Token("EOF", None)

    def peek_next_token(self):
        next_pos = self.pos + 1
        while next_pos < len(self.text) and self.text[next_pos].isspace():
            next_pos += 1

        if next_pos < len(self.text):
            next_char = self.text[next_pos]
            if next_char.isdigit():
                return self.parse_number()
            if next_char.isalpha() or next_char == "_":
                identifier = self.parse_identifier()
                if identifier in ["int", "float"]:
                    return Token("TYPE", identifier)
                elif identifier == "print":
                    return Token("PRINT", identifier)
                elif identifier == "if":
                    return Token("IF", identifier)
                return Identifier(identifier)
            if next_char == "=":
                return Operator("=")
            if next_char in ["+", "-", "*", "/", "%"]:
                return Operator(next_char)
            if next_char == ">":
                return Operator(">=")
            if next_char == "<":
                return Operator("<=")
            if next_char == "!":
                return Operator("!=")

        return Token("EOF", None)
