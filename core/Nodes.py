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
        return f"{self.var_name}, {self.var_type}, {self.var_value}"

class FunctionDefNode:
    def __init__(self, fn_name, fn_parms, fn_return_type, fn_body):
        self.fn_name = fn_name
        self.fn_parms = fn_parms
        self.fn_return_type = fn_return_type
        self.fn_body = fn_body
        
    def __repr__(self):
        return f"{self.fn_name}, {self.fn_parms}, {self.fn_return_type}, {self.fn_body}"

class ParameterNode:
    def __init__(self, par_name, par_type):
        self.par_name = par_name
        self.par_type = par_type
    
    def __repr__(self):
        return f'{self.par_name}, {self.par_type}'


class BlockNode:
    def __init__(self, statements):
        self.statements = statements
    
    def __repr__(self):
        return f"{self.statements}"

class RetrunNode:
    def __init__(self, return_value):
        self.return_value = return_value
    
    def __repr__(self):
        return f"{self.return_value}"
