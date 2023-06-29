from func_helper import get_rhs_of_stackvar #(code_id, sptr, inst_i, instructions, R, **kw):

def load_build_class(code_id,sptr,**kw):
    return [f'code{code_id}_stack_{sptr} = js_build_class']

def load_const(code_id,sptr,inst,co_const_helper,code_object ,**kw): 
    return [f'code{code_id}_stack_{sptr} = {co_const_helper[inst.arg]}']

def load_assertion_error(code_id,sptr,inst,co_const_helper,code_object ,**kw): 
    return [f'code{code_id}_stack_{sptr} = AssertionError']


def load_fast(code_id,sptr,inst,code_object ,**kw): 
#     r =  f'code{code_id}_stack_{sptr} = ( code{code_id}_locals_{code_object.co_varnames[inst.arg]} !== undefined ?  '
#     r +=  f'code{code_id}_locals_{code_object.co_varnames[inst.arg]}'
    
#     r+= f' : throwX( UnboundLocalError( \"a local variable \'{code_object.co_varnames[inst.arg]}\' referenced before assignment\")) )'
    
    r =  f'code{code_id}_stack_{sptr} = code{code_id}_locals_{code_object.co_varnames[inst.arg]}'
    v = f'code{code_id}_locals_{code_object.co_varnames[inst.arg]}'
    c = f'if( {v} === undefined ){{ throwX( UnboundLocalError( \"a local variable \'{code_object.co_varnames[inst.arg]}\' referenced before assignment\")) }}' 

    return [c,r]

def store_fast(code_id,sptr,inst, code_object , inst_i, instructions, R,**kw): 
    return [f'code{code_id}_locals_{code_object.co_varnames[inst.arg]} = { get_rhs_of_stackvar(code_id,sptr-1,inst_i,instructions,R) }']

def load_global(code_id,sptr,inst, code_object ,**kw): 
    co_name = code_object.co_names[inst.arg]
    if co_name == 'super':
        co_name = '__qdp__super__'
    return [f'code{code_id}_stack_{sptr} = {co_name}']

def load_closure(code_id,sptr,inst, code_object ,**kw): 
    r = f'code{code_id}_stack_{sptr} = ' 
    if inst.arg < len(code_object.co_cellvars):
        r += f'code{code_id}_cellvars_{code_object.co_cellvars[inst.arg]}' 
    else:
        r += f'code{code_id}_freevars_{code_object.co_freevars[inst.arg - len(code_object.co_cellvars)]}'
    return [r]

def load_deref(code_id,sptr,inst, code_object ,**kw): 
    """Loads the cell contained in slot i of the cell and free variable storage. Pushes a reference to the object the cell contains on the stack."""
    r = f'code{code_id}_stack_{sptr} = ' 
    if inst.arg < len(code_object.co_cellvars):
        r += f'code{code_id}_cellvars_{code_object.co_cellvars[inst.arg]}[0]' 
        v = f'code{code_id}_cellvars_{code_object.co_cellvars[inst.arg]}[0]'
        c = f'if( {v} === undefined ){{ throwX( UnboundLocalError( \"a local variable \'{code_object.co_cellvars[inst.arg]}\' referenced before assignment\")) }}' 

        # r += f'( {v} !== undefined ? {v} : throwX( UnboundLocalError( \"a local variable \'{code_object.co_cellvars[inst.arg]}\' referenced before assignment\")) )' 
    else:
        r += f'code{code_id}_freevars_{code_object.co_freevars[inst.arg - len(code_object.co_cellvars)]}[0]'
        v = f'code{code_id}_freevars_{code_object.co_freevars[inst.arg]}[0]'
        c = f'if( {v} === undefined ){{ throwX( NameError( \"free variable \'{code_object.co_freevars[inst.arg]}\' referenced before assignment\"))}} ' 
    
    return [c,r]

def load_classderef(code_id,sptr,inst, code_object ,**kw): 
    """Much like LOAD_DEREF but first checks the locals dictionary before consulting the cell. This is used for loading free variables in class bodies. """
    r = f'code{code_id}_stack_{sptr} = ' 
    if inst.arg < len(code_object.co_cellvars):
        r += f'code{code_id}_cellvars_{code_object.co_cellvars[inst.arg]}[0]' 
    else:
        r += f'code{code_id}_freevars_{code_object.co_freevars[inst.arg - len(code_object.co_cellvars)]}[0]'
    return [r]

