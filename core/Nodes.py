##############################################
#Nodes
###############################################

class NumberNode:
    def __init__(self, tok_value):
        self.tok_value = tok_value
    
    def __repr__(self):
        return f"{self.tok_value}"

class BinOpNode:
    def __init__(self, left_node, op_tok, right_node):
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node

    def __repr__(self):
        return f"{self.left_node}, {self.op_tok}, {self.right_node}"

class VarDeclNode:
    def __init__(self, var_name, var_type, var_value):
        self.var_name = var_name
        self.var_type = var_type
        self.var_value = var_value
    
    def __repr__(self):
        return f"Var name : {self.var_name}, var type : {self.var_type}, var value : {self.var_value}"

class FunctionDefNode:
    def __init__(self, fn_name, fn_parms, fn_return_type, fn_body):
        self.fn_name = fn_name
        self.fn_parms = fn_parms
        self.fn_return_type = fn_return_type
        self.fn_body = fn_body
        
    def __repr__(self):
        return f"(function name : {self.fn_name}, function parms : {self.fn_parms}, function return type : {self.fn_return_type}, function body : {self.fn_body})"

class ParameterNode:
    def __init__(self, par_name, par_type):
        self.par_name = par_name
        self.par_type = par_type
    
    def __repr__(self):
        return f"par name :{self.par_name}, par type : {self.par_type}"


class BlockNode:
    def __init__(self, statements):
        self.statements = statements
    
    def __repr__(self):
        return f"block statements : {self.statements}"

class RetrunNode:
    def __init__(self, return_value):
        self.return_value = return_value
    
    def __repr__(self):
        return f"return value : {self.return_value}"

class VarAccessNode:
    def __init__(self, var_name):
        self.var_name = var_name
    
    def __repr__(self):
        return f"VariableNode : {self.var_name}"