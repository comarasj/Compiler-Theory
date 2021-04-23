# Stephen Comarata
# EECE 5183 - 001 Compiler Theory 
# This program is the scoper class for the compiler project 
#
# scoper.py

from tokens import built_in_functions
from scope import Scope

class Scoper:


    def __init__( self, base_scope ):
        self.scopes = []
        self.scope_count = 1

        self.base_scope = Scope( base_scope, None, None, 0 )
        self.base_scope.procedures = built_in_functions
        self.scopes.append( self.base_scope )

        self.current_scope = self.base_scope
        self.next_scope = None


    def create_new_scope( self, scope_name ):
        new_scope = Scope( scope_name, self.current_scope.scope_name, self.current_scope.id, self.scope_count )
        self.scope_count = self.scope_count + 1
        self.next_scope = new_scope
        self.scopes.append( new_scope )
    
    def go_to_next_scope( self ):
        temp = self.current_scope
        self.current_scope = self.next_scope
        self.next_scope = temp
    

    def go_to_base_scope( self ):
        self.current_scope = self.base_scope
    

    def go_to_parent_scope( self ):
        parent_scope = self.get_parent_scope( self.current_scope )
        if parent_scope != None:
            self.current_scope = parent_scope
    

    def get_parent_scope( self, child_scope ):
        parent_id = child_scope.parent_id
        for i in self.scopes:
            if i.id == parent_id:
                return i
        return None


    def add_variable( self, variable_name, variable_type, is_array, array_length, global_flag ):
        if global_flag:
            self.base_scope.add_variable( variable_name, variable_type, is_array, array_length )
        else:
            self.current_scope.add_variable( variable_name, variable_type, is_array, array_length )
    

    def add_procedure( self, procedure_name, procedure_type, global_flag ):
        if global_flag:
            self.base_scope.add_procedure( procedure_name, procedure_type )
        else:
            self.current_scope.add_procedure( procedure_name, procedure_type )
            self.next_scope.add_procedure( procedure_name, procedure_type )
    

    def add_procedure_input_param( self, procedure_name, input_param, input_type, input_index, global_flag ):
        if global_flag:
            self.base_scope.add_procedure_input_parameter( procedure_name, input_param, input_type, input_index )
        else:
            self.current_scope.add_procedure_input_parameter( procedure_name, input_param, input_type, input_index )
            parent_scope = self.get_parent_scope( self.current_scope )
            parent_scope.add_procedure_input_parameter( procedure_name, input_param, input_type, input_index )


    def add_procedure_input_param_array_type( self, procedure_name, input_param, array_length, global_flag ):
        if global_flag:
            self.base_scope.add_procedure_input_parameter_array( procedure_name, input_param, array_length )
        else:
            self.current_scope.add_procedure_input_parameter( procedure_name, input_param, input_type, input_index )
            parent_scope = self.get_parent_scope( self.current_scope )
            parent_scope.add_procedure_input_parameter( procedure_name, input_param, input_type, input_index )


    def is_variable_in_current_scope( self, variable_name, global_flag ):
        if global_flag:
            if variable_name in self.base_scope.variables:
                return True
            return False
        else:
            if variable_name in self.current_scope.variables:
                return True
            return False


    def is_procedure_in_current_scope( self, procedure_name, global_flag ):
        if global_flag:
            if procedure_name in self.base_scope.procedures:
                return True
            return False
        else:
            if procedure_name in self.current_scope.procedures:
                return True
            return False


    def is_variable_in_scope( self, variable_name, search_scope=None ):
        if search_scope == None:
            search_scope = self.current_scope
        
        if variable_name in search_scope.variables:
            return True
        else:
            parent_scope = self.get_parent_scope( search_scope )
            if parent_scope != None:
                return self.is_variable_in_scope( variable_name, parent_scope )
        return False


    def is_procedure_in_scope( self, procedure_name, search_scope=None ):
        if search_scope == None:
            search_scope = self.current_scope
        
        if procedure_name in search_scope.procedures:
            return True
        else:
            parent_scope = self.get_parent_scope( search_scope )
            if parent_scope != None:
                return self.is_procedure_in_scope( procedure_name, parent_scope )
        return False


    def get_variable_type( self, variable_name, symbol, search_scope=None ):
        if search_scope == None:
            search_scope = self.current_scope
        if variable_name in search_scope.variables:
            variable = search_scope.variables[ variable_name ]
            symbol.type = self.convert_type( variable[ 'variable_type' ] )
            if variable[ 'is_array' ] == True:
                symbol.is_array = variable[ 'is_array' ]
                symbol.array_length = variable[ 'array_length' ]
        else:
            parent_scope = self.get_parent_scope( search_scope )
            if parent_scope != None:
                self.get_variable_type( variable_name, symbol, parent_scope )


    def get_procedure_type( self, procedure_name, symbol, search_scope=None ):
        if search_scope == None:
            search_scope = self.current_scope
        if procedure_name in search_scope.procedures:
            procedure = search_scope.procedures[ procedure_name ]
            symbol.type = self.convert_type( procedure[ 'procedure_type' ] )
        else:
            parent_scope = self.get_parent_scope( search_scope )
            if parent_scope != None:
                self.get_procedure_type( procedure_name, symbol, parent_scope )


    def get_procedure_args( self, procedure, search_scope=None ):
        if search_scope == None:
            search_scope = self.current_scope
        
        if procedure in search_scope.procedures: 
            return search_scope.procedures[ procedure ][ 'input_parameters' ]
        else:
            parent_scope = self.get_parent_scope( search_scope )
            if not parent_scope == None:
                return self.get_procedure_args( procedure, parent_scope )
        return None


    def convert_type( self, type1 ):
        if type1 == 'integer':
            return 'INT'
        elif type1 == 'float':
            return 'FLOAT'
        elif type1 == 'string':
            return 'STRING'
        elif type1 == 'bool':
            return 'BOOL'