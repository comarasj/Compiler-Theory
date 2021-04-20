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
from symbol import Symbol

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
            self.logger.report_error( 'Invalid bound, must be number', self.current_token.line_number )
            return False
        number_val = self.current_token.text
        if type( number_val ) is int and number_val >= 0:
            return True
        self.logger.report_error( 'Invalid bound, must be positive integer', self.current_token.line_number )
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
        dest = Symbol()

        if not self.destination( dest ):
            return False
        if not self.is_token_type( tokens.t_assignment ):
            return False
        self.next_token()

        expr = Symbol()
        if not self.expression( expr ):
            return False
        
        # Type check for compatibility
        if not self.type_check_compatibility( dest, expr ):
            self.logger.report_error( 'Invalid assignment, types do not match', self.current_token.line_number )
            return False

        return True


    def if_statement( self ):
        if not self.is_token_type( tokens.t_if ):
            return False
        self.next_token()
        if not self.is_token_type( tokens.t_lparen ):
            return False
        self.next_token()

        expr = Symbol()
        if not self.expression( expr ):
            return False
        
        # Type check expression resolves to bool

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

        expr = Symbol()
        if not self.expression( expr ):
            return False
        
        # Type check expression resolves to bool

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
        
        expr = Symbol()
        if not self.expression( expr ):
            return False
        
        # Type check that return is the same as procedure return

        return True


    def destination( self, dest ):
        if not self.is_token_type( tokens.t_identifier ):
            return False
        self.scoper.get_var_type( self.current_token.text, dest )
        self.next_token()
        
        if self.is_token_type( tokens.t_lbracket ):
            self.next_token()
            idx = Symbol()
            if not self.expression( idx ):
                return False
            # self.next_token()

            if not self.is_token_type( tokens.t_rbracket ):
                return False
            self.next_token()     
        return True


    def expression( self, expr ):
        if self.is_token_type( tokens.t_not ):
           self.next_token()
           if not self.arithOp( expr ):
               return False
        elif not self.arithOp( expr ):
            return False

        if not self.expression_prime( expr ):
            return False
        return True
    

    def expression_prime( self, expr ):
        if self.is_token_type( tokens.t_and ) or self.is_token_type( tokens.t_or ):
            self.next_token()

            rhs = Symbol()
            if not self.arithOp( rhs ):
                return False
            
            if not self.type_check_expression( expr, rhs, '' ):
                return False

            self.next_token()
            if not expression_prime( expr ):
                return False
        return True


    def arithOp( self, arOp ):
        if not self.relation( arOp ):
            return False

        if not self.arithOp_prime( arOp ):
            return False
        
        return True
    

    def arithOp_prime( self, arOp ):
        if self.is_token_type( tokens.t_add ) or self.is_token_type( tokens.t_subtract ):
            self.next_token()

            rhs = Symbol()
            if not self.relation( rhs ):
                return False

            if not self.type_check_arithmetic( arOp, rhs, '' ):
                return False

            if not self.arithOp_prime( arOp ):
                return False
        return True


    def relation( self, rel ):
        if not self.term( rel ):
            return False

        if not self.relation_prime( rel ):
            return False
        return True
    

    def relation_prime( self, rel ):
        if ( self.is_token_type( tokens.t_equal_to ) or
             self.is_token_type( tokens.t_not_equal_to ) or
             self.is_token_type( tokens.t_greater_than ) or
             self.is_token_type( tokens.t_greater_than_or_equal_to ) or
             self.is_token_type( tokens.t_less_than ) or
             self.is_token_type( tokens.t_less_than_or_equal_to ) ):

            self.next_token()
            if not self.term( rel ):
                return False
            if not self.relation_prime( rel ):
                return False
        return True
    

    def term( self, term ):
        if not self.factor( term ):
            return False

        if not self.term_prime( term ):
            return False
        return True


    def term_prime( self, term ):
        if self.is_token_type( tokens.t_multiply ) or self.is_token_type( tokens.t_divide ):
            self.next_token()

            rhs = Symbol()
            if not self.factor( rhs ):
                return False
            
            if not self.type_check_arithmetic( term, rhs, '' ):
                return False

            self.next_token()
            if not self.term_prime( term ):
                return False
        return True
    

    def factor( self, factor ):
        if self.is_token_type( tokens.t_lparen ):
            self.next_token()
            if not self.expression( factor ):
                return False
            if not self.is_token_type( tokens.t_rparen ):
                return False
        elif self.is_token_type( tokens.t_subtract ):
            self.next_token()
            if not self.number() and not self.string():
                return False
        elif self.procedure_call_or_name( factor ):
            pass
        elif self.number( factor ):
            self.next_token()
        elif self.string( factor ):
            self.next_token()
        elif self.is_token_type( tokens.t_true ) or self.is_token_type( tokens.t_false ):
            factor.type = 'BOOL'
            self.next_token()
        else:
            return False
        return True


    def procedure_call_or_name( self, iden ):
        if not self.identifier():
            return False

        identifier_name = self.current_token.text
        # Scope Checking
        proc = self.scoper.is_procedure_in_scope( identifier_name )
        var = self.scoper.is_variable_in_scope( identifier_name )
        if not self.scoper.is_procedure_in_scope( identifier_name ) and not self.scoper.is_variable_in_scope( identifier_name ):
            self.logger.report_error( '{} does not exist in scope'.format( identifier_name ), self.current_token.line_number )
            return False
        identifier_type = ''
        if proc:
            identifier_type = self.scoper.get_proc_type( identifier_name, iden )
        else:
            identifier_type = self.scoper.get_var_type( identifier_name, iden )

        
        self.next_token()
        if self.is_token_type( tokens.t_lparen ):
            self.next_token()
            if not self.procedure_call():
                return False
            if not self.is_token_type( tokens.t_rparen ):
                return False
            self.next_token()
        elif not self.name( iden ):
            return False
        return True


    def procedure_call( self ):
        if self.argument_list():
            pass
        return True

    #TODO come back to me
    def argument_list( self ):

        arg = Symbol()

        if not self.expression( arg ):
            return False
        while( self.is_token_type( tokens.t_comma ) ):
            arg_p = Symbol()
            if not self.expression( arg_p ):
                return False


    def name( self, iden ):
        if self.is_token_type( tokens.t_lbracket ):
            self.next_token()
            idx = Symbol()
            if not self.expression( idx ):
                return False
            if not self.is_token_type( tokens.t_rbracket ):
                return False
            self.next_token()
            iden.is_indexed_array = True
        return True


    def number( self, num ):
        if not self.is_token_type( tokens.t_number ):
            return False
        if type( self.current_token.text ) is float:
            num.type = 'FLOAT'
        elif type( self.current_token.text ) is int:
            num.type = 'INT'
        return True
    

    def string( self, string ):
        #TODO come back to me
        if not self.is_token_type( tokens.t_identifier ):
            return False
        string.type = 'STRING'
        return True
    

    def type_check_expression( self, lhs, rhs, operator ):
        return True


    def type_check_arithmetic( self, lhs, rhs, operator ):
        if ( lhs.type != 'INT' and lhs.type != 'FLOAT' ) or ( rhs.type != 'INT' and rhs.type != 'FLOAT' ):
            # They are not corrent type
            return False
        if ( lhs.is_array and not lhs.is_indexed_array ) or ( lhs.is_array and not lhs.is_indexed_array ):
            #array stuff
            pass
        elif lhs.type == 'INT' and rhs.type == 'FLOAT':
            # valid
            # Code gen stuff
            pass
        elif lhs.type == 'FLOAT' and rhs.type == 'INT':
            # valid
            # Code gen stuff
            pass
        # Both are the same type
        return True
    

    def type_check_compatibility( self, dest, expr ):
        # 727
        if dest.is_array or expr.is_array:
            if dest.is_array and expr.is_array:
                if dest.is_indexed_array != expr.is_indexed_array:
                    self.logger.report_error( 'Arrays must be indexed or unindexed', self.current_token.line_number )
                    return False
                elif not dest.is_indexed_array:
                    if dest.array_length != expr.array_length:
                        self.logger.report_error( 'Arrays must be same length', self.current_token.line_number )
                        return False
                else:
                    if dest.type != expr.type:
                        return False
            else:
                if ( dest.is_array and not dest.is_indexed_array ) or ( expr.is_array and not expr.is_indexed_array ):
                    self.logger.report_error( 'Array must be indexed', self.current_token.line_number )
                    return False
            return True



        if dest.type == expr.type:
            return True

        elif dest.type == 'INT':
            if expr.type == 'FLOAT':
                return True
            elif expr.type == 'BOOL':
                return True

        elif dest.type == 'FLOAT':
            if expr.type == 'INT':
                return True

        elif dest.type == 'BOOL':
            if expr.type == 'INT':
                return True

        return False
    
