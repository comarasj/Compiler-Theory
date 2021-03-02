# Stephen Comarata
# EECE 5183 - 001 Compiler Theory 
# This program is the driver program for the compiler project 
#
# compiler.py

from scanner import Scanner
from parser import Parser

if __name__ == '__main__':
    myscanner = Scanner( 'text.txt' )
    tokens = myscanner.read()
    print( tokens )