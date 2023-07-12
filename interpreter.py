class Interpreter:
    def interpret(self, tree, data):
        if isinstance(tree, tuple):
            operator = tree[0]
            if operator == "OPERATOR":
                operator_token = tree[1]
                if len(tree) == 4:
                    left = self.interpret(tree[2], data)
                    right = self.interpret(tree[3], data)
                    return self.perform_operation(operator_token, left, right)
            elif operator == "INT" or operator == "FLT":
                return tree[1]
            elif operator == "ID":
                variable_name = tree[1].value
                if variable_name in data.variables:
                    return data.read(variable_name)
                else:
                    return None
            elif operator == "ASSIGN":
                variable = tree[1]
                expression = self.interpret(tree[2], data)
                if variable.value in data.variables:
                    existing_value = data.read(variable.value)
                    if isinstance(existing_value, tuple) and existing_value[0] == "OPERATOR" and existing_value[1] == "+":
                        expression = self.perform_operation("+", existing_value[2], expression)
                    data.write(variable, expression)
                else:
                    data.write(variable, expression)
                return None
            elif operator == "PRINT":
                expression = self.interpret(tree[1], data)
                print(expression)
                return None
            elif operator == "+":
                if isinstance(left, str) or isinstance(right, str):
                    return str(left) + str(right)
                else:
                    return left + right
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
        else:
            raise Exception("Invalid operator")
