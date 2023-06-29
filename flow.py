import dis

def find_handler_end(code, handler_start):
    min_end = handler_start
    end = -99
    for inst_i, inst in list(enumerate(dis.get_instructions(code)))[handler_start:]:
        if inst_i < min_end:
            continue
        if inst.opname == 'JUMP_IF_NOT_EXC_MATCH':
            min_end = inst.arg
            
        if inst.opname == 'SETUP_FINALLY':
            min_end = find_handler_end(code, inst_i + inst.arg + 1)
        
        if inst.opname == 'POP_EXCEPT':
            end = inst_i
            break
        if inst.opname == 'RERAISE':
            end = inst_i
            break
    
    
    return end

def find_block_end(code, block_start):
    
    c=-1
    max_end=-1
    # print('bs',block_start)
    for inst_i, inst in list(enumerate(dis.get_instructions(code)))[block_start:]:
        if inst_i == max_end:
            return max_end 
        
        
        if inst.opname == 'SETUP_FINALLY':
            if inst_i == block_start:
                max_end = inst_i + inst.arg 
            c+=1
            
        if inst.opname == 'POP_BLOCK': 
            if c==0: 
                return inst_i
            c-=1
            
            
        
    raise Exception('NO block end ',block_start)

jump_ops = ['POP_JUMP_IF_TRUE','POP_JUMP_IF_FALSE','JUMP_FORWARD','JUMP_ABSOLUTE', 'JUMP_IF_NOT_EXC_MATCH']
def analyze_flow(code):
    blocks,handler, jumps = [],[],[]
    for inst_i, inst in enumerate(dis.get_instructions(code)):
        handler += [[]]
        blocks += [[]]
        jumps += [(None,None)]
        
    for inst_i, inst in enumerate(dis.get_instructions(code)):
        if inst.opname in jump_ops: 
            trg = inst.arg
            if inst.opname == 'JUMP_FORWARD':
                trg += inst_i + 1
                
        if inst.opname == 'FOR_ITER':
            jumps[inst_i] = ('for',inst_i + inst.arg + 1)
        
    for inst_i, inst in enumerate(dis.get_instructions(code)):
        
        if inst.opname == 'SETUP_FINALLY':
            h_start = inst.arg + inst_i + 1
            
            block_end = find_block_end(code,inst_i)
            # print(block_end)
            for i in range(inst_i, block_end+1):
                blocks[i] += [h_start]
                
  
            h_start = inst.arg + inst_i + 1
            h_end = find_handler_end(code, h_start)
            # print('h',h_start,h_end)
            for i in range(h_start, h_end+1):
                handler[i] += [h_start] 
                
        if inst.opname in jump_ops: 
            trg = inst.arg
                
            if inst.opname == 'JUMP_FORWARD':
                trg += inst_i + 1
            
            if inst.opname == 'POP_JUMP_IF_TRUE':
                cond = 'true'
            elif inst.opname == 'POP_JUMP_IF_FALSE':
                cond = 'false'
            elif inst.opname == 'JUMP_IF_NOT_EXC_MATCH' :
                cond = 'not_exc_match'
            else:
                cond = 'NO' 
            
            jumps[inst_i] = (cond,trg)
            
    for inst_i,(cond,trg) in enumerate(jumps):
        if cond is None:
            continue
        if  trg < inst_i:
            conti = False
            for cond2,trg2 in jumps[inst_i+1:]:
                if trg2 is not None:
                    if trg2 < inst_i:
                        conti = True
            if conti:
                cond += '/continue'
            else:
                if 'for' not in jumps[trg]:
                    cond += '/while'
                    jumps[trg] = ('do',inst_i)
                else:
                    cond = 'endfor'
            jumps[inst_i] = (cond,trg)


    for inst_i,(cond,trg) in enumerate(jumps):
        if cond is None:
            continue
        if  trg > inst_i:
            is_break = False
            for inst_i2,(cond2,trg2) in list(enumerate(jumps))[inst_i+1:trg]:
                if trg2 is None:
                    continue
                if 'do' in cond2: 
                    is_break -= 1
                if 'while' in cond2: 
                    is_break += 1
                 
                    
            if is_break > 0:
                cond += '/break'
            jumps[inst_i] = (cond,trg)
 
    for inst_i,(cond,trg) in enumerate(jumps):
        if cond is None:
            continue
        if 'continue' in cond or 'break' in cond:
                continue
        if  trg > inst_i:
            is_ugly = False
            for inst_i2,(cond2,trg2) in list(enumerate(jumps))[:trg]:
                if trg2 is None:
                    continue
                if 'continue' in cond2 or 'break' in cond2:
                    continue
                if  inst_i2 < inst_i and trg2 > inst_i and trg2 < trg:
                    # print(inst_i,inst_i2,9)
                    is_ugly=True
                
                if  inst_i2 > inst_i and trg2 > trg:
                    # print(inst_i,inst_i2)
                    is_ugly=True
                 
                    
            if is_ugly:
                cond += '/ugly'
            jumps[inst_i] = (cond,trg)
      
    # for i,he in enumerate(handler):
    #     print(f'{i:3d}',blocks[i],handler[i],jumps[i])
    
    n_blocks = []
    
    for inst_i,b  in enumerate(blocks):
        if len(b) > 0:
            h_extra = None
            b_extra = None
                
            if inst_i == 0:
                h_start = b[0]
                h_end = find_handler_end(code, h_start)
                b_start = inst_i
                b_end = find_block_end(code,inst_i)
                n_blocks += [(h_start,h_end,h_extra,b_start,b_end,b_extra)]
            else:
                
                if len(b) == len( blocks[inst_i-1]) + 1:
                    h_start = b[-1]
                    h_end = find_handler_end(code, h_start)
                    if len(blocks[h_start] ) > 0:
                        h_extra = blocks[h_start][-1]
                    
                    b_start = inst_i
                    b_end = find_block_end(code,inst_i)
                    if len(blocks[inst_i] ) > 1:
                        b_extra = blocks[inst_i][-2]
                    n_blocks += [(h_start,h_end,h_extra,b_start,b_end,b_extra)]
                    
                
        
    return n_blocks,jumps  

