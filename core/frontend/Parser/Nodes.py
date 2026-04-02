
from dataclasses import dataclass
from typing import Any, List

# --- EXPRESSION NODES (Math & Logic) ---

@dataclass
class BinOpNode:
    left_node : Any
    op_tok : Any
    right_node : Any

@dataclass
class UnaryOpNode:
    op_tok : Any
    node : Any
 
@dataclass
class LogicalOpNode:
    left_node : Any
    op_tok : Any
    right_node : Any

@dataclass
class ChainedComparisonNode:
    left_operand : Any
    comparisons : List[Any]

# --- VARIABLE NODES ---

@dataclass
class VarDeclNode:
    var_name : Any
    var_type : Any
    var_value : Any

@dataclass
class VarAccessNode:
    var_name  : Any

@dataclass
class AssignNode:
    var_name : Any
    value : Any

@dataclass
class ListNode:
    elements : List[Any]
    
@dataclass
class IndexAccessNode:
    container : Any
    index : Any
        
# --- FUNCTION & BLOCK NODES ---

@dataclass
class FunctionDefNode:
    fn_name : Any
    fn_parms : List[Any]
    fn_return_type : Any
    fn_body : Any

@dataclass
class ParameterNode:
    par_name : Any
    par_type : Any

@dataclass
class BlockNode:
    statements : List[Any]
    

@dataclass
class CallNode:
    fn_name : Any
    args : List[Any]

# --- CONTROL FLOW NODES ---

@dataclass
class IfNode:
    cases : List[Any]
    else_case : Any

@dataclass
class ReturnNode:
    return_value : Any

@dataclass
class WhileNode:
    condition : Any
    body : Any

@dataclass
class ForNode:
    var_name : Any
    iterable : Any
    body : Any

@dataclass
class BreakNode:
    pass

@dataclass
class ContinueNode:
    pass