# Stephen Comarata
# EECE 5183 - 001 Compiler Theory 
# This program is the logger class for the compiler project 
#
# logger.py

class Logger:
    def __init__( self, verbose ):
        self.verbose = verbose

    
    def set_origin( self, origin ):
        self.origin = origin


    def report_error( self, msg, line_number ):
        error_msg = '{0} error: {1} \n         Line Number: {2}'.format( self.origin, msg, line_number )
        print( error_msg )
    

    def report_warning( self, msg, line_number ):
        warn_msg = '{0} warning: {1} \n         Line Number: {2}'.format( self.origin, msg, line_number )
        print( warn_msg )
    

    def info( self, msg, line_number ):
        if self.verbose:
            info_msg = '{0} info: {1} \n         Line Number: {2}'.format( self.origin, msg, line_number )
            print( info_msg )
