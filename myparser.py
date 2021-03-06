# Stephen Comarata
# EECE 5183 - 001 Compiler Theory 
# This program is the parser class for the compiler project 
#
# myparser.py - named myparser because python doesnt like parser keyword

# Imported libraries
import re, sys

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
        self.line_number = 0
        self.resync_flag = False


    def is_token_type( self, test_token ):
        if self.current_token.name == test_token.name:
            return True
        return False


    def next_token( self ):
        try:
            self.current_token = next( self.token_list )
            self.line_number = self.current_token.line_number
        except:
            self.logger.report_error( 'Expected more tokens but found end of file', self.line_number )
            sys.exit( 2 )

    # Start to parse
    def parse( self ):
        self.next_token()
        if self.program():
            if self.resync_flag:
                print( 'Parse completed with errors.. Please address issues' )
            else:
                print( 'Successful Parse!' )
        else:
            print( 'Unsuccessful Parse.. Please address issues' )


    def resync( self, resync_type ):
        self.resync_flag = True
        if resync_type == 'procedure':
            self.logger.report_warning( 'Attempting to resync to end of procedure', self.line_number )
            while( not self.is_token_type( tokens.t_procedure ) ):
                self.next_token()
            if not self.is_token_type( tokens.t_procedure ):
                self.logger.report_error( 'Could not resync to end of invalid procedure' )
                return False
            self.logger.report_warning( 'Resync successful', self.line_number )
            return True
        elif resync_type == 'variable':
            self.logger.report_warning( 'Attempting to resync to next line', self.line_number )
            while( not self.is_token_type( tokens.t_semicolon ) ):
                self.next_token()
            self.logger.report_warning( 'Resync successful', self.line_number )
            return True

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
            self.logger.report_warning( 'Period not included at end of program', self.line_number )
            # return False
        self.logger.info( 'Correct Program', self.line_number )
        return True


    def program_header( self ):
        if not self.is_token_type( tokens.t_program ):
            self.logger.report_error( 'Missing "program" keyword', self.line_number )
            return False
        self.next_token()

        if not self.identifier():
            self.logger.report_error( 'Missing program identifier', self.line_number )
            return False
        self.next_token()

        if not self.is_token_type( tokens.t_is ):
            self.logger.report_error( 'Missing "is" keyword', self.line_number )
            return False
        self.next_token()

        self.logger.info( 'Correct program header', self.line_number )
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
            self.logger.report_error( 'Missing valid type mark', self.line_number )
            return False
        return True
    

    def bound( self ):
        if not self.is_token_type( tokens.t_number ):
            self.logger.report_error( 'Invalid bound, must be number', self.line_number )
            return False
        number_val = self.current_token.text
        if type( number_val ) is int and number_val >= 0:
            return True
        self.logger.report_error( 'Invalid bound, must be positive integer', self.line_number )
        return False


    def program_body( self ):
        # Check for declarations
        if not self.declaration():
            return False

        # Check for begin
        if not self.is_token_type( tokens.t_begin ):
            self.logger.report_error( 'Missing "begin" keyword', self.line_number )
            return False
        self.next_token()

        self.scoper.go_to_base_scope()

        # Check for valid statements
        if not self.valid_code():
            return False

        # Check for end
        if not self.is_token_type( tokens.t_end ):
            self.logger.report_error( 'Missing "end" keyword', self.line_number )
            return False
        self.next_token()

        # Check for program 
        if not self.is_token_type( tokens.t_program ):
            self.logger.report_error( 'Missing "program" keyword', self.line_number )
            return False
        
        self.logger.info( 'Correct program body', self.line_number )
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
                    # # Try to resync
                    self.logger.report_error( 'Invalid Procedure Declaration', self.line_number )

                    if not self.resync( 'procedure' ):
                        return False
                    self.next_token()
                if not self.is_token_type( tokens.t_semicolon ):
                    self.logger.report_error( 'Missing ";"', self.line_number )
                    return False
                self.scoper.go_to_parent_scope()
                self.next_token()

            # Check for variables
            elif self.is_token_type( tokens.t_variable ):
                if not self.variable_declaration( global_flag, False ):
                    # # Try to resync
                    self.logger.report_error( 'Invalid Variable Declaration', self.line_number )
                    if not self.resync( 'variable' ):
                        return False
                if not self.is_token_type( tokens.t_semicolon ):
                    self.logger.report_error( 'Missing ";"', self.line_number )
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
            self.logger.report_error( 'Missing "procedure" keyword', self.line_number )
            return False

        self.next_token()
        if not self.identifier():
            self.logger.report_error( 'Missing procedure identifier', self.line_number )
            return False
        procedure_name = self.current_token.text

        # Scope Checking
        if self.scoper.is_procedure_in_current_scope( procedure_name, global_flag ):
            self.logger.report_error( '{} already exists in scope'.format( procedure_name ), self.line_number )
            return False

        self.scoper.create_new_scope( procedure_name )        

        self.next_token()

        if not self.is_token_type( tokens.t_colon ):
            self.logger.report_error( 'Missing ":"', self.line_number )
            return False
        
        self.next_token()
        if not self.type_mark():
            return False
        procedure_type = self.current_token.text
        self.scoper.add_procedure( procedure_name, procedure_type, global_flag )
        
        self.scoper.go_to_next_scope()

        self.next_token()

        if not self.is_token_type( tokens.t_lparen ):
            self.logger.report_error( 'Missing "("', self.line_number )
            return False

        self.next_token()

        if not self.parameter_list( procedure_name, global_flag ):
            return False

        if not self.is_token_type( tokens.t_rparen ):
            self.logger.report_error( 'Missing ")"', self.line_number )
            return False

        self.logger.info( 'Correct procedure header', self.line_number )
        return True


    def procedure_body( self ):
        # Check for declarations
        if not self.declaration():
            return False
        # Check for begin
        if not self.is_token_type( tokens.t_begin ):
            self.logger.report_error( 'Missing "begin" keyword', self.line_number )
            return False
        self.next_token()
        # Check for valid code
        if not self.valid_code():
            return False
        if not self.is_token_type( tokens.t_end ):
            self.logger.report_error( 'Missing "end" keyword', self.line_number )
            return False
        self.next_token()

        if not self.is_token_type( tokens.t_procedure ):
            self.logger.report_error( 'Missing "procedure" keyword', self.line_number )
            return False
        self.next_token()
        
        self.logger.info( 'Correct procedure body', self.line_number )
        return True        


    def parameter_list( self, procedure_name, global_flag ):
        if not self.is_token_type( tokens.t_rparen ):
            param_idx = 0
            while( True ):
                self.parameter( procedure_name, param_idx )
                if not self.is_token_type( tokens.t_comma ):
                    break
                self.next_token()
        return True


    def parameter( self, procedure_name, param_idx ):
        if not self.variable_declaration( False, True, procedure_name, param_idx ):
            return False


    def variable_declaration( self, global_flag, input_param_flag, procedure_name=None, param_idx=None ):
        if not self.is_token_type( tokens.t_variable ):
            self.logger.report_error( 'Missing "variable" keyword', self.line_number )
            return False
        self.next_token()
        if not self.identifier():
            self.logger.report_error( 'Missing variable identifier', self.line_number )
            return False
        var_name = self.current_token.text
        if self.scoper.is_variable_in_current_scope( var_name, global_flag ):
            self.logger.report_error( '{} already exists in scope'.format( var_name ), self.line_number )
            return False

        self.next_token()

        if not self.is_token_type( tokens.t_colon ):
            self.logger.report_error( 'Missing ":"', self.line_number )
            return False
        self.next_token()
        if not self.type_mark():
            return False
        var_type = self.current_token.name
        is_array = False
        array_length = 0
        self.next_token()
        if self.is_token_type( tokens.t_lbracket ):
            is_array = True
            self.next_token()
            if not self.bound():
                return False
            array_length = self.current_token.text
            self.next_token()
            if not self.is_token_type( tokens.t_rbracket ):
                return False
            self.next_token()
        self.scoper.add_variable( var_name, var_type, is_array, array_length, global_flag )
        if input_param_flag:
            self.scoper.add_procedure_input_param( procedure_name, var_name, var_type, param_idx, global_flag )
            if is_array:
                self.scoper.add_procedure_input_param_array_type( procedure_name, var_name, array_length, global_flag )
        return True
    

    '''
    Zero or more statements needed
    Check for valid code declarations
    caller is of type token
    '''
    def valid_code( self ):
        while self.statement():
            if not self.is_token_type( tokens.t_semicolon ):
                self.logger.report_error( 'Missing ";"', self.line_number )
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
            self.logger.report_error( 'Missing ":="', self.line_number )
            return False
        self.next_token()

        expr = Symbol()
        if not self.expression( expr ):
            return False
        
        # Type check for compatibility
        if not self.type_check_compatibility( dest, expr ):
            self.logger.report_error( 'Invalid assignment, types do not match', self.line_number )
            return False

        return True


    def if_statement( self ):
        if not self.is_token_type( tokens.t_if ):
            # self.logger.report_error( 'Missing "if" keyword', self.line_number )
            return False
        self.next_token()
        if not self.is_token_type( tokens.t_lparen ):
            self.logger.report_error( 'Missing "("', self.line_number )
            return False
        self.next_token()

        expr = Symbol()
        if not self.expression( expr ):
            return False
        
        # Type check expression resolves to bool
        # if expr.type != 'INT' and expr.type != 'BOOL':
        #     self.logger.report_error( 'If statement expression did not resolve to a boolean', self.line_number )
        #     return False

        if not self.is_token_type( tokens.t_rparen ):
            self.logger.report_error( 'Missing ")"', self.line_number )
            return False
        self.next_token()
        if not self.is_token_type( tokens.t_then ):
            self.logger.report_error( 'Missing "then" keyword', self.line_number )
            return False
        self.next_token()
        if not self.valid_code():
            return False

        if self.is_token_type( tokens.t_else ):
            self.next_token()
            if not self.valid_code():
                return False

        if not self.is_token_type( tokens.t_end ):
            self.logger.report_error( 'Missing "end" keyword', self.line_number )
            return False
        
        self.next_token()

        if not self.is_token_type( tokens.t_if ):
            self.logger.report_error( 'Missing "if" keyword', self.line_number )
            return False

        self.next_token()

        return True
    

    def loop_statment( self ):
        if not self.is_token_type( tokens.t_for ):
            # self.logger.report_error( 'Missing "for" keyword', self.line_number )
            return False
        self.next_token()
        if not self.is_token_type( tokens.t_lparen ):
            self.logger.report_error( 'Missing "("', self.line_number )
            return False
        self.next_token()
        if not self.assignment_statement():
            return False
        if not self.is_token_type( tokens.t_semicolon ):
            self.logger.report_error( 'Missing ";"', self.line_number )
            return False
        self.next_token()

        expr = Symbol()
        if not self.expression( expr ):
            return False
        
        # Type check expression resolves to bool
        if expr.type != 'INT' and expr.type != 'BOOL':
            self.logger.report_error( 'Loop statement expression did not resolve to a boolean', self.line_number )
            return False


        if not self.is_token_type( tokens.t_rparen ):
            self.logger.report_error( 'Missing ")"', self.line_number )
            return False
        self.next_token()
        if not self.valid_code():
            return False

        if not self.is_token_type( tokens.t_end ):
            self.logger.report_error( 'Missing "end" keyword', self.line_number )
            return False

        self.next_token()
    
        if not self.is_token_type( tokens.t_for ):
            self.logger.report_error( 'Missing "for" keyword', self.line_number )
            return False
        
        self.next_token()

        return True

    
    def return_statement( self ):
        if not self.is_token_type( tokens.t_return ):
            # self.logger.report_error( 'Missing "return" keyword', self.line_number )
            return False
        self.next_token()
        
        expr = Symbol()
        if not self.expression( expr ):
            return False

        proc = Symbol()
        proc_name = self.scoper.current_scope.scope_name
        self.scoper.get_procedure_type( proc_name, proc )

        # Type check that return is the same as procedure return
        if not self.type_check_compatibility( proc, expr ):
            self.logger.report_error( 'Return type does not match procedure type', self.line_number )
            return False

        return True


    def destination( self, dest ):
        if not self.is_token_type( tokens.t_identifier ):
            return False
        self.scoper.get_variable_type( self.current_token.text, dest )
        dest.id = self.current_token.text
        self.next_token()
        
        if self.is_token_type( tokens.t_lbracket ):
            self.next_token()
            idx = Symbol()
            if not self.expression( idx ):
                return False
            
            if not dest.is_array:
                self.logger.report_error( 'Variable is not an array and cannot be indexed', self.line_number )
                return False

            if idx.type != 'INT':
                self.logger.report_error( 'Array must be indexed by an integer', self.line_number )
                return False


            if not self.is_token_type( tokens.t_rbracket ):
                return False
            self.next_token()
            dest.is_indexed_array = True
        return True


    def expression( self, expr ):
        if self.is_token_type( tokens.t_not ):
            self.next_token()
            if not self.arithOp( expr ):
                return False
            if expr.type != 'INT' and expr.type != 'BOOL':
                self.logger.report_error( 'Not is only supported for bool and int', self.line_number )
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
            
            # Type check for expressions operators like ( & | )
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
            
            # Type check for aritmetic operators like ( + - )
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

            op = self.current_token.text
            self.next_token()

            rhs = Symbol()
            if not self.term( rhs ):
                return False
            
            # Type check for relation operators like ( > < = )
            if not self.type_check_relation( rel, rhs, op ):
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
            
            # Type check for term operators like ( * / ) - same rules apply here as arithmetics
            if not self.type_check_arithmetic( term, rhs, '' ):
                return False

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
            self.next_token()
        elif self.is_token_type( tokens.t_subtract ):
            self.next_token()
            if not self.number( factor ) and not self.string( factor ):
                return False
            self.next_token()
        elif self.procedure_call_or_name( factor ):
            pass
        elif self.is_token_type( tokens.t_subtract ):
            # Negative number
            self.next_token()
            if name( factor ) or number( factor ):
                if factor.type != 'INT' and factor.type != 'FLOAT':
                    self.logger.report_error( 'Minus/negative operator only supported for numbers', self.line_number )
                    return False
            else:
                self.logger.report_error( 'Invalid minus/negative operator', self.line_number )
                return False
            
            self.next_token()

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
        iden.id = identifier_name
        # Scope Checking
        proc = self.scoper.is_procedure_in_scope( identifier_name )
        var = self.scoper.is_variable_in_scope( identifier_name )
        if not self.scoper.is_procedure_in_scope( identifier_name ) and not self.scoper.is_variable_in_scope( identifier_name ):
            self.logger.report_error( '{} does not exist in scope'.format( identifier_name ), self.line_number )
            return False
        identifier_type = ''
        if proc:
            identifier_type = self.scoper.get_procedure_type( identifier_name, iden ) 
        else:
            identifier_type = self.scoper.get_variable_type( identifier_name, iden )

        self.next_token()
        if self.is_token_type( tokens.t_lparen ):
            self.next_token()
            if not self.procedure_call( iden ):
                return False
            if not self.is_token_type( tokens.t_rparen ):
                return False
            self.next_token()
        elif not self.name( iden ):
            return False
        return True


    def procedure_call( self, proc ):
        if not self.argument_list( proc ):
            return False
        return True


    def argument_list( self, proc ):
        index = 0
        arg = Symbol()
        procedure_args = self.scoper.get_procedure_args( proc.id )
        if len( procedure_args ) == 0 and self.is_token_type( tokens.t_rparen ):
            return True

        if not self.expression( arg ):
            if len( procedure_args ) != 0:
                self.logger.report_error( 'Too few procedure arguments provided', self.line_number )
            return False

        parameter_symbol = self.get_indexed_arg( procedure_args, index )

        if not self.type_check_compatibility( arg, parameter_symbol ):
            self.logger.report_error( 'Provided procedure argument does not match defined procedure parameter type', self.line_number )
            return False

        index = index + 1

        while( self.is_token_type( tokens.t_comma ) ):
            self.next_token()
            arg_p = Symbol()
            if not self.expression( arg_p ):
                self.logger.report_error( 'Invalid argument expression', self.line_number )
                return False
            
            if index >= len( procedure_args ):
                self.logger.report_error( 'Too many arguments provided', self.line_number )
                return False
            
            parameter_symbol = self.get_indexed_arg( procedure_args, index )

            if not self.type_check_compatibility( arg_p, parameter_symbol ):
                self.logger.report_error( 'Provided procedure argument does not match defined procedure parameter type', self.line_number )
                return False

            index = index + 1

        if index != len( procedure_args ):
            self.logger.report_error( 'Too few procedure arguments provided', self.line_number )

        return True

    def name( self, iden ):
        if self.is_token_type( tokens.t_lbracket ):
            self.next_token()
            idx = Symbol()
            if not self.expression( idx ):
                return False

            if not iden.is_array:
                self.logger.report_error( 'Variable is not an array and cannot be indexed', self.line_number )
                return False

            if idx.type != 'INT':
                self.logger.report_error( 'Array must be indexed by an integer', self.line_number )
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
        if not self.is_token_type( tokens.t_quote ):
            return False
        self.next_token()
        if not self.is_token_type( tokens.t_string ):
            return False
        self.next_token()
        if not self.is_token_type( tokens.t_quote ):
            return False
        string.type = 'STRING'
        return True
    

    def type_check_expression( self, lhs, rhs, operator ):
        if lhs.type == 'BOOL' and rhs.type == 'BOOL':
            return True
        elif lhs.type == 'INT' and rhs.type == 'INT':
            return True

        elif ( lhs.is_array and not lhs.is_indexed_array ) and ( rhs.is_array and not rhs.is_indexed_array ):
            if lhs.array_length != rhs.array_length:
                self.logger.report_error( 'When doing operations on arrays, array must be the same size', self.line_number )
                return False
        self.logger.report_error( 'Invalid expression types', self.line_number )
        return False


    def type_check_arithmetic( self, lhs, rhs, operator ):
        if ( lhs.type != 'INT' and lhs.type != 'FLOAT' ) or ( rhs.type != 'INT' and rhs.type != 'FLOAT' ):
            # They are not corret type
            return False
        elif ( lhs.is_array and not lhs.is_indexed_array ) and ( rhs.is_array and not rhs.is_indexed_array ):
            if lhs.array_length != rhs.array_length:
                self.logger.report_error( 'When doing operations on arrays, array must be the same size', self.line_number )
                return False
        elif lhs.type == 'INT' and rhs.type == 'FLOAT':
            # valid
            pass
        elif lhs.type == 'FLOAT' and rhs.type == 'INT':
            # valid
            pass
        # Both are the same type
        return True
    

    def type_check_compatibility( self, dest, expr ):
        if dest.is_array or expr.is_array:
            if dest.is_array and expr.is_array:
                if dest.is_indexed_array != expr.is_indexed_array:
                    self.logger.report_error( 'Arrays must be indexed or unindexed', self.line_number )
                    return False
                elif not dest.is_indexed_array:
                    if dest.array_length != expr.array_length:
                        self.logger.report_error( 'Arrays must be same length', self.line_number )
                        return False
                else:
                    if dest.type != expr.type:
                        return False
            else:
                if ( dest.is_array and not dest.is_indexed_array ) or ( expr.is_array and not expr.is_indexed_array ):
                    self.logger.report_error( 'Array must be indexed', self.line_number )
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


    def type_check_relation( self, lhs, rhs, op ):
        if ( lhs.is_array and not lhs.is_indexed_array ) and ( rhs.is_array and not rhs.is_indexed_array ):
            if lhs.array_length != rhs.array_length:
                self.logger.report_error( 'When doing operations on arrays, array must be the same size', self.line_number )
                return False
        elif lhs.type == 'INT':
            if rhs.type == 'BOOl':
                return True
            elif rhs.type == 'FLOAT':
                return True
            elif rhs.type == 'INT':
                return True
        elif lhs.type == 'FLOAT':
            if rhs.type == 'FLOAT':
                return True
            elif rhs.type == 'INT':
                return True
        elif lhs.type == 'BOOL':
            if rhs.type == 'BOOL':
                return True
            elif rhs.type == 'INT':
                return True
        elif lhs.type == 'STRING':
            if rhs.type == 'STRING' and ( op == '==' or op == '!=' ):
                return True
        self.logger.report_error( 'Types incompatible for relations', self.line_number )
        return False


    def get_indexed_arg( self, procedure_args, index ):
        arg = Symbol()
        for parameter in procedure_args:
            if procedure_args[ parameter ][ 'index' ] == index:
                arg.id = parameter
                arg.type = self.scoper.convert_type( procedure_args[ parameter ][ 'variable_type' ] )
        return arg