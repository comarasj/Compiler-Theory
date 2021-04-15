# Stephen Comarata
# EECE 5183 - 001 Compiler Theory 
# This program is the logger class for the compiler project 
#
# logger.py

class Logger:
    def __init__( self, verbose ):
        self.verbose = verbose
    

    def report_error( self, origin, msg, line_number ):
        error_msg = '{0} error: {1} Line Number: {2}'.format( origin, msg, line_number )
        print( error_msg )
    

    def report_warning( self, origin, msg, line_number ):
        if self.verbose:
            warn_msg = '{0} warning: {1} Line Number: {2}'.format( origin, msg, line_number )
            print( warn_msg )
