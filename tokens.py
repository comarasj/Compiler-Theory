# Stephen Comarata
# EECE 5183 - 001 Compiler Theory 
# This program is the token class for the compiler project 
#
# tokens.py

class Token:
    def __init__( self, name, text, line_number=0 ):
        self.name = name
        self.text = text
        self.line_number = line_number


keywords = [ 'program', 'is', 'begin', 'end', 'global', 'procedure', 
             'variable', 'integer', 'float', 'string', 'bool', 'if', 
             'then', 'else', 'for', 'return', 'not', 'true', 'false' ]


t_comment_start = Token( 'comment', '/*' )
t_comment_end = Token( 'comment', '*/' )
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
t_identifier = Token( 'identifier', 'identifier' )
t_string = Token( 'string', 'string' )
t_number = Token( 'number', 'number' )
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


keyword_tokens = [
    t_program,
    t_is,
    t_begin,
    t_end,
    t_global,
    t_procedure,
    t_variable,
    t_integer,
    t_float,
    t_string,
    t_bool,
    t_if,
    t_then,
    t_else,
    t_for,
    t_return,
    t_not,
    t_true,
    t_false
]


operator_tokens = [
    t_comment_start,
    t_comment_end,
    t_comment,
    t_assignment,
    t_greater_than_or_equal_to,
    t_less_than_or_equal_to,
    t_equal_to,
    t_not_equal_to,
    t_greater_than,
    t_less_than,
    t_comma,
    t_add,
    t_subtract,
    t_multiply,
    t_divide,
    t_semicolon,
    t_colon,
    t_lparen,
    t_rparen,
    t_lbracket,
    t_rbracket,
    t_and,
    t_or
]


built_in_functions = {
    'getbool': { 
        'type': 'bool', 
        'input_params': {}
    },
    'getinteger': { 
        'type': 'integer', 
        'input_params': {}
    },
    'getfloat': { 
        'type': 'float', 
        'input_params': {}
    },
    'getstring': { 
        'type': 'string', 
        'input_params': {}
    },
    'putbool': { 
        'type': 'bool', 
        'input_params': { 
            'value': { 
                'type': 'bool', 
                'is_array': False, 
                'array_length': 0 
            }
        }
    },
    'putinteger': { 
        'type': 'bool', 
        'input_params': { 
            'value': { 
                'type': 'integer', 
                'is_array': False, 
                'array_length': 0 
            }
        }
    },
    'putfloat': { 
        'type': 'bool', 
        'input_params': { 
            'value': { 
                'type': 'float', 
                'is_array': False, 
                'array_length': 0 
            }
        }
    },
    'putstring': { 
        'type': 'bool', 
        'input_params': { 
            'value': { 
                'type': 'string', 
                'is_array': False, 
                'array_length': 0 
            }
        }
    },
    'sqrt': { 
        'type': 'float', 
        'input_params': { 
            'value': { 
                'type': 'integer', 
                'is_array': False, 
                'array_length': 0 
            }
        }
    }
}
