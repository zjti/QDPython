from func_helper import get_code_object_id, get_rhs_of_stackvar
from ops import *
import dis
from func_helper import make_func_footer,make_func_header
from func_helper import get_jump_map, is_catch_SETUP_FINALLY
from co_helper import prepare_co_consts
from flow import setup_ctrl_flow 


import ops.load_store as load_store
import ops.raise_reraise as raise_reraise
import ops.build_list_map_dict as build_list_map_dict
import ops.dup_is_format_contains as dup_is_format_contains
import ops.compare_binary_inplace as compare_binary_inplace
import ops.call_get_return as call_get_return
import ops.unpack as unpack



    
#returns (new stack_ptr , returnvalue)
op_dispatch = {
    'LOAD_CONST': lambda arg,sptr,ctx : (sptr + 1, load_store.load_const(**ctx)),
    'LOAD_GLOBAL': lambda arg,sptr,ctx : (sptr + 1, load_store.load_global(**ctx)),
    'LOAD_FAST': lambda arg,sptr,ctx : (sptr + 1, load_store.load_fast(**ctx)),
    'LOAD_DEREF': lambda arg,sptr,ctx : (sptr + 1, load_store.load_deref(**ctx)),
    'LOAD_CLASSDEREF': lambda arg,sptr,ctx : (sptr + 1, load_store.load_classderef(**ctx)),
    'LOAD_ASSERTION_ERROR' : lambda arg,sptr,ctx : (sptr + 1, load_store.load_assertion_error(**ctx)),

    'LOAD_CLOSURE': lambda arg,sptr,ctx : (sptr + 1, load_store.load_closure(**ctx)),
    'LOAD_METHOD': lambda arg,sptr,ctx : (sptr + 1, load_store.load_method(**ctx)),
    'STORE_GLOBAL': lambda arg,sptr,ctx : (sptr - 1, load_store.store_global(**ctx)),
    'STORE_FAST': lambda arg,sptr,ctx : (sptr - 1, load_store.store_fast(**ctx)),
    'STORE_DEREF': lambda arg,sptr,ctx : (sptr - 1, load_store.store_deref(**ctx)),
    
    'INPLACE_ADD': lambda arg,sptr,ctx : (sptr - 1,  compare_binary_inplace.inplace_add(**ctx)),
    'INPLACE_MULTIPLY': lambda arg,sptr,ctx : (sptr - 1, compare_binary_inplace.inplace_multiply(**ctx)),
    'INPLACE_SUBTRACT': lambda arg,sptr,ctx : (sptr - 1,compare_binary_inplace.inplace_subtract(**ctx)),
    'INPLACE_TRUE_DIVIDE': lambda arg,sptr,ctx : (sptr - 1, compare_binary_inplace.inplace_true_divide(**ctx)),
    'INPLACE_FLOOR_DIVIDE': lambda arg,sptr,ctx : (sptr - 1, compare_binary_inplace.inplace_floor_divide(**ctx)),

    'BINARY_ADD': lambda arg,sptr,ctx : (sptr - 1, compare_binary_inplace.binary_add(**ctx)),
    'BINARY_MULTIPLY': lambda arg,sptr,ctx : (sptr - 1,compare_binary_inplace.binary_multiply(**ctx)),
    'BINARY_SUBTRACT': lambda arg,sptr,ctx : (sptr - 1, compare_binary_inplace.binary_subtract(**ctx)),
    'BINARY_TRUE_DIVIDE': lambda arg,sptr,ctx : (sptr - 1, compare_binary_inplace.binary_true_divide(**ctx)),
    'BINARY_FLOOR_DIVIDE': lambda arg,sptr,ctx : (sptr - 1, compare_binary_inplace.binary_floor_divide(**ctx)),
    'BINARY_MODULO': lambda arg,sptr,ctx : (sptr - 1, compare_binary_inplace.binary_modulo(**ctx)),

    'BINARY_SUBSCR': lambda arg,sptr,ctx : (sptr - 1, compare_binary_inplace.binary_subscr(**ctx)),
    
    'MAKE_FUNCTION' : lambda arg,sptr,ctx : (sptr - (1 + (arg&8==8) + (arg&4==4)+ (arg&2==2)+(arg&1==1) ), make_function(**ctx)),
    'CALL_FUNCTION' : lambda arg,sptr,ctx : (sptr - arg, call_get_return.call_function(**ctx)),
    'CALL_FUNCTION_KW' : lambda arg,sptr,ctx : (sptr - arg - 1, call_get_return.call_function_kw(**ctx)),
    'CALL_FUNCTION_EX' : lambda arg,sptr,ctx : (sptr - 1 - (arg&1==1), call_get_return.call_function_ex(**ctx)),
    'CALL_METHOD' : lambda arg,sptr,ctx : (sptr - arg - 1, call_get_return.call_method(**ctx)),

    'POP_TOP' : lambda arg,sptr,ctx : (sptr - 1, None),
    'DUP_TOP' : lambda arg,sptr,ctx : (sptr + 1, dup_is_format_contains.dup_top(**ctx)), 
    'NOP' : lambda arg,sptr,ctx : (sptr, None),
    'COMPARE_OP' : lambda arg,sptr,ctx : (sptr - 1, compare_binary_inplace.compare_op(**ctx)),
    'CONTAINS_OP' : lambda arg,sptr,ctx : (sptr - 1, dup_is_format_contains.contains_op(**ctx)),
    'IS_OP' : lambda arg,sptr,ctx : (sptr - 1, dup_is_format_contains.is_op(**ctx)),
    
    'POP_JUMP_IF_TRUE' : lambda arg,sptr,ctx : (sptr - 1, None),
    'POP_JUMP_IF_FALSE' : lambda arg,sptr,ctx : (sptr - 1, None),
    'JUMP_FORWARD' : lambda arg,sptr,ctx : (sptr , None),
    'JUMP_ABSOLUTE' : lambda arg,sptr,ctx : (sptr , None),
    
    'BUILD_CONST_KEY_MAP': lambda arg,sptr,ctx : (sptr  - arg, build_list_map_dict.build_const_key_map(**ctx)),
    'BUILD_MAP': lambda arg,sptr,ctx : (sptr- 2*arg + 1, build_list_map_dict.build_map(**ctx)),
    'BUILD_TUPLE' : lambda arg,sptr,ctx : (sptr - arg + 1, build_list_map_dict.build_tuple(**ctx)),
    'BUILD_LIST' : lambda arg,sptr,ctx : (sptr - arg + 1, build_list_map_dict.build_list(**ctx)),
    
    'LIST_EXTEND' : lambda arg,sptr,ctx : (sptr - 1,build_list_map_dict.list_extend(**ctx)),
    'LIST_APPEND' : lambda arg,sptr,ctx : (sptr - 1,build_list_map_dict.list_append(**ctx)),
    'MAP_ADD' : lambda arg,sptr,ctx : (sptr - 2, build_list_map_dict.map_add(**ctx)),
    'DICT_MERGE' : lambda arg,sptr,ctx : (sptr - 1, build_list_map_dict.dict_merge(**ctx)),
    'DICT_UPDATE' : lambda arg,sptr,ctx : (sptr - 1, build_list_map_dict.dict_update(**ctx)),
    'UNPACK_SEQUENCE' : lambda arg,sptr,ctx : (sptr + arg -1, unpack.unpack_sequence(**ctx)),
    
    'GET_ITER': lambda arg,sptr,ctx : (sptr ,call_get_return.get_iter(**ctx)),
    'FOR_ITER': lambda arg,sptr,ctx : (sptr + 1, None),
    
    'RETURN_VALUE': lambda arg,sptr,ctx : (sptr-1, call_get_return.return_value(**ctx)),

    
    'SETUP_FINALLY': lambda arg,sptr,ctx : (sptr , None),
    'POP_BLOCK': lambda arg,sptr,ctx : (sptr , None),
    'POP_EXCEPT': lambda arg,sptr,ctx : (sptr , None),
    'RERAISE': lambda arg,sptr,ctx : (sptr -1 , raise_reraise.reraise(**ctx)),
    'RAISE_VARARGS': lambda arg,sptr,ctx : (sptr - arg , raise_reraise.raise_varargs(**ctx)),
    'JUMP_IF_NOT_EXC_MATCH':lambda arg,sptr,ctx : (sptr - 2 , None),
    
    'DELETE_FAST': lambda arg,sptr,ctx : (sptr , todo(**ctx)),
    
    'LOAD_BUILD_CLASS': lambda arg,sptr,ctx : (sptr + 1 , load_store.load_build_class(**ctx)),
    'LOAD_NAME': lambda arg,sptr,ctx : (sptr + 1 , load_store.load_name(**ctx)),
    'LOAD_ATTR': lambda arg,sptr,ctx : (sptr  , load_store.load_attr(**ctx)),
    'STORE_NAME': lambda arg,sptr,ctx : (sptr - 1 , load_store.store_name(**ctx)),
    'STORE_ATTR': lambda arg,sptr,ctx : (sptr - 2 , load_store.store_attr(**ctx)),
    'STORE_SUBSCR': lambda arg,sptr,ctx : (sptr - 3 , load_store.store_subscr(**ctx)),
    
    'FORMAT_VALUE': lambda arg,sptr,ctx : (sptr - (arg&4==4) , dup_is_format_contains.format_value(**ctx)),
    'BUILD_STRING': lambda arg,sptr,ctx : (sptr - arg + 1 , build_list_map_dict.build_string(**ctx)),

}


