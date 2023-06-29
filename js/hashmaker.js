var __hash__map__ = new WeakMap;
var __hash__map__count__ = 0;

function js__hash__(x){
    // - WeakMap to asign unique hash to objects
    // - not used for dict because tuple needs spezial case
    if(__hash__map__.has(x)){
        print('j')
        return __hash__map__.get(x);
    }else{
        print('n')
        __hash__map__.set(x,++__hash__map__count__);
        return __hash__map__count__;
    }
}

function js_hash4map(x){
    // - everthing except tuple is its own hash.
    // - tuple uses js__hash__ for objects then {json encoded tuple} + '_tupple_hash_XXX_' as hash.
    
    if (x instanceof pytuple){
        j_arr = []
        for (const e of x.__arr__){
            if (e  instanceof pytuple){
                   j_arr.push(hash4map(e));
            }else{
                if (typeof e == 'object'){
                    j_arr.push(js__hash__(e));
                }else if (typeof e == 'bigint'){
                    j_arr.push(String(e)+'n__');
                }else{
                    j_arr.push(e);
                }
            }
        }
        return  JSON.stringify(j_arr) + '_tupple_hash_XXX_'
    }else{
        return x
    }
}