def load_method(code_id,sptr,inst, code_object,  inst_i, instructions, R,**kw): 
    tos = get_rhs_of_stackvar(code_id,sptr-1, inst_i, instructions, R)
    
    r = f'var [code{code_id}_stack_{sptr-1},code{code_id}_stack_{sptr}] = js_load_method({tos},"{code_object.co_names[inst.arg]}")'
     
    return [r]


def store_deref(code_id,sptr,inst ,code_object,  inst_i, instructions, R,**kw): 
    stackvar_tos = get_rhs_of_stackvar(code_id,sptr-1, inst_i, instructions, R)
    
    if inst.arg < len(code_object.co_cellvars):
        r = f'code{code_id}_cellvars_{code_object.co_cellvars[inst.arg]}[0]' 
    else:
        r = f'code{code_id}_freevars_{code_object.co_freevars[inst.arg - len(code_object.co_cellvars)]}[0]'
    #r += f' = code{code_id}_stack_{sptr - 1}' 
    r += f'= {stackvar_tos}'
    return [r]
    
def store_subscr(code_id,sptr,inst, code_object , inst_i, instructions, R,**kw): 
    """ TOS1[TOS] = TOS2."""

    stackvar_tos = get_rhs_of_stackvar(code_id,sptr-1, inst_i, instructions, R)
    stackvar_tos1 = get_rhs_of_stackvar(code_id,sptr-2, inst_i, instructions, R)
    stackvar_tos2 = get_rhs_of_stackvar(code_id,sptr-3, inst_i, instructions, R)

    return [f'{stackvar_tos1}.__setitem__({stackvar_tos},{stackvar_tos2})']


def load_name(code_id, sptr, inst, inst_i, instructions, code_object, qualname,R, **kw):
    co_name = code_object.co_names[inst.arg]
    if co_name == 'super':
        co_name = '__qdp__super__'
    # r = f'code{code_id}_stack_{sptr} = ((arguments.callee.hasOwnProperty("{co_name}"))?' 
    # r += f' arguments.callee.{co_name}' 
    # r += f': {co_name} )' 
    if qualname == '__main__':
        return load_global(code_id,sptr,inst, code_object ,**kw)
    
    r = f'code{code_id}_stack_{sptr} = arguments.callee.{co_name}'
    return [r]

def store_name(code_id, sptr, inst, inst_i, instructions, code_object, qualname, R, **kw):
    if qualname == '__main__':
        return store_global(code_id, sptr, inst, inst_i, instructions, code_object,  R, **kw)
        
    return [ f'arguments.callee.{code_object.co_names[inst.arg]} = { get_rhs_of_stackvar(code_id,sptr-1,inst_i,instructions,R) }']

def store_global(code_id, sptr, inst, inst_i, instructions, code_object,  R, **kw):
    return [f'{code_object.co_names[inst.arg]} = { get_rhs_of_stackvar(code_id,sptr-1,inst_i,instructions,R) }']


def store_attr(code_id, sptr, inst, inst_i, instructions, code_object,R, **kw):
    tos = get_rhs_of_stackvar(code_id,sptr-1, inst_i, instructions, R)
    tos1 = get_rhs_of_stackvar(code_id,sptr-2, inst_i, instructions, R)

    return [f'{tos}.{code_object.co_names[inst.arg]}  = {tos1}']

def load_attr(code_id, sptr, inst, inst_i, instructions, code_object,R, **kw):
    tos = get_rhs_of_stackvar(code_id,sptr-1, inst_i, instructions, R)
    
    return [f'code{code_id}_stack_{sptr-1} = {tos}.{code_object.co_names[inst.arg]} ']

    