def make_function(code_id, sptr, inst, inst_i, instructions, code_object, debug ,**kw):
    
    qualname = code_object.co_consts[instructions[inst_i-1][0].arg]
    new_code_object = code_object.co_consts[instructions[inst_i-2][0].arg]
    
    new_co_const_helper, new_const_defs = prepare_co_consts(new_code_object)
    
    # remove qualname and new_code from stack :
    get_rhs_of_stackvar(code_id,sptr-1, inst_i, instructions, kw['R'])
    get_rhs_of_stackvar(code_id,sptr-2, inst_i, instructions, kw['R'])
    
    cells=[]
    n = 2
    if inst.arg & 8 == 8:
        n+=1
        
        cells = get_rhs_of_stackvar(code_id,sptr-n, inst_i, instructions,  kw['R'], skip_new_statement=False)

        cells = cells.split('[')[1]
        cells = cells.split(']')[0]
        cells = cells.split(',')
        pass
        #cells
        
    if inst.arg & 4 == 4:
        #default_anotations 
        pass
    if inst.arg & 2 == 2:
        n+=1
        default_kw = get_rhs_of_stackvar(code_id,sptr-n, inst_i, instructions, kw['R'])
        
        print('dkw',n, default_kw)


    if inst.arg & 1 == 1:
        n+=1
        default_pos = get_rhs_of_stackvar(code_id,sptr-n, inst_i, instructions, kw['R'])
        print('dp',n, default_pos)
         
    R = kw['R']
    Rn,_,_ = co2js(new_code_object,cells = cells, qualname=qualname, debug=debug)
    R += Rn
    new_code_id = get_code_object_id(new_code_object)
    
    has_varargs = new_code_object.co_flags & 4 == 4
    has_kwargs = new_code_object.co_flags & 8 == 8
    
    argc = new_code_object.co_argcount + has_varargs + has_kwargs 
    argc += new_code_object.co_posonlyargcount + new_code_object.co_kwonlyargcount
  
    
    R += [f'code{new_code_id}.has_varargs = { ("true" if has_varargs else "false") }']
    R += [f'code{new_code_id}.has_kwargs = {("true" if has_kwargs else "false")}']
    R += [f'code{new_code_id}.argcount = {new_code_object.co_argcount }']
    if len(new_co_const_helper)>0:
        R += [f'code{new_code_id}.__doc__ = {new_co_const_helper[0]}']
    
    # cells_name = [f'"{c}"' for c in cells]
    # cells_name_cells = [f'"{c}":{c}' for c in cells]
    # R += [f'code{code_id}.cells = {{ {",".join(cells_name_cells)} }}']
    if inst.arg & 1 == 1:
        R += [f'code{new_code_id}.default_pos = {default_pos}'] 
    if inst.arg & 2 == 2:
        R += [f'code{new_code_id}.default_kw = {default_kw}'] 
    
    argnames=list(new_code_object.co_varnames[:argc])
    #.0 fix:
    argnames = [l.replace('.0','dot0') for l in argnames] 

    # R += [f'code{new_code_id}.argnames = new pytuple({argnames})']
    R += [f'code{new_code_id}.argnames = {argnames}']
    R += [f'code{new_code_id}.__class__ = "function"']
    
    # R += [f'code{new_code_id}.default_arg_map = new pydict( {default_arg_map} )']
    R += [f'code{code_id}_stack_{sptr-n} = code{new_code_id}']
    
    print(qualname, new_code_object)
    return []

