# Stephen Comarata
# EECE 5183 - 001 Compiler Theory 
# This program is the parser class for the compiler project 
#
# myparser.py

# Imported libraries
import re

# Imported file classes
import tokens
from scoper import Scoper

class Parser:


    def __init__( self, _token_list, logger ):
        self.token_list = _token_list
        self.current_token = None
        self.scoper = Scoper( 'GLOBAL' )
        self.logger = logger
        self.logger.set_origin( 'Parser' )


    def is_token_type( self, test_token ):
        if self.current_token.name == test_token.name:
            return True
        return False


    def next_token( self ):
        try:
            self.current_token = next( self.token_list )
        except:
            self.logger.report_error( 'Expected more tokens but found end of file' )
            sys.exit( 2 )

    # Start to parse
    def parse( self ):
        self.next_token()
        self.program()


    def program( self ):
        # Check program header
        if not self.program_header():
            return False
        # Check program body
        if not self.program_body():
            return False
        
        self.next_token()
        
        # Check for period
        if not self.is_token_type( tokens.t_period ):
            return False
        print( 'Correct Program' )
        return True


    def program_header( self ):
        if not self.is_token_type( tokens.t_program ):
            return False
        self.next_token()

        if not self.identifier():
            return False
        self.next_token()

        if not self.is_token_type( tokens.t_is ):
            return False
        self.next_token()

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
        if not self.is_token_type( tokens.t_number ):
            return False
        number_val = self.current_token.text
        if type( number_val ) is int and number_val >= 0:
            return True
        return False


    def program_body( self ):
        # Check for declarations
        if not self.declaration():
            return False

        # Check for begin
        if not self.is_token_type( tokens.t_begin ):
            return False
        self.next_token()

        self.scoper.go_to_base_scope()

        # Check for valid statements
        if not self.valid_code():
            return False

        # Check for end
        if not self.is_token_type( tokens.t_end ):
            return False
        self.next_token()

        # Check for program 
        if not self.is_token_type( tokens.t_program ):
            return False
        
        print( 'Correct program body' )
        return True 


    # There can be 0 to many declarations
    def declaration( self ):
        while( not self.is_token_type( tokens.t_begin ) ):
            global_flag = False
            # Check for global 
            if self.is_token_type( tokens.t_global ):
                global_flag = True
                self.next_token()
            # Check for procedure
            if self.is_token_type( tokens.t_procedure ):
                if not self.procedure_declaration( global_flag ):
                    # raise Exception( 'Parsing Error: Invalid Procedure Declaration' )
                    # # Try to resync
                    return False
                if not self.is_token_type( tokens.t_semicolon ):
                    return False
                self.scoper.go_to_base_scope()
                self.next_token()

            # Check for variables
            elif self.is_token_type( tokens.t_variable ):
                if not self.variable_declaration( global_flag, False ):
                    # raise Exception( 'Parsing Error: Invalid Variable Declaration' )
                    # # Try to resync
                    return False
                if not self.is_token_type( tokens.t_semicolon ):
                    return False
                self.next_token()
            else:
                return False
        return True


    def procedure_declaration( self, global_flag ):
        # Check procedure header
        if not self.procedure_header( global_flag ):
            return False
        # Check procedure body
        self.next_token()
        if not self.procedure_body():
            return False
        return True


    def procedure_header( self, global_flag ):
        if not self.is_token_type( tokens.t_procedure ):
            return False

        self.next_token()
        if not self.identifier():
            return False
        procedure_name = self.current_token.text

        # Scope Checking
        if self.scoper.is_procedure_in_current_scope( procedure_name, global_flag ):
            self.logger.report_error( '{} already exists in scope'.format( procedure_name ), self.current_token.line_number )
            return False

        self.scoper.create_new_scope( procedure_name )
        self.scoper.add_procedure( procedure_name, global_flag )

        self.next_token()

        if not self.is_token_type( tokens.t_colon ):
            return False
        
        self.next_token()
        if not self.type_mark():
            return False
        procedure_type = self.current_token.text
        self.scoper.add_procedure_type( procedure_name, procedure_type, global_flag ) 

        self.scoper.go_to_next_scope()

        self.next_token()

        if not self.is_token_type( tokens.t_lparen ):
            return False

        self.next_token()

        if not self.parameter_list( procedure_name, global_flag ):
            return False

        if not self.is_token_type( tokens.t_rparen ):
            return False

        

        print( 'Correct procedure header' )
        return True


    def procedure_body( self ):
        # Check for declarations
        if not self.declaration():
            return False
        # Check for begin
        if not self.is_token_type( tokens.t_begin ):
            return False
        self.next_token()
        # Check for valid code
        if not self.valid_code():
            return False
        if not self.is_token_type( tokens.t_end ):
            return False
        self.next_token()

        if not self.is_token_type( tokens.t_procedure ):
            return False
        self.next_token()
        
        print( 'Correct procedure body' )
        return True        


    def parameter_list( self, procedure_name, global_flag ):
        if not self.is_token_type( tokens.t_rparen ):
            while( True ):
                self.parameter()
                if not self.is_token_type( tokens.t_comma ):
                    break
                self.next_token()
        return True


    def parameter( self ):
        if not self.variable_declaration( False, True ):
            return False


    def variable_declaration( self, global_flag, input_param_flag ):
        if not self.is_token_type( tokens.t_variable ):
            return False
        self.next_token()
        if not self.identifier():
            return False
        var_name = self.current_token.text
        if self.scoper.is_variable_in_current_scope( var_name, global_flag ):
            self.logger.report_error( '{} already exists in scope'.format( var_name ), self.current_token.line_number )
            return False
        
        self.scoper.add_variable( var_name, global_flag )
        if input_param_flag:
            self.scoper.add_procedure_input_param( var_name )
        self.next_token()

        if not self.is_token_type( tokens.t_colon ):
            return False
        self.next_token()
        if not self.type_mark():
            return False
        var_type = self.current_token.name
        self.scoper.add_variable_type( var_name, var_type, global_flag )
        if input_param_flag:
            self.scoper.add_procedure_input_param_type( var_name, var_type )

        self.next_token()
        if self.is_token_type( tokens.t_lbracket ):
            self.next_token()
            if not self.bound():
                return False
            array_length = self.current_token.text
            self.scoper.add_variable_array_type( var_name, array_length, global_flag )
            if input_param_flag:
                self.scoper.add_procedure_input_param_array_type( var_name, array_length )
            self.next_token()
            if not self.is_token_type( tokens.t_rbracket ):
                return False
            self.next_token()
        return True
    

    '''
    Zero or more statements needed
    Check for valid code declarations
    caller is of type token
    '''
    def valid_code( self ):
        while self.statement():
            if not self.is_token_type( tokens.t_semicolon ):
                return False
            self.next_token()
        return True


    def statement( self ):
        if ( not self.assignment_statement() and not self.if_statement() and not self.loop_statment() and not self.return_statement() ):
            return False
        return True


    def assignment_statement( self ):
        if not self.destination():
            return False
        if not self.is_token_type( tokens.t_assignment ):
            return False
        self.next_token()
        if not self.expression():
            return False
        return True


    def if_statement( self ):
        if not self.is_token_type( tokens.t_if ):
            return False
        self.next_token()
        if not self.is_token_type( tokens.t_lparen ):
            return False
        self.next_token()
        if not self.expression():
            return False
        if not self.is_token_type( tokens.t_rparen ):
            return False
        self.next_token()
        if not self.is_token_type( tokens.t_then ):
            return False
        self.next_token()
        if not self.valid_code():
            return False

        if self.is_token_type( tokens.t_else ):
            self.next_token()
            if not self.valid_code():
                return False
            self.next_token()

        if not self.is_token_type( tokens.t_end ):
            return False
        
        self.next_token()

        if not self.is_token_type( tokens.t_if ):
            return False

        self.next_token()

        return True
    

    def loop_statment( self ):
        if not self.is_token_type( tokens.t_for ):
            return False
        self.next_token()
        if not self.is_token_type( tokens.t_lparen ):
            return False
        self.next_token()
        if not self.assignment_statement():
            return False
        if not self.is_token_type( tokens.t_semicolon ):
            return False
        self.next_token()
        if not self.expression():
            return False
        if not self.is_token_type( tokens.t_rparen ):
            return False
        self.next_token()
        if not self.valid_code():
            return False
        self.next_token()

        if not self.is_token_type( tokens.t_end ):
            return False

        self.next_token()
    
        if not self.is_token_type( tokens.t_for ):
            return False
        
        self.next_token()

        return True

    
    def return_statement( self ):
        if not self.is_token_type( tokens.t_return ):
            return False
        self.next_token()
        if not self.expression():
            return False
        return True


    def destination( self ):
        if not self.is_token_type( tokens.t_identifier ):
            return False
        self.next_token()
        
        if self.is_token_type( tokens.t_lbracket ):
            self.next_token()
            if not self.expression():
                return False
            self.next_token()

            if not self.is_token_type( tokens.t_rbracket ):
                return False     
        return True


    def expression( self ):
        if self.is_token_type( tokens.t_not ):
           self.next_token()
           if not self.arithOp():
               return False
        elif not self.arithOp():
            return False

        if not self.expression_prime():
            return False
        return True
    

    def expression_prime( self ):
        if self.is_token_type( tokens.t_and ) or self.is_token_type( tokens.t_or ):
            self.next_token()
            if not self.arithOp():
                return False
            self.next_token()
            if not expression_prime():
                return False
        return True


    def arithOp( self ):
        if not self.relation():
            return False

        if not self.arithOp_prime():
            return False
        
        return True
    

    def arithOp_prime( self ):
        if self.is_token_type( tokens.t_add ) or self.is_token_type( tokens.t_subtract ):
            self.next_token()
            if not self.relation():
                return False

            if not self.arithOp_prime():
                return False
        return True


    def relation( self ):
        if not self.term():
            return False

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

            self.next_token()
            if not self.term():
                return False
            if not self.relation_prime():
                return False
        return True
    

    def term( self ):
        if not self.factor():
            return False

        if not self.term_prime():
            return False
        return True


    def term_prime( self ):
        if self.is_token_type( tokens.t_multiply ) or self.is_token_type( tokens.t_divide ):
            self.next_token()
            if not self.factor():
                return False
            self.next_token()
            if not self.term_prime():
                return False
        return True
    

    def factor( self ):
        if self.is_token_type( tokens.t_lparen ):
            self.next_token()
            if not self.expression():
                return False
            if not self.is_token_type( tokens.t_rparen ):
                return False
        elif self.is_token_type( tokens.t_subtract ):
            self.next_token()
            if not self.number() and not self.string():
                return False
        elif self.procedure_call_or_name():
            pass
        elif self.number():
            self.next_token()
        elif self.string():
            self.next_token()
        elif self.is_token_type( tokens.t_true ) or self.is_token_type( tokens.t_false ):
            self.next_token()
        else:
            return False
        return True


    def procedure_call_or_name( self ):
        if not self.identifier():
            return False

        identifier_name = self.current_token.text
        # Scope Checking
        proc = self.scoper.is_procedure_in_scope( identifier_name )
        var = self.scoper.is_variable_in_scope( identifier_name )
        if not self.scoper.is_procedure_in_scope( identifier_name ) and not self.scoper.is_variable_in_scope( identifier_name ):
            self.logger.report_error( '{} does not exist in scope'.format( identifier_name ), self.current_token.line_number )
            return False
        self.next_token()
        if self.is_token_type( tokens.t_lparen ):
            self.next_token()
            if not self.procedure_call():
                return False
            if not self.is_token_type( tokens.t_rparen ):
                return False
            self.next_token()
        elif not self.name():
            return False
        return True


    def procedure_call( self ):
        if self.argument_list():
            pass
        return True

    #TODO come back to me
    def argument_list( self ):
        if not self.expression():
            return False
        while( self.is_token_type( tokens.t_comma ) ):
            if not self.expression():
                return False


    def name( self ):
        if self.is_token_type( tokens.t_lbracket ):
            self.next_token()
            if not self.expression():
                return False
            if not self.is_token_type( tokens.t_rbracket ):
                return False
            self.next_token()
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