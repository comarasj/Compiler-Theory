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
        if not self.declaration():
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

        if not self.is_token_type( tokens.t_period ):
            return False
        
        print( 'Correct program body' )
        return True 


    # There can be 0 to many declarations
    def declaration( self ):
        while( not self.is_token_type( tokens.t_begin ) ):
            # Check for global 

            # Check for procedure
            if self.is_token_type( tokens.t_procedure ):
                self.current_token = next( self.token_list )
                if not self.procedure_declaration():
                    print( 'Invalid Procedure Declaration' )
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


    def procedure_declaration( self ):
        # Check procedure header
        if not self.procedure_header():
            return False
        # Check procedure body
        self.current_token = next( self.token_list )
        if not self.procedure_body():
            return False


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

        print( 'Correct procedure header' )
        return True


    def procedure_body( self ):
        # Check for declarations
        if not self.declaration():
            return False
        # Check for begin
        if not self.is_token_type( tokens.t_begin ):
            return False
        self.current_token = next( self.token_list )
        # Check for valid code
        if not self.valid_code( tokens.t_procedure ):
            return False
        
        
        if not self.is_token_type( tokens.t_end ):
            return False
        self.current_token = next( self.token_list )

        if not self.is_token_type( tokens.t_procedure ):
            return False
        self.current_token = next( self.token_list )

        if not self.is_token_type( tokens.t_semicolon ):
            return False
        
        print( 'Correct procedure body' )
        return True        


    def handle_input_params( self, procedure_name ):
        if not self.is_token_type( tokens.t_lparen ):
            return False
        self.current_token = next( self.token_list )
        if not self.is_token_type( tokens.t_rparen ):
            while( True ):
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


    '''
    Check for valid code declarations
        caller is of type token
    '''
    def valid_code( self, caller ):
        if self.is_token_type( tokens.t_if ):
            # handle if statement
            self.current_token = next( self.token_list )
            if not self.if_header():
                return False
            
            if not self.if_body():
                return False
            
            if not self.if_end():
                return False

        elif self.is_token_type( tokens.t_for ):
            # handle for loop
            return False
        elif self.is_token_type( tokens.t_variable ):
            # handle variable assignment
            return False
        elif self.is_token_type( tokens.t_string ):
            # handle variable operations
            return False
        elif self.is_token_type( tokens.t_return ):
            # handle return
            return False


        return True


    def if_header( self ):
        if not self.is_token_type( tokens.t_lparen ):
            return False
        self.current_token = next( self.token_list )

        # Check for an identifier or number or true or false
        if self.is_token_type( tokens.t_string ):
            if not self.scoper.is_variable_in_scope( self.current_token.text ):
                return False
        elif not self.is_token_type( tokens.t_number ) and not self.is_token_type( tokens.t_true and not self.is_token_type( tokens.t_false ) ):
            return False
        self.current_token = next( self.token_list )
         
        # Check for comparison operator
        if not ( self.is_token_type( tokens.t_equal_to ) or self.is_token_type( tokens.t_greater_than ) or
                 self.is_token_type( tokens.t_greater_than_or_equal_to ) or self.is_token_type( tokens.t_less_than ) or
                 self.is_token_type( tokens.t_less_than_or_equal_to ) or self.is_token_type( tokens.t_not_equal_to ) ):
            return False
        self.current_token = next( self.token_list )
        
        # Check for an identifier or number or true or false
        if self.is_token_type( tokens.t_string ):
            if not self.scoper.is_variable_in_scope( self.current_token.text ):
                return False
        elif not self.is_token_type( tokens.t_number ):
            return False
        self.current_token = next( self.token_list )

        if not self.is_token_type( tokens.t_rparen ):
            return False
        self.current_token = next( self.token_list )

        if not self.is_token_type( tokens.t_then ):
            return False
        self.current_token = next( self.token_list )
        return True


    def if_body( self ):
        # Statements
        self.valid_code()
        return True

    def if_end( self ):
        if not self.is_token_type( tokens.t_end ):
            return False
        self.current_token = next( self.token_list )

        if not self.is_token_type( tokens.t_if ):
            return False
        self.current_token = next( self.token_list )

        if not self.is_token_type( tokens.t_semicolon ):
            return False
        
        return True


    def expression( self ):
        pass