class Interpreter:
    is_false = True
    def interpret(self, tree, data):
        if isinstance(tree, tuple):
            operator = tree[0]

            if operator == "ASSIGN":
                variable = tree[1]
                expression = self.interpret(tree[2], data)
                data.write(variable, expression)

            elif operator == "IF":
                condition = self.interpret(tree[1], data)

                if condition:
                    self.interpret(tree[1], data)

            elif operator == "OPERATOR":
                operator_token = tree[1]
                if len(tree) == 4:
                    left = self.interpret(tree[2], data)

                    if operator_token == "-":
                        return self.perform_operation(operator_token, left)

                    right = self.interpret(tree[3], data)

                    result = self.perform_operation(operator_token, left, right)
                    if result == False:
                        Interpreter.is_false = False
                        return False

                    return result

            elif operator == "PRINT":
                if Interpreter.is_false != False:
                    expression = self.interpret(tree[1], data)
                    print(expression)
                Interpreter.is_false = True
                return

            elif operator == "INT" or operator == "FLT" or operator == "STR":
                return tree[1]

            elif operator == "ID":
                variable_name = tree[1].value
                return data.read(variable_name)

        else:
            return tree

    def perform_operation(self, operator, left, right=None):
        if operator == "+":
            return left + right
        elif operator == "-":
            if right is None:
                return -left
            else:
                return left - right
        elif operator == "*":
            return left * right
        elif operator == "/":
            return left / right
        elif operator == "%":
            return left % right
        elif operator == "//":
            return left // right
        elif operator == "**":
            return left ** right
        elif operator == "==":
            return left == right
        elif operator == ">=":
            return left >= right
        elif operator == ">":
            return left > right
        elif operator == "<=":
            return left <= right
        elif operator == "<":
            return left < right
        elif operator == "!=":
            return left != right
        else:
            raise Exception("Invalid operator")
        
