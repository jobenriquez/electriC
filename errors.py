class IllegalCharError(Exception):
    def __init__(self, char, message = "Illegal character error"):
        super().__init__(f"{message}: '{char}' is not recognized by the lexer.") 

class UnexpectedFileExtentionError(Exception):
    def __init__(self, message = f"Unsupported file extension error: a file ending with .ec is expected"):
        self.message = message
        super().__init__(self.message)

class UnterminatedCommentError(Exception):
    def __init__(self, message = "Unterminated comment error: a '*/' is expected to terminate the multiline comment."):
        self.message = message
        super().__init__(self.message)