def setup_ctrl_flow(R,instructions,code_object,code_id):

    add_pre_lines = {k:[] for k in range(len(instructions)+1)}
    add_post_lines = {k:[] for k in range(len(instructions)+1)}
    
    n_blocks,jumps = analyze_flow(code_object)
    
    j_blocks = []
    for (h_start,h_end,h_extra,b_start,b_end,b_extra) in n_blocks:
        add_pre_lines[b_start] += ['}try{']
        add_pre_lines[b_start] += [f'if(code{code_id}_instr_ptr <= {b_start} ){{']
        
        _,_,sptr = instructions[h_start]
        catchop = f'if (err instanceof js.ReferenceError){{ err = NameError(err.message)}}'
        catchop += f'if (err instanceof js.Error){{ err = Exception(err.message)}}'
        catchop += f'if( err.__class__ == "type") {{err=err();}} ;'
        catchop += f'code{code_id}_stack_{sptr-1} = err.__class__ ;'
        catchop += f'code{code_id}_stack_{sptr-2} = err '
        n = [f'}} }}catch(err){{ {catchop}; code{code_id}_instr_ptr = {h_start} }} // {b_end}']
        n += [f' if(code{code_id}_instr_ptr <= {b_end} ){{']
        n += [' ']
        add_post_lines[b_end] = n + add_post_lines[h_start] 
        
        
        
        if b_extra != h_extra:
            print("EXTRA")
            if b_extra:
                add_pre_lines[h_start] += ['}try{']
                add_pre_lines[h_start] += [f'if(code{code_id}_instr_ptr <= {h_start} ){{ //extra']

                n = [f'}} }}catch{{  {catchop}; code{code_id}_instr_ptr = {b_extra} }} ']
                n += [f' if(code{code_id}_instr_ptr <= {b_extra} ){{ // extra']
                n += [' ']
                add_post_lines[b_end] = n + add_post_lines[h_start] 
        
        add_pre_lines[h_start] += [f' }}if(code{code_id}_instr_ptr <= {h_start} ){{ ']
        
    # print(n_blocks)
    
    
    for inst_i,(cond,trg) in enumerate(jumps):
        if cond:
            j_blocks += [(cond,inst_i,trg)]
        
    
    for cond , start,trg in j_blocks:
        _,_,sptr = instructions[start]

        if 'NO' in cond:
            cond_v =  'true'
        elif 'true' in cond: 
            cond_v = f'bool( code{code_id}_stack_{sptr-1} ) '
        elif 'false' in cond: 
            cond_v = f'!bool( code{code_id}_stack_{sptr-1} ) '
        elif 'not_exc_match' in cond: 
            cond_v = f'!issubclass( code{code_id}_stack_{sptr-2},code{code_id}_stack_{sptr-1} ) '
            
        
        
        if 'do' in cond:
            add_pre_lines[start] =  [f'}} if(code{code_id}_instr_ptr <= {start} ){{ do{{  {{code{code_id}_instr_ptr = {start}'] + add_pre_lines[start] 
        elif 'while' in cond:
            
            add_pre_lines[start] +=  [f'}}  }}while( {cond_v} )']
            
                
            add_pre_lines[start] += [f'}}if(code{code_id}_instr_ptr <= {start} ){{']
        elif 'continue' in cond:
            add_pre_lines[start] += [f'}}if(code{code_id}_instr_ptr <= {start} && {cond_v} ){{continue}}{{']
        elif 'break' in cond:
            add_pre_lines[start] += [f'}}if(code{code_id}_instr_ptr <= {start} && {cond_v} ){{break}}{{']
        elif 'for' in cond:
            if 'endfor' in cond:
                add_pre_lines[start] += [f'}} }} }}if(code{code_id}_instr_ptr <= {start}){{ ']
            else:
                n = [f'}}if(code{code_id}_instr_ptr <= {start} ){{ for(code{code_id}_stack_{sptr} of code{code_id}_stack_{sptr-1}  ){{   ']
                n += [f'{{code{code_id}_instr_ptr = {start}',' ', ]
                add_pre_lines[start] = n + add_pre_lines[start]
        else:
            add_pre_lines[start] += [f'}}if(code{code_id}_instr_ptr <= {start} && {cond_v} ){{ code{code_id}_instr_ptr = {trg}  }}']
            add_pre_lines[start] += [f'if(code{code_id}_instr_ptr <= {start} ){{ ']

            if trg not in [i for i,(cond,trg) in enumerate(jumps) if cond ]:
                
                add_pre_lines[trg] += [f'}}if(code{code_id}_instr_ptr <= {trg} ){{']
                
        
        
        
    F = [] 
    
    F += ['{']
    for inst_i,(_,lines,_) in enumerate(instructions):
        F += add_pre_lines[inst_i]
        F += [R[li] for li in lines]
        F += add_post_lines[inst_i]
    
    F += add_pre_lines[inst_i+1]
    F += ['}']
    

    return F