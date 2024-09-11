from syntax_analyzer import *


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def is_at_and(self):
        return self.peek()[0] == "END_OF_FILE"

    def peek(self):
        return self.tokens[self.current]

    def previous(self):
        return self.tokens[self.current - 1]

    def check(self, type_to_compare):
        if self.is_at_and():
            return False
        return self.peek()[0] == type_to_compare

    def token_value(self):
        return self.peek()[1]

    def advance(self):
        if not self.is_at_and():
            self.current += 1
        return self.previous()

    def match(self, types):
        for type_ in types:
            if self.check(type_):
                self.advance()
                return True
        return False

    def match_by_value(self, values):
        for value_ in values:
            if self.token_value() == value_:
                self.advance()
                return True
        return False

    def consume(self, type_, message):
        if self.check(type_):
            return self.advance()
        raise SyntaxError(message)

    def consume_array(self, types, message):
        for type_ in types:
            if self.check(type_):
                return self.advance()
        raise SyntaxError(message)

    def consume_by_value(self, value, message):
        if self.token_value() == value:
            return self.advance()
        raise SyntaxError(message)

    def parse(self):
        statements = []
        while not self.is_at_and():
            statements.append(self.declaration())
        return statements

    def declaration(self):
        if self.match(["DATA_TYPE"]):
            type = self.previous()
            if self.check("VARIABLE_IDENTIFIER"):
                return self.var_declaration(type)
            elif self.check("FUNCTION_IDENTIFIER"):
                return self.fun_declaration(type)
            elif self.token_value() == "*":
                return self.pointer_declaration(type)
            elif self.token_value().find("struct") != -1:
                return self.struct_declaration()
            else:
                raise SyntaxError(f"Unexpected token {self.token_value()}")
        else:
            return self.statement()

    def statement(self):
        if self.match_by_value(["if"]):
            return self.if_statement()
        elif self.match_by_value(["while"]):
            return self.while_statement()
        elif self.check("LOOP_OPERATOR") and self.match_by_value(["do"]):
            return self.do_while_statement()
        elif self.match_by_value(["for"]):
            return self.for_statement()
        elif self.match_by_value(["return"]):
            return self.return_statement()
        elif self.match_by_value(["break"]):
            return self.break_statement()
        elif self.match_by_value(["continue"]):
            return self.continue_statement()
        elif self.match(["LIBRARY_INCLUDE"]):
            return Library(self.previous()[1][8::])
        elif self.match(["MULTILINE_COMMENT"]) or self.match(["COMMENT"]):
            pass
        else:
            return self.expression_statement()

    def if_statement(self):
        self.consume_by_value("(", "Expect '(' after 'if'.")
        condition = self.expression()
        self.consume_by_value(")", "Expect ')' after if condition.")

        then_branch = Block(self.compound_statement())
        else_branch = None
        if self.match_by_value(["else"]):
            else_branch = Block(self.compound_statement())
        return IfStatement(condition, then_branch, else_branch)
    def while_statement(self):
        self.consume_by_value("(", "Expect '(' after 'while'.")
        condition = self.expression()
        self.consume_by_value(")", "Expect ')' after condition.")
        body = Block(self.compound_statement())

        return WhileStatement(condition, body)

    def do_while_statement(self):
        body = Block(self.compound_statement())

        self.consume_by_value("while", "Expect 'while' after do-block.")
        self.consume_by_value("(", "Expect '(' after 'while'.")
        condition = self.expression()
        self.consume_by_value(")", "Expect ')' after condition.")
        self.consume_by_value(";", "Expect ';' after do-while loop declaration.")

        return DoWhileStatement(condition, body)

    def for_statement(self):
        self.consume_by_value("(", "Expect '(' after 'for'.")

        # For loop initializer
        if self.match_by_value([";"]):
            initializer = None
        elif self.match(["DATA_TYPE"]):
            type = self.previous()
            initializer = self.var_declaration(type)
        else:
            initializer = self.expression_statement()

        # For loop condition
        condition = None if self.match_by_value([";"]) else self.expression()
        if condition != None:
            self.consume_by_value(";", "Expect ';' after loop condition.")

        # For loop increment
        increment = []
        if self.token_value() != ")":
            while True:
                increment.append(self.expression())
                if not self.match_by_value([","]):
                    break
        else:
            increment = None

        self.consume_by_value(")", "Expect ')' after for clauses.")

        body = Block(self.compound_statement())

        if condition is None:
            condition = Literal(True)

        return ForStatement(initializer, condition, increment, body)



    def return_statement(self):
        keyword = self.previous()
        value = None if self.token_value() == ";" else self.expression()
        self.consume_by_value(";", "Expect ';' after return value.")
        return ReturnStatement(value)

    def break_statement(self):
        self.consume_by_value(";", "Expect ';' after 'break'.")
        return BreakStatement()

    def continue_statement(self):
        self.consume_by_value(";", "Expect ';' after 'continue'.")
        return ContinueStatement()

    def expression_statement(self):
        expr = self.expression()
        self.consume_by_value(";", "Expect ';' after expression.")
        return ExpressionStatement(expr)

    def var_declaration(self, var_type):
        declarations = []
        while True:
            identifier = self.consume("VARIABLE_IDENTIFIER", "Expect variable name after variable type.")
            initializer = None
            if self.match_by_value(["["]):
                return self.arr_declaration(var_type,identifier)
            if self.match_by_value(["="]):
                initializer = self.expression()
                for item in declarations:
                    item.initializer = initializer
            declarations.append(VarDeclaration(var_type, identifier, initializer))
            if not self.match_by_value([","]):
                break
        self.consume_by_value(";", "Expect ';' after variable declaration.")
        for item in declarations:
            return item

    def pointer_declaration(self, type):
        dimension = 0
        while True:
            if self.match_by_value(["*"]):
                dimension = dimension + 1
            else:
                break
        identifier = self.consume("VARIABLE_IDENTIFIER", "Expect variable name after variable type.")
        initializer = None
        if self.match_by_value(["="]):
            initializer = self.arr_initialization()
        self.consume_by_value(";", "Expect ';' after variable declaration.")
        return PointerDeclaration(type, dimension, identifier, initializer)

    def arr_declaration(self, type, identifier):
        size = []
        while True:
            if not self.token_value() == "]":
                size.append(self.expression())
            self.consume_by_value(']', "Expected ']' after array size")
            if not self.match_by_value(["["]):
                break
        initializers = []
        if self.match_by_value(["="]):
            initializers = self.arr_initialization()
        self.consume_by_value(";", "Expect ';' after array declaration.")
        return ArrayDeclaration(type, identifier, size, initializers)

    def arr_initialization(self):
        initializers = []
        if self.match_by_value(["{"]):
            while True:

                if self.match_by_value(["{"]) and self.token_value() != "}":
                    inner_init = []
                    while True:
                        inner_init.append(self.expression())
                        if not self.match_by_value([","]):
                            initializers.append(inner_init)
                            break
                    self.consume_by_value('}', "Expected '}' after array initialization")
                    if self.token_value() == ",":
                        self.advance()
                else:
                    initializers.append(self.expression())
                    if not self.match_by_value([","]):
                        break
            self.consume_by_value('}', "Expected '}' after array initialization")
        else:
            initializers.append(self.expression())
        return ArrayInitialization(initializers)

    def fun_declaration(self, return_type):
        # return_type = self.consume("DATA_TYPE", "Expect return type after 'fun'.")
        name = self.consume("FUNCTION_IDENTIFIER", "Expect function name after return type.")
        parameters = []
        self.consume_by_value("(", "Expect '(' after function name.")
        if self.token_value() != ")":
            data_type = self.consume("DATA_TYPE", "Expect parameter type.")
            id = self.consume("VARIABLE_IDENTIFIER", "Expect parameter name.")
            init = Literal(self.peek()) if self.match_by_value("=") else None
            if init != None:
                self.advance()
            parameters.append(VarDeclaration(data_type, id, init))
            # data_type = self.consume("DATA_TYPE", "Expect parameter type.")
            # parameters.append(self.var_declaration(data_type))
            while self.match_by_value([","]):
                data_type = self.consume("DATA_TYPE", "Expect parameter type.")
                id = self.consume("VARIABLE_IDENTIFIER", "Expect parameter name.")
                init = Literal(self.peek()) if self.match_by_value("=") else None
                if init != None:
                    self.advance()
                parameters.append(VarDeclaration(data_type, id, init))
                # data_type = self.consume("DATA_TYPE", "Expect parameter type.")
                # parameters.append(self.var_declaration(data_type))
        self.consume_by_value(")", "Expect ')' after parameters.")
        body = Block(self.compound_statement())
        return FunDeclaration(return_type, name, parameters, body)

    def struct_declaration(self):
        name = self.previous()[1]
        self.consume_by_value("{", "Expect '{' before structure body.")

        fields = []
        while self.token_value() != "}" and not self.is_at_and():
            data_type = self.consume("DATA_TYPE", "Expect parameter type.")
            id = self.consume("VARIABLE_IDENTIFIER", "Expect parameter name.")
            init = Literal(self.peek()) if self.match_by_value("=") else None
            if init != None:
                self.advance()
            fields.append(VarDeclaration(data_type, id, init))

            self.consume_by_value(";", "Expect ';' after field declaration.")

        self.consume_by_value("}", "Expect '}' after structure body.")
        self.consume_by_value(";", "Expect ';' after structure declaration.")
        return StructDeclaration(name, fields)

    def compound_statement(self):
        statements = []
        self.consume_by_value("{", "Expect '{' before compound statement.")
        while self.token_value() != "}" and not self.is_at_and():
            statements.append(self.declaration())
        self.consume_by_value("}", "Expect '}' after compound statement.")
        return statements

    def expression(self):
        return self.equality()

    def equality(self):
        expr = self.ternary_operator()
        if self.match(["EQUALITY"]):
            operator = self.previous()
            right = self.expression()
            return Equality(expr, operator, right)
        return expr

    def ternary_operator(self):
        expr = self.logical_or()
        if self.match_by_value(["?"]):
            condition = expr
            true_expr = self.logical_or()
            self.consume_by_value(":", "Expected ':' in ternary declaration.")
            false_expr = self.logical_or()
            # self.consume_by_value(";", "Expected ';' after ternary declaration.")
            return TernaryOperator(condition, true_expr, false_expr)
        return expr


    def logical_or(self):
        expr = self.logical_and()
        while self.match_by_value(["||"]):
            operator = self.previous()
            right = self.logical_and()
            expr = Logical(expr, operator, right)
        return expr

    def logical_and(self):
        expr = self.comparison()
        while self.match_by_value(["&&"]):
            operator = self.previous()
            right = self.comparison()
            expr = Logical(expr, operator, right)
        return expr

    def comparison(self):
        expr = self.term()

        while self.match(["COMPARISON"]):
            operator = self.previous()
            right = self.term()
            expr = Comparison(expr, operator, right)

        return expr

    def term(self):
        expr = self.factor()

        while self.match(["ARITHMETIC_TERM"]):
            operator = self.previous()
            right = self.factor()
            expr = Binary(expr, operator, right)

        return expr

    def factor(self):
        expr = self.unary()

        while self.match(["ARITHMETIC_FACTOR"]):
            operator = self.previous()
            right = self.unary()
            expr = Binary(expr, operator, right)

        return expr

    def unary(self):
        if self.match(["UNARY"]):
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)

        if self.match(["VARIABLE_IDENTIFIER"]):
            identifier = self.previous()
            if self.match(["UNARY"]) and self.previous()[1] in ['++', '--']:
                operator = self.previous()
                return Unary(operator, Variable(identifier))
            else:
                # return Variable(identifier)
                self.current -= 1
                return self.call_statement()

        return self.call_statement()

    def call_statement(self):
        expr = self.previous() if self.match(["FUNCTION_IDENTIFIER"]) else self.call_property()
        parameters = []

        while True:
            if self.match_by_value(["("]):
                if self.token_value() != ")":
                    parameters.append(self.expression())
                    while self.match_by_value([","]):
                        parameters.append(self.expression())

                self.consume_by_value(")", "Expect ')' after parameters.")
                callee = expr
                return Call(Func(callee), parameters)
            else:
                break

        return expr

    def call_property(self):
        expr = self.primary()
        if self.match_by_value(["."]):
            object_name = expr
            property = self.primary()
            return CallProperty(object_name, property)
        return expr

    def primary(self):
        if self.match(["BOOLEAN_VARIABLES", "NUMERIC_VARIABLES", "STRING_LITERAL"]):
            return Literal(self.previous())
        elif self.match(["VARIABLE_IDENTIFIER"]):
            if self.token_value() == "[":
                id = self.previous()
                index = []
                while True:
                    if self.match_by_value(["["]):
                        if self.token_value() != "]":
                            index.append(self.expression())
                        self.consume_by_value("]", "Expect ']' after calling array element.")
                    else:
                        return ArrayRef(id, index)
            return Variable(self.previous())
        elif self.match_by_value(["("]):
            expr = self.expression()
            self.consume_by_value(")", "Expect ')' after expression.")
            return Grouping(expr)
        else:
            raise SyntaxError("Expect expression.")
