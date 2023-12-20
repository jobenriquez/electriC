class Error:
    def __init__(self, error_name, details):
        self.error_name = error_name
        self.details = details

    def as_string(self):
        result = f'{self.error_name}: {self.details}'
        return result
    
class IllegalCharError(Error):
    def __init__(self, details):
        super().__init__('Illegal character error', details)
    
# class IllegalCharError(Exception):
#     def __init__(self, char, message = "Illegal character error:"):
#         super().__init__(f"{message}: '{char}'") 

class UnterminatedCommentError(Error):
    def __init__(self, details):
        super().__init__('Multiline comment unterminated', details)

# class UnexpectedFileExtentionError(Exception):
#     def __init__(self, message = f"Unsupported file extension error: a file ending with .ec is expected"):
#         self.message = message
#         super().__init__(self.message)