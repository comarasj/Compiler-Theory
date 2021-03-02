

class Token:
    def __init__( self, name, text ):
        self.name = name
        self.text = text

comment_start = Token( 'comment', '/*' )
comment_end = Token( 'comment', '/*' )
comment = Token( 'comment', '//' )

assignment = Token( 'assignment', '=' )
add = Token( 'addition', '+' )


recognized_ops = [
    assignment,
    add
]