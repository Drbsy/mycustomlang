from core.frontend.Lexer import Lexer
from core.frontend.Parser import Parser
from core.frontend.Semantic.Analyzer import Analyzer
from rich import print as rprint
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
script_path = os.path.join(BASE_DIR, 'examples', 'main.txt')


print_lexer : bool = True
print_parser: bool = True
print_semactic : bool = True


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
    rprint(result)
    return result

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
        ast = run_parser(pars, tokens)
    
    if print_semactic:
        analyzer = Analyzer()
        analyzer.analyze(ast)

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()