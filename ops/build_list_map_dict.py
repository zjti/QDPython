from func_helper import get_rhs_of_stackvar #(code_id, sptr, inst_i, instructions, R, **kw):

def build_string(code_id, sptr, inst, inst_i, instructions, code_object , R, **kw):
    r = f"code{code_id}_stack_{sptr-inst.arg} = "
    args = [get_rhs_of_stackvar(code_id,sptr-inst.arg+i, inst_i, instructions,R) for i in range(inst.arg)]
    r+= f"[{','.join(args)}].join('')"
    return [r]

def build_const_key_map(code_id, sptr, inst, inst_i, instructions, code_object , R, **kw):
    #remove unused tuple from stack:
    get_rhs_of_stackvar(code_id,sptr-1, inst_i, instructions,R)
    
    keys = code_object.co_consts[instructions[inst_i-1][0].arg]
    # keys = [(f"'{k}'" if type(k)==str else f"{k}" )  for k in keys]
    keys = [f'"{k}"' for k in keys]
    values = [get_rhs_of_stackvar(code_id, sptr - 1 - len(keys) + j, inst_i, instructions, R )  for j in range(len(keys)) ] 
    r = f'code{code_id}_stack_{sptr-1-inst.arg} = new pydict( ['
    r += ','.join( [ f'[{k},{v}]' for k,v in zip(keys,values)   ] )
    r += '] )'
    
    return [r]

def build_map(code_id, sptr, inst, inst_i, instructions, code_object , R, **kw):
    stackvar_result = f'code{code_id}_stack_{sptr-2*inst.arg}'
    new_map = []
    for i in range(inst.arg):
        # k = f'code{code_id}_stack_{sptr-2*inst.arg+2*i}'
        # v = f'code{code_id}_stack_{sptr-2*inst.arg+2*i+1}'
        k = get_rhs_of_stackvar(code_id, sptr-2*inst.arg+2*i, inst_i, instructions, R )
        v = get_rhs_of_stackvar(code_id, sptr-2*inst.arg+2*i+1, inst_i, instructions, R )
        new_map+= [f' [{k},{v}]']
    new_map = ','.join(new_map)  
    return [ f"{stackvar_result} = new pydict([{new_map}])" ]
        

def build_list(code_id, sptr, inst, inst_i, instructions, code_object , R, **kw):
    values = [get_rhs_of_stackvar(code_id, sptr - 1 - j, inst_i, instructions, R )  for j in range(inst.arg) ] 
    r = f'code{code_id}_stack_{sptr-inst.arg} = new pylist( [' 
    r += ','.join( [ f'{v}' for v in values[::-1]   ] )
    r += '])'
    
    return [r]

def build_tuple(code_id, sptr, inst, inst_i, instructions, code_object , R, **kw):
    values = [get_rhs_of_stackvar(code_id, sptr - 1 - j, inst_i, instructions, R )  for j in range(inst.arg) ] 
    r = f'code{code_id}_stack_{sptr-inst.arg} = new pytuple( [' 
    r += ','.join( [ f'{v}' for v in values[::-1]   ] )
    r += '])'
    
    return [r]

def list_extend(code_id, sptr, inst, inst_i, instructions, code_object , R, **kw):
    tos_tuple = get_rhs_of_stackvar(code_id, sptr - 1, inst_i, instructions, R )
    
    #r = f'code{code_id}_stack_{sptr-1-inst.arg}.__arr__.push({tos_tuple})'
    r = f'code{code_id}_stack_{sptr-1-inst.arg} = code{code_id}_stack_{sptr-1-inst.arg}.__iadd__({tos_tuple})'
   
    return [r]

def list_append(code_id, sptr, inst, inst_i, instructions, code_object , R, **kw):
    tos = get_rhs_of_stackvar(code_id, sptr - 1, inst_i, instructions, R )
    
    r = f'code{code_id}_stack_{sptr-1-inst.arg}.__arr__.push( {tos} )' 
   
    return [r]

def map_add(code_id, sptr, inst, inst_i, instructions, code_object , R, **kw):
    tos = get_rhs_of_stackvar(code_id, sptr - 1, inst_i, instructions, R )
    tos1 = get_rhs_of_stackvar(code_id, sptr - 2, inst_i, instructions, R )
    
    # r = f'code{code_id}_stack_{sptr-2-inst.arg}.__map__.set( {tos1},{tos} )' 
    r = f'code{code_id}_stack_{sptr-2-inst.arg}.__setitem__( {tos1},{tos} )' 
   
    return [r]

def dict_merge(code_id, sptr, inst, inst_i, instructions, code_object , R, **kw):
    tos = get_rhs_of_stackvar(code_id, sptr - 1, inst_i, instructions, R )
    tosi =  f'code{code_id}_stack_{sptr-1-inst.arg}'
    
    return [ f"if ([...{tosi}.__map__.keys()].some(x => {tos}.__map__.has(x)) ) {{ throw new Error('DICT_MERGE');}}",
            f"{tosi}.__map__ = new Map([...{tosi}.__map__,...{tos}.__map__])"]

def dict_merge(code_id, sptr, inst, inst_i, instructions, code_object , R, **kw):
    tos = get_rhs_of_stackvar(code_id, sptr - 1, inst_i, instructions, R )
    tosi =  f'code{code_id}_stack_{sptr-1-inst.arg}'
     
    return [ f"{tosi}.__map__ = new Map([...{tosi}.__map__,...{tos}.__map__])" ]

                