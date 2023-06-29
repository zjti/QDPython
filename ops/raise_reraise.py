from func_helper import get_rhs_of_stackvar #(code_id, sptr, inst_i, instructions, R, **kw):

def raise_varargs(code_id, sptr, inst, inst_i, instructions, code_object ,R, **kw):
    # tos = get_rhs_of_stackvar(code_id, sptr - 1, inst_i, instructions, R )
    if inst.arg == 2:
        tos = get_rhs_of_stackvar(code_id, sptr - 1, inst_i, instructions, R )
        tos1 = get_rhs_of_stackvar(code_id, sptr - 2, inst_i, instructions, R )
        return [ f'throw {tos}({tos1})' ]
    if inst.arg == 1:
        tos = get_rhs_of_stackvar(code_id, sptr - 1, inst_i, instructions, R )
        return [ f'throw {tos}' ]
    if inst.arg == 0:
        return [ f'throw Exception("No Exception to reraise")' ]
    
def reraise(code_id, sptr, inst, inst_i, instructions, code_object ,R, **kw):
    return [f'throw code{code_id}_stack_{sptr-2}']