# Stephen Comarata
# EECE 5183 - 001 Compiler Theory 
# This program is the scanner class for the compiler project 
#
# scanner.py

# Imported libraries
import re

# Imported file classes
from tokens import operator_tokens, keyword_tokens, Token, t_comment, t_comment_start, t_comment_end

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
            return Token( "identifier", part, self.line_count )
        else:
            raise Exception( 'Scanning Error: Line #{} Idenifiers may not begin with numbers'.format( self.line_count ) )

    def read( self ):
        # open input file
        file_object = open( self.input_file, 'r' )
        lines = file_object.readlines()
        for line in lines:
            self.line_count = self.line_count + 1
            # split line by whitespace
            line = line.lower()
            parts = re.split( '\s+', line )

            for op in operator_tokens:
                if op.text == t_comment.text:
                    comment_flag = False
                    new_parts = []
                    for part in parts:
                        if not comment_flag:
                            if isinstance( part, str ):
                                split = part.split( op.text )
                                for s in split:
                                    if len( s ) > 0:
                                        new_parts.append( s )
                                    else: 
                                        # new_parts.append( Token( op.name, op.text, self.line_count ) )
                                        comment_flag = True
                                        break

                            else:
                                new_parts.append( part )

                    parts = new_parts
                else:         
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
        multi_line_comment = []
        remove_tokens = []
        for token in self.token_list:
            if token.text == t_comment_start.text:
                multi_line_comment.append( token.line_number )
                remove_tokens.append( token )
            elif token.text == t_comment_end.text:
                multi_line_comment.pop()
                remove_tokens.append( token )
            elif len( multi_line_comment ) > 0:
                remove_tokens.append( token )
        for token in remove_tokens:
            self.token_list.remove( token )

        return self.token_list
