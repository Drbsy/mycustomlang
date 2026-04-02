_ = None
from core.frontend.Lexer.Lexer import TokenType
from core.frontend.Parser.Nodes import *
import sly

class Parser(sly.Parser):

    tokens = {i.name for i in TokenType}

    precedence = (
        ('left', 'TOK_OR'),
        ('left', 'TOK_AND'),
        ('right', 'TOK_NOT'),
        ('left', 'TOK_EQUAL_TO', 'TOK_NOT_EQUAL_TO'),
        ('left', 'TOK_GREATER', 'TOK_GREATER_EQUAL', 'TOK_LESS', 'TOK_LESS_EQUAL'),
        ('left', 'TOK_PLUS', 'TOK_MINUS'),
        ('left', 'TOK_STAR', 'TOK_SLASH'),
        ('right', 'UMINUS'),
    )

    #--------------------------------------------------
    # --- ENTRY POINT ---
    #--------------------------------------------------

    @_('global_statement_list TOK_EOF', 'global_statement_list', 'empty')
    def program(self, p):
        return p[0] if p[0] else []
    
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
    
    @_('expr_value TOK_L_BRACKET logical_or TOK_R_BRACKET')
    def primary_expr(self ,p):
        return IndexAccessNode(container=p.expr_value, index=p.logical_or)
    
    # ---  COMPARISON STATEMENT LIST ----

    @_('comparison_pair')
    def comparison_list(self, p):
        return [p.comparison_pair]
    
    @_('comparison_list comparison_pair')
    def comparison_list(self, p):
        p.comparison_list.append(p.comparison_pair)
        return p.comparison_list
    
    #--------------------------------------------------
    # --- STATEMENT TYPES ---
    #--------------------------------------------------

    # --- GLOBAL STATEMENT ---

    @_('function_def', 'var_def', 'if_stmt', 'while_stmt', 'for_stmt',
        'loop_control_stmt', 'assign_stmt', 'compound_assign_stmt', 'expr_stmt')
    def global_statement(self, p):
        return p[0]

    # --- LOCAL STATEMENT ---

    @_('var_def', 'return_stmt', 'if_stmt', 'while_stmt', 'for_stmt',
        'loop_control_stmt', 'assign_stmt', 'compound_assign_stmt', 'expr_stmt')
    def local_statement(self, p):
        return p[0]

    #--------------------------------------------------
    # --- BASIC VALUES ---
    #--------------------------------------------------

    @_('TOK_NUMBER')
    def factor(self, p):
        return p.TOK_NUMBER
    
    @_('TOK_STRING')
    def string_literal(self, p):
        return p.TOK_STRING[1:-1]

    @_('TOK_TRUE','TOK_FALSE')
    def bool_literal(self, p):
        return {'true' : True,'false': False}[p[0].lower()]
    
    @_('factor', 'string_literal', 'bool_literal', 'TOK_ID', 'primary_expr', 'list_literal')
    def expr_value(self, p):

        if hasattr(p, 'TOK_ID'):
            return VarAccessNode(p.TOK_ID)
        
        return p[0]

    @_('logical_or')
    def expr_stmt(self, p):
        return p[0]
    
    @_('TOK_L_PAREN logical_or TOK_R_PAREN')
    def primary_expr(self, p):
        return p.logical_or

    # --- FUNCTION CALLS ---

    @_('TOK_ID TOK_L_PAREN arguments_list TOK_R_PAREN')
    def primary_expr(self, p):
        return CallNode(fn_name=p.TOK_ID , args=p.arguments_list)
    
    # --- List ---

    @_('TOK_L_BRACKET list_contents TOK_R_BRACKET')
    def list_literal(self, p):
        return ListNode(p.list_contents)
    
    @_('logical_or TOK_COMMA list_contents',
       'logical_or',
       'empty')
    def list_contents(self, p):
        if hasattr(p, 'list_contents'):
            return [p.logical_or] + p.list_contents
        elif hasattr(p, 'logical_or'):
            return [p.logical_or]
        return []

    #--------------------------------------------------
    # --- ARITHMETIC ---
    #--------------------------------------------------

    @_('arithmetic TOK_PLUS arithmetic',
       'arithmetic TOK_MINUS arithmetic',
       'arithmetic TOK_STAR arithmetic',
       'arithmetic TOK_SLASH arithmetic')
    def arithmetic(self, p):
        return BinOpNode(left_node= p[0], op_tok=p[1], right_node=p[2])
    
    @_('expr_value') 
    def arithmetic(self, p):
        return p[0]
    
    @_('TOK_MINUS arithmetic %prec UMINUS')
    def arithmetic(self, p):
        return UnaryOpNode(op_tok='-', node=p.arithmetic)

    @_('TOK_ID TOK_PLUS_ASSIGN logical_or',
       'TOK_ID TOK_MINUS_ASSIGN logical_or',
       'TOK_ID TOK_STAR_ASSIGN logical_or',
       'TOK_ID TOK_SLASH_ASSIGN logical_or')
    def compound_assign_stmt(self, p):
        op_map = {'+=' : '+',
              '-=' : '-',
              '*=' : '*',
              '/=' : '/'}
        
        return AssignNode(var_name=p.TOK_ID,
            value=BinOpNode(
                left_node=VarAccessNode(p[0]), 
                op_tok=op_map[p[1]], 
                right_node=p.logical_or
                )  
    ) 
    
    #--------------------------------------------------
    # --- COMPARISON ---
    #--------------------------------------------------

    @_('TOK_EQUAL_TO arithmetic',
       'TOK_NOT_EQUAL_TO arithmetic',
       'TOK_GREATER arithmetic',
       'TOK_GREATER_EQUAL arithmetic',
       'TOK_LESS arithmetic',
       'TOK_LESS_EQUAL arithmetic')
    def comparison_pair(self, p):
        return (p[0], p.arithmetic)

    @_('arithmetic comparison_list')
    def comparison(self, p):
        return ChainedComparisonNode(left_operand=p.arithmetic, comparisons=p.comparison_list)
    
    @_('arithmetic') 
    def comparison(self, p):
        return p[0]

    #--------------------------------------------------
    # --- LOGICAL OPERATORS ---
    #--------------------------------------------------

    # --- OR ---
    @_('logical_and TOK_OR logical_or',
       'logical_and')
    def logical_or(self, p):
        if len(p)>1:
            return LogicalOpNode(left_node=p[0], op_tok=p[1], right_node=p[2])
        return p[0]
    
    # --- AND ---

    @_('logical_not TOK_AND logical_and',
       'logical_not')
    def logical_and(self, p):
        if len(p)>1:
            return LogicalOpNode(left_node=p[0], op_tok=p[1], right_node=p[2])
        return p[0]

    # --- NOT ---

    @_('TOK_NOT logical_not')
    def logical_not(self, p):
        return UnaryOpNode(op_tok=p[0],node=p.logical_not)
    
    @_('comparison')
    def logical_not(self,p):
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
    
    @_('empty')
    def implicit_type(self, p):
        return "AUTO"
    
    @_('TOK_COLON type_definition')
    def explicit_type(self, p):
        return p.type_definition
     
    @_('explicit_type', 'implicit_type')
    def variable_type(self, p):
        return p[0]
    
    #--------------------------------------------------
    # --- VAR LOGIC ---
    #--------------------------------------------------

    @_('TOK_VAR TOK_ID variable_type TOK_ASSIGN logical_or')
    def var_def(self, p):
        return VarDeclNode(
            var_name = p.TOK_ID,
            var_type = p.variable_type,
            var_value= p.logical_or)
    
    @_('TOK_ID TOK_ASSIGN logical_or')
    def assign_stmt(self, p):
        return AssignNode(var_name=p.TOK_ID , value=p.logical_or)

    #--------------------------------------------------
    # --- FUNCTION LOGIC ---
    #--------------------------------------------------
    
    @_('TOK_ID TOK_COLON type_definition')
    def parameter(self,p):
        return ParameterNode(
            par_name= p.TOK_ID,
            par_type= p.type_definition
        )
    
    @_('parameter')
    def parameters_list(self,p):
        return [p.parameter]
    
    @_('parameters_list TOK_COMMA parameter')
    def parameters_list(self,p):
        p.parameters_list.append(p.parameter)
        return p.parameters_list

    @_('empty')
    def parameters_list(self,p):
        return []
    
    @_('TOK_L_BRACE op_local_statement_list TOK_R_BRACE')
    def body_def(self, p):
        return BlockNode(p.op_local_statement_list)
    
    @_('TOK_FUNCTION TOK_ID TOK_L_PAREN parameters_list TOK_R_PAREN TOK_ARROW return_type_definition body_def')
    def function_def(self, p):
        return FunctionDefNode(
            fn_name=p.TOK_ID,
            fn_parms=p.parameters_list,
            fn_return_type=p.return_type_definition,
            fn_body=p.body_def
        )

    @_('TOK_FUNCTION TOK_ID TOK_L_PAREN parameters_list TOK_R_PAREN body_def')
    def function_def(self, p):
        return FunctionDefNode(
            fn_name=p.TOK_ID,
            fn_parms=p.parameters_list,
            fn_return_type="AUTO",
            fn_body=p.body_def
        )

    # --- CALL FUNCTION LOGIC ---

    @_('logical_or')
    def arguments_list(self, p):
        return [p.logical_or]

    @_('arguments_list TOK_COMMA logical_or')
    def arguments_list(self, p):
        p.arguments_list.append(p.logical_or)
        return p.arguments_list
    
    @_('empty')
    def arguments_list(self, p):
        return []


    #--------------------------------------------------
    # --- CONTROL FLOW ---
    #--------------------------------------------------

    # --- IF/ELIF/ELSE ---

    # --- IF / ELSE ----

    @_('TOK_IF TOK_L_PAREN logical_or TOK_R_PAREN body_def elif_blocks TOK_ELSE body_def')
    def if_stmt(self, p):
        all_cases = [(p.logical_or, p.body_def0)] + p.elif_blocks 
        return IfNode(cases=all_cases, else_case=p.body_def1)

    @_('TOK_IF TOK_L_PAREN logical_or TOK_R_PAREN body_def elif_blocks')
    def if_stmt(self, p):
        all_cases = [(p.logical_or, p.body_def)] + p.elif_blocks 
        return IfNode(cases=all_cases, else_case=None)
    
    # --- ELIF ----
    @_('TOK_ELIF TOK_L_PAREN logical_or TOK_R_PAREN body_def elif_blocks')
    def elif_blocks(self ,p):
        return [(p.logical_or, p.body_def)] + p.elif_blocks 
    
    @_('empty')
    def elif_blocks(self, p):
        return []
    
    # --- RETURN ---

    @_('TOK_RETURN [ logical_or ] ')
    def return_stmt(self ,p):
        return ReturnNode(return_value=p.logical_or)
    
    # --- WHILE ---

    @_('TOK_WHILE_LOOP TOK_L_PAREN logical_or TOK_R_PAREN body_def')
    def while_stmt(self, p):
        return WhileNode(condition=p.logical_or , body=p.body_def)
    
    # --- FOR ---

    @_('TOK_FOR TOK_L_PAREN TOK_ID TOK_IN logical_or TOK_R_PAREN body_def')
    def for_stmt(self, p):
        return ForNode(var_name=p.TOK_ID, iterable=p.logical_or,body=p.body_def)
    
    # --- BREAK / CONTINUE ---

    @_('TOK_BREAK', 'TOK_CONTINUE')
    def loop_control_stmt(self, p):
        if hasattr(p, 'TOK_BREAK'):
            return BreakNode()
        return ContinueNode()
    
    #--------------------------------------------------
    # --- UTILITIES ---
    #--------------------------------------------------

    @_('')
    def empty(self, p):
        return []
    
    
