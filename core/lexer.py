import enum
import re

class TokenType(enum.Enum):
    #keywords
    TOK_VAR = enum.auto()
    TOK_FUNCTION = enum.auto()
    TOK_RETURN = enum.auto()
    TOK_IF = enum.auto()
    TOK_ELSE = enum.auto()
    TOK_ELIF = enum.auto()
    TOK_WHILE_LOOP = enum.auto()
    TOK_AND = enum.auto()
    TOK_OR = enum.auto()
    TOK_NOT = enum.auto()
    TOK_BREAK = enum.auto()
    TOK_CONTINUE = enum.auto()
    TOK_FOR = enum.auto()
    TOK_CONST = enum.auto()
    
    #operators and symbols
    TOK_PLUS = enum.auto()
    TOK_MINUS = enum.auto()
    TOK_STAR = enum.auto()
    TOK_SLASH = enum.auto()
    TOK_ASSIGN = enum.auto()
    TOK_EQUAL_TO = enum.auto()
    TOK_NOT_EQUAL_TO = enum.auto()
    TOK_GREATER = enum.auto()
    TOK_LESS = enum.auto()
    TOK_GREATER_EQUAL = enum.auto()
    TOK_LESS_EQUAL = enum.auto()
    TOK_BANG = enum.auto()
    TOK_MODULO = enum.auto()
    TOK_POW = enum.auto()
    TOK_PLUS_ASSIGN = enum.auto()
    TOK_HASH = enum.auto()
    TOK_ARROW = enum.auto()
    TOK_QUESTION = enum.auto()
    TOK_DOUBLE_COLON = enum.auto()

    #structural
    TOK_L_PAREN = enum.auto()
    TOK_R_PAREN = enum.auto()
    TOK_L_BRACE = enum.auto()
    TOK_R_BRACE = enum.auto()
    TOK_L_BRACKET = enum.auto()
    TOK_R_BRACKET = enum.auto()
    TOK_COMMA = enum.auto()
    TOK_DOT = enum.auto()
    TOK_SEMICOLON = enum.auto()
    TOK_COLON = enum.auto()
    TOK_NEWLINE = enum.auto()
    TOK_EOF = enum.auto()

    #literals and iden
    TOK_NUMBER = enum.auto()
    TOK_STRING = enum.auto()
    TOK_ID = enum.auto()
    

    #booland
    TOK_TRUE = enum.auto()
    TOK_FALSE = enum.auto()
    
    #special
    TOK_NULL = enum.auto()

    #comments
    TOK_COMMENT = enum.auto()
    TOK_BLOCK_COMMENT = enum.auto()
    
    #input output
    TOK_PRINT = enum.auto()
    TOK_CLEAR = enum.auto()


    #datatype
    TOK_TYPE_INT = enum.auto()
    TOK_TYPE_STRING = enum.auto()
    TOK_TYPE_FLOAT = enum.auto()
    TOK_TYPE_BOOL = enum.auto()
    TOK_TYPE_LIST = enum.auto()
    TOK_TYPE_MAP = enum.auto()
    TOK_TYPE_AUTO = enum.auto()
    TOK_TYPE_VOID = enum.auto()
    TOK_MISMATCH = enum.auto()


KEYWORDS = {
    "var": TokenType.TOK_VAR,
    "fn": TokenType.TOK_FUNCTION,
    "return": TokenType.TOK_RETURN,
    "if": TokenType.TOK_IF,
    "else": TokenType.TOK_ELSE,
    "elif": TokenType.TOK_ELIF,
    "while": TokenType.TOK_WHILE_LOOP,
    "and": TokenType.TOK_AND,
    "or": TokenType.TOK_OR,
    "not": TokenType.TOK_NOT,
    "break": TokenType.TOK_BREAK,
    "continue": TokenType.TOK_CONTINUE,
    "for": TokenType.TOK_FOR,
    "const": TokenType.TOK_CONST,
    "true": TokenType.TOK_TRUE,
    "false": TokenType.TOK_FALSE,
    "null": TokenType.TOK_NULL,
    "print": TokenType.TOK_PRINT,
    "clear": TokenType.TOK_CLEAR,
    "int": TokenType.TOK_TYPE_INT,
    "string": TokenType.TOK_TYPE_STRING,
    "float": TokenType.TOK_TYPE_FLOAT,
    "bool": TokenType.TOK_TYPE_BOOL,
    "list": TokenType.TOK_TYPE_LIST,
    "map": TokenType.TOK_TYPE_MAP,
    "auto": TokenType.TOK_TYPE_AUTO,
    "void": TokenType.TOK_TYPE_VOID 
}


