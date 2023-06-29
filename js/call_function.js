function js_call_function(){
    var func = arguments[0] 
    var args_resolved = []
    
    // check if its not a py function and call directly
    if (typeof func.has_kwargs == 'undefined'){
        for (var i = 1; i < arguments.length; i++) {
            args_resolved.push(arguments[i])
        }
        // print('here',args_resolved)
        return func(...args_resolved )
    }
    
    var varargs = []
    for (var i = 1; i < arguments.length; i++) {
        if (args_resolved.length < func.argcount){
            args_resolved.push(arguments[i])
        }else{
            varargs.push(arguments[i])
        }
    }
    if (args_resolved.length < func.argcount){
        m =  func.argcount - args_resolved.length
        n = func.default_pos.__arr__.length
        for (var i = 0; i < m; i++) {
            // print(func.default_pos,n-m+i)
            args_resolved.push(func.default_pos.__arr__[n-m+i])
        }
    }
    
    if (func.default_kw){
        for (let [key, value] of func.default_kw.__map__) {
             args_resolved.push(value);
        }
    }
    
    if (func.has_varargs){
        args_resolved.push(new pytuple(varargs))
    }
     
    if (func.has_kwargs){
        args_resolved.push(new pydict(new Map()))
    }
    // print('AAA',new pylist(args_resolved))
    return func(...args_resolved)
}

function js_call_function_kw(){
    var func = arguments[0] 
    var args_resolved = []
    
    // check if its not a py function and call directly
    if (typeof func.has_kwargs == 'undefined'){
        for (var i = 1; i < arguments.length; i++) {
            args_resolved.push(arguments[i])
        }
        return func(...args_resolved )
    }
    
    var name_tuple = arguments[1]
    // print(name_tuple)
    // console.log(name_tuple)
    var num_kw = name_tuple.__arr__.length
    
    //print('...')
    var varargs = []
    for (var i = 2; i < arguments.length - num_kw; i++) {
        if (args_resolved.length < func.argcount){
            args_resolved.push(arguments[i])
        }else{
            varargs.push(arguments[i])
        }
    }
    if (args_resolved.length < func.argcount){
        m =  func.argcount - args_resolved.length
        n = func.default_pos.__arr__.length
        for (var i = 0; i < m; i++) {
            args_resolved.push(func.default_pos.__arr__[n-m+i])
        }
    }
    if (func.default_kw){
        for (let [key, value] of func.default_kw.__map__) {
            args_resolved.push(value);
        }
    }
     
    
    if (func.has_varargs){
        args_resolved.push(new pytuple(varargs))
    }
    
    var kw_map = new Map()
    for (var i = 0; i < num_kw; i++) {
        var key = name_tuple.__arr__[i];
        var ki = func.argnames.indexOf(key)
        if (ki == -1){
            kw_map.set(key, arguments[arguments.length-num_kw+i])
        }else{
            args_resolved[ki] = arguments[arguments.length-num_kw+i]
        }
    }
     
    if (func.has_kwargs){
        // console.log(kw_map)
        // print(new pydict(kw_map))
        args_resolved.push(new pydict(kw_map))
    }
    // print(new pylist(args_resolved))
    return func(...args_resolved)
}

function js_call_function_ex(func, pos_args, kw_args){
    
  
    // check if its not a py function and call directly
    var args_resolved = []
    if (typeof func.has_kwargs == 'undefined'){
        for (var i = 1; i < arguments.length; i++) {
            args_resolved.push(arguments[i])
        }
        return func(...args_resolved )
    }
    var dp_map = []
    if (func.default_pos){
        
        var j = 0;
        
        // print(func.argcount, func.default_pos.__arr__.length)
        for (var i = 0 ; i < func.argcount; i++){
            if (i >= func.argcount - func.default_pos.__arr__.length){
                dp_map.push( [func.argnames[i] , func.default_pos.__arr__[j]] );
                j++;
            }else{
                dp_map.push( [func.argnames[i] , None] );
            }

        }
    }else{
       for (var i = 0 ; i < func.argcount; i++){
            dp_map.push( [func.argnames[i] , None] );
       }
    }
    n_default_arg_map = new pydict( dp_map )


    if (func.default_kw){
        n_default_arg_map.__map__ = new Map([...n_default_arg_map.__map__,...func.default_kw.__map__])
    }

    
    var vararg_name,kwarg_name;
    if (func.has_kwargs){
        kwarg_name = func.argnames[ func.argnames.length-1]   
    }
    if (func.has_varargs){
        if (func.has_kwargs){
            vararg_name = func.argnames[ func.argnames.length-2]   
            n_default_arg_map.__setitem__(vararg_name, new pylist([]));
            n_default_arg_map.__setitem__(kwarg_name, new pydict([]));
        }else{
            vararg_name = func.argnames[ func.argnames.length-1]   
            n_default_arg_map.__setitem__(vararg_name, new pylist([]));
        }
        
    }
    

    
    for (var i = 0; i < pos_args.__arr__.length; i++){
        if (i < func.argcount){
            n_default_arg_map.__setitem__(func.argnames[i], pos_args.__arr__[i])
        }else{
            n_default_arg_map.__getitem__(vararg_name).append(pos_args.__arr__[i])
        }
    }
    n_default_arg_map.__setitem__(vararg_name, new pytuple(n_default_arg_map.__getitem__(vararg_name).__arr__))
    
    for (let [key, value] of kw_args.__map__) {
        if ( n_default_arg_map.__map__.has(key)){
             n_default_arg_map.__setitem__(value[0],value[1])
        }else{
             n_default_arg_map.__getitem__(kwarg_name).__setitem__(value[0],value[1])
        }
    }
    
    for (let [key, value] of n_default_arg_map.__map__) {
             args_resolved.push(value[1])
    }
    
    return func(...args_resolved)

}
