import array

from syntax_analyzer import *


class ASTPrinter:
    def __init__(self):
        self.indentation_level = 0

    def print_var_declaration(self, node):
        self.print_indentation()
        print("VarDeclaration:")
        self.indentation_level += 2
        self.print_indentation()
        print(f"Type: {node.var_type[1]}")
        self.print_indentation()
        print(f"Identifier: {node.identifier[1]}")
        if node.initializer:
            self.print_indentation()
            print("Initializer:")
            self.indentation_level += 2
            self.print_ast(node.initializer)
            self.indentation_level -= 2
        self.indentation_level -= 2

    def print_pointer_declaration(self, node):
        self.print_indentation()
        print("Pointer:")
        self.indentation_level += 2
        self.print_indentation()
        print(f"Type: {node.data_type[1]}")
        self.print_indentation()
        print(f"Dimension: {node.dimension}")
        self.print_indentation()
        print(f"Identifier: {node.identifier[1]}")
        if node.initializer:
            self.print_indentation()
            print("Initializer:")
            self.indentation_level += 2
            self.print_ast(node.initializer)
            self.indentation_level -= 2
        self.indentation_level -= 2

    def print_fun_declaration(self, node):
        self.print_indentation()
        print("FunDeclaration:")
        self.indentation_level += 2
        self.print_indentation()
        print(f"Return Type: {node.return_type[1]}")
        self.print_indentation()
        print(f"Name: {node.name}")
        self.print_indentation()
        print("Parameters:")
        self.indentation_level += 2
        for param in node.parameters:
            self.print_ast(param)
        self.print_indentation()
        print("Body:")
        self.print_ast(node.body)
        self.indentation_level -= 2
        self.indentation_level -= 2

    def print_equality(self, node):
        self.print_indentation()
        print("Equality:")
        self.indentation_level += 2
        self.print_ast(node.expr)
        self.print_indentation()
        print(f"Operator: {node.operator[1]}")
        self.print_ast(node.right)
        self.indentation_level -= 2

    def print_logical(self, node):
        self.print_indentation()
        print("Logical:")
        self.indentation_level += 2
        self.print_ast(node.expr)
        self.print_indentation()
        print(f"Operator: {node.operator[1]}")
        self.print_ast(node.right)
        self.indentation_level -= 2

    def print_comparison(self, node):
        self.print_indentation()
        print("Comparison:")
        self.indentation_level += 2
        self.print_ast(node.expr)
        self.print_indentation()
        print(f"Operator: {node.operator[1]}")
        self.print_ast(node.right)
        self.indentation_level -= 2

    def print_binary(self, node):
        self.print_indentation()
        print("Binary:")
        self.indentation_level += 2
        self.print_ast(node.left)
        self.print_indentation()
        print(f"Operator: {node.operator[1]}")
        self.print_ast(node.right)
        self.indentation_level -= 2

    def print_unary(self, node):
        self.print_indentation()
        print("Unary:")
        self.indentation_level += 2
        self.print_indentation()
        print(f"Operator: {node.operator[1]}")
        self.print_ast(node.right)
        self.indentation_level -= 2

    def print_grouping(self, node):
        self.print_indentation()
        print("Grouping ()")
        self.indentation_level += 2
        self.print_ast(node.expression)
        self.indentation_level -= 2

    def print_literal(self, node):
        self.print_indentation()
        print(f"Literal: {node.value[1]}")

    def print_variable(self, node):
        self.print_indentation()
        print(f"Variable: {node.name[1]}")

    def print_func_identifier(self, node):
        self.print_indentation()
        print(f"Func identifier: {node.name[1]}")

    def print_func(self, node):
        self.print_indentation()
        print(f"Func name: {node.name}")

    def print_return_statement(self, node):
        self.print_indentation()
        print("Return Statement:")
        if node.value is not None:
            self.indentation_level += 2
            self.print_ast(node.value)
            self.indentation_level -= 2

    def print_if_statement(self, node):
        self.print_indentation()
        print("If Statement:")
        self.indentation_level += 2
        self.print_indentation()
        print("Condition:")
        self.indentation_level += 2
        self.print_ast(node.condition)
        self.indentation_level -= 2
        self.print_indentation()
        print("Then Branch:")
        self.indentation_level += 2
        self.print_ast(node.thenBranch)
        self.indentation_level -= 2
        if node.elseBranch is not None:
            self.print_indentation()
            print("Else Branch:")
            self.indentation_level += 2
            self.print_ast(node.elseBranch)
            self.indentation_level -= 2

    def print_while_statement(self, node):
        self.print_indentation()
        print("While Statement:")
        self.indentation_level += 2
        self.print_indentation()
        print("Condition:")
        self.indentation_level += 2
        self.print_ast(node.condition)
        self.indentation_level -= 2
        self.print_ast(node.body)
        self.indentation_level -= 2
    def print_do_while_statement(self, node):
        self.print_indentation()
        print("Do-While Statement:")
        self.indentation_level += 2
        self.print_indentation()
        print("Condition:")
        self.indentation_level += 2
        self.print_ast(node.condition)
        self.indentation_level -= 2
        self.print_ast(node.body)
        self.indentation_level -= 2

    def print_for_statement(self, node):
        self.print_indentation()
        print("For Statement:")
        self.indentation_level += 2
        self.print_indentation()
        print("Initializer:")
        self.indentation_level += 2
        if node.initializer is not None:
            self.print_ast(node.initializer)
        self.indentation_level -= 2
        self.print_indentation()
        print("Condition:")
        self.indentation_level += 2
        if node.condition is not None:
            self.print_ast(node.condition)
        self.indentation_level -= 2
        self.print_indentation()
        print("Increment:")
        self.indentation_level += 2
        if node.increment is not None:
            self.print_ast(node.increment)
        self.indentation_level -= 2
        self.print_ast(node.body)
        self.indentation_level -= 2

    def print_break_statement(self, node):
        self.print_indentation()
        print("Break Statement")

    def print_call(self, node):
        self.print_indentation()
        print("Function Call:")
        self.indentation_level += 2
        self.print_indentation()
        print("Callee:")
        self.indentation_level += 2
        self.print_ast(node.callee)
        self.indentation_level -= 2
        self.print_indentation()
        print("Arguments:")
        self.indentation_level += 2
        for arg in node.arguments:
            self.print_ast(arg)
        self.indentation_level -= 2
        self.indentation_level -= 2

    def print_call_property(self, node):
        self.print_indentation()
        print("Calling property:")
        self.indentation_level += 2
        self.print_indentation()
        print("Object Name:")
        self.indentation_level += 2
        self.print_ast(node.object_name)
        self.indentation_level -= 2
        self.print_indentation()
        print("Property:")
        self.indentation_level += 2
        self.print_ast(node.property_obj)
        self.indentation_level -= 2
        self.indentation_level -= 2

    def print_expression_statement(self, node):
        self.print_indentation()
        print("Expression Statement:")
        self.indentation_level += 2
        self.print_ast(node.expression)
        self.indentation_level -= 2

    def print_block(self, node):
        self.print_indentation()
        print("Block:")
        self.indentation_level += 2
        for statement in node.statements:
            self.print_ast(statement)
        self.indentation_level -= 2

    def print_continue_statement(self, node):
        self.print_indentation()
        print("Continue Statement")

    def print_library(self, node):
        self.print_indentation()
        print("Library:", node.name)

    def print_get(self, node):
        self.print_indentation()
        print("Get:")
        self.indentation_level += 2

        self.print_indentation()
        print("Object:")
        self.indentation_level += 2
        self.print_ast(node.object)
        self.indentation_level -= 2

        self.print_indentation()
        print(f"Property: {node.name}")
        self.indentation_level -= 2

    def print_struct_declaration(self, node):
        print("Struct Declaration:")
        print("Name:", node.name)
        print("Fields:")
        self.indentation_level += 2
        for field in node.fields:
            self.print_indentation()
            self.print_ast(field)
        self.indentation_level -= 2

    def print_ternary(self, node):
        self.print_indentation()
        print("Ternary:")
        self.indentation_level += 2
        self.print_indentation()
        print("Condition:")
        self.indentation_level += 2
        self.print_ast(node.condition)
        self.indentation_level -= 2
        self.print_indentation()
        print("Then Branch:")
        self.indentation_level += 2
        self.print_ast(node.true_expr)
        self.indentation_level -= 2
        self.print_indentation()
        print("Else Branch:")
        self.indentation_level += 2
        self.print_ast(node.false_expr)
        self.indentation_level -= 2

    def print_array_declaration(self, node):
        self.print_indentation()
        print("ArrDeclaration:")
        self.indentation_level += 2
        self.print_indentation()
        print(f"Type: {node.data_type[1]}")
        self.print_indentation()
        print(f"Identifier: {node.identifier[1]}")
        if node.size:
            self.print_indentation()
            print("Size:")
            self.indentation_level += 2
            self.print_ast(node.size)
            self.indentation_level -= 2
        if node.initialization:
            self.print_indentation()
            print("Initializers:")
            self.indentation_level += 2
            self.print_ast(node.initialization)
            self.indentation_level -= 2
        self.indentation_level -= 2

    def print_array_initialization(self, node):
        elements = node.elements
        for item in elements:
            if isinstance(item, list):
                self.print_indentation()
                print("Array:")
                self.indentation_level += 2
                self.print_ast(item)
                self.indentation_level -= 2
            else:
                self.print_ast(item)

    def print_array_ref(self, node):
        self.print_indentation()
        print("ArrayRef:")
        self.indentation_level += 2
        self.print_indentation()
        print(f"Identifier: {node.id[1]}")
        self.print_indentation()
        self.indentation_level += 2
        print("Indexes:")
        for item in node.index:
            self.print_ast(item)
        self.indentation_level -= 2
        self.indentation_level -= 2



    def print_ast(self, node):
        if isinstance(node, VarDeclaration):
            self.print_var_declaration(node)
        elif isinstance(node, FunDeclaration):
            self.print_fun_declaration(node)
        elif isinstance(node, ArrayDeclaration):
            self.print_array_declaration(node)
        elif isinstance(node, PointerDeclaration):
            self.print_pointer_declaration(node)
        elif isinstance(node, ArrayInitialization):
            self.print_array_initialization(node)
        elif isinstance(node, ArrayRef):
            self.print_array_ref(node)
        elif isinstance(node, Equality):
            self.print_equality(node)
        elif isinstance(node, Logical):
            self.print_logical(node)
        elif isinstance(node, Comparison):
            self.print_comparison(node)
        elif isinstance(node, Binary):
            self.print_binary(node)
        elif isinstance(node, Unary):
            self.print_unary(node)
        elif isinstance(node, Grouping):
            self.print_grouping(node)
        elif isinstance(node, Literal):
            self.print_literal(node)
        elif isinstance(node, Variable):
            self.print_variable(node)
        elif isinstance(node, Func):
            self.print_func_identifier(node)
        elif isinstance(node, Func):
            self.print_func(node)
        elif isinstance(node, ReturnStatement):
            self.print_return_statement(node)
        elif isinstance(node, IfStatement):
            self.print_if_statement(node)
        elif isinstance(node, WhileStatement):
            self.print_while_statement(node)
        elif isinstance(node, DoWhileStatement):
            self.print_do_while_statement(node)
        elif isinstance(node, ForStatement):
            self.print_for_statement(node)
        elif isinstance(node, BreakStatement):
            self.print_break_statement(node)
        elif isinstance(node, Call):
            self.print_call(node)
        elif isinstance(node, CallProperty):
            self.print_call_property(node)
        elif isinstance(node, ExpressionStatement):
            self.print_expression_statement(node)
        elif isinstance(node, Block):
            self.print_block(node)
        elif isinstance(node, TernaryOperator):
            self.print_ternary(node)
        elif isinstance(node, ContinueStatement):
            self.print_continue_statement(node)
        elif isinstance(node, Library):
            self.print_library(node)
        # elif isinstance(node, Get):
        #     self.print_get(node)
        elif isinstance(node, StructDeclaration):
            self.print_struct_declaration(node)
        elif isinstance(node, list) or isinstance(node, tuple):
            for item in node:
                self.print_ast(item)
        elif node is None:
            pass
        # else:
        #     super().print_ast(node)

    def print_indentation(self):
        print(" " * self.indentation_level, end="")
