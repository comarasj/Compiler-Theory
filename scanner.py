
import re
from tokens import recognized_ops, Token, comment, comment_start, comment_end

class Scanner:
    def __init__( self, input_file ):
        self.input_file = input_file
        self.token_list = []

    def make_token( self, part ):
        if isinstance(part, Token):
            return part
        elif re.fullmatch("[0-9]*", part):
            return Token("integer", part)
        elif re.fullmatch("[a-zA-Z_][a-zA-Z0-9_]*", part):
            return Token("name", part)

    def read( self ):
        # open input file
        file_object = open( self.input_file, 'r' )
        file_contents = file_object.read()
        
        # split input file by whitespace
        parts = re.split('\s+', file_contents)
        for op in recognized_ops:
            new_parts = []
            for part in parts:
                if isinstance( part, str ):
                    split = part.split( op.text )
                    for s in split:
                        if len( s ) > 0:
                            new_parts.append( s )
                        new_parts.append( op )
                    new_parts.pop()
                else:
                    new_parts.append( part )
            parts = new_parts
        
        # Clean up the parts and tokenize strings and numbers
        for part in parts:
            self.token_list.append( self.make_token( part ) )

        return self.token_list          
