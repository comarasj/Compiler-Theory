# Stephen Comarata
# EECE 5183 - 001 Compiler Theory 
# This program is the scope class for the compiler project 
#
# scope.py


class Scope:    
    def __init__( self, scope_name, parent_name, parent_id, id ):
        self.variables = {}
        self.procedures = {}
        self.scope_name = scope_name
        self.parent = parent_name
        self.parent_id = parent_id
        self.id = id
    
    
    def add_variable( self, variable_name, variable_type, is_array, array_length ):
        self.variables[ variable_name ] = { 'variable_type': variable_type, 'is_array': is_array, 'array_length': array_length }
    

    def add_procedure( self, procedure_name, procedure_type ):
        self.procedures[ procedure_name ] = { 'procedure_type': procedure_type, 'input_parameters': {} }

    
    def add_procedure_input_parameter( self, procedure_name, name, variable_type, input_index ):
        self.procedures[ procedure_name ][ 'input_parameters' ][ name ] = { 'variable_type': variable_type, 'is_array': False, 'array_length': 0, 'index': input_index }
    

    def add_procedure_input_parameter_array( self, procedure_name, name, array_length ):
        self.procedures[ procedure_name ][ 'input_parameters' ][ name ][ 'is_array' ] = True
        self.procedures[ procedure_name ][ 'input_parameters' ][ name ][ 'is_array' ] = array_length
    

