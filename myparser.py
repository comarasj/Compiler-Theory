import re
import tokens
from scoper import Scoper

class Parser:
    def __init__( self, _token_list ):
        self.token_list = _token_list
        self.current_token = None
        self.scoper = Scoper( 'GLOBAL' )

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
        if not self.declarations():
            return False
        self.current_token = next( self.token_list )

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


    # There can be 0 to many declarations
    def declarations( self ):
        while( not self.is_token_type( tokens.t_begin ) ):
            # Check for global 

            # Check for procedure
            if self.is_token_type( tokens.t_procedure ):
                self.current_token = next( self.token_list )
                # Check procedure header
                if not self.procedure_header():
                    return False
                # Check procedure body
                self.current_token = next( self.token_list )
                if not self.procedure_body():
                    return False
                # Check procedure end
                if not self.procedure_end():
                    return False

            # Check for variables
            elif self.is_token_type( tokens.t_variable ):
                self.current_token = next( self.token_list )
                if not self.variable_declaration():
                    print( 'Invalid Variable Declaration' )
                    return False
            else:
                return False
        return True


        
    def procedure_header( self ):
        if not self.is_token_type( tokens.t_string ):
            return False
        if not self.scoper.create_new_scope( self.current_token.text ):
            return False

        procedure_name = self.current_token.text
        self.scoper.add_procedure( procedure_name )

        self.current_token = next( self.token_list )

        if not self.is_token_type( tokens.t_colon ):
            return False
        
        self.current_token = next( self.token_list )
    
        if ( not self.is_token_type( tokens.t_integer ) and 
           not self.is_token_type( tokens.t_float ) and 
           not self.is_token_type( tokens.t_string ) and 
           not self.is_token_type( tokens.t_bool ) ):
            return False
        
        procedure_type = self.current_token.text
        self.scoper.add_procedure_type( procedure_name, procedure_type ) 

        self.current_token = next( self.token_list )

        if not self.handle_input_params( procedure_name ):
            return False
        self.scoper.next_scope()
        return True
        
    def procedure_body( self ):
        # Check for declarations
        if not self.declarations():
            return False
        self.current_token = next( self.token_list )

        # Check for begin
        if not self.is_token_type( tokens.t_begin ):
            return False
        self.current_token = next( self.token_list )

    def procedure_end( self ):
        pass

    def handle_input_params( self, procedure_name ):
        if not self.is_token_type( tokens.t_lparen ):
            return False
        self.current_token = next( self.token_list )
        if not self.is_token_type( tokens.t_rparen ):
            while( True ):
                #TODO Populate parameters in identifiers list
                if not self.is_token_type( tokens.t_variable ):
                    return False
                self.current_token = next( self.token_list )

                if not self.is_token_type( tokens.t_string ):
                    return False
                var_name = self.current_token.text
                self.scoper.add_procedure_input_param( procedure_name, var_name )
                self.current_token = next( self.token_list )

                if not self.is_token_type( tokens.t_colon ):
                    return False
                self.current_token = next( self.token_list )

                if ( not self.is_token_type( tokens.t_integer ) and 
                   not self.is_token_type( tokens.t_float ) and 
                   not self.is_token_type( tokens.t_string ) and 
                   not self.is_token_type( tokens.t_bool ) ):
                    return False
                var_type = self.current_token.text
                self.scoper.add_procedure_input_param_type( procedure_name, var_name, var_type )
                self.current_token = next( self.token_list )
                if self.is_token_type( tokens.t_comma ):
                    self.current_token = next( self.token_list )
                elif self.is_token_type( tokens.t_rparen ):
                    break
                else:
                    return False
        return True


    def variable_declaration( self ):
        if not self.create_var_declaration():
            return False
        self.current_token = next( self.token_list )
        return True
    

    def create_var_declaration( self ):
        var_name = self.current_token.text
        self.scoper.add_variable( var_name )
        self.current_token = next( self.token_list )
        if not self.is_token_type( tokens.t_colon ):
            return False
        self.current_token = next( self.token_list )
        if ( not self.is_token_type( tokens.t_integer ) and 
               not self.is_token_type( tokens.t_float ) and 
               not self.is_token_type( tokens.t_string ) and 
               not self.is_token_type( tokens.t_bool ) ):
            print( 'Invalid variable type' )
            return False
        var_type = self.current_token.name
        self.scoper.add_variable_type( var_name, var_type )
        self.current_token = next( self.token_list )
        if not self.is_token_type( tokens.t_semicolon ):
            return False
        return True

