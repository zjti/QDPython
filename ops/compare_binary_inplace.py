from func_helper import get_rhs_of_stackvar #(code_id, sptr, inst_i, instructions, R, **kw):

def compare_op(code_id,sptr, inst,  **kw): 
     
    r = f'code{code_id}_stack_{sptr-2} = '
    r += get_rhs_of_stackvar(code_id,sptr -2 , **kw) 
    r += ['<', '<=', '==', '!=', '>', '>='][inst.arg]
    r += get_rhs_of_stackvar(code_id,sptr -1 , **kw) 
    return [r]

def inplace_add(**kw): 
    return do_something_binary_or_inplace(**kw)

def inplace_multiply(**kw): 
    return do_something_binary_or_inplace(**kw)

def inplace_subtract(**kw): 
    return do_something_binary_or_inplace(**kw)

def inplace_true_divide(**kw): 
    return do_something_binary_or_inplace(**kw)

def inplace_floor_divide(**kw): 
    return do_something_binary_or_inplace(**kw)

def binary_add(**kw): 
    return do_something_binary_or_inplace(**kw)

def binary_multiply(**kw): 
    return do_something_binary_or_inplace(**kw)

def binary_subtract(**kw): 
    return do_something_binary_or_inplace(**kw)

def binary_true_divide(**kw): 
    return do_something_binary_or_inplace(**kw)

def binary_floor_divide(**kw): 
    return do_something_binary_or_inplace(**kw)

def binary_modulo(**kw): 
    return do_something_binary_or_inplace(**kw)
                
def binary_subscr(code_id,sptr,  inst_i, instructions, R,**kw): 
    stackvar_tos = get_rhs_of_stackvar(code_id,sptr-1, inst_i, instructions, R)
    stackvar_tos1 = get_rhs_of_stackvar(code_id,sptr-2, inst_i, instructions, R)
    r = f'code{code_id}_stack_{sptr-2} = {stackvar_tos1}.__getitem__({stackvar_tos})'
    return [r]


def do_something_binary_or_inplace(code_id, sptr, inst, inst_i, instructions, code_object, R, **kw):
    stackvar_tos = get_rhs_of_stackvar(code_id,sptr-1, inst_i, instructions, R)
    stackvar_tos1 = get_rhs_of_stackvar(code_id,sptr-2, inst_i, instructions, R)
    
    helper = {
        'INPLACE_ADD':'js__iadd__',
        'INPLACE_MULTIPLY':'js__imul__',
        'INPLACE_SUBTRACT':'js__isub__',
        'INPLACE_TRUE_DIVIDE':'js__itruediv__',
        'INPLACE_FLOOR_DIVIDE':'js__ifloordiv__',
        'BINARY_ADD':'js__add__',
        'BINARY_MULTIPLY':'js__mul__',
        'BINARY_SUBTRACT':'js__sub__',
        'BINARY_TRUE_DIVIDE':'js__truediv__',
        'BINARY_FLOOR_DIVIDE':'js__floordiv__',
        'BINARY_MODULO':'js__modulo__',
             }
                
    func = helper[inst.opname]
    r = f'code{code_id}_stack_{sptr-2} = {func}({stackvar_tos1},{stackvar_tos})'
   
    return [r]