# 'INPLACE_ADD': lambda code_id,sptr,inst,ctx :do_something_binary_or_inplace(code_id, sptr, inst, **ctx) ,
# 'INPLACE_MULTIPLY': lambda code_id,sptr,inst,ctx :do_something_binary_or_inplace(code_id, sptr, inst, **ctx) ,
# 'INPLACE_SUBTRACT': lambda code_id,sptr,inst,ctx :do_something_binary_or_inplace(code_id, sptr, inst, **ctx) ,
# 'INPLACE_TRUE_DIVIDE': lambda code_id,sptr,inst,ctx :do_something_binary_or_inplace(code_id, sptr, inst, **ctx) ,
# 'BINARY_ADD': lambda code_id,sptr,inst,ctx :do_something_binary_or_inplace(code_id, sptr, inst, **ctx) ,
# 'BINARY_MULTIPLY': lambda code_id,sptr,inst,ctx :do_something_binary_or_inplace(code_id, sptr, inst, **ctx) ,
# 'BINARY_SUBTRACT': lambda code_id,sptr,inst,ctx :do_something_binary_or_inplace(code_id, sptr, inst, **ctx) ,
# 'BINARY_TRUE_DIVIDE': lambda code_id,sptr,inst,ctx :do_something_binary_or_inplace(code_id, sptr, inst, **ctx) ,
# 'BINARY_SUBSCR': lambda code_id,sptr,inst,ctx :do_something_binary_or_inplace(code_id, sptr, inst, **ctx) ,

    
# 'CALL_FUNCTION':  lambda code_id,sptr,inst,ctx :[ 
#     f'code{code_id}_stack_{sptr-inst.arg-1} = js_call_function({get_rhs_of_stackvar(code_id,sptr-inst.arg -1 , **ctx) } \
# ,{", ".join([get_rhs_of_stackvar(code_id,sptr-inst.arg + i, **ctx) for i in range(inst.arg)])} )' 
# ],
# 'CALL_FUNCTION': lambda code_id,sptr,inst,ctx :call_function(code_id, sptr, inst, **ctx) ,
# 'CALL_FUNCTION_KW': lambda code_id,sptr,inst,ctx :call_function_kw(code_id, sptr, inst, **ctx) ,

  
 
    
# 'POP_TOP':  lambda code_id,sptr,inst,ctx :[],
# 'NOP': lambda code_id,sptr,inst,ctx :[] ,
 
# # 'POP_JUMP_IF_FALSE': pop_jump_if_false,
# # 'POP_JUMP_IF_TRUE': pop_jump_if_true,
# # 'JUMP_FORWARD': jump_forward, 
# # 'JUMP_ABSOLUTE': jump_absolute,
# 'POP_JUMP_IF_FALSE': lambda code_id,sptr,inst,ctx :[],
# 'POP_JUMP_IF_TRUE': lambda code_id,sptr,inst,ctx :[],
# 'JUMP_FORWARD': lambda code_id,sptr,inst,ctx :[], 
# 'JUMP_ABSOLUTE': lambda code_id,sptr,inst,ctx :[],
    
# 'GET_ITER': get_iter, 
# 'FOR_ITER': for_iter, 
    

# 'SETUP_FINALLY': lambda code_id,sptr,inst,ctx :[], 
# 'POP_BLOCK': lambda code_id,sptr,inst,ctx :[], 
# 'POP_EXCEPT': lambda code_id,sptr,inst,ctx :[], 
# 'RERAISE': lambda code_id,sptr,inst,ctx :[  ], 
# 'JUMP_IF_NOT_EXC_MATCH':  lambda code_id,sptr,inst,ctx :[  ],
    
# 'DELETE_FAST': lambda code_id,sptr,inst,ctx :[  ], 
# 'LOAD_BUILD_CLASS':lambda code_id,sptr,inst,ctx :load_build_class(code_id, sptr, inst, **ctx) ,
# 'LOAD_NAME':lambda code_id,sptr,inst,ctx :load_name(code_id, sptr, inst, **ctx) ,
# 'STORE_NAME':lambda code_id,sptr,inst,ctx :store_name(code_id, sptr, inst, **ctx) ,
# 'STORE_ATTR':  lambda code_id,sptr,inst,ctx :store_attr(code_id, sptr, inst, **ctx) ,
# 'STORE_SUBSCR':  lambda code_id,sptr,inst,ctx :store_subscr(code_id, sptr, inst, **ctx) ,
# }

