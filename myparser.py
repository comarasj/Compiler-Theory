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
        
        self.current_token = next( self.token_list )
        if not self.is_token_type( tokens.t_period ):
            return False
        print( 'Correct Program' )
        return True


    def program_header( self ):
        if not self.is_token_type( tokens.t_program ):
            return False
        self.current_token = next( self.token_list )

        if not self.identifier():
            return False
        self.current_token = next( self.token_list )

        if not self.is_token_type( tokens.t_is ):
            return False
        self.current_token = next( self.token_list )

        print( 'Correct program header' )
        return True

    
    def identifier( self ):
        if not self.is_token_type( tokens.t_identifier ):
            return False
        return True
    

    def type_mark( self ):
        if ( not self.is_token_type( tokens.t_integer ) and 
               not self.is_token_type( tokens.t_float ) and 
               not self.is_token_type( tokens.t_string ) and 
               not self.is_token_type( tokens.t_bool ) ):
            return False
        return True
    

    def bound( self ):
        if not self.is_token_type( number ):
            return False
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
        
        print( 'Correct program body' )
        return True 


    # There can be 0 to many declarations
    def declaration( self ):
        while( not self.is_token_type( tokens.t_begin ) ):
            # Check for global 

            # Check for procedure
            if self.is_token_type( tokens.t_procedure ):
                if not self.procedure_declaration():
                    raise Exception( 'Parsing Error: Invalid Procedure Declaration' )
                    return False
                if not self.is_token_type( tokens.t_semicolon ):
                    return False
                self.current_token = next( self.token_list )

            # Check for variables
            elif self.is_token_type( tokens.t_variable ):
                if not self.variable_declaration():
                    raise Exception( 'Parsing Error: Invalid Variable Declaration' )
                    return False
                if not self.is_token_type( tokens.t_semicolon ):
                    return False
                self.current_token = next( self.token_list )
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
        if not self.is_token_type( tokens.t_procedure ):
            return False

        self.current_token = next( self.token_list )
        if not self.identifier():
            return False
        if not self.scoper.create_new_scope( self.current_token.text ):
            return False

        procedure_name = self.current_token.text
        self.scoper.add_procedure( procedure_name )

        self.current_token = next( self.token_list )

        if not self.is_token_type( tokens.t_colon ):
            return False
        
        self.current_token = next( self.token_list )
        if not self.type_mark():
            return False
        procedure_type = self.current_token.text
        self.scoper.add_procedure_type( procedure_name, procedure_type ) 

        self.current_token = next( self.token_list )

        if not self.is_token_type( tokens.t_lparen ):
            return False

        self.current_token = next( self.token_list )

        if not self.parameter_list( procedure_name ):
            return False

        if not self.is_token_type( tokens.t_rparen ):
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
        if not self.valid_code():
            return False        
        
        if not self.is_token_type( tokens.t_end ):
            return False
        self.current_token = next( self.token_list )

        if not self.is_token_type( tokens.t_procedure ):
            return False
        self.current_token = next( self.token_list )
        
        print( 'Correct procedure body' )
        return True        


    def parameter_list( self, procedure_name ):
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
        if not self.is_token_type( tokens.t_variable ):
            return False
        self.current_token = next( self.token_list )
        if not self.identifier():
            return False
        var_name = self.current_token.text
        self.scoper.add_variable( var_name )
        self.current_token = next( self.token_list )

        if not self.is_token_type( tokens.t_colon ):
            return False
        self.current_token = next( self.token_list )
        if not self.type_mark():
            return False
        var_type = self.current_token.name
        self.scoper.add_variable_type( var_name, var_type )
        self.current_token = next( self.token_list )
        if self.is_token_type( tokens.t_lbracket ):
            if not self.bound():
                return False
            if not self.is_token_type( tokens.t_lbracket ):
                return False
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
    Zero or more statements needed
    Check for valid code declarations
    caller is of type token
    '''
    def valid_code( self ):
        while self.statement():
            if self.is_token_type( tokens.t_semicolon ):
                return False
        return True


    def statement( self ):
        if ( not self.assignment_statement() and 
           not self.if_statement() and 
           not self.loop_statment() and
           not self.return_statement() ):
            return False
        return True


    def assignment_statement( self ):
        if not self.destination():
            return False
        self.current_token = next( self.token_list )
        if not self.is_token_type( tokens.t_assignment ):
            return False
        self.current_token = next( self.token_list )
        if not self.expression():
            return False
        return True


    def if_statement( self ):
        return True
    

    def loop_statment( self ):
        return True

    
    def return_statement( self ):
        return True


    def destination( self ):
        if not self.is_token_type( tokens.t_identifier ):
            return False
        self.current_token = next( self.token_list )
        
        if self.is_token_type( tokens.t_lbracket ):
            self.current_token = next( self.token_list )
            if not self.expression():
                return False
            self.current_token = next( self.token_list )

            if not self.is_token_type( tokens.t_rbracket ):
                return False     
        return True


    def expression( self ):
        if self.is_token_type( tokens.t_not ):
           self.current_token = next( self.token_list )
           if not self.arithOp():
               return False
        elif not self.arithOp():
            return False
        self.current_token = next( self.token_list )
        if not self.expression_prime():
            return False
        return True
    

    def expression_prime( self ):
        if self.is_token_type( tokens.t_and ) or self.is_token_type( tokens_or ):
            self.current_token = next( self.token_list )
            if not self.arithOp():
                return False
            self.current_token = next( self.token_list )
            if not expression_prime():
                return False
        return True


    def arithOp( self ):
        if not self.relation():
            return False
        self.current_token = next( self.token_list )
        if not self.arithOp_prime():
            return False
        
        return True
    

    def arithOp_prime( self ):
        if self.is_token_type( tokens.t_add ) or self.is_token_type( tokens.t_subtract ):
            self.current_token = next( self.token_list )
            if not self.relation():
                return False
            self.current_token = next( self.token_list )
            if not self.arithOp_prime():
                return False
        return True


    def relation( self ):
        if not self.term():
            return False
        self.current_token = next( self.token_list )
        if not self.relation_prime():
            return False
        return True
    

    def relation_prime( self ):
        if ( self.is_token_type( tokens.t_equal_to ) or
             self.is_token_type( tokens.t_not_equal_to ) or
             self.is_token_type( tokens.t_greater_than ) or
             self.is_token_type( tokens.t_greater_than_or_equal_to ) or
             self.is_token_type( tokens.t_less_than ) or
             self.is_token_type( tokens.t_less_than_or_equal_to ) ):

            self.current_token = next( self.token_list )
            if not self.term():
                return False
            self.current_token = next( self.token_list )
            if not self.relation_prime():
                return False
        return True
    

    def term( self ):
        if not self.factor():
            return False
        self.current_token = next( self.token_list )
        if not self.term_prime():
            return False
        return True


    def term_prime( self ):
        if self.is_token_type( tokens.t_multiply ) or self.is_token_type( tokens.t_divide ):
            self.current_token = next( self.token_list )
            if not self.factor():
                return False
            self.current_token = next( self.token_list )
            if not self.term_prime():
                return False
        return True
    

    def factor( self ):
        if self.is_token_type( tokens.t_lparen ):
            self.current_token = next( self.token_list )
            if not self.expression():
                return False
            if not self.is_token_type( tokens.t_rparen ):
                return False
        elif self.is_token_type( tokens.t_subtract ):
            self.current_token = next( self.token_list )
            if not self.number() and not self.string():
                return False
        elif ( not self.procedure_call() and
               not self.name() and
               not self.number() and
               not self.string() and
               not self.is_token_type( tokens.t_true ) and
               not self.is_token_type( token.t_false ) ):
            return False
        else:
            return False
        return True
    

    def procedure_call( self ):
        return True


    def argument_list( self ):
        return True


    def argument_list_prime( self ):
        return True


    def name( self ):
        if not self.identifier():
            return False
        self.current_token - next( self.token_list )
        if self.is_token_type( tokens.t_lbracket ):
            if not self.expression():
                return False
            if not self.is_token_type( tokens.t_rbracket ):
                return False
        return True


    def number( self ):
        if not self.is_token_type( tokens.t_number ):
            return False
        return True
    

    def string( self ):
        #TODO come back to me
        if not self.is_token_type( tokens.t_identifier ):
            return False
        return True