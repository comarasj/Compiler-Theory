class Scoper:
    def __init__( self, base_scope ):
        self.current_scope_name = base_scope
        self.scopes = { base_scope: { 'procedures': {}, 'variables': {}, 'parent': None } }
        self.current_scope_table = {}
        self.next_scope_name = ''
    
    def create_new_scope( self, scope_name ):
        if scope_name in self.scopes:
            print( 'Scoping Error, ' + str( scope_name ) + 'already exists!' )
            return False
        self.scopes[ scope_name ] = { 'procedures': {}, 'variables': {}, 'parent': self.current_scope_name }
        self.next_scope_name = scope_name
        return True
    
    def next_scope( self ):
        temp = self.current_scope_name
        self.current_scope_name = self.next_scope_name
        self.next_scope_name = temp # default back to previous

    def add_procedure( self, procedure_name ):
        self.scopes[ self.current_scope_name ][ 'procedures' ][ procedure_name ] = { 'type': '', 'input_params': {} }

    def add_variable( self, variable_name ):
        self.scopes[ self.current_scope_name ][ 'variables' ][ variable_name ] = { 'type': '' }

    def add_procedure_type( self, procedure_name, procedure_type ):
        self.scopes[ self.current_scope_name ][ 'procedures' ][ procedure_name ][ 'type' ] = procedure_type

    def add_variable_type( self, variable_name, variable_type ):
        self.scopes[ self.current_scope_name ][ 'variables' ][ variable_name ][ 'type' ] = variable_type

    def add_procedure_input_param( self, procedure_name, input_param ):
        self.scopes[ self.current_scope_name ][ 'procedures' ][ procedure_name ][ 'input_params' ][ input_param ] = { 'type': '' }
    
    def add_procedure_input_param_type( self, procedure_name, input_param, input_type ):
        self.scopes[ self.current_scope_name ][ 'procedures' ][ procedure_name ][ 'input_params' ][ input_param ][ 'type' ] = input_type
    
    def get_parent_scope( self, child_scope_name ):
        return self.scopes[ child_scope_name ].parent

    def is_variable_in_scope( self, variable_name, search_scope ):
        if search_scope == None:
            search_scope = self.current_scope_name
        
        if self.scopes[ search_scope ]:
            if self.scopes[ search_scope ][ variable_name]: 
                return True
            else:
                parent_scope = self.get_parent_scope( search_scope )
                if not parent_scope == None:
                    return self.is_variable_in_scope( variable_name, parent_scope )
        return False

