from syntax_analyzer import VarDeclaration, ArrayDeclaration, FunDeclaration


class Scope:
    def __init__(self, object=None, outer_scope=None):
        self.variables = []
        self.outer_scope = outer_scope
        self.object = object

    def declare_variable(self, var_obj):
        self.variables.append(var_obj)

    def get_variable(self, var_name):
        for var_obj in self.variables:
            if isinstance(var_obj, (VarDeclaration, ArrayDeclaration)) and var_obj.identifier[1] == var_name:
                return var_obj
        if self.outer_scope is not None:
            return self.outer_scope.get_variable(var_name)
        else:
            return None

    def set_object(self, obj):
        self.object = obj

    def get_object(self):
        return self.object

    def has_variable(self, var_name):
        for var_obj in self.variables:
            if isinstance(var_obj, (VarDeclaration, ArrayDeclaration)) and var_obj.identifier[1] == var_name:
                return True
        if self.outer_scope is not None:
            return self.outer_scope.has_variable(var_name)
        else:
            return False

    def get_function(self, func_name):
        for func_obj in self.variables:
            if isinstance(func_obj, FunDeclaration) and func_obj.name[1] == func_name:
                return func_obj
        if self.outer_scope is not None:
            return self.outer_scope.get_function(func_name)
        else:
            return None

    def has_function(self, func_name):
        for func_obj in self.variables:
            if isinstance(func_obj, FunDeclaration) and func_obj.name[1] == func_name:
                return True
        if self.outer_scope is not None:
            return self.outer_scope.has_function(func_name)
        else:
            return False

