
class Token:
    def __init__( self, text ):
        self.text = text
    


class Scanner:
    def __init__( self, input_file ):
        self.input_file = input_file

    def read( self ):
        # open input file
        file_object = open( self.input_file, 'r' )
        file_contents = file_object.read()
        print( file_contents )

