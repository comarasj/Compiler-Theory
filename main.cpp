/** EECE 5183 - 001 Compiler Theory 
 * Stephen Comarata
 * main.cpp
 * 
 * This program is the driver program for the compiler project 
 * 
 * 
 */


//Includes
#include <iostream>
#include <fstream>
#include "scanner.cpp"
using namespace std;


int main() {
    fstream file1;
    file1.open("text.txt", ios::in);

    if( !file1 ) {
        cout << "File does not exist" << endl;
        return 0;
    }

    Scanner scanner( file1 );

}