function list(arr){
    print(arr)
    return new pylist(arr.__arr__)
}
pylist = class {
    constructor(arr){
        this.__arr__=arr;
        this.__class__=list;
    }
    append(v){
        this.__arr__.push(v)
        return None
    }
    __setitem__(k,v){
        this.__arr__[k]=v
        return None
    }
    __getitem__(k){
        var v;
        if (k >= 0){
            v= this.__arr__[k]
        }else{
            v= this.__arr__[this.__arr__.length+Number(k)]
        }
        if (v === undefined){
            throw Error('list error', k, this)
        }
        return v
    }
    __iadd__(other){
        // list += tuple : OK
        this.__arr__ = this.__arr__.concat( other.__arr__);
        return this
    }
    __add__(other){
        // list + tuple : NOT-OK
        if (other instanceof pylist){
            return new pylist(this.__arr__.concat( other.__arr__));
        }
        return other.__radd__(this)
    }
    __rmul__(o){
        return this.__mul__(o)
    }
    __mul__(o){
        if ((typeof o == 'bigint') || (typeof o == 'boolean')){
            return new pylist(Array(Number(o)).fill(this.__arr__).flat() );
        }
        throw Error('list mul error')
    }
    
    __iter__(){
        iter_obj = this.__arr__.values()
        iter_obj.__next__ = iter_obj.next
        return iter_obj
    }
    __len__(){ return this.__arr__.length;}
    
    __str__(){
        var s = [];
        for (const e of this.__arr__) {
             s.push( str(e) );
        }
        return '[' + s.join(', ') + ']';
    }
}