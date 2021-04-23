# Stephen Comarata
# EECE 5183 - 001 Compiler Theory 
# This program is the scope class for the compiler project 
#
# scope.py


class Symbol:

    def __init__( self ):
        self.id = ''
        self.type = ''
        self.is_array = False
        self.is_indexed_array = False
        self.array_length = 0