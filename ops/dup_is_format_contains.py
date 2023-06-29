from func_helper import get_rhs_of_stackvar #(code_id, sptr, inst_i, instructions, R, **kw):

def is_op(code_id,sptr,inst, **kw):
    r = f'code{code_id}_stack_{sptr-2} = '
    r += f'( {("!" if inst.arg == 1 else "")}js_is_op('
    r += get_rhs_of_stackvar(code_id,sptr -2 , **kw)  + ', '
    r += get_rhs_of_stackvar(code_id,sptr -1 , **kw)  + '))'
    return [r]

def dup_top(code_id,sptr, **kw):
    # return [ f'code{code_id}_stack_{sptr} = code{code_id}_stack_{sptr-1} ']
    return [ f'code{code_id}_stack_{sptr} = {get_rhs_of_stackvar(code_id,sptr -1 , remove_old_line=False, **kw)} ']

def format_value(code_id,sptr,inst, code_object , inst_i, instructions, R,**kw): 
    # todo implement all flags and format_specs
    
    to_format = get_rhs_of_stackvar(code_id,sptr-1, inst_i, instructions, R)
    stack_result = f'code{code_id}_stack_{sptr-1}'
    if inst.arg&4==4:
        stack_result = f'code{code_id}_stack_{sptr-2}'
        to_format = get_rhs_of_stackvar(code_id,sptr-2, inst_i, instructions, R)

        
    return [f'{stack_result} = str({to_format})' ]

def contains_op(code_id,sptr,inst, **kw): 
    tos1 = get_rhs_of_stackvar(code_id,sptr -2 , **kw) 
    tos = get_rhs_of_stackvar(code_id,sptr -1 , **kw) 
    
    nin = f'{tos}.__arr__.includes({tos1})'
    
    if inst.arg == 1:
        return [f'code{code_id}_stack_{sptr-2} = !{nin}']
    else:
        return [f'code{code_id}_stack_{sptr-2} = {nin}']