TokenPatterns = [
    ('SKIP',r'[ \t]+'),
    ('TOK_NUMBER',r'\d+(\.\d+)?'),
    ('TOK_STRING',r'\"[^\"]*\"'),
    ('TOK_EQUAL_TO',r'=='),
    ('TOK_NOT_EQUAL_TO',r'!='),
    ('TOK_GREATER_EQUAL',r'>='),
    ('TOK_LESS_EQUAL',r'<='),
    ('TOK_PLUS_ASSIGN',r'\+='),
    ('TOK_POW',r'\*\*'),
    ('TOK_ARROW',r'->'),
    ("TOK_AND",r'&&'),
    ('TOK_OR',r'\|\|'),
    ('TOK_DOUBLE_COLON',r'::'),
    ('TOK_BLOCK_COMMENT', r'/\*[\s\S]*?\*/'),
    ('TOK_COMMENT',r'//.*'),
    ('TOK_ASSIGN',r'='),
    ('TOK_PLUS',r'\+'),
    ('TOK_MINUS',r'-'),
    ('TOK_STAR',r'\*'),
    ('TOK_SLASH',r'/'),
    ('TOK_MODULO',r'%'),
    ('TOK_GREATER',r'>'),
    ('TOK_LESS',r'<'),
    ('TOK_BANG',r'!'),
    ('TOK_QUESTION',r'\?'),
    ('TOK_HASH',r'#'),
    ('TOK_L_PAREN',r'\('),
    ('TOK_R_PAREN',r'\)'),
    ('TOK_L_BRACE',r'\{'),
    ('TOK_R_BRACE',r'\}'),
    ('TOK_L_BRACKET',r'\['),
    ('TOK_R_BRACKET',r'\]'),
    ('TOK_COMMA',r','),
    ('TOK_DOT',r'\.'),
    ('TOK_COLON',r':'),
    ('TOK_SEMICOLON',r';'),
    ('TOK_NEWLINE',r'\n'),
    ('TOK_ID',r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ('MISMATCH',r'.')
]

class Token:
    def __init__(self,type,line,value,start,end,col):
        self.type = type
        self.line = line
        self.value = value
        self.start = start
        self.end = end
        self.col = col
    

    def __repr__(self):
        return f"Token({self.type.name}, '{self.value}', Line:{self.line}, Col: {self.col})"

class Lexer:
    def __init__(self , source_code):
        self.source_code = source_code
        self.tokens = []
        self.line = 1
        self.line_start = 0
    
    def tokenize(self):

        master_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in TokenPatterns)

        for match in re.finditer(master_regex , self.source_code):
            kind = match.lastgroup
            value = match.group()
            start = match.start()
            end = match.end()
            column = start - self.line_start + 1

            if kind == 'SKIP':
                continue
                
            elif kind == 'TOK_NEWLINE':
                self.line +=1
                self.line_start = end
                continue
            
            elif kind == 'TOK_ID':
                token_type = KEYWORDS.get(value, TokenType.TOK_ID)
                self.tokens.append(Token(token_type, self.line, value, start, end, column))

            elif kind == "MISMATCH":
                raise RuntimeError(f"Unexpected charcter {value!r} on line {self.line}")
            
            else:
                token_type = TokenType[kind]
                self.tokens.append(Token(token_type, self.line, value, start, end, column))

        source_len = len(self.source_code)
        self.tokens.append(Token(TokenType.TOK_EOF, self.line, "EOF", source_len, source_len, 1))
        return self.tokens