class IllegalCharError(Exception):
    def __init__(self, char, message = "Illegal Character Error"):
        super().__init__(f"{message}: '{char}' is not recognized by the lexer.") 

class UnexpectedFileExtentionError(Exception):
    def __init__(self, message = f"Unsupported File Extension Error: a file ending with .ec is expected"):
        self.message = message
        super().__init__(self.message)

class UnterminatedCommentError(Exception):
    def __init__(self, message = "Unterminated Comment Error: a '*/' is expected to terminate a multiline comment."):
        self.message = message
        super().__init__(self.message)

class UnterminatedStringError(Exception):
    def __init__(self, delimiter, message = "Unterminated String/Char Error"):
        self.message = message
        super().__init__(f"{message}: a {delimiter} is expected to terminate a string/char literal.")

class UnmatchedDelimiterError(Exception):
    def __init__(self, delimiter, message = "Unmatched String/Char Delimiter Error"):
        self.message = message
        super().__init__(f"{message}: a {delimiter} is expected to terminate a string/char literal.")
        
class ExcelPermissionError(Exception):
    def __init__(self, message = "Excel Permission Denied Error: the excel file is currently running and cannot be overwritten."):
        self.message = message
        super().__init__(self.message)

class SyntaxError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)