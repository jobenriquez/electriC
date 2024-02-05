from errors import SyntaxError
from constants import *

#############################
#           Nodes           #
#############################

# Different node types that build up the Abstract Syntax Tree (AST)

class ECProgStatementNode:
    def __init__(self, body):
        self.body = body

    def __repr__(self):
        return f'ECProgStatement({self.body})'
    
class BodyNode:
    def __init__(self, statements):
        self.statements = statements

    def __repr__(self):
        return f'Body({self.statements})'
    
class DeclarationStatementNode:
    def __init__(self, data_type, identifier_init_list):
        self.data_type = data_type
        self.identifier_init_list = identifier_init_list

    def __repr__(self):
        return f'DeclarationStatement({self.data_type}, {self.identifier_init_list})'

class IdentifierNode:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'Identifier({self.name})'
    
class LiteralNode:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'Literal({self.value})'
    
class NumberNode:
	def __init__(self, tok):
		self.tok = tok

	def __repr__(self):
		return f'{self.tok}'

class BinOpNode:
	def __init__(self, left_node, op_tok, right_node):
		self.left_node = left_node
		self.op_tok = op_tok
		self.right_node = right_node

	def __repr__(self):
		return f'({self.left_node}, {self.op_tok}, {self.right_node})'
    
class AssignmentStatementNode:
    def __init__(self, identifier, ass_op, value):
        self.identifier = identifier
        self.ass_op = ass_op
        self.value = value

    def __repr__(self):
        return f'AssignmentStatement({self.identifier}, {self.ass_op}, {self.value})'
            
class UnaryStatementNode:
    def __init__(self, identifier, unary_op):
        self.identifier = identifier
        self.unary_op = unary_op
    
    def __repr__(self):
        return f'AssignmentStatement({self.identifier}, {self.unary_op})'
    
class InputStatementNode:
    def __init__(self, identifier, scan_statement):
        self.identifier = identifier
        self.scan_statement = scan_statement
    
    def __repr__(self):
        return f'InputStatement({self.identifier}, {self.scan_statement})'
    
class OutputStatementNode:
    def __init__(self, output_statement, initialization):
        self.output_statement = output_statement
        self.initialization = initialization
    
    def __repr__(self):
        return f'OutputStatement({self.output_statement}, {self.initialization})'
    
class ECKeywordNode:
    def __init__(self, var1, op, var2):
        self.var1 = var1
        self.op = op
        self.var2 = var2
    
    def __repr__(self):
        return f'ECKeyword({self.var1}, {self.op}, {self.var2})'
    
class SquareRootNode:
    def __init__(self, node):
        self.node = node

    def __repr__(self):
        return f'SquareRoot({self.node})'

class IterativeDoStatementNode:
    def __init__(self, loop_type, condition, body):
        self.loop_type = loop_type
        self.condition = condition
        self.body = body

    def __repr__(self):
        return f'IterativeDoStatement({self.loop_type}, {self.condition}, {self.body})'
    
class IterativeForStatementNode:
    def __init__(self, variable, condition, unary_exp,  body):
        self.variable = variable
        self.condition = condition
        self.unary_exp = unary_exp
        self.body = body

    def __repr__(self):
        return f'IterativeForStatement({self.variable}; {self.condition}; {self.unary_exp}), {self.body})'
    
class ConditionalStatementNode:
    def __init__(self, condition, if_body, elif_conditions=None, elif_bodies=None, else_body=None):
        self.condition = condition
        self.if_body = if_body
        self.elif_conditions = elif_conditions if elif_conditions is not None else []
        self.elif_bodies = elif_bodies if elif_bodies is not None else []
        self.else_body = else_body

    def __repr__(self):
        return f'ConditionalStatement({self.condition}, {self.if_body}, {self.elif_conditions}, {self.elif_bodies}, {self.else_body})'

class ReturnStatementNode:
	def __init__(self, value):
		self.value = value

	def __repr__(self):
		return f'ReturnStatement({self.value})'
    
