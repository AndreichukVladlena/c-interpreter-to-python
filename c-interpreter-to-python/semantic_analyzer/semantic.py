from semantic_analyzer.scope import Scope
from syntax_analyzer import *
from semantic_analyzer import *

class SemanticAnalyzer:
    def __init__(self):
        self.global_scope = Scope()
        self.current_scope = self.global_scope

    def analyze(self, expr):
        if isinstance(expr, VarDeclaration):
            self.validate_variable_declaration(expr)
        elif isinstance(expr, FunDeclaration):
            self.validate_function_declaration(expr)
        elif isinstance(expr, ReturnStatement):
            self.validate_return_statement(expr)
        elif isinstance(expr, IfStatement):
            self.validate_if_statement(expr)
        elif isinstance(expr, WhileStatement):
            self.validate_while_statement(expr)
        elif isinstance(expr, ForStatement):
            self.validate_for_statement(expr)
        elif isinstance(expr, BreakStatement):
            self.validate_break_statement(expr)
        elif isinstance(expr, ContinueStatement):
            self.validate_continue_statement(expr)
        elif isinstance(expr, Block):
            self.validate_block(expr)
        elif isinstance(expr, ExpressionStatement):
            self.validate_expression_statement(expr)
        elif isinstance(expr, Call):
            self.validate_function_call(expr)
        elif isinstance(expr, CallProperty):
            self.validate_call_property(expr)
        elif isinstance(expr, ArrayInitialization):
            self.validate_array_initialization(expr)
        elif isinstance(expr, ArrayDeclaration):
            self.validate_array_declaration(expr)
        elif isinstance(expr, ArrayRef):
            self.validate_array_reference(expr)
        elif isinstance(expr, Equality):
            self.validate_equality(expr)
        elif isinstance(expr, Variable):
            self.validate_variable(expr)

    def validate_variable_declaration(self, var_decl):
        if var_decl.var_type[1] not in ['int', 'float', 'char', 'void', 'long int', 'long long int', 'const int',
                                        'const float', 'const double']:
            raise Exception(f"Incorrect data type: {var_decl.var_type[1]}.")

        self.current_scope.declare_variable(var_decl)

        var_type = None
        if var_decl.initializer:
            self.analyze(var_decl.initializer)
            value = var_decl.initializer
            if isinstance(value, Variable):
                var_name = value.name[1]
                if not self.current_scope.has_variable(var_name):
                    raise Exception(f"Variable '{var_name}' not found.")
                var_decl = self.current_scope.get_variable(var_name)
                var_type = var_decl.var_type[1]
            elif isinstance(value, Literal):
                var_type = self.determine_literal_type(value)

        # if var_decl.var_type[1] != var_type:
        if var_type not in var_decl.var_type[1]:
            raise Exception("Incorrect literal type.")

    def validate_function_declaration(self, func_decl):
        if func_decl.return_type[1] not in ['int', 'float', 'char', 'void']:
            raise Exception(f"Incorrect data type: {func_decl.return_type}.")

        self.current_scope.declare_variable(func_decl)

        func_scope = Scope(func_decl, outer_scope=self.current_scope)
        self.current_scope = func_scope

        for param in func_decl.parameters:
            self.current_scope.declare_variable(param)

        self.analyze(func_decl.body)

        self.current_scope = self.current_scope.outer_scope

    def validate_return_statement(self, return_stmt):
        if self.current_scope.outer_scope is None or not isinstance(self.current_scope.outer_scope.object, FunDeclaration):
            raise Exception("Return statement used outside of a function.")

        if return_stmt.value:
            if isinstance(return_stmt.value, Variable):
                var_name = return_stmt.value.name[1]
                if not self.current_scope.has_variable(var_name):
                    raise Exception(f"Variable '{var_name}' not found.")
                var_decl = self.current_scope.get_variable(var_name)
                return_type = var_decl.var_type[1]
            elif isinstance(return_stmt.value, Literal):
                return_type = self.determine_literal_type(return_stmt.value)
            else:
                raise Exception("Invalid return value.")

            func_return_type = self.current_scope.outer_scope.object.return_type[1]
            if return_type not in func_return_type and ('float' not in func_return_type and 'int' not in return_type):
                raise Exception("Invalid return type.")
        else:
            if self.current_scope.outer_scope.return_type != "void":
                raise Exception("Return statement requires a value.")

    def validate_if_statement(self, if_stmt):
        self.analyze(if_stmt.condition)
        self.current_scope = Scope(if_stmt, self.current_scope)
        self.analyze(if_stmt.thenBranch)
        if if_stmt.elseBranch:
            self.analyze(if_stmt.elseBranch)
        self.current_scope = self.current_scope.outer_scope

    def validate_while_statement(self, while_stmt):
        self.current_scope = Scope(while_stmt, self.current_scope)
        self.analyze(while_stmt.condition)
        self.analyze(while_stmt.body)
        self.current_scope = self.current_scope.outer_scope

    def validate_for_statement(self, for_stmt):
        self.current_scope = Scope(for_stmt, self.current_scope)
        self.analyze(for_stmt.initializer)
        self.analyze(for_stmt.condition)
        self.analyze(for_stmt.increment)
        self.analyze(for_stmt.body)
        self.current_scope = self.current_scope.outer_scope

    def validate_do_while_statement(self, do_while_stmt):
        self.current_scope = Scope(do_while_stmt, self.current_scope)
        self.analyze(do_while_stmt.body)
        self.analyze(do_while_stmt.condition)
        self.current_scope = self.current_scope.outer_scope

    def validate_break_statement(self, break_stmt):
        if not self.inside_loop_context():
            raise Exception("Break statement outside of loop context.")

    def validate_continue_statement(self, continue_stmt):
        if not self.inside_loop_context():
            raise Exception("Continue statement outside of loop context.")

    def inside_loop_context(self):
        scope = self.current_scope
        while scope.object is not None:
            if isinstance(scope.object, (WhileStatement, ForStatement, DoWhileStatement)):
                return True
            scope = scope.outer_scope
        return False

    def validate_block(self, block):
        block_scope = Scope(block, outer_scope=self.current_scope)
        self.current_scope = block_scope

        for expr in block.statements:
            self.analyze(expr)

        self.current_scope = self.current_scope.outer_scope

    def validate_expression_statement(self, expr_stmt):
        self.analyze(expr_stmt.expression)

    def validate_function_call(self, func_call):
        function_name = func_call.callee.name[1]

        system_func = ['printf', 'scanf']

        function_declaration = self.current_scope.get_function(function_name)

        if not function_declaration and function_name not in system_func:
            raise Exception(f"Function '{function_name}' is not declared.")

        if not isinstance(function_declaration, FunDeclaration) and function_name not in system_func:
            raise Exception(f"'{function_name}' is not a function.")

        if function_name not in system_func:
            if len(func_call.arguments) != len(function_declaration.parameters):
                raise Exception(f"Invalid number of arguments for function '{function_name}'.")

        if function_name not in system_func:
            for arg, param in zip(func_call.arguments, function_declaration.parameters):
                arg_type=None
                if isinstance(arg, Variable):
                    var_name = arg.name[1]
                    if not self.current_scope.has_variable(var_name):
                        raise Exception(f"Variable '{var_name}' not found.")
                    var_decl = self.current_scope.get_variable(var_name)
                    arg_type = var_decl.var_type[1]
                elif isinstance(arg, Literal):
                    arg_type = self.determine_literal_type(arg)

                if arg_type not in param.var_type[1]:
                    raise Exception(
                        f"Invalid type of argument for parameter '{param.identifier[1]}' in function '{function_name}'.")
        if function_name not in system_func:
            return function_declaration.return_type

    def validate_call_property(self, call_property):
        object_name = call_property.object_name
        property_name = call_property.property_obj

        object_var = self.current_scope.get_variable(object_name)
        if not object_var:
            raise Exception(f"Object '{object_name}' not found.")

        if not hasattr(object_var, property_name):
            raise Exception(f"Property '{property_name}' not found in object '{object_name}'.")

    def validate_array_initialization(self, array_init):
        initials = array_init.elements

        # for item in initials:

        data_type = array_init.elements[0].__class__.__name__
        for element in array_init.elements:
            if not isinstance(element, globals()[data_type]):
                raise Exception(f"Array initialization elements should be of type {data_type}.")

    def validate_array_declaration(self, array_decl):
        for size in array_decl.size:
            if size is not None:
                if isinstance(size, Literal):
                    size_value = size.value[1]
                    if 'int' not in self.determine_literal_type(size) or int(size_value) <= 0:
                        raise Exception("Array size must be a non-negative integer literal.")
                elif isinstance(size, Variable):
                    var_name = size.name[1]
                    if not self.current_scope.has_variable(var_name):
                        raise Exception(f"Variable '{var_name}' not found.")

                    var = self.current_scope.get_variable(var_name)
                    var_type = var.var_type[1]
                    if 'int' not in var_type or var < 0:
                        raise Exception(f"Variable '{var_name}' must be a non-negative integer.")
                else:
                    raise Exception("Array size must be a literal or a variable.")

    def validate_array_reference(self, array_ref):
        array_id = array_ref.id
        if not self.current_scope.has_variable(array_id):
            raise Exception(f"Array '{array_id}' not found.")

        if not isinstance(array_ref.index, int):
            raise Exception("Array index must be an integer.")

    def validate_equality(self, equality_expr):
        self.analyze(equality_expr.expr)
        if isinstance(equality_expr.expr, Variable):
            var_name = equality_expr.expr.name[1]
            if not self.current_scope.has_variable(var_name):
                raise Exception(f"Variable '{var_name}' not found.")
            var_decl = self.current_scope.get_variable(var_name)
            arg_type = var_decl.var_type[1]
            if 'const' in arg_type:
                raise Exception("You can't redefine const variable.")


        self.analyze(equality_expr.right)

    def validate_variable(self, variable_expr):
        var_name = variable_expr.name[1]

        if not self.current_scope.has_variable(var_name):
            raise Exception(f"Variable '{var_name}' is not defined.")

    def determine_literal_type(self, literal_obj):
        if literal_obj.value[0] == 'NUMERIC_VARIABLES':
            if literal_obj.value[1].isdigit():
                return 'int'
            elif literal_obj.value[1].replace('.', '', 1).isdigit():
                return 'float'
            return 'int'
        elif literal_obj.value[0] == 'BOOLEAN_VARIABLES':
            return 'bool'
        elif literal_obj.value[0] == 'STRING_LITERAL':
            return 'str'
        else:
            Exception("Unsupported data type.")