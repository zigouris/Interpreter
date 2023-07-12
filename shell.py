from lexer import Lexer
from parse import Parser
from interpreter import Interpreter
from data import Data

interpreter = Interpreter()
data = Data()

while True:
    text = input("Z# ")
    lexer = Lexer(text)
    parser = Parser(lexer, data)

    tree = parser.parse()

    result = interpreter.interpret(tree, data)
    if result is not None:
        print(result)
