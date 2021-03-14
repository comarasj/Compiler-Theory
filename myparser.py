import re
import tokens

class Parser:
    def __init__( self, _token_list ):
        self.token_list = _token_list
        self.current_token = None

    def is_token_type( self, test_token ):
        if self.current_token.name == test_token.name:
            return True
        return False

    # Start to parse
    def parse( self ):
        self.current_token = next( self.token_list )
        self.program()
    
    def program( self ):
        # Check program header
        if not self.program_header():
            return False
        # Check program body
        if not self.program_body():
            return False
        # Check program end '.'
        if not self.program_end():
            return False
        return True

    def program_header( self ):
        if not self.is_token_type( tokens.t_program ):
            return False
        self.current_token = next( self.token_list )

        if not self.is_token_type( tokens.t_string ):
            return False
        self.current_token = next( self.token_list )

        if not self.is_token_type( tokens.t_is ):
            return False
        self.current_token = next( self.token_list )

        print( 'Correct program header' )
        return True
    
    def program_body( self ):
        # Check for declarations

        # Check for begin
        if not self.is_token_type( tokens.t_begin ):
            return False
        self.current_token = next( self.token_list )

        # Check for valid statements
        ##
        ##

        # Check for end
        if not self.is_token_type( tokens.t_end ):
            return False
        self.current_token = next( self.token_list )

        # Check for program 
        if not self.is_token_type( tokens.t_program ):
            return False
        self.current_token = next( self.token_list )

        print( 'Correct program body' )

        return True
    
    def program_end( self ):
        # Check for period '.'
        if not self.is_token_type( tokens.t_period ):
            return False
        return True