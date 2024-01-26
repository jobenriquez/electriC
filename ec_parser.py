from errors import SyntaxError
from constants import *

#############################
#           Nodes           #
#############################

class ECProgStatementNode:
    def __init__(self, body):
        self.body = body

    def __repr__(self):
        return f'ECProgStatementNode({self.body})'
    
class BodyNode:
    def __init__(self, statements):
        self.statements = statements

    def __repr__(self):
        return f'BodyNode({self.statements})'
    
class DeclarationStatementNode:
    def __init__(self, data_type, identifier_init_list):
        self.data_type = data_type
        self.identifier_init_list = identifier_init_list

    def __repr__(self):
        return f'DeclarationStatementNode({self.data_type}, {self.identifier_init_list})'

class IdentifierNode:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'IdentifierNode({self.name})'
    
class LiteralNode:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'LiteralNode({self.value})'
    
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
        return f'AssignmentStatementNode({self.identifier}, {self.ass_op}, {self.value})'
            
class UnaryStatementNode:
    def __init__(self, identifier, unary_op):
        self.identifier = identifier
        self.unary_op = unary_op
    
    def __repr__(self):
        return f'AssignmentStatementNode({self.identifier}, {self.unary_op})'
    
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
    
    def parse_body(self):
        statements = []

        while self.current_token.type_ != 'DEL_RBRACE':
            current_statement = self.identify_statements()
            statements.append(current_statement)
            if self.current_token.type_ == 'DEL_SEMICOLON':
                self.consume_token()  # Consume the semicolon
            else:
                raise SyntaxError("Expected ';' after statement")

        return BodyNode(statements)

    def identify_statements(self):
        if self.current_token.type_ in TOKEN_DATA_TYPES:
            return self.parse_declaration_statement()
        if self.current_token.type_ == 'IDENTIFIER':
            return self.parse_assignment_unary_statement()
        
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
            raise SyntaxError("Invalid data type")

    def parse_variable_list(self, expected_data_type):
        identifier_list = []

        if self.current_token.type_ == 'IDENTIFIER':        
            identifier = self.parse_identifier()
            if self.current_token.type_ not in ('OP_ASS', 'DEL_COMMA', None):
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
        if expected_data_type == "string" or "char":
            if self.current_token.type_ in TOKEN_ASS_OPS:
                type_of_delimeter = None
                #self.match_type('OP_ASS')
                self.consume_token()

                if self.current_token.type_ == 'DEL_DBLQUOTE': 
                    self.match_type('DEL_DBLQUOTE')
                    type_of_delimeter = 'DEL_DBLQUOTE' # Save the type of delimiter used for checking
                elif self.current_token.type_ == 'DEL_SGLQUOTE':
                    self.match_type('DEL_SGLQUOTE')
                    type_of_delimeter = 'DEL_SGLQUOTE'

                try:
                    initialization = self.parse_literal(expected_data_type)
                    if type_of_delimeter == 'DEL_DBLQUOTE': 
                        self.match_type('DEL_DBLQUOTE') # Ensure that the delimiter used matches
                    elif type_of_delimeter == 'DEL_SGLQUOTE':
                        self.match_type('DEL_SGLQUOTE')
                    return initialization
                except SyntaxError as e:
                    raise SyntaxError(f"Error in variable initialization: {e}")
            else:
                return None
        elif expected_data_type == "int" or "float":
            if self.current_token.type_ == 'OP_ASS':
                self.match_type('OP_ASS')
                try:
                    initialization = self.parse_literal(expected_data_type)
                    return initialization
                except SyntaxError as e:
                    raise SyntaxError(f"Error in variable initialization: {e}")
            else:
                return None

    def parse_literal(self, expected_data_type):
        if self.current_token.type_ == 'IDENTIFIER':
            return self.parse_identifier()
        elif self.current_token.type_ == 'DEL_LPAREN':
            return self.parse_additive_expression()
        elif self.current_token.type_ == 'LIT_INT' and expected_data_type == 'int':
            return self.parse_additive_expression()
        elif self.current_token.type_ == 'LIT_FLT' and expected_data_type == 'float':
            return self.parse_additive_expression()
        elif self.current_token.type_ == 'LIT_CHAR' and expected_data_type == 'char':
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
        
    def get_data_type_value(self, literal_type):
        return TOKEN_DATA_TYPE_VALUES[literal_type]
        
    def parse_assignment_unary_statement(self):
        if self.current_token.type_ == 'IDENTIFIER':
            identifier = self.parse_identifier()
            next_token = self.peek_next_token()

            if self.current_token.type_ in TOKEN_ASS_OPS:
                if next_token.type_ in TOKEN_DATA_TYPE_VALUES:
                    ass_op_type = self.current_token.value
                    data_type = self.get_data_type_value(next_token.type_)
                    value = self.parse_initialization(data_type)
                    return AssignmentStatementNode(identifier, ass_op_type, value)
            elif self.current_token.type_ in TOKEN_UNR_OPS:
                unary_op = self.current_token.value
                self.consume_token()
                return UnaryStatementNode(identifier, unary_op)
            else:
                raise SyntaxError(f"Expected an assignment or unary operator, but found {self.current_token.type_}")
        else:
            raise SyntaxError(f"Expected an identifier, but found {self.current_token.type_}")