from func_helper import get_rhs_of_stackvar #(code_id, sptr, inst_i, instructions, R, **kw):

def get_iter(code_id,sptr,inst, code_object , inst_i, instructions, R,**kw): 
    tos = get_rhs_of_stackvar(code_id,sptr-1, inst_i, instructions, R)
    
    return [f'code{code_id}_stack_{sptr-1} = {tos}.__iter__()' ]

def call_function(code_id, sptr, inst, inst_i, instructions, code_object ,R ,**kw):
        
    func = get_rhs_of_stackvar(code_id,sptr-inst.arg -1 ,inst_i, instructions,R)
    args = ', '.join([get_rhs_of_stackvar(code_id,sptr-inst.arg+i ,inst_i, instructions, R ,skip_new_statement=False) for i in range(inst.arg)])
    
    stack_res = f'code{code_id}_stack_{sptr-inst.arg-1}'
    if func.startswith('code') and not '_' in func:
        r = f'{stack_res} = {func}( {args} )'
        return [r]
    
    if func == '__qdp__super__':
        
        r = f'{stack_res} = __qdp__super__( arguments[0] , code{code_id}_freevars___class__ ,  {args} )'
        return [r]
        
    r = f'{stack_res} = js_call_function({func}, {args})'

    return [r]

def call_function_kw(code_id, sptr, inst, inst_i, instructions, code_object ,R ,**kw):
        
    func = get_rhs_of_stackvar(code_id,sptr-inst.arg -2 ,inst_i, instructions,R)
    args = ', '.join([get_rhs_of_stackvar(code_id,sptr-inst.arg-1+i ,inst_i, instructions,R) for i in range(inst.arg)])
    name_tuple = get_rhs_of_stackvar(code_id,sptr-1 ,inst_i, instructions,R)
    r = f'code{code_id}_stack_{sptr-inst.arg-2} = js_call_function_kw({func},{name_tuple},{args} )'
    return [r]

def call_function_ex(code_id, sptr, inst, inst_i, instructions, code_object ,R ,**kw):
    
    if inst.arg & 1 == 0:
        func = get_rhs_of_stackvar(code_id,sptr-2 ,inst_i, instructions,R)
        pos_args_tuple = get_rhs_of_stackvar(code_id,sptr-1 ,inst_i, instructions,R)
        name_dict = 'dict()'

        r = f'code{code_id}_stack_{sptr-2} = js_call_function_ex({func},{pos_args_tuple},{name_dict} )'
    else:
        func = get_rhs_of_stackvar(code_id,sptr-3 ,inst_i, instructions,R)
        pos_args_tuple = get_rhs_of_stackvar(code_id,sptr-2 ,inst_i, instructions,R)
        name_dict = get_rhs_of_stackvar(code_id,sptr-1 ,inst_i, instructions,R)

        r = f'code{code_id}_stack_{sptr-3} = js_call_function_ex({func},{pos_args_tuple},{name_dict} )'
    return [r]

def call_method(code_id, sptr, inst, inst_i, instructions, code_object ,R ,**kw):
    
    args = []
    for i in range(inst.arg+1):
        args += [get_rhs_of_stackvar(code_id,sptr-1 -inst.arg + i ,inst_i, instructions,R)]
  
    
    r = f'code{code_id}_stack_{sptr-2 - inst.arg} = (code{code_id}_stack_{sptr-1 - inst.arg})?(code{code_id}_stack_{sptr-2 - inst.arg} ({",".join(args)})):'
    r += f'(code{code_id}_stack_{sptr-2 - inst.arg} ({",".join(args[1:])}))'
    return [r]
    
def return_value(code_id, sptr, inst, inst_i, instructions, code_object ,R ,debug, **kw):
    if debug:
        r = [f"console.log(\"return from code{code_id} , {kw['qualname']}\")",
            f"return {  get_rhs_of_stackvar(code_id,sptr-1, inst_i, instructions, R) }"]
    else:
        r = [f"return {  get_rhs_of_stackvar(code_id,sptr-1, inst_i, instructions, R) }"]
    return r


