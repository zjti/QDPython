from func_helper import get_rhs_of_stackvar #(code_id, sptr, inst_i, instructions, R, **kw):

def unpack_sequence(code_id, sptr, inst, inst_i, instructions, code_object ,R, **kw):
    tos_tuple = get_rhs_of_stackvar(code_id, sptr - 1, inst_i, instructions, R )
    return [ f'code{code_id}_stack_{sptr-1+ inst.arg -a -1} = {tos_tuple}.__arr__[{a}]' for a in range(inst.arg)   ]
    