from core.lexer import Lexer
from core.parser import Parser

code = """
var lol = 3

fn calculate_area(length: float, width: float) -> float {
    var area: float = 100
    var is_active = true
}

fn main() -> void {
    var status: string = "Running"
}
"""

lexer = Lexer(code)
parser = Parser()

print_lexer = False
print_parser = True



def lexer_test():
    tokens = lexer.tokenize()
    for token in tokens:
        print(token)

def parser_test():
    tokens = list(lexer.tokenize())
    for t in tokens:
        if not isinstance(t.type, str):
            t.type = t.type.name
        t.lineno = t.line    
        t.index = t.start 
  
    parser = Parser()
    reslut = parser.parse(iter(tokens))

    print("AST result:", reslut)

try:
    if print_lexer:
        lexer_test()
    
    if print_parser:
        parser_test()

except Exception as e:
    print(f"Lexer Error: {e}")