def todo(inst,**kw):
    print(inst.opname, 'todo')

def load_build_class(code_id, sptr, inst, inst_i, instructions, code_object ,**kw):
    return []

def co2js(code_object, R=None,cells=None,qualname='__main__', debug=True):
    
    if R is None:
        R = []
    
    
    co_const_helper, const_defs = prepare_co_consts(code_object)

    code_id = get_code_object_id(code_object)
    
    # instructions[i] = ints_i : [inst, [produced_lines_in_R], sptr ]
    instructions = [[inst, [], -1] for inst in dis.get_instructions(code_object)]
    
    code_ctx = {'co_const_helper':co_const_helper,'instructions':instructions, 'code_object':code_object, 'R':R}
    code_ctx['add_lines'] = {i:[] for i,_ in  enumerate(dis.get_instructions(code_object))}
    code_ctx['code_id']= code_id
    code_ctx['R']= R
    sptr = 0
    
    sptr_xtra = {}
    
    for inst_i,inst in enumerate(dis.get_instructions(code_object)):
        code_ctx['inst_i'] = inst_i
        code_ctx['inst'] = inst
       
        if inst.opname == 'SETUP_FINALLY':
            sptr_xtra[ inst_i + inst.arg + 1] = sptr+3
        if inst.opname == 'JUMP_IF_NOT_EXC_MATCH':
                sptr_xtra[ inst.arg ] = sptr-2
        if inst.opname == 'FOR_ITER':
            sptr_xtra[ inst_i + inst.arg + 1] = sptr-1
        if inst_i in sptr_xtra:  
            sptr = sptr_xtra[inst_i]
            
            
        code_ctx['sptr'] = sptr
        code_ctx['qualname'] = qualname
        code_ctx['debug'] = debug
        
        # if inst_i in code_ctx['add_lines']:
        #     for l in code_ctx['add_lines'][inst_i] :
        #         R.append(l)
        
        instructions[inst_i][2] = sptr
        
        mod_lines_start = len(R)
        R.append(f'// inst_{inst_i} : {inst.opname}({inst.arg})  (sptr:{sptr})')
        
        if inst.opname in op_dispatch:
            sptr , new_lines = op_dispatch[inst.opname]( inst.arg, sptr, code_ctx)
        else:
            raise Exception(f'{inst.opname} not implemented')
        
        if new_lines:
            R += new_lines
         
        # sptr = ops_stack_mvmt[inst.opname](inst.arg,sptr)
         
        instructions[inst_i][1] = list(range(mod_lines_start,len(R)))
    
    R = setup_ctrl_flow(R, instructions, code_object, code_id)

    return add_rest(R,instructions,code_object, cells, qualname ,debug)
 

def add_rest(R,instructions,code_object, cells, qualname, debug):
    #add function header and footer
    co_const_helper, const_defs = prepare_co_consts(code_object)

    Rtotal = []
    Rtotal+= make_func_header(code_object, cells, qualname, debug)
    Rtotal += const_defs
    Rtotal += R
    Rtotal += make_func_footer(code_object, qualname)

    #.0 fix:
    Rtotal = [l.replace('_locals_.0','_locals_dot0') for l in Rtotal] 
    return Rtotal, instructions, code_object