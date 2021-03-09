

class Token:
    def __init__( self, name, text ):
        self.name = name
        self.text = text
        self.line_number = 0


keywords = [ 'program', 'is', 'begin', 'end', 'global', 'procedure', 
             'variable', 'integer', 'float', 'string', 'bool', 'if', 
             'then', 'else', 'for', 'return', 'not', 'true', 'false' ]


t_comment_start = Token( 'comment', '/*' )
t_comment_end = Token( 'comment', '/*' )
t_comment = Token( 'comment', '//' )

t_program = Token( 'program', 'program' )
t_is = Token( 'is', 'is' )
t_begin = Token( 'begin', 'begin' )
t_end = Token( 'end', 'end' )
t_global = Token( 'global', 'global' )
t_procedure = Token( 'procedure', 'procedure' )
t_variable = Token( 'variable', 'variable' )
t_integer = Token( 'integer', 'integer' )
t_float = Token( 'float', 'float' )
t_string = Token( 'string', 'string' )
t_bool = Token( 'bool', 'bool' )
t_if = Token( 'if', 'if' )
t_then = Token( 'then', 'then' )
t_else = Token( 'else', 'else' )
t_for = Token( 'for', 'for' )
t_return = Token( 'return', 'return' )
t_not = Token( 'not', 'not' )
t_true = Token( 'true', 'true' )
t_false = Token( 'false', 'false' )

t_assignment = Token( 'assignment', ':=' )
t_greater_than_or_equal_to = Token( 'greater than or equal to', '>=' )
t_less_than_or_equal_to = Token( 'less than or equal to', '<=' )
t_equal_to = Token( 'equal to', '==' )
t_not_equal_to = Token( 'not equal to', '!=' )

t_greater_than = Token( 'greater than', '>' )
t_less_than = Token( 'less than', '<' )
t_comma = Token( 'comma', ',' )
t_add = Token( 'addition', '+' )
t_subtract = Token( 'subtraction', '-' )
t_multiply = Token( 'multiply', '*' )
t_divide = Token( 'divide', '/' )
t_semicolon = Token( 'semicolon', ';' )
t_colon = Token( 'colon', ':' )
t_lparen = Token( 'left parenthese', '(' )
t_rparen = Token( 'right parenthese', ')' )
t_lbracket = Token( 'left bracket', '[' )
t_rbracket = Token( 'right bracket', ']' )
t_and = Token( 'and', '&' )
t_or = Token( 'or', '|' )

# Check for number before checking for period
t_period = Token( 'period', '.' )


recognized_ops = [
    
]