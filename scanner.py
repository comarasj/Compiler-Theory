# Stephen Comarata
# EECE 5183 - 001 Compiler Theory 
# This program is the scanner class for the compiler project 
#
# scanner.py

# Imported libraries
import re, sys

# Imported file classes
from tokens import operator_tokens, keyword_tokens, Token, t_comment, t_comment_start, t_comment_end, t_period, t_program, t_quote

class Scanner:
    def __init__( self, input_file, logger ):
        self.input_file = input_file
        self.token_list = []
        self.line_count = 0
        self.logger = logger
        self.logger.set_origin( 'Scanner' )


    def make_token( self, part ):
        if isinstance( part, Token ):
            return part
        elif re.fullmatch( "[0-9]+\.[0-9]*", part ):
            return Token( "number", float( part ), self.line_count )
        elif re.fullmatch( "[0-9]*", part ):
            return Token( "number", int( part ), self.line_count )
        elif re.fullmatch( "[a-zA-Z_][a-zA-Z0-9_]*", part ):
            return Token( "identifier", part, self.line_count )
        elif t_period.text == part:
            return Token( t_period.name, t_period.text, self.line_count )
        elif re.fullmatch( '[^"]*', part ):
            return Token( "string", part, self.line_count )
        else:
            raise Exception( 'Scanning Error: Line #{} Idenifiers may not begin with numbers'.format( self.line_count ) )


    def read( self ):
        # open input file
        try:
            file_object = open( self.input_file, 'r' )
        except:
            self.logger.report_error( 'Could not open ' + self.input_file + ' ', 0 )
            sys.exit( 2 )
        lines = file_object.readlines()
        for line in lines:
            self.line_count = self.line_count + 1
            # split line by whitespace
            split = re.split( t_quote.text, line )
            if len( split ) > 1:
                # do stuff
                new_parts = []
                print( 'here' )
                count = 0
                for s in split:
                    if count % 2 == 0:
                        new_parts.append( s )
                    else:
                        new_parts.append( Token( op.name, op.text, self.line_count ) )
                        new_parts.append( Token( 'string', s, self.line_count  ) )
                        new_parts.append( Token( op.name, op.text, self.line_count ) )

                    count = count + 1
                parts = []
                for part in new_parts:
                    if isinstance( part, str ):
                        part = part.lower()
                        part = part.strip()
                        part = re.split( '\s+', part )
                        for s in part:
                           parts.append( s ) 
                    else:
                        parts.append( part )
            else:
                line = line.lower()
                line = line.strip()
                parts = re.split( '\s+', line )
            # Check for operators  
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
            
            # Check for keywords
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
                            if part == 'program.':
                                new_parts.append( Token( t_program.name, t_program.text, self.line_count ) )
                                new_parts.append( Token( t_period.name, t_period.text, self.line_count ) )
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
