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
    
class InputStatementNode:
    def __init__(self, identifier, scan_statement):
        self.identifier = identifier
        self.scan_statement = scan_statement
    
    def __repr__(self):
        return f'InputStatementNode({self.identifier}, {self.scan_statement})'
    
class OutputStatementNode:
    def __init__(self, output_statement, initialization):
        self.output_statement = output_statement
        self.initialization = initialization
    
    def __repr__(self):
        return f'OutputStatementNode({self.output_statement}, {self.initialization})'
    
class ECKeywordNode:
    def __init__(self, var1, op, var2):
        self.var1 = var1
        self.op = op
        self.var2 = var2
    
    def __repr__(self):
        return f'ECKeywordNode({self.var1}, {self.op}, {self.var2})'
    
class SquareRootNode:
    def __init__(self, node):
        self.node = node

    def __repr__(self):
        return f'SquareRootNode({self.node})'

    
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
                self.consume_token() 
            else:
                raise SyntaxError("Expected ';' after statement")

        return BodyNode(statements)

    def identify_statements(self):
        if self.current_token.type_ in TOKEN_DATA_TYPES:
            return self.parse_declaration_statement()
        if self.current_token.type_ == 'IDENTIFIER':
            return self.parse_assignment_unary_statement()
        if self.current_token.type_ == 'RESERVED_WORD' and self.current_token.value in ['Print', 'PrintLine']:
            return self.parse_output_statement()
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
        if expected_data_type in ['int', 'float', 'integer', None]:
            if self.current_token.type_ in TOKEN_ASS_OPS:
                self.consume_token()
                initialization = self.parse_literal(expected_data_type)
                return initialization
            else:
                return None
        elif expected_data_type in ['string', 'char', 'bool', 'boolean', None]:
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
        if self.current_token.type_ == 'IDENTIFIER':
            return self.parse_identifier()
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
        elif self.current_token.value == 'Scan':
            return self.parse_input_statement()
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
            if self.current_token.type_ == 'DEL_RPAREN':
                self.consume_token()
                return OutputStatementNode(f'{output_statement}()', value)
            else:
                raise SyntaxError(f"Expected ')', but found {self.current_token.type_}")
        else:
            raise SyntaxError(f"Expected '(', but found {self.current_token.type_}")
        
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
            if self.current_token.type_ in ['LIT_INT', 'LIT_FLT']:
                var1 = self.current_token.value
                self.consume_token()
                if self.current_token.type_ == 'DEL_COMMA':
                    self.consume_token()
                    if self.current_token.type_ in ['LIT_INT', 'LIT_FLT']:
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
            if self.current_token.type_ in ['LIT_INT', 'LIT_FLT']:
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