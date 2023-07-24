class Parser:
    operators = "+-*/"

    def __init__(self, lexer, data):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
        self.data = data

    def error(self):
        raise Exception("Invalid syntax")

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def parse_type(self):
        token = self.current_token
        self.eat("TYPE")
        return token.value

    def parse_variable(self):
        variable = self.current_token
        self.eat("ID")
        return ("ID", variable)

    def parse_assignment(self):
        variable = self.current_token
        self.eat("ID")
        if self.current_token.type == "OPERATOR" and self.current_token.value == "=":
            self.eat("OPERATOR")
            expression = self.parse_expr()

            if isinstance(expression, tuple) and expression[0] == "ID":
                expression = self.data.read(expression[1].value)

            return ("ASSIGN", variable, expression)
        else:
            if variable.value in self.data.variables:
                expression = self.data.read(variable.value)
                return ("EXPR", expression)
            else:
                self.error()

    def parse_print(self):
        self.eat("PRINT")
        expression = self.parse_expr()

        if isinstance(expression, tuple) and expression[0] == "ID":
            expression = self.data.read(expression[1].value)

        return ("PRINT", expression)

    def parse_block(self):
        statements = []
        self.eat("OPERATOR", "{")
        while not (self.current_token.type == "OPERATOR" and self.current_token.value == "}"):
            statement = self.parse_statement()
            if statement is not None:
                statements.append(statement)
        self.eat("OPERATOR", "}")
        return ("BLOCK", statements)

    def parse_statement(self):
        token = self.current_token

        if token.type == "ID":
            next_token = self.lexer.peek_next_token()
            if next_token.type == "OPERATOR" and next_token.value == "=":
                return self.parse_assignment()
            else:
                self.error()
        elif token.type == "PRINT":
            return self.parse_print()
        elif token.type == "IF":
            return self.parse_if()
        else:
            self.error()

    def parse_if(self):
        condition = None
        block = None
        self.eat("IF")
        self.eat("OPERATOR", "(")
        condition = self.parse_expr()
        self.eat("OPERATOR", ")")
        block = self.parse_block()
        return ("IF", condition, block)

    def parse_print_in_if(self):
        self.eat("PRINT")
        expression = self.parse_expr()
        return ("PRINT", expression)

    def parse_expr(self):
        return self.parse_comparison()

    def parse_comparison(self):
        left = self.parse_add_sub()

        while self.current_token.type == "OPERATOR" and self.current_token.value in ["==", ">=", ">", "<", "<=", "!="]:
            operator_token = self.current_token
            self.eat("OPERATOR")

            right = self.parse_add_sub()

            if isinstance(left, tuple) and left[0] == "ID":
                left = self.data.read(left[1].value)

            if isinstance(right, tuple) and right[0] == "ID":
                right = self.data.read(right[1].value)

            left = ("OPERATOR", operator_token.value, left, right)

        return left

    def parse_add_sub(self):
        left = self.parse_term()

        while (
            self.current_token.type == "OPERATOR"
            and self.current_token.value in ["+", "-"]
        ):
            operator_token = self.current_token
            if operator_token.value in Parser.operators:
                self.eat("OPERATOR")

            right = self.parse_term()

            if isinstance(left, tuple) and left[0] == "ID":
                left = self.data.read(left[1].value)

            if isinstance(right, tuple) and right[0] == "ID":
                right = self.data.read(right[1].value)

            left = ("OPERATOR", operator_token.value, left, right)

        return left

    def parse_term(self):
        token = self.current_token

        left = self.parse_factor()

        while (
            self.current_token.type == "OPERATOR"
            and self.current_token.value in ["*", "/", "%"]
        ):
            operator_token = self.current_token
            if operator_token.value in Parser.operators:
                self.eat("OPERATOR")

            right = self.parse_factor()

            if isinstance(left, tuple) and left[0] == "ID":
                left = self.data.read(left[1].value)

            if isinstance(right, tuple) and right[0] == "ID":
                right = self.data.read(right[1].value)

            left = ("OPERATOR", operator_token.value, left, right)

        return left

    def parse_print_in_if(self):
        self.eat("PRINT")
        expression = self.parse_expr()
        return ("PRINT", expression)

    def parse_factor(self):
        token = self.current_token

        if token.type == "INT" or token.type == "FLT":
            self.eat(token.type)
            return token.value
        elif token.type == "OPERATOR" and token.value == "-":
            self.eat("OPERATOR")
            factor = self.parse_factor()
            return ("OPERATOR", "-", 0, factor)
        elif token.type == "OPERATOR" and token.value in ["==", ">=", ">", "<=", "!=", "<"]:
            operator = token.value
            self.eat("OPERATOR")
            right = self.parse_expr()
            left = self.current_token.value
            return ("OPERATOR", operator, left, right)
        elif token.type == "ID":
            variable = token
            self.eat("ID")
            return ("ID", variable)
        elif token.type == "STR":
            string_value = token.value
            self.eat("STR")
            return string_value
        elif token.type == "PRINT":
            self.eat("PRINT")
            expression = self.parse_expr()

            if isinstance(expression, tuple) and expression[0] == "ID":
                expression = self.data.read(expression[1].value)

            return ("PRINT", expression)
        elif token.type == "IF":
            self.eat("IF")
            expression = self.parse_expr()

            if isinstance(expression, tuple) and expression[0] == "ID":
                expression = self.data.read(expression[1].value)

            return ("IF", expression)

        elif token.type == "OPERATOR" and token.value == "(":
            self.eat("OPERATOR")
            expression = self.parse_expr()
            if self.current_token.type == "OPERATOR" and self.current_token.value == ")":
                self.eat("OPERATOR")
                return expression
            else:
                self.error()

        elif token.type == "OPERATOR" and token.value == "}":
            self.eat("OPERATOR")

        else:
            self.error()

    def parse(self):
        token = self.current_token

        if token.type == "TYPE":
            return self.parse_variable()
        elif token.type == "ID":
            next_token = self.lexer.peek_next_token()

            if next_token.type == "OPERATOR" and next_token.value in ["+", "-", "*", "/", "%"]:
                return self.parse_expr()
            elif next_token.type == "OPERATOR" and next_token.value == "=":
                return self.parse_assignment()
            elif next_token.type == "OPERATOR" and next_token.value == "PRINT":
                return self.parse_print()
            elif next_token.type == "OPERATOR" and next_token.value == "IF":
                return self.parse_if()
            else:
                self.error()
        else:
            return self.parse_expr()

