_ = None
from core.lexer import TokenType
import sly
from core.Nodes import *

class Parser(sly.Parser):

    tokens = {i.name for i in TokenType}

    # --- ENTRY POINT ---

    @_('statement_list TOK_EOF', 'statement_list')
    def program(self, p):
        return p.statement_list
    
    # --- BASIC VALUES ---

    @_('TOK_NUMBER')
    def factor(self, p):
        return p.TOK_NUMBER
    
    @_('TOK_STRING')
    def sting_literal(self, p):
        return p.TOK_STRING[1:-1]

    @_('TOK_TRUE','TOK_FALSE')
    def bool_literal(self, p):
        return {'true' : True,'false': False}[p[0].lower()]
    
    @_('factor', 'sting_literal', 'bool_literal')
    def expr_value(self, p):
        return p[0]

    # --- TYPE SYSTEM ---

    @_('TOK_TYPE_INT', 'TOK_TYPE_STRING', 'TOK_TYPE_FLOAT', 'TOK_TYPE_BOOL', 'TOK_TYPE_LIST')
    def type_definition(self, p):
        return p[0]

    @_('TOK_TYPE_INT', 'TOK_TYPE_STRING', 'TOK_TYPE_FLOAT', 'TOK_TYPE_BOOL' ,'TOK_TYPE_VOID')
    def return_type_definition(self, p):
        return p[0]
    
    @_('')
    def implicit_type(self, p):
        return "AUTO"
    
    @_('TOK_COLON type_definition')
    def explicit_type(self, p):
        return p.type_definition
     
    @_('explicit_type', 'implicit_type')
    def variable_type(self, p):
        return p[0]
    
    #--- LISTS AND EMPTY SLOTS ---
    
    @_('statement')
    def statement_list(self, p):
        return [p.statement]
    
    @_('statement_list statement')
    def statement_list(self, p):
        p.statement_list.append(p.statement)
        return p.statement_list
    
    @_('')
    def empty(self, p):
        return []
    
    @_('statement_list', 'empty')
    def op_statement_list(self, p):
        return p[0]
    
    # --- VAR LOGIC ---

    @_('TOK_VAR TOK_ID variable_type TOK_ASSIGN expr_value')
    def statement(self, p):
        return VarDeclNode(
            var_name = p.TOK_ID,
            var_type = p.variable_type,
            var_value= p.expr_value)
    
    
    # --- FUNCTION LOGIC ---

    @_('TOK_ID TOK_COLON type_definition')
    def paramter(self,p):
        return ParameterNode(
            par_name= p.TOK_ID,
            par_type= p.type_definition
        )
    
    @_('paramter')
    def paramters_list(self,p):
        return [p.paramter]
    
    @_('paramters_list TOK_COMMA paramter')
    def paramters_list(self,p):
        p.paramters_list.append(p.paramter)
        return p.paramters_list

    @_('')
    def paramters_list(self,p):
        return []
    
    @_('op_statement_list')
    def body_def(self, p):
        return BlockNode(p.op_statement_list)
    
    @_('function_def')
    def statement(self, p):
        return p.function_def
    
    @_('TOK_FUNCTION TOK_ID TOK_L_PAREN paramters_list TOK_R_PAREN TOK_ARROW return_type_definition TOK_L_BRACE body_def TOK_R_BRACE')
    def function_def(self, p):
        return FunctionDefNode(
            fn_name=p.TOK_ID,
            fn_parms=p.paramters_list,
            fn_return_type=p.return_type_definition,
            fn_body=p.body_def
        )