from core.frontend.Semantic.TypeChecker import TypeCherker

class Analyzer:
    def __init__(self):
        self.type_checker = TypeCherker()
        self.errors = []

    def analyze(self , ast):
        if not ast :
            print("ast is emty")
            return
        
        for node in ast:
            try:
                self.type_checker.check(node)
            except Exception as e:
                self.errors.append(str(e))
            

        if self.errors:
            print("Semactic Errors")
            for error in self.errors:
                print(f"{error}")
            
            else:
                print("\nno error found")
