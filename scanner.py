
import re
from tokens import operator_tokens, keyword_tokens, Token

class Scanner:
    def __init__( self, input_file ):
        self.input_file = input_file
        self.token_list = []
        self.line_count = 0

    def make_token( self, part ):
        if isinstance( part, Token ):
            return part
        elif re.fullmatch( "[0-9]*", part ):
            return Token( "number", part, self.line_count )
        elif re.fullmatch( "[a-zA-Z_][a-zA-Z0-9_]*", part ):
            return Token( "string", part, self.line_count )

    def read( self ):
        # open input file
        file_object = open( self.input_file, 'r' )
        file_contents = file_object.read()
        
        # split input file by end line
        lines = re.split('\n+', file_contents)
        for line in lines:
            self.line_count = self.line_count + 1
            # split line by whitespace
            line = line.lower()
            parts = re.split( '\s+', line )
            
            for op in operator_tokens:
                new_parts = []
                for part in parts:
                    if isinstance( part, str ):
                        split = part.split( op.text )
                        for s in split:
                            if len( s ) > 0:
                                new_parts.append( s )
                            new_parts.append( Token( op.name, op.text, self.line_count ) )
                        new_parts.pop()
                    else:
                        new_parts.append( part )
                parts = new_parts
            
            for keyword in keyword_tokens:
                new_parts = []
                for part in parts:
                    if isinstance( part, str ):
                        split = part.split( keyword.text )
                        keyword_found = True
                        for s in split:
                            if s != '':
                                keyword_found = False
                        if keyword_found:
                            new_parts.append( Token( keyword.name, keyword.text, self.line_count ) )
                        else:
                            new_parts.append( part )
                    else:
                        new_parts.append( part )
                parts = new_parts
            new_parts = []
            for part in parts:
                new_parts.append( self.make_token( part ) )
            parts = new_parts

            self.token_list.extend( parts )
        return self.token_list
