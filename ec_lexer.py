from constants import *
from errors import IllegalCharError, UnexpectedFileExtentionError, UnterminatedStringError, UnmatchedDelimiterError, UnterminatedCommentError, ExcelPermissionError
import os
import pandas as pd

def read(file):
    # Check if the file extension is ec
    _, file_extension = os.path.splitext(file) 
    file_extension = file_extension.lower()

    if file_extension != ".ec":
        raise UnexpectedFileExtentionError()
    with open(file, "r") as file_obj:
        contents = file_obj.read()
    
    tokens = run(contents)

    # Export tokens to a spreadsheet file
    try:
        data = {'Token type': [token.type_ for token in tokens], 'Token value': [token.value for token in tokens]}
        df = pd.DataFrame(data)
        df.to_excel('tokens_table.xlsx', index=False)
    except Exception as e:
        raise ExcelPermissionError()
    
    return tokens
        
def run(contents):
        lexer = Lexer(contents)
        tokens = lexer.make_tokens()
        return tokens
        
class Token:
    def __init__(self, type_, value = None):
        self.type_ = type_
        self.value = value

    def __repr__(self):
        return f'{self.type_}: {self.value}'
    
class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = -1
        self.current_char = None
        self.increment_pos()
        self.in_quotes = False
        self.quote_count = 0

    def increment_pos(self):
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None
    
    def make_number(self): 
        num_str = ''
        dot_present = False

        while self.current_char != None and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                if dot_present == True: break # Break out of loop if there are two or more decimal points
                dot_present = True
                num_str += '.'
            else:
                num_str += self.current_char

            self.increment_pos()

        if dot_present == False:
            return Token(TT_INTLIT, int(num_str))
        else:
            return Token(TT_FLOATLIT, float(num_str))
        
    def make_identifier(self):
        id_str = ''

        while self.current_char != None and self.current_char in ALPHANUMERIC + '_':
            id_str += self.current_char
            self.increment_pos()

        if id_str in DATA_TYPES: 
            return Token(DATA_TYPES[id_str], id_str)
        elif id_str in BOOL_TYPES:
            return Token(BOOL_TYPES[id_str], id_str)
        elif id_str in KEYWORDS:
            return Token(TT_KEYWORD, id_str)
        elif id_str in RESERVED_WORDS:
            return Token(TT_RESERVEDWORD, id_str)
        else: 
            return Token(TT_IDENTIFIER, id_str) 

    def make_string_literal(self, delimiter_type):
        id_string = ''
        
        if delimiter_type == "double_quote":
            while self.current_char != '"':
                id_string += self.current_char
                self.increment_pos()
                if self.current_char == "'":
                    raise UnmatchedDelimiterError("double quote ('\"')")
                if self.current_char == None:
                    raise UnterminatedStringError("double quote ('\"')")
        elif delimiter_type == "single_quote":
             while self.current_char != "'":
                id_string += self.current_char
                self.increment_pos()
                if self.current_char == '"':
                    raise UnmatchedDelimiterError('single quote ("\'")')
                if self.current_char == None:
                    raise UnterminatedStringError('single quote ("\'")')

        self.in_quotes = False

        if len(id_string) == 1: 
            return Token(TT_CHARLIT, id_string)
        elif len(id_string) > 1: 
            return Token(TT_STRLIT, id_string)

    def skip_singleline_comment(self):
        # Loop until the line ends or it encounters a new line
        while self.current_char not in ('\n', None): 
            self.increment_pos()

    def skip_multiline_comment(self):
        # Loop until '*/' is encountered
        while self.current_char != '*' or (self.pos + 1 < len(self.text) and self.text[self.pos + 1] != '/'):
            # Raise an error if EOF is reached
            if self.pos + 1 >= len(self.text): 
                raise UnterminatedCommentError()
            self.increment_pos()

        self.increment_pos() # Increment over '*'
        self.increment_pos() # Increment over '/'

    def raise_multiple_char_error(self):
        illegal_char = ""
        while self.current_char not in (' ', '\t', '\n', '_', *ALPHANUMERIC, None):
            illegal_char += self.current_char
            self.increment_pos()
        raise IllegalCharError(illegal_char)
    
    #Check for multiple character error on characters
    def check_multiple_char_error_length_1(self): 
        if self.pos + 1 < len(self.text) and self.text[self.pos + 1] not in (' ', '(', '\t', '\n', ';', '_', "'", '"', *ALPHANUMERIC, None):
            self.raise_multiple_char_error()

    def check_multiple_char_error_length_2(self): 
        if self.pos + 2 < len(self.text) and self.text[self.pos + 2] not in (' ', '(', '\t', '\n', ';', '_', "'", '"', *ALPHANUMERIC, None):
            self.raise_multiple_char_error()

    # def check_multiple_char_error_length_3(self): 
    #     if self.pos + 3 < len(self.text) and self.text[self.pos + 3] not in (' ', '\t', '\n', ';', '_', *ALPHANUMERIC, None):
    #         self.raise_multiple_char_error()
    
    # def check_multiple_char_error_ass_op(self): 
    #     if self.pos + 2 < len(self.text) and self.text[self.pos + 2] not in (' ', '\t', '\n', ';', '_', "'", '"', '(', *ALPHANUMERIC, None):
    #         self.raise_multiple_char_error()

    #Tokenizer class
    def make_tokens(self):
        tokens = []

        # Loop until EOF
        while self.current_char != None: 
            if self.current_char in ' \t \n': # Skip whitespace, tab, and newline characters
                self.increment_pos()
            elif self.in_quotes:
                tokens.append(self.make_string_literal(delimiter_type))
                if tokens[-1] == None: # Remove None from token if the literal is blank
                    tokens.pop()
            elif self.current_char == '"':
                #tokens.append(Token(TT_DOUBLEQUOTE,'"'))
                delimiter_type = "double_quote"
                self.quote_count += 1
                if self.quote_count % 2 != 0: 
                    self.in_quotes = True
                self.increment_pos()
            elif self.current_char == "'":
                #tokens.append(Token(TT_SINGLEQUOTE,"'"))
                delimiter_type = "single_quote"
                self.quote_count += 1
                if self.quote_count % 2 != 0:
                    self.in_quotes = True
                self.increment_pos()
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            elif self.current_char in LETTERS + '_':
                tokens.append(self.make_identifier())
            elif self.current_char == '+':
                if self.pos + 1 < len(self.text) and self.text[self.pos + 1] == '=':
                    self.check_multiple_char_error_length_2()
                    tokens.append(Token(TT_ADDASS, '+='))
                    self.increment_pos() 
                    self.increment_pos() 
                elif self.pos + 1 < len(self.text) and self.text[self.pos + 1] == '+': 
                    self.check_multiple_char_error_length_2()
                    tokens.append(Token(TT_INC, '++'))
                    self.increment_pos()
                    self.increment_pos()
                # elif self.pos + 1 < len(self.text) and self.text[self.pos + 1] == '(': 
                #     self.check_multiple_char_error_length_2()
                #     tokens.append(Token(TT_ADD, '+'))
                #     tokens.append(Token(TT_LPAREN, '('))
                #     self.increment_pos()
                #     self.increment_pos()
                else:
                    self.check_multiple_char_error_length_1()
                    tokens.append(Token(TT_ADD,'+'))
                    self.increment_pos()
            elif self.current_char == '-':
                if self.pos + 1 < len(self.text) and self.text[self.pos + 1] == '=':
                    self.check_multiple_char_error_length_2()
                    tokens.append(Token(TT_SUBASS, '-='))  
                    self.increment_pos()
                    self.increment_pos()
                elif self.pos + 1 < len(self.text) and self.text[self.pos + 1] == '-':
                    self.check_multiple_char_error_length_2()
                    tokens.append(Token(TT_DEC, '--'))
                    self.increment_pos()
                    self.increment_pos()
                # elif self.pos + 1 < len(self.text) and self.text[self.pos + 1] == '(': 
                #     self.check_multiple_char_error_length_2()
                #     tokens.append(Token(TT_SUB, '-'))
                #     tokens.append(Token(TT_LPAREN, '('))
                #     self.increment_pos()
                #     self.increment_pos()
                else:
                    self.check_multiple_char_error_length_1()
                    tokens.append(Token(TT_SUB,'-'))
                    self.increment_pos()
            elif self.current_char == '*':
                if self.pos + 1 < len(self.text) and self.text[self.pos + 1] == '*':
                    self.check_multiple_char_error_length_2()
                    tokens.append(Token(TT_EXP, '**'))
                    self.increment_pos()
                    self.increment_pos()
                elif self.pos + 1 < len(self.text) and self.text[self.pos + 1] == '=':
                    self.check_multiple_char_error_length_2()
                    tokens.append(Token(TT_MULASS, '*='))
                    self.increment_pos()
                    self.increment_pos()
                # elif self.pos + 1 < len(self.text) and self.text[self.pos + 1] == '(': 
                #     self.check_multiple_char_error_length_2()
                #     tokens.append(Token(TT_MUL, '*'))
                #     tokens.append(Token(TT_LPAREN, '('))
                #     self.increment_pos()
                #     self.increment_pos()
                else:
                    self.check_multiple_char_error_length_1()
                    tokens.append(Token(TT_MUL, '*'))
                    self.increment_pos()
            elif self.current_char == '/':
                if self.pos + 1 < len(self.text) and self.text[self.pos + 1] == '=':
                    self.check_multiple_char_error_length_2()
                    tokens.append(Token(TT_DIVASS, '/='))
                    self.increment_pos()
                    self.increment_pos()
                elif self.pos + 1 < len(self.text) and self.text[self.pos + 1] == '/':
                    self.skip_singleline_comment()
                elif self.pos + 1 < len(self.text) and self.text[self.pos + 1] == '*':
                    self.skip_multiline_comment()
                # elif self.pos + 1 < len(self.text) and self.text[self.pos + 1] == '(': 
                #     self.check_multiple_char_error_length_2()
                #     tokens.append(Token(TT_DIV, '/'))
                #     tokens.append(Token(TT_LPAREN, '('))
                #     self.increment_pos()
                #     self.increment_pos()
                else:
                    self.check_multiple_char_error_length_1()
                    tokens.append(Token(TT_DIV,'/'))
                    self.increment_pos()
            elif self.current_char == '%':                
                if self.pos + 1 < len(self.text) and self.text[self.pos + 1] == '=':
                    self.check_multiple_char_error_length_2()
                    tokens.append(Token(TT_MODASS, '%='))
                    self.increment_pos()
                    self.increment_pos()
                # elif self.pos + 1 < len(self.text) and self.text[self.pos + 1] == '(': 
                #     self.check_multiple_char_error_length_2()
                #     tokens.append(Token(TT_MOD, '%'))
                #     tokens.append(Token(TT_LPAREN, '('))
                #     self.increment_pos()
                #     self.increment_pos()
                else:
                    self.check_multiple_char_error_length_1()
                    tokens.append(Token(TT_MOD,'%'))
                    self.increment_pos()
            elif self.current_char == '=':
                if self.pos + 1 < len(self.text) and self.text[self.pos + 1] == '=':
                    if self.pos + 2 < len(self.text) and self.text[self.pos + 2] not in (' ', '\t', '\n', ';', '_', "'", '"', '(' *ALPHANUMERIC, None):
                        self.raise_multiple_char_error()
                    tokens.append(Token(TT_EQT, '=='))
                    self.increment_pos()
                    self.increment_pos()
                else:
                    if self.pos + 1 < len(self.text) and self.text[self.pos + 1] not in (' ', '\t', '\n', ';', '_', "'", '"', '(', *ALPHANUMERIC, None):
                        self.raise_multiple_char_error()
                    tokens.append(Token(TT_ASS, '='))
                    self.increment_pos()
            elif self.current_char == '>':
                if self.pos + 1 < len(self.text) and self.text[self.pos + 1] == '=':
                    self.check_multiple_char_error_length_2()
                    tokens.append(Token(TT_GRTEQ, '>='))
                    self.increment_pos()
                    self.increment_pos()
                else:
                    self.check_multiple_char_error_length_1()
                    tokens.append(Token(TT_GRT,'>'))
                    self.increment_pos()
            elif self.current_char == '<':
                if self.pos + 1 < len(self.text) and self.text[self.pos + 1] == '=':
                    self.check_multiple_char_error_length_2()
                    tokens.append(Token(TT_LSTEQ, '<='))
                    self.increment_pos()
                    self.increment_pos()
                else:
                    self.check_multiple_char_error_length_1()
                    tokens.append(Token(TT_LST,'<'))
                    self.increment_pos()
            elif self.current_char == '&':
                if self.pos + 1 < len(self.text) and self.text[self.pos + 1] == '&':
                    self.check_multiple_char_error_length_2()
                    tokens.append(Token(TT_LOGAND, '&&'))
                    self.increment_pos()
                    self.increment_pos()
                else:
                    raise IllegalCharError(self.current_char)
            elif self.current_char == '|':
                if self.pos + 1 < len(self.text) and self.text[self.pos + 1] == '|':
                    self.check_multiple_char_error_length_2()
                    tokens.append(Token(TT_LOGOR, '||'))
                    self.increment_pos()
                    self.increment_pos()
                else:
                    raise IllegalCharError(self.current_char)
            elif self.current_char == '!':
                if self.pos + 1 < len(self.text) and self.text[self.pos + 1] == '=':
                    self.check_multiple_char_error_length_2()
                    tokens.append(Token(TT_NEQT, '!='))
                    self.increment_pos()
                    self.increment_pos()
                else:
                    self.check_multiple_char_error_length_1()
                    tokens.append(Token(TT_LOGNOT,'!'))
                    self.increment_pos()
            elif self.current_char == '(':
                tokens.append(Token(TT_LPAREN,'('))
                self.increment_pos()
            elif self.current_char == ')':
                tokens.append(Token(TT_RPAREN,')'))
                self.increment_pos()
            elif self.current_char == '[':
                tokens.append(Token(TT_LBRACKET, '['))
                self.increment_pos()
            elif self.current_char == ']':
                tokens.append(Token(TT_RBRACKET, ']'))
                self.increment_pos()
            elif self.current_char == '{':
                tokens.append(Token(TT_LBRACE, '{'))
                self.increment_pos()
            elif self.current_char == '}':
                tokens.append(Token(TT_RBRACE, '}'))
                self.increment_pos()
            elif self.current_char == ';':
                if self.pos + 1 < len(self.text) and self.text[self.pos + 1] not in (' ', '\t', '\n', None):
                    illegal_char = ""
                    while self.current_char not in (' ', '\t', '\n', None):
                        illegal_char += self.current_char
                        self.increment_pos()
                    raise IllegalCharError(illegal_char)
                tokens.append(Token(TT_SEMICOLON, ';'))
                self.increment_pos()
            elif self.current_char == ',':
                self.check_multiple_char_error_length_1()
                tokens.append(Token(TT_COMMA, ','))
                self.increment_pos()
            else:
                raise IllegalCharError(self.current_char)
        return tokens
    
    