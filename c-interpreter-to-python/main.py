from lexical_analyzer.main import *
from syntax_analyzer.parser import *
from semantic_analyzer.semantic import *

from syntax_analyzer.printer import *

file_path = "input1.txt"
c_code = read_c_file(file_path)
if c_code:
    print("Success reading!")

    tokenize_result = tokenize_c_code(c_code)
    tokens = tokenize_result


    # for token in tokens:
    #     print(token)

    print("Syntax")

    parser = Parser(tokens)

    ast = parser.parse()

    ast_printer = ASTPrinter()
    for item in ast:
        ast_printer.print_ast(item)

    semantic_analyzer = SemanticAnalyzer()

    for item in ast:
        semantic_analyzer.analyze(item)



