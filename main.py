from core.lexer import Lexer
from core.parser import Parser

script_path = r'examples\main.txt'

print_lexer : bool = False
print_parser: bool = True



def read_script_file(script_path):
    data = []
    with open(script_path, 'r') as f:
        for line in f:
            data.append(line)
    return data


def normalize_tokens(tokens):
    for t in tokens:
        if not isinstance(t.type, str):
            t.type = t.type.name
        t.lineno = t.line    
        t.index = t.start 
    return tokens

def print_tokens(tokens):
    for t in tokens:
        print(t)
    
def run_parser(parser_obj, tokens):
    tokens = normalize_tokens(tokens)
    result = parser_obj.parse(iter(tokens))
    print(result)

try:
    script_lines = read_script_file(script_path)
    script_text = ''.join(script_lines)

    lex = Lexer(script_text)
    pars = Parser()

    tokens = lex.tokenize()
    
    print('\n\n' + '_' *120 +'\n\n')
    if print_lexer:
        print_tokens(tokens)
        print('\n\n' + '_' *120 +'\n\n')

    if print_parser:
        run_parser(pars, tokens)

except Exception as e:
    print(f"Error: {e}")