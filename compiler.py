# Stephen Comarata
# EECE 5183 - 001 Compiler Theory 
# This program is the driver program for the compiler project 
#
# compiler.py

# Imported libraries
import sys, getopt

# Imported file classes
from myparser import Parser
from scanner import Scanner
from logger import Logger



# Main Function
def main( input_file, output_file, verbose ):
    logger = Logger( verbose )
    scanner = Scanner( input_file, logger )
    tokens = scanner.read()
    iter_tokens = iter( tokens )
    mynewparser = Parser( iter_tokens, logger )
    mynewparser.parse()


if __name__ == '__main__':
    # Handle input args
    argv = sys.argv[ 1: ]
    input_file = ''
    output_file = ''
    verbose = False
    syntax = '''
###############################################################
# Program Syntax                                              #
###############################################################
# Run Program like:                                           #
# python compiler.py -i <input_file> -o <output_file>     or  #
# python compiler.py -i <input_file> -o <output_file> -v  or  #
# python compiler.py -h                                       #
###############################################################
# Where:                                                      #
# -i <input_file> : the name/location of the src input file   #
# -o <output_file : the name/location of the desired output   #
# -v              : OPTIONAL : indicates verbose output       #
# -h              : OPTIONAL : indicates need for more help   #
###############################################################
    '''
    try:
        opts, args = getopt.getopt( argv, 'h:i:o:v', [ 'ifile=', 'ofile=' ] )
    except getopt.GetoptError:
        print( syntax )
        sys.exit( 2 )

    for opt, arg in opts:
        if opt == '-h':
            print( syntax )
            sys.exit()
        elif opt in ("-i", "--ifile"):
            input_file = arg
        elif opt in ("-o", "--ofile"):
            output_file = arg
        elif opt == '-v':
            verbose = True
    
    if input_file == '' or output_file == '':
        print( 'Not enough arguments given : ' )
        print( syntax )
        sys.exit( 2 )

    main( input_file, output_file, verbose )
