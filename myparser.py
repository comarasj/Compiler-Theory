import re 

class Parser:
    def __init__( self, _token_list ):
        self.token_list = _token_list
        self.current_token = None

    # Start to parse
    def parse( self ):
        self.current_token = next( self.token_list )
        


