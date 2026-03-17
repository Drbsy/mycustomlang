from core.Parser.Nodes import *
from core.Semantic.SymbolTable import (
    ScopeManager, Symbol, SymbolKind, DataTypes, get_type
    )

class TypeCherker:
    def __init__(self):
        self.scope  = ScopeManager()
    
    #--------------------------------------------------
    # --- ENTRY POINT ---
    #--------------------------------------------------

    def check(self , node) -> DataTypes:
        match node:
            case bool():
                return DataTypes.BOOL
            case int():
                return DataTypes.INT
            case float():
                return DataTypes.FLOAT
            case str():
                return DataTypes.STRING
            case list():
                return DataTypes.LIST
            case None:
                return DataTypes.VOID

        method_name = f"check_{type(node).__name__}"
        method = getattr(self , method_name , None)

        if method is None:
            raise Exception(f"Type Checker : No handler exist for the node '{type(node).__name__}'")
        
        return method(node)
    
    #--------------------------------------------------
    # --- VARIABLES ---
    #--------------------------------------------------

    def check_VarAccessNode(self , node : VarAccessNode) -> DataTypes:
        symbol = self.scope.lookup(node.var_name)

        if Symbol is None:
            raise Exception(f"Type Checker : The Var '{type(node).__name__}' is not declared")
        
        return symbol.type

    def check_VarDeclNode(self , node : VarDeclNode) -> DataTypes:
        value_type = self.check(node.var_value)
        declared_type = self.check(node.var_type)

        if declared_type == DataTypes.AUTO:
            resolved_type = value_type
        
        else:
            if declared_type != value_type:
                raise Exception(
                    f"Type Error : var '{node.var_name} is declared as type'"
                    f"assigned value of type {value_type.name}"
                )
            resolved_type = declared_type
        
        Symbol = Symbol(
            name = node.var_name,
            kind = SymbolKind.VARIABLE,
            type = resolved_type
        )
        self.scope.define(node.var_name, Symbol)

        return resolved_type

    def check_AssignNode(self, node: AssignNode) -> DataTypes:
        symbol = self.scope.lookup(node.var_name)
        if symbol is None:
            raise Exception(f"Type Error: var '{node.var_name}' is not declared")
        
        if symbol.kind == SymbolKind.FUNCTION:
            raise Exception(
                f"Type Error: '{symbol.name}' is a func"
                f"func cannot be reassigned"
            )
        
        symbol_type = self.check(node.value)

        if symbol.type == DataTypes.AUTO:
            symbol.type = symbol_type
            return symbol_type
        if symbol.type == DataTypes.FLOAT and symbol_type == DataTypes.INT:
            return DataTypes.FLOAT
        
        if symbol.type == symbol_type:
            return symbol.type
        else:
            raise Exception(f"Type Error: Cannot assign '{symbol_type.name}' to '{symbol.name}' which is of type '{symbol.type.name}'")

    #--------------------------------------------------
    # --- OPERATORS ---
    #--------------------------------------------------

    def check_BinOpNode(self, node : BinOpNode) -> DataTypes:
        left = self.check(node.left_node)
        right = self.check(node.right_node)
        op = {'+', '-', '/', '*', '**'}
        numeric  = {DataTypes.FLOAT, DataTypes.INT}

        if node.op_tok in op:

            if node.op_tok == '+' and left == DataTypes.STRING and right == DataTypes.STRING:
                return DataTypes.STRING
            
            if left in numeric  and right in numeric:
                if left == DataTypes.INT and right == DataTypes.INT:
                    return DataTypes.INT
                else:
                    return DataTypes.FLOAT
            
            raise Exception(
                f"Type Error : Cannot '{node.op_tok}' between '{left.name}' and '{right.name}'"
                )
        
        raise Exception(
            f"Type Error : unknown binary operator '{node.op_tok}'"
            )

    def check_UnaryOpNode(self, node : UnaryOpNode) -> DataTypes:
        operand = self.check(node.node)
        numeric  = {DataTypes.FLOAT, DataTypes.INT}
        not_ops = {'not', '!'}

        if node.op_tok == '-':
            if operand in numeric :
                return operand
            raise Exception(
                f"Type Error : unary '-' to a value of type '{operand.name}'"
                )
        
        if node.op_tok in not_ops:
            if operand == DataTypes.BOOL:
                return DataTypes.BOOL
            
            raise Exception(
                f"Type Error : '{node.op_tok}' requires a bool operand, got '{operand.name}'"
            )
    
        raise Exception(
            f"Type Error : Unknown unary operator '{node.op_tok}'"
            )
    
    def check_LogicalOpNode(self, node : LogicalOpNode) -> DataTypes:
        left = self.check(node.left_node)
        right = self.check(node.right_node)

        if left == DataTypes.BOOL and right == DataTypes.BOOL:
            return DataTypes.BOOL
        
        raise Exception(
            f"TypeError: Cannot apply logical operator '{node.op_tok}' to types '{left.name}' and '{right.name}' — boolean values required."
        )
    
    def check_ChainedComparisonNode(self, node : ChainedComparisonNode ) -> DataTypes: 
        left = self.check(node.left_operand)
        numeric  = {DataTypes.FLOAT, DataTypes.INT}
        valid_ops = {'==', '!=', '<', '>', '<=', '>='}

        for op, operand in node.comparisons:
            
            if op not in valid_ops:
                raise Exception(
                    f"Type Error: Unknown comparison operator '{op}'"
                )
        
            right = self.check(operand)

            if op in ('==', '!='):
                
                if left in numeric and right in numeric:
                    pass

                elif left != right :
                    raise Exception(
                        f"Type Eroor : '{op}' is not valid to compare '{left.name}' and '{right.name}'"
                    )
            else : 
                if left not in numeric or right not in numeric:
                    raise Exception(
                        f"Type Error: Operator '{op}' requires numeric types,got '{left.name}' and '{right.name}' "
                    )
            
            left = right
        
        return DataTypes.BOOL

    #--------------------------------------------------
    # --- COLLECTIONS ---
    #--------------------------------------------------


    def check_ListNode(self, node: ListNode) -> DataTypes:
        for elem in node.elements:
            self.check(elem)
        return DataTypes.LIST

    def check_IndexAccessNode(self, node : IndexAccessNode) -> DataTypes:
        container_type = self.check(node.container)
        index_type = self.check(node.index)

        if container_type != DataTypes.LIST:
            raise Exception(
                f"Type Error: Index access '[]' requires a 'list', got '{container_type.name}'"
            )

        if index_type != DataTypes.INT:
            raise Exception(
            f"Type Error: List index must be 'int', got '{index_type.name}'"
        )

        return DataTypes.AUTO
    
    
    #--------------------------------------------------
    # --- FUNCTIONS ---
    #--------------------------------------------------

    def check_FunctionDefNode(self, node : FunctionDefNode):
        return_type = None

        if node.fn_return_type != "AUTO":
            return_type = get_type(node.fn_return_type)
        else :
            return_type = DataTypes.AUTO

        param_symbols = []

        for p in node.fn_parms:
            param_symbols.append(Symbol(
                name=p.par_name,
                kind=SymbolKind.PARAMETER,
                type=get_type(p.par_type)
                )
            )

        fn_symbol = Symbol(
            name=node.fn_name,
            kind=SymbolKind.FUNCTION,
            type=return_type,
            params=param_symbols,
            return_type=return_type
        )

        self.scope.define(node.fn_name, fn_symbol)

        self.scope.enter_function(fn_symbol, f"fn:{node.fn_name}")

        for param_sym in param_symbols:
            self.scope.define(param_sym.name, param_sym)

        self.check_BlockNode(node.fn_body)

        self.scope.exit_function()
        return DataTypes.VOID

    def check_CallNode(self, node: CallNode) -> DataTypes:
        symbol = self.scope.lookup(node.fn_name)
        
        if symbol is None:
            raise Exception(
            f"Type Error: Func '{node.fn_name}' does nt exist"
        )
        if symbol.kind != SymbolKind.FUNCTION:
            raise Exception(
            f"Type Error: '{node.fn_name}' is not a func"
        )

        if len(node.args) != len(symbol.params):
            raise Exception(
                f"Type Error: '{node.fn_name}' expects {len(symbol.params)} argument(s), "
                f"got {len(node.args)}"
            )
        
        for i, (arg, param) in enumerate(zip(node.args, symbol.params)):
            arg_type = self.check(arg)

            if param.type == DataTypes.FLOAT and arg_type == DataTypes.INT:
                continue

            if param.type != DataTypes.AUTO and arg_type != param.type:
                raise Exception(
                    f"Type Error: Argument {i + 1} of '{node.fn_name}' "
                    f"expects '{param.type.name}', got '{arg_type.name}'"
                )

        return symbol.return_type
    

    def check_BlockNode(self, node : BlockNode):
        if node.statements:
            for stmt in node.statements:
                self.check(stmt)
        return DataTypes.VOID
    
    def check_IfNode(self, node: IfNode):


        for condition, body in node.cases:
            cond_type = self.check(condition)
            

            if cond_type != DataTypes.BOOL:
                raise Exception(
                f"Type Error: if/elif condition must be bool, got '{cond_type.name}'"
            )

            self.scope.scope_enter("if_block")
            self.check_BlockNode(body)
            self.scope.scope_exit()


        if node.else_case:
            self.scope("else_block")
            self.check_BlockNode(node.else_case)
            self.scope.scope_exit
        
        return DataTypes.VOID
    
    def check_WhileNode(self, node: WhileNode) -> DataTypes:
        cond_type = self.check(node.condition)

        if cond_type != DataTypes.BOOL:
                raise Exception(
                f"Type Error: while condition must be bool, got {cond_type.name}"
            )
        
        self.scope.scope_enter("while_block", is_loop=True)
        self.check_BlockNode(node.body)
        self.scope.scope_exit()
        return DataTypes.VOID

    #TODO Control Flow 
    #! BlockNode | IfNode | WhileNode | ForNode | ReturnNode | BreakNode | ContinueNode
