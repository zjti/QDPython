import dis
from func_helper import get_code_object_id


def tuple_to_js(tup):
    tup_elems = []
    for e in tup:
        if type(e)== str:
            tup_elems.append(f'"{e}"')
        elif type(e)== int:
            tup_elems.append(f'{e}n')
        elif type (e) == tuple:
            tup_elems.append( tuple_to_js(e))
        else:
            tup_elems.append(f'{e}')
            
    js_tup = f'new pytuple([{",".join(tup_elems)}])'
    return js_tup

def get_child_code_obejct(code_object):
    return [co for co in code_object.co_consts if str(type(co)) == "<class 'code'>" ]

def prepare_co_consts(code_object):
    """setup helper dict for load_const instructions.
       create list of const_defs for object_types
       
       co_const_helper:
            if type(co_const[const_i] ) != None and != CodeObject:
                if const_i is loaded multiple times:
                   co_const_helper[const_i] = f'code{code_num}_constdef_{const_i}' #const_var
                if const_i is loaded only once:
                   co_const_helper[const_i] = f'new pyxytype( CONST )' #const_def
            else:
                co_const_helper[const_i] = None
            
       
       returns -> (dict,list)
       """
    load_const_count = {k:0 for k in code_object.co_consts}
    for inst_i,inst in enumerate(dis.get_instructions(code_object)):
        if inst.opname == 'LOAD_CONST':
            load_const_count[ code_object.co_consts[inst.arg] ] += 1
            if load_const_count[ code_object.co_consts[inst.arg] ] == 1:
                #check if in loop
                for inst_j,other_inst in enumerate(dis.get_instructions(code_object)):
                    if other_inst.opname == 'JUMP_ABSOLUTE':
                        if inst_j > inst_i and other_inst.arg  < inst_i:
                            #found loop -> make load_const_counter greater 1
                            load_const_count[ code_object.co_consts[inst.arg] ] += 1
    
    code_num = get_code_object_id(code_object)
    co_const_helper = {}
    const_defs = []
    for const_i,co_const in enumerate(code_object.co_consts):
        if co_const is None or str(type(co_const)) == "<class 'code'>":
            co_const_helper[const_i] = 'None'
        elif type (co_const) == str:
            esc_co_const = co_const.replace('"','\\"')
            co_const_helper[const_i] = f'"{esc_co_const}"'
        elif type (co_const) == tuple:
            const_def = tuple_to_js(co_const)
        elif type (co_const) == int:
            co_const_helper[const_i] = f'{co_const}n'
        elif type (co_const) == bool:
            if co_const:
                co_const_helper[const_i] = 'true'
            else:
                co_const_helper[const_i] = 'false'
        elif type (co_const) == float:
            co_const_helper[const_i] = f'{co_const}'
        else:
            raise Exception(f'type {type(co_const)} not available')
            
        if const_i not in co_const_helper: # if its not None or CodeObject
            if load_const_count[co_const] == 1:
                co_const_helper[const_i] = const_def
            else:
                const_var = f'code{code_num}_constdef_{const_i}'
                const_defs.append(f'var {const_var} = {const_def}' )
                co_const_helper[const_i] = const_var
        
    return co_const_helper,const_defs

def find_const_locals(code_object):
    """ local_x in const_locals if:
            -local_x not in args
            -local_x only used in one store fast
    """
    f_locals = code_object.co_varnames
    
    # 
    has_varargs = code_object.co_flags & 4 == 4
    has_kwargs = code_object.co_flags & 8 == 8
    
    argc = code_object.co_argcount + has_varargs + has_kwargs 
    argc += code_object.co_posonlyargcount + code_object.co_kwonlyargcount
    
    store_fast_count = {k:0 for k in f_locals[argc:]}
    
    for inst_i,inst in enumerate(dis.get_instructions(code_object)):
        if inst.opname == 'STORE_FAST':
            store_fast_count[ code_object.co_varnames[inst.arg] ] += 1
            
    const_locals = [k for k,v in store_fast_count.items() if v == 1]
    return const_locals

def find_const_cellvars(code_object , store_deref_count = None ):
    """ cell_x in const_cells if:
            -local_x only used in one store_deref (in all child code_object)
    """
    if store_deref_count is None:
        f_cells = code_object.co_cellvars
        store_deref_count = {k:0 for k in f_cells}
    
    for inst_i,inst in enumerate(dis.get_instructions(code_object)):
        if inst.opname == 'STORE_DEREF':
            if  inst.arg < len(code_object.co_cellvars):
                varname = code_object.co_cellvars[inst.arg] 
            else:
                varname = code_object.co_freevars[inst.arg - len(code_object.co_cellvars)]

            if varname in store_deref_count:
                store_deref_count[ varname ] += 1
     
    # search in child code_objects:
    child_code_objects = get_child_code_obejct(code_object)
    for child_code_object in child_code_objects:
        find_const_cellvars(child_code_object, store_deref_count)
            
    const_cells = [k for k,v in store_deref_count.items() if v == 1]
    return const_cells
