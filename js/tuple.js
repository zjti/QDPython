function tuple(arr){
    return new pytuple( arr.__arr__)
}
pytuple = class{
    constructor(arr){
        this.__arr__ = arr
        this.__class__ = tuple;

    }
    __getitem__(k){
        var v;
        if (k >= 0){
            v= this.__arr__[k]
        }else{
            v= this.__arr__[this.__arr__.length+Number(k)]
        }
        if (v === undefined){
            throw Error('tuple error', k, this)
        }
        return v
    }
    __iter__(){
        iter_obj = this.__arr__.values()
        iter_obj.__next__ = iter_obj.next
        return iter_obj
    }
    __add__(other){
        // tuple + tuple : OK
        if (other instanceof pytuple){
            return new pytuple(this.__arr__.concat( other.__arr__));
        }
        return other.__radd__(this)
    }
    
    __str__(){
        var s = [];
        for (let e of this.__arr__) {
             s.push( str(e)  );
        }
        return '(' + s.join(', ') + ')';
    }
}