function dict(){
    // print(arguments[0],arguments[1],arguments[2])
    if (arguments.length == 1){
        return arguments[0]
    }
    if (arguments.length == 0){
        return new pydict([])
    }
    var d = new pydict([]);
    var i = 1;
    for (k of arguments[0].__arr__){
        d.__setitem__(k,arguments[i])
        i++;
    } 
    if (i == 1 && arguments[1] instanceof pydict){
        return arguments[1]
    }
    return d;
}

pydict = class{
    constructor(kv_pairs){
        this.__map__ = new Map()
        for (let kvp of kv_pairs){
            this.__map__.set( js_hash4map(kvp[0]),kvp) 
        }
    }
    __getitem__(k){
        var v= this.__map__.get(js_hash4map(k)) 
        if (v === undefined){
            throw Error('key error', k)
        }
        return v[1]
    }
    
    __setitem__(k,v){
        this.__map__.set(js_hash4map(k),[k,v])
    }
    __str__(){
        var s = [];
        for (let [key, value] of this.__map__) {
             s.push( str(value[0]) +':'+ str(value[1]) );
        }
        return '{' + s.join(', ') + '}';
    }
    __iter__(){
        iter_obj = this.__map__.keys()
        iter_obj.__next__ = iter_obj.next
        return iter_obj
    }
    items(){
        
        iter_obj = {
            __iter__ : function(){
                var r= this.__map__[Symbol.iterator]()
                r.__next__ = r.next
                return r
            }
        }
        return iter_obj
    }
    __len__(){ return this.__map__.size;}


}