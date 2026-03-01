_ = None
from core.lexer import TokenType
import sly
from core.Nodes import *

class Parser(sly.Parser):

    tokens = {i.name for i in TokenType}

    #--------------------------------------------------
    # --- ENTRY POINT ---
    #--------------------------------------------------

    @_('global_statement_list TOK_EOF', 'global_statement_list')
    def program(self, p):
        return p.global_statement_list
    
    #--------------------------------------------------
    # --- STATEMENT TYPES ---
    #--------------------------------------------------

    # --- GLOBAL STATMENT ---

    @_('function_def', 'var_def')
    def global_statement(self, p):
        return p[0]

    # --- LOCAL STATMENT ---
    @_('var_def', 'return_stmt')
    def local_statement(self, p):
        return p[0]

    #--------------------------------------------------
    # --- BASIC VALUES ---
    #--------------------------------------------------

    @_('TOK_NUMBER')
    def factor(self, p):
        return p.TOK_NUMBER
    
    @_('TOK_STRING')
    def sting_literal(self, p):
        return p.TOK_STRING[1:-1]

    @_('TOK_TRUE','TOK_FALSE')
    def bool_literal(self, p):
        return {'true' : True,'false': False}[p[0].lower()]
    
    @_('factor', 'sting_literal', 'bool_literal', 'TOK_ID')
    def expr_value(self, p):

        if hasattr(p, 'TOK_ID'):
            return VarAccessNode(p.TOK_ID)
        
        return p[0]

    #--------------------------------------------------
    # --- TYPE SYSTEM ---
    #--------------------------------------------------

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
    
    #--------------------------------------------------
    # --- EMPTY SLOTS ---
    #--------------------------------------------------

    @_('')
    def empty(self, p):
        return []

    #--------------------------------------------------
    #--- LISTS ---
    #--------------------------------------------------
    
    # --- GLOBAL STATEMENT LIST ---

    @_('global_statement')
    def global_statement_list(self, p):
        return [p.global_statement]

    @_('global_statement_list global_statement')
    def global_statement_list(self, p):
        p.global_statement_list.append(p.global_statement)
        return p.global_statement_list
    
    @_('global_statement_list', 'empty')
    def op_global_statement_list(self, p):
        return p[0]

    # --- LOCAL STATEMENT LIST ----

    @_('local_statement')
    def local_statement_list(self, p):
        return [p.local_statement]

    @_('local_statement_list local_statement')
    def local_statement_list(self, p):
        p.local_statement_list.append(p.local_statement)
        return p.local_statement_list
    
    @_('local_statement_list', 'empty')
    def op_local_statement_list(self, p):
        return p[0]

    #--------------------------------------------------
    # --- VAR LOGIC ---
    #--------------------------------------------------
    @_('TOK_VAR TOK_ID variable_type TOK_ASSIGN expr_value')
    def var_def(self, p):
        return VarDeclNode(
            var_name = p.TOK_ID,
            var_type = p.variable_type,
            var_value= p.expr_value)
    
    #--------------------------------------------------
    # --- FUNCTION LOGIC ---
    #--------------------------------------------------

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
    
    @_('TOK_L_BRACE op_local_statement_list TOK_R_BRACE')
    def body_def(self, p):
        return BlockNode(p.op_local_statement_list)
    
    @_('TOK_FUNCTION TOK_ID TOK_L_PAREN paramters_list TOK_R_PAREN TOK_ARROW return_type_definition body_def')
    def function_def(self, p):
        return FunctionDefNode(
            fn_name=p.TOK_ID,
            fn_parms=p.paramters_list,
            fn_return_type=p.return_type_definition,
            fn_body=p.body_def
        )

    #--------------------------------------------------
    # --- RETURN ---
    #--------------------------------------------------

    @_('TOK_RETURN expr_value')
    def return_stmt(self ,p):
        return RetrunNode(return_value=p.expr_value)
    