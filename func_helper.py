code_2_num = dict()

import dis
from flow import find_handler_end


def get_code_object_id(code_object):
    if code_object not in code_2_num:
        code_2_num[code_object] = len(code_2_num)
    return code_2_num[code_object]

def get_rhs_of_stackvar(code_id, sptr, inst_i, instructions, R, remove_old_line= True, skip_new_statement= True,**kw ):
    
    var = f'code{code_id}_stack_{sptr}'
    
    for inst,lines_mod,_ in instructions[:inst_i][::-1]:
        if len(lines_mod)>0:
            # check only last line:
            # if R[lines_mod[-1]].split('=')[0].strip() == var:
            #     R[lines_mod[-1]] = f'//(removed by inst_{inst_i} ) ' + R[lines_mod[-1]]
            
            for line_n in lines_mod[::-1]:
                if R[line_n].split('.')[0].strip() == var:
                    return var
                if '[' in R[line_n].split('=')[0] :
                    if var in R[line_n].split('=')[0] :
                        return var
                
                # if '=' in R[line_n]:
                #     if '?' in R[line_n].split('=')[1] :
                #         if var in R[line_n].split('=')[0] :
                #             return var
                 
                if R[line_n].split('=')[0].strip() == var:
                    if skip_new_statement:
                        if 'new ' in  R[line_n].split('=')[1]:
                            return var
                    if remove_old_line:
                        R[line_n] = f'//(removed by inst_{inst_i} ) ' + R[line_n]
                    return R[line_n].split('=', 1)[1].strip()
        if inst.is_jump_target or 'JUMP' in inst.opname:
            return var
            
    return var

def is_catch_SETUP_FINALLY(inst_i,instructions, code):
    """
    at inst_i is a SETUP_FINALLY.
    is it a try/final or a try/catch ???
    """
    if instructions[inst_i][0].opname != 'SETUP_FINALLY':
        raise Exception('no SETUP_FINALLY')
    handler_start = inst_i + instructions[inst_i][0].arg + 1
    handler_end = find_handler_end(code,handler_start)
    print(handler_start,handler_end)
    for inst,_,_ in instructions[handler_start:handler_end ]:
        if inst.opname == 'POP_EXCEPT':
            print('catch_block')
            return True
    print('NOcatch_block')
    return False
    

def get_jump_map(code_object, instructions):
    d = {}
    for inst_i,(inst,_,sptr) in enumerate(instructions):
        trg = inst_i + 1
        if 'JUMP' in inst.opname:
            if 'JUMP_FORWARD' == inst.opname:
                trg = inst_i + inst.arg + 1
            else:
                trg = inst.arg 

        if 'FOR_ITER' == inst.opname:
            trg = inst_i + inst.arg 
            
        if 'SETUP_FINALLY' == inst.opname:
            trg = inst_i + inst.arg + 1
        
        if trg != inst_i+1:
            d[inst_i] = (trg, inst.opname, sptr)

    return d

def make_func_header(code_object, cells, qualname ,debug):
    code_id = get_code_object_id(code_object)
    R = []
    
    for i in range(len(code_object.co_freevars)):
        R += [f'var code{code_id}_freevars_{code_object.co_freevars[i]}= {cells[i]};']
    for i in range(len(code_object.co_cellvars)):
        R += [f'var code{code_id}_cellvars_{code_object.co_cellvars[i]} = [undefined];']
    
    has_varargs = code_object.co_flags & 4 == 4
    has_kwargs = code_object.co_flags & 8 == 8
    argc = code_object.co_argcount + has_varargs + has_kwargs 
    argc += code_object.co_posonlyargcount + code_object.co_kwonlyargcount
    
    
    argstring = ','.join( [f' code{code_id}_locals_{varname}' for varname in code_object.co_varnames[:argc]] )
    R += [f'function code{code_id}( {argstring} ) {{ ']
    
    if debug:
        R += [f'console.log("enter function code{code_id}, {qualname}"); '] 
    
    
    non_arg_locals = ','.join([f' code{code_id}_locals_{varname}' for varname in code_object.co_varnames[argc::] ])
    if non_arg_locals:
        R+= [f'var {non_arg_locals} ;']
    
    stack_vars = ','.join([f' code{code_id}_stack_{i}' for i in range(code_object.co_stacksize) ])
    if stack_vars:
        R+= [f'var {stack_vars} ;']
    
    R+= ['var error;'] 
    R+= [f'code{code_id}_instr_ptr = 0;'] 
    return R

def make_func_footer(code_object, qualname):
    code_id = get_code_object_id(code_object)
    return [f'}} // end function code{code_id} ']
