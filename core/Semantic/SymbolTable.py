from dataclasses import dataclass, field
from typing import Any, Optional, List , Dict
import enum


class SymbolKind(enum.Enum):
    VARIABLE = enum.auto()
    FUNCTION = enum.auto()
    PARAMETER = enum.auto()

class DataTypes(enum.Enum):
    INT = enum.auto()
    FLOAT = enum.auto()
    STRING = enum.auto()
    BOOL = enum.auto()
    LIST = enum.auto()
    VOID = enum.auto()
    AUTO   = enum.auto()

TYPE_MAP: Dict[str, DataTypes] = {
    "int" : DataTypes.INT,
    "float" : DataTypes.FLOAT,
    "string" : DataTypes.STRING,
    "bool" : DataTypes.BOOL,
    "list" : DataTypes.LIST,
    "void" : DataTypes.VOID,
    "AUTO" : DataTypes.AUTO,
}

def get_type(type_str: str) -> DataTypes:
    result = TYPE_MAP.get(type_str.lower() if type_str != "AUTO" else "AUTO")
    if result is None:
        raise Exception(f"Semantic Error: Unknown type '{type_str}'") 
    return result

#--------------------------------------------------
# --- SYMBOL ---
#--------------------------------------------------

@dataclass
class Symbol:
    name : str
    kind : SymbolKind
    type : DataTypes
    scope_level : int = 0
    value : Any = None
    # --- FUNCTION ONLY ---
    params : List[Any] = field(default_factory=list)
    return_type : DataTypes = DataTypes.VOID

#--------------------------------------------------
# --- SYMBOLTABLE ---
#--------------------------------------------------

class SymbolTable:
    def __init__(self,name:str ,parent : Optional['SymbolTable'] = None, is_loop : bool = False, scope_level : int = 0):
        self.name = name
        self.parent = parent
        self.symbols : Dict[str, Symbol] = {}
        self.children : List['SymbolTable'] = []
        self.is_loop = is_loop
        self.scope_level : int = scope_level
    
    def define(self, name : str, symbol : Symbol):
        if name in self.symbols:
            raise Exception (f"This variable {name} has been already declared in this scope.")
        
        symbol.scope_level = self.scope_level
        self.symbols[name] = symbol
        
    def lookup(self ,name : str):
        #Check the current scope
        if name in self.symbols:
            return self.symbols[name]
        
        #Check the upper scope
        if self.parent is not None:
            return self.parent.lookup(name)

        return None

    def lookup_local(self , name : str) -> Optional[Symbol]:
        return self.symbols.get(name)
    
    def is_inside_loop(self) -> bool:
        if self.is_loop:
            return True
        return self.parent.is_inside_loop() if self.parent else False
    
#--------------------------------------------------
# --- SCOPE MANGER ---
#--------------------------------------------------

class ScopeManager:
    def __init__(self):
        self.global_scope : SymbolTable = SymbolTable(name="global", scope_level=0)
        self.current_scope : SymbolTable = self.global_scope
        self.scope_stack : List[SymbolTable] = [self.global_scope]
        self.current_function : Optional[Symbol] = None 
    
    def scope_enter(self, name :str, is_loop :bool = False):
        level = len(self.scope_stack)
        new_scope = SymbolTable(
            name = name,
            parent=self.current_scope,
            is_loop=is_loop,
            scope_level=level
        )
        self.current_scope.children.append(new_scope)
        self.current_scope = new_scope
        self.scope_stack.append(new_scope)
        print(f"Entering new scope: '{name}' : (level={level}, (loop={is_loop})")

    def scope_exit(self):
        if len(self.scope_stack) > 1:
            exited = self.scope_stack.pop()
            self.current_scope = self.scope_stack[-1]
            print(f"Exited scope '{exited.name}'. Returned to '{self.current_scope.name}'")
        else:
            raise Exception("Semantic Error: Cannot exit the global scope.")
    
    #--------------------------------------------------

    def define(self, name :str, symbol : Symbol):
        self.current_scope.define(name,symbol)

    def lookup(self, name: str) -> Optional[Symbol]:
        return self.current_scope.lookup(name)
    
    def lookup_local(self, name : str):
        return self.current_scope.lookup_local(name)
    
    #--------------------------------------------------
    def check_loop_validity(self):
        if not self.current_scope.is_inside_loop():
            raise Exception("Semantic Error: 'break'/'continue' used outside of a loop.")
    
    #--------------------------------------------------

    def enter_function(self, fn_symbol : Symbol , scope_name: str):
        self.scope_enter(scope_name)
        self.current_function = fn_symbol
    
    def exit_function(self):
        self.scope_exit()
        self.current_function = None
    
    def get_current_function(self) -> Optional[Symbol]:
        return self.current_function