#############################
#           Parser          #
#############################
    
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None 
        self.token_index = 0

    def consume_token(self):
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]
            self.token_index += 1
        
    def peek_next_token(self):
        if self.token_index < len(self.tokens):
            return self.tokens[self.token_index]
    
    def peek_token_after_next(self):
        if self.token_index < len(self.tokens):
            return self.tokens[self.token_index+1]

    def match_type(self, expected_type):
        if self.current_token.type_ == expected_type:
            self.consume_token()
        else:
            raise SyntaxError(f"Expected {expected_type}, but found {self.current_token.type_}")
        
    def match_resword(self, expected_value):
        if self.current_token.value == expected_value:
            self.consume_token()
        else:
            raise SyntaxError(f"Expected {expected_value}, but found {self.current_token.value}")
    
    # The starting point of an electriC program
    def parse_ec_prog_statement(self):
        self.consume_token()

        if self.current_token is None:
            raise SyntaxError("Unexpected end of input")
        
        self.match_resword("Main")

        if self.current_token.type_ == 'DEL_LBRACE':
            self.consume_token()
        else:
            raise SyntaxError("Expected '{' after 'Main'") 
        
        body = self.parse_body()
        if self.current_token.type_ == 'DEL_RBRACE':
            self.consume_token() 
        else:
            raise SyntaxError("Expected '}' at the end of the statement")

        return ECProgStatementNode(body)
    
    # Parse each line of the body
    def parse_body(self):
        statements = []

        while self.current_token.type_ != 'DEL_RBRACE':
            current_statement = self.identify_statements()
            statements.append(current_statement)
            
        return BodyNode(statements)
    
    def check_semicolon(self):
        if self.current_token.type_ == 'DEL_SEMICOLON':
            self.consume_token() 
        else:
            raise SyntaxError("Expected ';' after statement")

    def identify_statements(self):
        #Declaration Statement
        if self.current_token.type_ in TOKEN_DATA_TYPES: 
            node = self.parse_declaration_statement()    
            self.check_semicolon()
            return node
        #Assignment Statement
        elif self.current_token.type_ == 'IDENTIFIER':
            node = self.parse_assignment_unary_statement()
            self.check_semicolon()
            return node
        #Output Statement
        elif self.current_token.type_ == 'RESERVED_WORD' and self.current_token.value in ['Print', 'PrintLine']:
            node =  self.parse_output_statement()
            self.check_semicolon()
            return node
        #Return Statement
        elif self.current_token.type_ == 'RESERVED_WORD' and self.current_token.value == 'return':
            node = self.parse_return_statement()
            self.check_semicolon()
            return node
        #Iterative Statements
        elif self.current_token.type_ == 'RESERVED_WORD' and self.current_token.value == 'do':
            node = self.parse_do_while_statement()
            self.check_semicolon()
            return node
        elif self.current_token.type_ == 'RESERVED_WORD' and self.current_token.value == 'while':
            return self.parse_while_statement()
        elif self.current_token.type_ == 'RESERVED_WORD' and self.current_token.value == 'for':
            return self.parse_for_statement()
        #Conditional Statement
        elif self.current_token.type_ == 'RESERVED_WORD' and self.current_token.value == 'if':
            return self.parse_if_statement()
        else:
            raise SyntaxError("Invalid statement encountered")
    
    def parse_declaration_statement(self):
        if self.token_index < len(self.tokens):
            data_type = self.identify_data_type()
            identifier_init_list = self.parse_variable_list(data_type)

            return DeclarationStatementNode(data_type, identifier_init_list)
        else:
            raise SyntaxError("Unexpected end of input")

    def identify_data_type(self):
        if self.current_token.type_ in TOKEN_DATA_TYPES:
            data_type = self.current_token.value
            self.consume_token() 
            return data_type
        else:
            raise SyntaxError("Invalid data type encountered")

    def parse_variable_list(self, expected_data_type):
        identifier_list = []

        # Check if it follows the correct format
        if self.current_token.type_ == 'IDENTIFIER':        
            identifier = self.parse_identifier()
            if self.current_token.type_ not in ('OP_ASS', 'DEL_COMMA', 'DEL_SEMICOLON', None):
                raise SyntaxError(f"Expected an assignment operator or a semicolon, but found {self.current_token.type_}")
            
            initialization = self.parse_initialization(expected_data_type)
            identifier_list.append((identifier, initialization))

            # Check if there are more identifiers
            while self.current_token.type_ == 'DEL_COMMA':
                self.match_type('DEL_COMMA')
                next_identifier = self.parse_identifier()
                next_initialization = self.parse_initialization(expected_data_type)
                identifier_list.append((next_identifier, next_initialization))
        else:
            raise SyntaxError(f"Expected an identifier, but found {self.current_token.type_}")
        return identifier_list
    
    def parse_identifier(self):
        if self.current_token.type_ == 'IDENTIFIER':
            identifier_value = self.current_token.value
            self.consume_token()
            return IdentifierNode(identifier_value)
        else:
            raise SyntaxError(f"Expected an identifier, but found {self.current_token.type_}")
    
    def parse_initialization(self, expected_data_type):
        # Ensure that assignment operators other than '=' only work with int and float literals
        if expected_data_type in ['int', 'float', 'integer', None]:
            if self.current_token.type_ in TOKEN_ASS_OPS:
                self.consume_token()
                initialization = self.parse_literal(expected_data_type)
                return initialization
            else:
                return None
        elif expected_data_type in ['string', 'char', 'bool', 'boolean', 'character', None]:
            if self.current_token.type_ not in ['OP_ASS', None]:
                raise SyntaxError(f"Expected an assignment operator, but found {self.current_token.type_}")
            if self.current_token.type_ == 'OP_ASS':
                self.consume_token()
                initialization = self.parse_literal(expected_data_type)
                return initialization
            else:
                return None
        else:
            raise SyntaxError(f"Unexpected token: {self.current_token.type_}")

    def parse_literal(self, expected_data_type):
            # Disallow boolean operations on identifiers of type string, bool, and char
        if self.current_token.type_ == 'IDENTIFIER' and expected_data_type not in ['string', 'bool', 'boolean', 'char', 'character']:
            return self.parse_additive_expression()
        elif self.current_token.type_ == 'RESERVED_WORD' and self.current_token.value == 'Scan':
            input_node = self.parse_input_statement()
            self.consume_token()
            return input_node
        elif self.current_token.type_ == 'KEYWORD':
            return self.parse_ec_keywords()
        elif self.current_token.type_ == 'DEL_LPAREN':
            return self.parse_additive_expression()
        elif self.current_token.type_ == 'LIT_INT' and expected_data_type == 'int' or expected_data_type == 'integer':
            return self.parse_additive_expression()
        elif self.current_token.type_ == 'LIT_FLT' and expected_data_type == 'float':
            return self.parse_additive_expression()
        elif self.current_token.type_ == 'LIT_CHAR' and expected_data_type == 'char' or expected_data_type == 'character':
            literal = self.current_token.value
            self.consume_token()
            return LiteralNode(literal)
        elif self.current_token.type_ == 'LIT_STR' and expected_data_type == 'string':
            literal = self.current_token.value
            self.consume_token()
            return LiteralNode(literal)
        elif self.current_token.type_ == 'LIT_BOOLTRUE' and expected_data_type == 'boolean' or expected_data_type == 'bool':
            literal = self.current_token.value
            self.consume_token()
            return LiteralNode(literal)
        elif self.current_token.type_ == 'LIT_BOOLFALSE' and expected_data_type == 'boolean' or expected_data_type == 'bool':
            literal = self.current_token.value
            self.consume_token()
            return LiteralNode(literal)
        else:
            raise SyntaxError(f"Expected literal of type {expected_data_type}, but found {self.current_token.type_}")
        
    # The next three methods ensure that boolean expressions are evaluated correctly, following the order PMDAS
    def parse_additive_expression(self):
        left_node = self.parse_multiplicative_expression() 

        while self.current_token.type_ in ('OP_ADD', 'OP_SUB'):
            op_token = self.current_token
            self.consume_token()
            right_node = self.parse_multiplicative_expression()

            left_node = BinOpNode(left_node, op_token, right_node)

        return left_node

    def parse_multiplicative_expression(self):
        left_node = self.parse_primary_expression() 

        while self.current_token.type_ in ('OP_MUL', 'OP_DIV', 'OP_MOD'):
            op_token = self.current_token
            self.consume_token()
            right_node = self.parse_primary_expression() 

            left_node = BinOpNode(left_node, op_token, right_node)

        return left_node

    def parse_primary_expression(self):
        if self.current_token.type_ == 'LIT_INT':
            current_value = self.current_token.value
            self.consume_token()
            return NumberNode(int(current_value))
        elif self.current_token.type_ == 'LIT_FLT':
            current_value = self.current_token.value
            self.consume_token()
            return NumberNode(float(current_value))
        elif self.current_token.type_ == 'DEL_LPAREN':
            self.consume_token()
            expression_node = self.parse_additive_expression()
            if self.current_token.type_ == 'DEL_RPAREN':
                self.consume_token()
                return expression_node
            else:
                raise SyntaxError("Expected ')' after expression within parentheses")
        elif self.current_token.type_ == 'IDENTIFIER':
            return self.parse_identifier()
        else:
            raise SyntaxError(f"Unexpected token: {self.current_token.type_}")

    def parse_input_statement(self):
        self.consume_token()
        if self.current_token.type_ == 'DEL_LPAREN':
            self.consume_token()
            if self.current_token.type_ == 'DEL_RPAREN':
                return 'Scan()'
            else:
                raise SyntaxError(f"Expected ')', but found {self.current_token.type_}")
        else:
            raise SyntaxError(f"Expected '(', but found {self.current_token.type_}")
        
    def parse_output_statement(self):
        output_statement = self.current_token.value
        self.consume_token()

        if self.current_token.type_ == 'DEL_LPAREN':
            self.consume_token()
            values = []

            while self.current_token.type_ != 'DEL_RPAREN':
                if self.current_token.type_ == 'LIT_INT':
                    value = self.parse_literal('int')
                elif self.current_token.type_ == 'KEYWORD':
                    value = self.parse_ec_keywords()
                elif self.current_token.type_ == 'LIT_FLT':
                    value = self.parse_literal('float')
                elif self.current_token.type_ == 'LIT_STR':
                    value = self.parse_literal('string')
                elif self.current_token.type_ == 'LIT_CHAR':
                    value = self.parse_literal('char')
                elif self.current_token.type_ == 'LIT_BOOLTRUE':
                    value = self.parse_literal('bool')
                elif self.current_token.type_ == 'LIT_BOOLFALSE':
                    value = self.parse_literal('bool')
                elif self.current_token.type_ == 'IDENTIFIER':
                    value = self.parse_identifier()
                else:
                    raise SyntaxError(f"Unexpected token: {self.current_token.type_}")

                values.append(value)

                if self.current_token.type_ == 'DEL_RPAREN':
                    break
                elif self.current_token.type_ == 'OP_ADD':
                    self.consume_token()
                else:
                    raise SyntaxError(f"Expected '+' or ')', but found {self.current_token.type_}")

            self.consume_token()
            return OutputStatementNode(f'{output_statement}()', values)
        else:
            raise SyntaxError(f"Expected '(', but found {self.current_token.type_}")

    # This method primarily handles the parsing of statements starting with an identifier (e.g. x = y, x = Scan(), or x++)
    def parse_assignment_unary_statement(self):
        if self.current_token.type_ == 'IDENTIFIER':
            identifier = self.parse_identifier()
            next_token = self.peek_next_token()
            if next_token.value in KEYWORDS:
                self.consume_token()
                return self.parse_ec_keywords()
            elif self.current_token.type_ == 'OP_ASS' and next_token.value == 'Scan':
                self.consume_token()
                scan = self.parse_input_statement()
                self.consume_token()
                return InputStatementNode(identifier, scan)
            elif self.current_token.type_ in TOKEN_ASS_OPS and next_token.type_ not in ['LIT_STR', 'LIT_CHAR']:
                ass_op_type = self.current_token.value
                self.consume_token()
                value = self.parse_additive_expression()
                return AssignmentStatementNode(identifier, ass_op_type, value)
            elif self.current_token.type_ == 'OP_ASS' and next_token.type_ == 'LIT_STR':
                ass_op_type = self.current_token.value
                self.consume_token()
                value = self.parse_literal('string')
                return AssignmentStatementNode(identifier, ass_op_type, value)
            elif self.current_token.type_ == 'OP_ASS' and next_token.type_ == 'LIT_CHAR':
                ass_op_type = self.current_token.value
                self.consume_token()
                value = self.parse_literal('char')
                return AssignmentStatementNode(identifier, ass_op_type, value)
            elif self.current_token.type_ in TOKEN_UNR_OPS:
                unary_op = self.current_token.value
                self.consume_token()
                return UnaryStatementNode(identifier, unary_op)
            else:
                raise SyntaxError(f"Expected an assignment or unary operator, but found {self.current_token.type_}")
        else:
            raise SyntaxError(f"Expected an identifier, but found {self.current_token.type_}")
        
    def parse_ec_keywords(self):
        if self.current_token.value == 'CV1':
            return self.parse_square_root(self.two_param_keyword('OP_MUL: *'))
        elif self.current_token.value == 'CV2':
            return self.two_param_keyword('OP_DIV: /')
        elif self.current_token.value == 'CV3':
            return self.two_param_keyword('OP_MUL: *')
        elif self.current_token.value == 'CVK':
            return self.one_param_keyword('OP_DIV: /', 1000)
        elif self.current_token.value == 'CKV':
            return self.one_param_keyword('OP_MUL: *', 1000)
        elif self.current_token.value == 'CVM':
            return self.one_param_keyword('OP_MUL: *', 1000)
        elif self.current_token.value == 'CMV':
            return self.one_param_keyword('OP_DIV: /', 1000)
        elif self.current_token.value == 'CMK':
            return self.one_param_keyword('OP_DIV: /', 1000000)
        elif self.current_token.value == 'CO1':
            return self.two_param_keyword('OP_DIV: /')
        elif self.current_token.value == 'CO2':
            return self.two_param_keyword('OP_DIV: /')
        elif self.current_token.value == 'CO3':
            return self.two_param_keyword('OP_DIV: /')
        elif self.current_token.value == 'CW1':
            return self.two_param_keyword('OP_DIV: /')
        elif self.current_token.value == 'CW2':
            return self.two_param_keyword('OP_MUL: *')
        elif self.current_token.value == 'CW3':
            return self.two_param_keyword('OP_MUL: *')
        elif self.current_token.value == 'CWK':
            return self.one_param_keyword('OP_DIV: /', 1000)
        elif self.current_token.value == 'CKM':
            return self.one_param_keyword('OP_MUL: *', 1000)
        elif self.current_token.value == 'CMW':
            return self.one_param_keyword('OP_MUL: *', 1000000)
        elif self.current_token.value == 'CWM':
            return self.one_param_keyword('OP_DIV: /', 1000000)
        elif self.current_token.value == 'CWH':
            return self.one_param_keyword('OP_DIV: /', 745.7)
        elif self.current_token.value == 'CKH':
            return self.one_param_keyword('OP_MUL: *', 1.341)
        elif self.current_token.value == 'CMH':
            return self.one_param_keyword('OP_MUL: *', 1341)
        elif self.current_token.value == 'CHW':
            return self.one_param_keyword('OP_MUL: *', 745.7)
        elif self.current_token.value == 'CHK':
            return self.one_param_keyword('OP_DIV: /', 1.341)
        elif self.current_token.value == 'CHM':
            return self.one_param_keyword('OP_DIV: /', 1341)
        elif self.current_token.value == 'CA1':
            return self.two_param_keyword('OP_DIV: /')
        elif self.current_token.value == 'CA2':
            return self.two_param_keyword('OP_DIV: /')
        elif self.current_token.value == 'CA3':
            return self.parse_square_root(self.two_param_keyword('OP_DIV: /'))
        elif self.current_token.value == 'CMA':
            return self.one_param_keyword('OP_DIV: /', 1000)
        elif self.current_token.value == 'CAM':
            return self.one_param_keyword('OP_MUL: *', 1000)
        elif self.current_token.value == 'CCH':
            return self.two_param_keyword('OP_MUL: *')
        elif self.current_token.value == 'CCA':
            return self.two_param_keyword('OP_DIV: /')
        elif self.current_token.value == 'CHTM':
            return self.one_param_keyword('OP_MUL: *', 60)
        elif self.current_token.value == 'CMTS':
            return self.one_param_keyword('OP_MUL: *', 60)
        elif self.current_token.value == 'CHTS':
            return self.one_param_keyword('OP_MUL: *', 3600)
        elif self.current_token.value == 'CMTH':
            return self.one_param_keyword('OP_DIV: /', 60)
        elif self.current_token.value == 'CSTM':
            return self.one_param_keyword('OP_DIV: /', 60)
        elif self.current_token.value == 'CSTH':
            return self.one_param_keyword('OP_DIV: /', 3600)
        else:
            raise SyntaxError("Invalid reserved word encountered")

    def two_param_keyword(self, op):
        self.consume_token()
        if self.current_token.type_ == 'DEL_LPAREN':
            self.consume_token()
            if self.current_token.type_ in ['LIT_INT', 'LIT_FLT', 'IDENTIFIER']:
                var1 = self.current_token.value
                self.consume_token()
                if self.current_token.type_ == 'DEL_COMMA':
                    self.consume_token()
                    if self.current_token.type_ in ['LIT_INT', 'LIT_FLT', 'IDENTIFIER']:
                        var2 = self.current_token.value
                        self.consume_token()
                        if self.current_token.type_ == 'DEL_RPAREN':
                            self.consume_token()
                            return ECKeywordNode(var1, op, var2)
                        else:
                            raise SyntaxError(f"Expected ')', but found {self.current_token.type_}")
                    else:
                        raise SyntaxError(f"Expected literal of type int/float, but found {self.current_token.type_}")
                else:
                    raise SyntaxError(f"Expected a comma, but found {self.current_token.type_}")
            else:
                raise SyntaxError(f"Expected literal of type int/float, but found {self.current_token.type_}")
        else:
            raise SyntaxError(f"Expected '(', but found {self.current_token.type_}")
        
    def one_param_keyword(self, op, var2):
        self.consume_token()
        if self.current_token.type_ == 'DEL_LPAREN':
            self.consume_token()
            if self.current_token.type_ in ['LIT_INT', 'LIT_FLT', 'IDENTIFIER']:
                var1 = self.current_token.value
                self.consume_token()
                if self.current_token.type_ == 'DEL_RPAREN':
                    self.consume_token()
                    return ECKeywordNode(var1, op, var2)
                else:
                    raise SyntaxError(f"Expected ')', but found {self.current_token.type_}")
            else:
                raise SyntaxError(f"Expected literal of type int/float, but found {self.current_token.type_}")
        else:
            raise SyntaxError(f"Expected '(', but found {self.current_token.type_}")
        
    def parse_square_root(self, node):
        return SquareRootNode(node)
    
    # The next four methods handles the correct parsing of boolean expressions
    def parse_logical_or_expression(self):
        left_node = self.parse_logical_and_expression()

        while self.current_token.type_ == 'OP_LOGOR':
            op_token = self.current_token
            self.consume_token()
            right_node = self.parse_logical_and_expression()

            left_node = BinOpNode(left_node, op_token, right_node)

        return left_node
    
    def parse_logical_and_expression(self):
        left_node = self.parse_equality_expression()

        while self.current_token.type_ == 'OP_LOGAND':
            op_token = self.current_token
            self.consume_token()
            right_node = self.parse_equality_expression()

            left_node = BinOpNode(left_node, op_token, right_node)

        return left_node
    
    def parse_equality_expression(self):
        left_node = self.parse_relational_expression()

        while self.current_token.type_ in ['OP_EQT', 'OP_NEQT']:
            op_token = self.current_token
            self.consume_token()
            right_node = self.parse_relational_expression()

            left_node = BinOpNode(left_node, op_token, right_node)

        return left_node
    
    def parse_relational_expression(self):
        left_node = self.parse_additive_expression()

        if self.current_token.type_ in ('OP_GRT', 'OP_LST', 'OP_GRTEQ', 'OP_LSTEQ'):
            op_token = self.current_token
            self.consume_token()
            right_node = self.parse_additive_expression()

            return BinOpNode(left_node, op_token, right_node)
        
        return left_node
        
    def parse_while_statement(self):
        loop_type = "while_loop"
        self.consume_token()
        if self.current_token.type_ == 'DEL_LPAREN':
            self.consume_token()
        else:
            raise SyntaxError(f"Expected '(', but found {self.current_token.type_}")
        
        condition_node = self.parse_logical_or_expression()

        if self.current_token.type_ == 'DEL_RPAREN':
            self.consume_token()
        else:
            raise SyntaxError(f"Expected ')', but found {self.current_token.type_}") 
        
        if self.current_token.type_ == 'DEL_LBRACE':
            self.consume_token()
        else:
            raise SyntaxError(f"Expected '{'{'}', but found {self.current_token.type_}")
        
        body_node = self.parse_body()

        if self.current_token.type_ == 'DEL_RBRACE':
            self.consume_token()
        else:
            raise SyntaxError(f"Expected '{'}'}', but found {self.current_token.type_}")

        return IterativeDoStatementNode(loop_type, condition_node, body_node)
    
    def parse_do_while_statement(self):
        loop_type = "do_while_loop"
        self.consume_token()

        if self.current_token.type_ == 'DEL_LBRACE':
            self.consume_token()
        else:
            raise SyntaxError(f"Expected '{'{'}', but found {self.current_token.type_}")
        
        body_node = self.parse_body()

        if self.current_token.type_ == 'DEL_RBRACE':
            self.consume_token()
        else:
            raise SyntaxError(f"Expected '{'}'}', but found {self.current_token.type_}")
        
        if self.current_token.value == 'while':
            self.consume_token()
        else:
            raise SyntaxError(f"Expected 'while', but found {self.current_token.type_}")
        
        if self.current_token.type_ == 'DEL_LPAREN':
            self.consume_token()
        else:
            raise SyntaxError(f"Expected '(', but found {self.current_token.type_}")
        
        condition_node = self.parse_logical_or_expression()

        if self.current_token.type_ == 'DEL_RPAREN':
            self.consume_token()
        else:
            raise SyntaxError(f"Expected ')', but found {self.current_token.type_}") 

        return IterativeDoStatementNode(loop_type, condition_node, body_node)
    
    def parse_for_statement(self):
        self.consume_token()
        if self.current_token.type_ == 'DEL_LPAREN':
            self.consume_token()
        else:
            raise SyntaxError(f"Expected '(', but found {self.current_token.type_}")
        
        if self.current_token.type_ in ['DT_INT', 'DT_FLOAT']:
            variable = self.parse_declaration_statement()
        elif self.current_token.type_ == 'IDENTIFIER':
            variable = self.parse_variable_list('int')
        else:
            raise SyntaxError(f"Expected an identifier or declaration statement of type int/float, but found {self.current_token.type_}") 
        
        self.check_semicolon()
        condition_node = self.parse_logical_or_expression()
        self.check_semicolon()
        
        if self.current_token.type_ == 'IDENTIFIER':
            next_token = self.peek_next_token()

            if next_token.type_ in TOKEN_UNR_OPS:
                unary_exp = self.parse_assignment_unary_statement()
        else:
            raise SyntaxError(f"Expected a unary expression, but found {self.current_token.type_}") 

        if self.current_token.type_ == 'DEL_RPAREN':
            self.consume_token()
        else:
            raise SyntaxError(f"Expected ')', but found {self.current_token.type_}") 
        
        if self.current_token.type_ == 'DEL_LBRACE':
            self.consume_token()
        else:
            raise SyntaxError(f"Expected '{'{'}', but found {self.current_token.type_}")
        
        body_node = self.parse_body()

        if self.current_token.type_ == 'DEL_RBRACE':
            self.consume_token()
        else:
            raise SyntaxError(f"Expected '{'}'}', but found {self.current_token.type_}")

        return IterativeForStatementNode(variable, condition_node, unary_exp, body_node)

    def parse_if_statement(self):
        self.consume_token()
        if self.current_token.type_ == 'DEL_LPAREN':
            self.consume_token()
        else:
            raise SyntaxError(f"Expected '(', but found {self.current_token.type_}")
        
        condition_node = self.parse_logical_or_expression()

        if self.current_token.type_ == 'DEL_RPAREN':
            self.consume_token()
        else:
            raise SyntaxError(f"Expected ')', but found {self.current_token.type_}") 
        
        if self.current_token.type_ == 'DEL_LBRACE':
            self.consume_token()
        else:
            raise SyntaxError(f"Expected '{'{'}', but found {self.current_token.type_}")
        
        if_body_node = self.parse_body()

        if self.current_token.type_ == 'DEL_RBRACE':
            self.consume_token()
        else:
            raise SyntaxError(f"Expected '{'}'}', but found {self.current_token.type_}")
        
        else_body_node = None
        elif_conditions = []
        elif_bodies = []

        while self.current_token.type_ == 'RESERVED_WORD' and (self.current_token.value == 'elseif' or self.current_token.value == 'else'):
            if self.current_token.value == 'elseif':
                self.consume_token()
                if self.current_token.type_ == 'DEL_LPAREN':
                    self.consume_token()
                else:
                    raise SyntaxError(f"Expected '(', but found {self.current_token.type_}")
                
                elif_condition_node = self.parse_logical_or_expression()
                elif_conditions.append(elif_condition_node)

                if self.current_token.type_ == 'DEL_RPAREN':
                    self.consume_token()
                else:
                    raise SyntaxError(f"Expected ')', but found {self.current_token.type_}") 
                
                if self.current_token.type_ == 'DEL_LBRACE':
                    self.consume_token()
                else:
                    raise SyntaxError(f"Expected '{'{'}', but found {self.current_token.type_}")
                
                elif_body_node = self.parse_body()
                elif_bodies.append(elif_body_node)

                if self.current_token.type_ == 'DEL_RBRACE':
                    self.consume_token()
                else:
                    raise SyntaxError(f"Expected '{'}'}', but found {self.current_token.type_}")

            elif self.current_token.value == 'else':
                self.consume_token()

                if self.current_token.type_ == 'DEL_LBRACE':
                    self.consume_token()
                else:
                    raise SyntaxError(f"Expected '{'{'}', but found {self.current_token.type_}")
                
                else_body_node = self.parse_body()

                if self.current_token.type_ == 'DEL_RBRACE':
                    self.consume_token()
                else:
                    raise SyntaxError(f"Expected '{'}'}', but found {self.current_token.type_}")

        return ConditionalStatementNode(condition_node, if_body_node, elif_conditions, elif_bodies, else_body_node)

    def parse_return_statement(self):
        self.consume_token()

        if self.current_token.type_ == 'LIT_INT':
                value = self.parse_literal('int')
        elif self.current_token.type_ == 'KEYWORD':
            value = self.parse_ec_keywords()
        elif self.current_token.type_ == 'LIT_FLT':
            value = self.parse_literal('float')
        elif self.current_token.type_ == 'LIT_STR':
            value = self.parse_literal('string')
        elif self.current_token.type_ == 'LIT_CHAR':
            value = self.parse_literal('char')
        elif self.current_token.type_ == 'LIT_BOOLTRUE':
            value = self.parse_literal('bool')
        elif self.current_token.type_ == 'LIT_BOOLFALSE':
            value = self.parse_literal('bool')
        elif self.current_token.type_ == 'IDENTIFIER':
            value = self.parse_identifier()
        
        return ReturnStatementNode(value)



#############################
#        Known Issues       #
#############################
    
# 1. The parser may throw an "Expected ; after statement" error
#    erratically upon encountering an improperly handled or 
#    unhandled error. 
    
# 2. The parser cannot handle parentheses when evaluating 
#    boolean expressions (e.g. d || d && (d || d))
    
# 3. The parser does not support printing binary expressions 
#    starting with a variable (e.g. Print(x + 5 * 2);), but
#    it supports binary expressions when the first parameter/value
#    is a number (e.g. Print(5 + y * (2-ans))).