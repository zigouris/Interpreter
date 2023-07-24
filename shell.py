from lexer import Lexer
from parse import Parser
from interpreter import Interpreter
from data import Data

interpreter = Interpreter()
data = Data()

with open("test.z", "r") as f:
    lines = f.readlines()

for line in lines:
    text = line.strip()
    
    if not text:
        continue

    lexer = Lexer(text)
    parser = Parser(lexer, data)
    
    tree = parser.parse()
    result = interpreter.interpret(tree, data)
    if result is not None:
        print(result)
