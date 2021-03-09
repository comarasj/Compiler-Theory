# Stephen Comarata
# EECE 5183 - 001 Compiler Theory 
# This program is the driver program for the compiler project 
#
# compiler.py
from myparser import Parser
from scanner import Scanner

if __name__ == '__main__':
    scanner = Scanner( 'text.txt' )
    tokens = iter( scanner.read() )
    parser = Parser( tokens )
    parser.parse()