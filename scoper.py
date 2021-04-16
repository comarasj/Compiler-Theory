# Stephen Comarata
# EECE 5183 - 001 Compiler Theory 
# This program is the scoper class for the compiler project 
#
# scoper.py

class Scoper:


    def __init__( self, base_scope ):
        self.current_scope_name = base_scope
        self.scopes = { base_scope: { 'procedures': {}, 'variables': {}, 'parent': None } }
        self.current_scope_table = {}
        self.next_scope_name = ''
        self.base_scope = base_scope


    def create_new_scope( self, scope_name ):
        self.scopes[ scope_name ] = { 'procedures': {}, 'variables': {}, 'parent': self.current_scope_name }
        self.next_scope_name = scope_name


    def go_to_next_scope( self ):
        temp = self.current_scope_name
        self.current_scope_name = self.next_scope_name
        self.next_scope_name = temp # default back to previous


    def go_to_base_scope( self ):
        self.current_scope_name = self.base_scope


    def add_variable( self, variable_name, global_flag ):
        if global_flag:
            self.scopes[ self.base_scope ][ 'variables' ][ variable_name ] = { 'type': '', 'is_array': False, 'array_length': 0 }
        else:
            self.scopes[ self.current_scope_name ][ 'variables' ][ variable_name ] = { 'type': '' }


    def add_variable_type( self, variable_name, variable_type, global_flag ):
        if global_flag:
            self.scopes[ self.base_scope ][ 'variables' ][ variable_name ][ 'type' ] = variable_type
        else:
            self.scopes[ self.current_scope_name ][ 'variables' ][ variable_name ][ 'type' ] = variable_type


    def add_variable_array_type( self, variable_name, array_length, global_flag ):
        if global_flag:
            self.scopes[ self.base_scope ][ 'variables' ][ variable_name ][ 'is_array' ] = True
            self.scopes[ self.base_scope ][ 'variables' ][ variable_name ][ 'array_length' ] = array_length
        else:
            self.scopes[ self.current_scope_name ][ 'variables' ][ variable_name ][ 'is_array' ] = True
            self.scopes[ self.current_scope_name ][ 'variables' ][ variable_name ][ 'array_length' ] = array_length


    def add_procedure( self, procedure_name, global_flag ):
        if global_flag:
            self.scopes[ self.base_scope ][ 'procedures' ][ procedure_name ] = { 'type': '', 'input_params': {} }
        else:
            self.scopes[ self.current_scope_name ][ 'procedures' ][ procedure_name ] = { 'type': '', 'input_params': {} }


    def add_procedure_type( self, procedure_name, procedure_type, global_flag ):
        if global_flag:
            self.scopes[ self.base_scope ][ 'procedures' ][ procedure_name ][ 'type' ] = procedure_type
        else:
            self.scopes[ self.current_scope_name ][ 'procedures' ][ procedure_name ][ 'type' ] = procedure_type


    def add_procedure_input_param( self, procedure_name, input_param, global_flag ):
        if global_flag:
            self.scopes[ self.base_scope ][ 'procedures' ][ procedure_name ][ 'input_params' ][ input_param ] = { 'type': '' }
        else:
            self.scopes[ self.current_scope_name ][ 'procedures' ][ procedure_name ][ 'input_params' ][ input_param ] = { 'type': '' }


    def add_procedure_input_param_type( self, procedure_name, input_param, input_type, global_flag ):
        if global_flag:
            self.scopes[ self.base_scope ][ 'procedures' ][ procedure_name ][ 'input_params' ][ input_param ][ 'type' ] = input_type
        else:
            self.scopes[ self.current_scope_name ][ 'procedures' ][ procedure_name ][ 'input_params' ][ input_param ][ 'type' ] = input_type


    def get_parent_scope( self, child_scope_name ):
        return self.scopes[ child_scope_name ].parent


    def is_variable_in_scope( self, variable_name, search_scope ):
        if search_scope == None:
            search_scope = self.current_scope_name
        
        if self.scopes[ search_scope ]:
            if self.scopes[ search_scope ][ 'variables' ][ variable_name ]: 
                return True
            else:
                parent_scope = self.get_parent_scope( search_scope )
                if not parent_scope == None:
                    return self.is_variable_in_scope( variable_name, parent_scope )
        return False


    def is_procedure_in_scope( self, procedure_name, search_scope ):
        if search_scope == None:
            search_scope = self.current_scope_name
        
        if self.scopes[ search_scope ]:
            if self.scopes[ search_scope ][ 'procedures' ][ procedure_name ]: 
                return True
            else:
                parent_scope = self.get_parent_scope( search_scope )
                if not parent_scope == None:
                    return self.is_procedure_in_scope( procedure_name, parent_scope )
        return False
    

    def is_variable_in_current_scope( self, variable_name ):
        if self.scopes[ self.current_scope_name ]:
            if self.scopes[ self.current_scope_name ][ 'variables' ][ variable_name ]:
                return True
        return False
    

    def is_procedure_in_current_scope( self, procedure_name ):
        if self.scopes[ self.current_scope_name ]:
            if procedure_name in self.scopes[ self.current_scope_name ][ 'procedures' ]:
                return True
        return False