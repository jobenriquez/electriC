import string

#############################
#       Character set       # 
#############################
LETTERS = string.ascii_letters
DIGITS = '0123456789'
ALPHANUMERIC = DIGITS + LETTERS
#############################
#         Data types        #
#############################
TT_CHAR = 'DT_CHAR'
TT_INT = 'DT_INT'
TT_FLOAT = 'DT_FLOAT'
TT_STR = 'DT_STR'
TT_BOOL = 'DT_BOOL'
#############################
#          Literals         #
#############################
TT_INTLIT = 'LIT_INT'
TT_FLOATLIT = 'LIT_FLT'
TT_STRLIT = 'LIT_STR'
TT_CHARLIT = 'LIT_CHAR'
TT_BOOLTRUE = 'LIT_BOOLTRUE'
TT_BOOLFALSE = 'LIT_BOOLFALSE'
#############################
#   Assignment Operators    #
#############################
TT_ASS = 'OP_ASS'
TT_ADDASS = 'OP_ADDASS'
TT_SUBASS = 'OP_SUBASS'
TT_MULASS = 'OP_MULASS'
TT_DIVASS = 'OP_DIVASS'
TT_MODASS = 'OP_MODASS'
#############################
#   Arithmetic Operators    #
#############################
TT_ADD = 'OP_ADD'
TT_SUB = 'OP_SUB'
TT_MUL = 'OP_MUL'
TT_DIV = 'OP_DIV'
TT_MOD = 'OP_MOD'
TT_EXP = 'OP_EXP'
#############################
#      Unary Operators      #
#############################
TT_INC = 'OP_INC'
TT_DEC = 'OP_DEC'
#############################
#     Boolean Operators     #
#############################
TT_EQT = 'OP_EQT' #EQUAL TO
TT_NEQT = 'OP_NEQT'
TT_GRT = 'OP_GRT'
TT_LST = 'OP_LST'
TT_GRTEQ = 'OP_GR'
TT_LSTEQ = 'OP_LSTEQ'
TT_LOGAND = 'OP_LOGAND'
TT_LOGOR = 'OP_LOGOR'
TT_LOGNOT = 'OP_LOGNOT'
#############################
#         Delimiters        #
#############################
TT_LPAREN = 'DEL_LPAREN'
TT_RPAREN = 'DEL_RPAREN'
TT_LBRACKET = 'DEL_LBRACKET'
TT_RBRACKET = 'DEL_RBRACKET'
TT_LBRACE = 'DEL_LBRACE'
TT_RBRACE = 'DEL_RBRACE'
TT_COMMA = 'DEL_COMMA'
TT_SEMICOLON = 'DEL_SEMICOLON'
TT_SINGLEQUOTE = 'DEL_SGLQUOTE'
TT_DOUBLEQUOTE = 'DEL_DBLQUOTE'
#############################
#          Comments         #
#############################
TT_SGLCMNT = 'CMNT_SGLLNE'
TT_MLTCMNTOPN = 'CMNT_MLTLNE_OPN'
TT_MLTCMNTCLS = 'CMNT_MLTLNE_CLSE'
#################################
#  Keywords and Reserved words  #
#################################
DATA_TYPES = {
    'char': TT_CHAR,
    'character': TT_CHAR,
    'int': TT_INT,
    'integer': TT_INT,
    'float': TT_FLOAT,
    'string': TT_STR,
    'bool': TT_BOOL,
    'boolean': TT_BOOL
}
BOOL_TYPES = {
    'true': TT_BOOLTRUE,
    'false': TT_BOOLFALSE
}
RESERVED_WORDS = [
    'if',
    'else',
    'break',
    'Print',
    'PrintLine',
    'Scan',
    'return',
    'for',
    'while',
    'do',
    'true',
    'false',
    'continue',
    'Main'
]
KEYWORDS = [
    'CV1',
    'CV2',
    'CV3',
    'CVK',
    'CKV',
    'CVM',
    'CMV',
    'CMK',
    'CO1',
    'CO2',
    'CO3',
    'CW1',
    'CW2',
    'CW3',
    'CWK',
    'CKM',
    'CMW',
    'CWM',
    'CWH',
    'CKH',
    'CMH',
    'CHW',
    'CHK',
    'CHM',
    'CA1',
    'CA2',
    'CA3',
    'CMA',
    'CAM',
    'CCH',
    'CCA',
    'CHTM',
    'CMTS',
    'CHTS',
    'CMTH',
    'CSTM',
    'CSTH'
]
TOKEN_DATA_TYPES = [
    'DT_CHAR',
    'DT_INT',
    'DT_FLOAT',
    'DT_STR',
    'DT_BOOL'
]
TOKEN_DATA_TYPE_VALUES = {
    'LIT_INT': 'int',
    'LIT_FLT': 'float',
    'LIT_STR': 'string',
    'LIT_CHAR': 'char',
    'LIT_BOOLTRUE': 'bool',
    'LIT_BOOLFALSE':'bool'
}
TOKEN_ARITH_OPS = [
    'OP_ADD',
    'OP_SUB',
    'OP_MUL',
    'OP_DIV',
    'OP_MOD',
    'OP_EXP'
]
TOKEN_ASS_OPS = [
    'OP_ASS',
    'OP_ADDASS',
    'OP_SUBASS',
    'OP_MULASS',
    'OP_DIVASS',
    'OP_MODASS'
]
TOKEN_UNR_OPS = [
    'OP_INC',
    'OP_DEC'
]


#############################
#          Others           #
#############################
TT_IDENTIFIER = 'IDENTIFIER'
TT_KEYWORD = 'KEYWORD'
TT_RESERVEDWORD = 'RESERVED_WORD'