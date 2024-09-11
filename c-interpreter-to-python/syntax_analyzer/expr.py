

class Expr:
    pass


class VarDeclaration (Expr):
    def __init__(self, var_type, identifier, initializer=None):
        self.var_type = var_type
        self.identifier = identifier
        self.initializer = initializer


class FunDeclaration (Expr):
    def __init__(self, return_type, name, parameters, body):
        self.return_type = return_type
        self.name = name
        self.parameters = parameters
        self.body = body


class ArrayInitialization:
    def __init__(self, elements):
        self.elements = elements


class ArrayDeclaration:
    def __init__(self, data_type, identifier, size=None, initialization=None):
        self.data_type = data_type
        self.identifier = identifier
        self.size = size
        self.initialization = initialization


class ArrayRef(Expr):
    def __init__(self, id, index):
        self.id = id
        self.index = index


class PointerDeclaration:
    def __init__(self, data_type, dimension, identifier, initializer):
        self.data_type = data_type
        self.dimension = dimension
        self.identifier = identifier
        self.initializer = initializer


class StructDeclaration(Expr):
    def __init__(self, name, fields):
        self.name = name
        self.fields = fields

class Equality(Expr):
    def __init__(self, expr, operator, right):
        self.expr = expr
        self.operator = operator
        self.right = right


class Logical(Expr):
    def __init__(self, expr, operator, right):
        self.expr = expr
        self.operator = operator
        self.right = right


class Comparison(Expr):
    def __init__(self, expr, operator, right):
        self.expr = expr
        self.operator = operator
        self.right = right

class Binary(Expr):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right


class Unary(Expr):
    def __init__(self, operator, right):
        self.operator = operator
        self.right = right

class Grouping:
    def __init__(self, expression):
        self.expression = expression

class Literal(Expr):
    def __init__(self, value):
        self.value = value


class Variable(Expr):
    def __init__(self, name):
        self.name = name

class Func(Expr):
    def __init__(self, name):
        self.name = name


class ReturnStatement (Expr):
    def __init__(self, value):
        self.value = value


class IfStatement(Expr):
    def __init__(self, condition, thenBranch, elseBranch=None):
        self.condition = condition
        self.thenBranch = thenBranch
        self.elseBranch = elseBranch


class TernaryOperator(Expr):
    def __init__(self, condition, true_expr, false_expr):
        self.condition = condition
        self.true_expr = true_expr
        self.false_expr = false_expr


class WhileStatement(Expr):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body


class DoWhileStatement(Expr):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body


class ForStatement(Expr):
    def __init__(self, initializer, condition, increment, body):
        self.initializer = initializer
        self.condition = condition
        self.increment = increment
        self.body = body


class BreakStatement(Expr):
    def __init__(self):
        pass


class Call(Expr):
    def __init__(self, callee, arguments):
        self.callee = callee
        self.arguments = arguments

class CallProperty:
    def __init__(self, object_name, property_obj):
        self.object_name = object_name
        self.property_obj = property_obj


class ExpressionStatement(Expr):
    def __init__(self, expression):
        self.expression = expression


class Block(Expr):
    def __init__(self, statements):
        self.statements = statements


class ContinueStatement(Expr):
    def __init__(self):
        pass

# class Get(Expr):
#     def __init__(self, object, name):
#         self.object = object
#         self.name = name
class Library(Expr):
    def __init__(self, name):
        self.name = name


