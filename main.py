from core.lexer import Lexer
from core.parser import Parser

code = """
var x = 3

fn calculate_area(length: float, width: float) -> float {
    var area: float = 100
    var is_active = true
    var y = is_active
    return x
}

fn main() -> void {
    var status: string = "Running"
    return status
}
"""

lexer = Lexer(code)
parser = Parser()

print_lexer = False
print_parser = True



def lexer_test(tokens):
    for token in tokens:
        print(token)

def parser_test(tokens):
    for t in tokens:
        if not isinstance(t.type, str):
            t.type = t.type.name
        t.lineno = t.line    
        t.index = t.start 
  
    reslut = parser.parse(iter(tokens))

    print(reslut)

try:
    tokens = lexer.tokenize()

    if print_lexer:
        lexer_test(tokens)
    
    if print_parser:
        parser_test(tokens)

except Exception as e:
    print(f"Error: {e}")