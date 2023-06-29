function property(_fget=None, _fset=None, _fdel=None, _doc=None){
    
    var prop = {fget:_fget,fset:_fset,fdel:_fdel,doc:_doc } ;
    function setter(_fset){ prop.fset = _fset;return prop};
    prop.setter = setter;
    return prop
}

var bound_method_trap = {
    get(target, name) {
        if (name=='has_varargs'){return  target.__class__.__call__.has_varargs}
        if (name=='has_kwargs'){return  target.__class__.__call__.has_kwargs}
        if (name=='argcount'){return  target.__class__.__call__.argcount - 1} // bound_method_trap does insert the first argument (self)
        if (name=='argnames'){return  target.__class__.__call__.argnames.slice(1) } 
        if (name=='default_pos'){return  target.__class__.__call__.default_pos} 
        if (name=='default_kw'){return  target.__class__.__call__.default_kw} 
        if (name=='__class__'){return 'method'}
        
        return target[name]
    },
    apply(trg,thisArg,args){
        return trg.__call__(trg.__self__,...args)
    },
    
}

var super_trap ={
    get(target, name){
        
        return get_from_mro_model(target.instance, target.mro_model,name)
    },
    has(target, key) {
       return key in target.mro_model;
    }
}

function __qdp__super__(self,x){
    
    var super_instance = {instance: self , mro_model: x[0].__mro__.__arr__[1].mro_model , __class__ : x[0].__mro__.__arr__[1]}
 
    // console.log(super_instance.mro_model.hasOwnProperty('x'))
    var p = new Proxy(super_instance, super_trap)
    return p
}
// f()

var instance_trap = {
    get(target, name) {
        if (name=='get_instance_data'){return target}
        if (name=='has_varargs'){return  target.__class__.__call__.has_varargs}
        if (name=='has_kwargs'){return  target.__class__.__call__.has_kwargs}
        
        // the base for every instance is a function (see constructor_func : new_instance ), it does insert the first argument (self)
        if (name=='argcount'){return  target.__class__.__call__.argcount - 1} 
        if (name=='argnames'){return  target.__class__.__call__.argnames.slice(1) } 
        if (name=='default_pos'){return  target.__class__.__call__.default_pos} 
        if (name=='default_kw'){return  target.__class__.__call__.default_kw} 
        
        if (target.hasOwnProperty(name)){ 
            return target[name]
        }if (name == 'hasOwnProperty'){
            return target.hasOwnProperty
        }
        // if (name == '__str__'){
        //     function s(){return '< ' + target.__class__.__name__ + ' object >'}
        //     return s
        // }
        return get_from_mro_model(target, target.__class__.mro_model, name)

        
    },
    set(target,name, value){
        if (target.__class__.hasOwnProperty(name)){ 
            if (typeof target.__class__[name].fget == 'function'){
                // is property : 
                if (typeof target.__class__[name].fset == 'function'){
                    v = target.__class__[name].fset( target, value );
                }else{
                    throw Error("can't set property :", name)
                }
            }else{
                target[name] = value;
            }    
        }else{
            target[name] = value;
        }
        
        
    }
}

function get_from_mro_model( target, mro_model,name ){
    if (name in mro_model){
        if (typeof mro_model[name].fget == 'function'){
            // is property
            return mro_model[name].fget( target )
        }
        if (typeof mro_model[name]  == 'function'){
            // is it class, instance or method?
            // print('ismethod?')

            if (mro_model[name].__class__  == 'function'){
                // is method
                // print('ismethod')
                var bound_method = function(){};
                bound_method.__self__ = target;
                bound_method.__call__ = mro_model[name]
                return new Proxy(bound_method, bound_method_trap)
            }
        }
        return mro_model[name]
    }
}

var class_trap = {apply:function(trg,thisArg,args){return trg.constructor_func(...args)},
                get:function(trg,name){
                    // print('N:',name)
                    if (name=='__class__'){return 'type'}
                    if (name=='has_varargs'){return  trg.mro_model.__init__.has_varargs}
                    if (name=='has_kwargs'){return  trg.mro_model.__init__.has_kwargs}
                    if (name=='argcount'){
                        return  trg.mro_model.__init__.argcount - 1} // constructor_function does insert the first argument (self)
                    if (name=='argnames'){return  trg.mro_model.__init__.argnames.slice(1)} 
                    if (name=='default_pos'){return  trg.mro_model.__init__.default_pos} 
                    if (name=='default_kw'){return  trg.mro_model.__init__.default_kw} 
                    
                    if (name == '__str__'){
                        function s(){return '<class ' + trg.__name__ + ' >'}
                        return s
                    }
                    if (name=='mro_model'){return  trg.mro_model} 
                    return trg.mro_model[name]
                    // return trg[name]
                },
                has(trg, key) {
                    return key in trg.mro_model;
                },
                set:function(trg,name,value){
                    //update MRO_model
                    trg[name] = value
                    trg.mro_model.update(name,value)
                }
                
                
}

