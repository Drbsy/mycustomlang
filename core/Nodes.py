##############################################
# Nodes
##############################################

# --- EXPRESSION NODES (Math & Logic) ---

class BinOpNode:
    def __init__(self, left_node, op_tok, right_node):
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node

    def __repr__(self):
        return f"BinOpNode(Left node: {self.left_node}, op : {self.op_tok}, Right node: {self.right_node})"

class UnaryOpNode:
    def __init__(self, op_tok, node):
        self.op_tok = op_tok
        self.node = node
    
    def __repr__(self):
        return f"UnaryOpNode(op_tok : {self.op_tok}, node : {self.node})"

class LogicalOpNode:
    def __init__(self, left_node, op_tok, right_node):
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node
    
    def __repr__(self):
        return f"LogicalOpNode(Left node: {self.left_node}, op : {self.op_tok}, Right node: {self.right_node})"

class ChainedComparisonNode:
    def __init__(self, left_operand, comparisons):
        self.left_operand = left_operand
        self.comparisons = comparisons

    def __repr__(self):
        return f"ChainedComparisonNode(Left operand {self.left_operand}, comparisons : {self.comparisons})"

# --- VARIABLE NODES ---

class VarDeclNode:
    def __init__(self, var_name, var_type, var_value):
        self.var_name = var_name
        self.var_type = var_type
        self.var_value = var_value
    
    def __repr__(self):
        return f"VarDeclNode(Var name : {self.var_name}, var type : {self.var_type}, var value : {self.var_value})"

class VarAccessNode:
    def __init__(self, var_name):
        self.var_name = var_name
    
    def __repr__(self):
        return f"VarAccessNode(VariableNode : {self.var_name})"

class AssignNode:
    def __init__(self, var_name, value):
        self.var_name = var_name
        self.value = value

    def __repr__(self):
        return f"AssignNode(var : {self.var_name}, value : {self.value})"
        
# --- FUNCTION & BLOCK NODES ---

class FunctionDefNode:
    def __init__(self, fn_name, fn_parms, fn_return_type, fn_body):
        self.fn_name = fn_name
        self.fn_parms = fn_parms
        self.fn_return_type = fn_return_type
        self.fn_body = fn_body
        
    def __repr__(self):
        return f"FunctionDefNode(function name : {self.fn_name}, function parms : {self.fn_parms}, function return type : {self.fn_return_type}, function body : {self.fn_body})"

class ParameterNode:
    def __init__(self, par_name, par_type):
        self.par_name = par_name
        self.par_type = par_type
    
    def __repr__(self):
        return f"ParameterNode(par name :{self.par_name}, par type : {self.par_type})"

class BlockNode:
    def __init__(self, statements):
        self.statements = statements
    
    def __repr__(self):
        return f"BlockNode(block statements : {self.statements})"

class CallNode:
    def __init__(self, fn_name, args):
        self.fn_name = fn_name
        self.args = args

    def __repr__(self):
        return f"CallNode(fn_name : {self.fn_name}, args : {self.args})"

# --- CONTROL FLOW NODES ---

class IfNode:
    def __init__(self, cases, else_case):
        self.cases = cases
        self.else_case = else_case

    def __repr__(self):
        return f"IfNode(cases: {self.cases}, else : {self.else_case})"

class ReturnNode:
    def __init__(self, return_value):
        self.return_value = return_value
    
    def __repr__(self):
        return f"ReturnNode(return value : {self.return_value})"

class WhileNode:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body
    
    def __repr__(self):
        return f"WhileNode(condition : {self.condition}, body : {self.body})"
    
class ForNode:
    def __init__(self, var_name, iterable, body):
        self.var_name = var_name
        self.iterable = iterable
        self.body = body
    
    def __repr__(self):
        return f"ForNode(var_name : {self.var_name}, iterable : {self.iterable}, body : {self.body})"
    

class BreakNode:
    def __repr__(self):
        return "BreakNode()"

class ContinueNode:
    def __repr__(self):
        return "ContinueNode()"