function build_mro_model(base_classes, cur_class){
    var mro_model = {child_classes:[] }
    
    mro_model.__mro__ = []
    mro_model.update = function(name,value){
        print('update;')
        this[name]=value
        for (child of this.child_classes){
            if (name in child){
                // name is implemeted in child_class
            }else{
                // add name to mro:
                child.mro_model.update(name,value)
            }
        }
    }
    for (member of Object.keys(cur_class)){
        mro_model[member] = cur_class[member]
    }
    
    
    for (base of base_classes){
        mro_model.__mro__ =  mro_model.__mro__.concat(base.__mro__.__arr__)
        base.mro_model.child_classes.push(cur_class) // make weakref instead soon
        
        for (member of Object.keys(base.mro_model)){
            if (!(member in mro_model)){
                mro_model[member] = base.mro_model[member]
                // print(member,'======')
            }
        }
            
    }
    
    
    return mro_model
}

function js_build_class(){
    // print('build_class',arguments.length)
    
    var base_classes = []
    for (var i = 0; i < arguments.length;i++){
        // if (i != arguments.length-1){
        //     print('-',arguments[i], arguments[i].argcount)
        // }else{
        //     print('->',arguments[i])
        // }
        if (i >= 2){
            base_classes.push(arguments[i])
        }
    }
    
    var class_obj = arguments[0]
    class_obj.__name__ = arguments[1]
    
    // call the class body, it may return __class__ cellvaribale. (aka __classcell__) 
    var __classcell__ = class_obj()
    
     
    class_obj.mro_model = build_mro_model(base_classes,class_obj)
    
    if(!class_obj.mro_model.hasOwnProperty('__init__')){
        // add default constructor
        class_obj.mro_model.__init__ = function(){}
        class_obj.mro_model.__init__.has_kwargs=undefined
    }
    
    
    var class_with_constructor = new Proxy(class_obj, class_trap)
    class_obj.mro_model.__mro__ = new pylist( [class_with_constructor].concat(class_obj.mro_model.__mro__))
    
    //store current class object in __classcell__
    if (__classcell__ != null){
        __classcell__[0] = class_with_constructor
    }
     
    var constructor_func = function(){
        // new instance might be callable (so its a function):
        var new_instance = function(){ 
            // arguments.callee is the new instance
            if (arguments.callee.__class__.hasOwnProperty('__call__')){
                return arguments.callee.__class__.__call__( arguments.callee ,...arguments ); 
            }
            throw Error ('object is not callable')
        }

        new_instance.__class__= class_with_constructor
        class_obj.mro_model.__init__(new_instance,...arguments)       
        
        var new_instance_proxy = new Proxy(new_instance, instance_trap);
        
        return new_instance_proxy
    }
    class_obj.constructor_func = constructor_func
    return class_with_constructor
}

function js_load_method( obj, method_name){ 
    // print('LMM',method_name)
    // if (obj.hasOwnProperty(method_name)){
    if (method_name in obj ){
        // print('LM')
        return [obj[method_name],None]    
    }
    // if (obj.__class__.mro_model.hasOwnProperty(method_name)){
    if (method_name in obj.__class__.mro_model){
         // print('LM-M')
        // print('aaab',obj.__class__[method_name],method_name)
        return [obj.__class__.mro_model[method_name],obj]    
    }
    throw Error('load method error')
}

function isinstance(inst_trap, class_trap){
    if (class_trap.__class__ == tuple){
        for (e of class_trap.__arr__){
            if (isinstance(inst_trap,e)){
                return true
            }
        }
    }else{
        if (inst_trap.__class__ == class_trap){
            return true;
        }
        if (inst_trap.__class__.__mro__.__arr__.includes(class_trap)){
            return true;
        }
    }
    return false;
}

function issubclass(class_trap_child,class_trap_parent){
        
        return class_trap_child.__mro__.__arr__.includes(class_trap_parent)
}