function js__add__(arg1,arg2){
    var arg1_t = typeof arg1;
    var arg2_t = typeof arg2;
    if (arg1_t == 'function' || arg1_t == 'object'){
        if (typeof arg1.__add__ == 'function') return arg1.__add__(arg2);
    }
    if (arg2_t == 'function' || arg1_t == 'object'){
        if (typeof arg2.__radd__ == 'function') return arg2.__radd__(arg1);
    }
    if ((arg1_t == 'string') && (arg2_t == 'string')){
        return arg1+arg2
    }
    if ((arg1_t == 'string') || (arg2_t == 'string')){
           throw Error("can't add string and nonstring", arg1,arg2)
    }
    if ((arg1_t == 'bigint') && (arg2_t == 'bigint')){
        return arg1+arg2
    }
    if ((arg1_t == 'bigint') && (arg2_t == 'boolean')){
        return arg1+BigInt(arg2)
    }
    if ((arg1_t == 'boolean') && (arg2_t == 'bigint')){
        return BigInt(arg1)+arg2
    }
    return Number(arg1) + Number(arg2)


}

function js__mul__(arg1,arg2){
    var arg1_t = typeof arg1;
    var arg2_t = typeof arg2;
    if (arg1_t == 'function' || arg1_t == 'object'){
        if (typeof arg1.__mul__ == 'function') return arg1.__mul__(arg2);
    }
    if (arg2_t == 'function'|| arg1_t == 'object'){
        if (typeof arg2.__rmul__ == 'function') return arg2.__rmul__(arg1);
    }
    if ((arg1_t == 'string') && ((arg2_t == 'bigint') || (arg2_t == 'boolean'))){
        return arg1.repeat(Number(arg2))
    }
    if (((arg1_t == 'bigint') || (arg1_t == 'boolean')) && (typeof arg2 == 'string')){
        return arg2.repeat(Number(arg1))
    }
    if ((arg1_t == 'string') || (arg2_t == 'string')){
           throw Error("can't mul string and nonint", arg1,arg2)
    }
    if ((arg1_t == 'bigint') && (arg2_t == 'bigint')){
        return arg1*arg2
    }
    if ((arg1_t == 'bigint') && (arg2_t == 'boolean')){
        return arg1*BigInt(arg2)
    }
    if ((arg1_t == 'boolean') && (arg2_t == 'bigint')){
        return BigInt(arg1)*arg2
    }
    return Number(arg1) * Number(arg2) 
}

function js__sub__(arg1,arg2){
    var arg1_t = typeof arg1;
    var arg2_t = typeof arg2;
    if (arg1_t == 'function'){
        if (typeof arg1.__sub__ == 'function') return arg1.__sub__(arg2);
    }
    if (arg2_t == 'function'){
        if (typeof arg2.__rsub__ == 'function') return arg2.__rsub__(arg1);
    }
    
    if ((arg1_t == 'string') || (arg2_t == 'string')){
           throw Error("can't sub string", arg1,arg2)
    }
    if ((arg1_t == 'bigint') && (arg2_t == 'bigint')){
        return arg1-arg2
    }
    if ((arg1_t == 'bigint') && (arg2_t == 'boolean')){
        return arg1-BigInt(arg2)
    }
    if ((arg1_t == 'boolean') && (arg2_t == 'bigint')){
        return BigInt(arg1)-arg2
    }
    return Number(arg1) - Number(arg2)
}

function js__truediv__(arg1,arg2){
    var arg1_t = typeof arg1;
    var arg2_t = typeof arg2;
    if (arg1_t == 'function'){
        if (typeof arg1.__truediv__ == 'function') return arg1.__truediv__(arg2);
    }
    if (arg2_t == 'function'){
        if (typeof arg2.__rtruediv__ == 'function') return arg2.__rtruediv__(arg1);
    }
    if ((arg1_t == 'string') || (arg2_t == 'string')){
           throw TypeError("unsupported operand type(s) for /: '"+arg1_t+"' and '"+arg2_t+"'")
    }
    if (arg2 == 0){
           throw ZeroDivisionError("division or modulo by zero")

    }
    return Number(arg1) / Number(arg2)
}


function js__floordiv__(arg1,arg2){
    var arg1_t = typeof arg1;
    var arg2_t = typeof arg2;
    if (arg1_t == 'function'){
        if (typeof arg1.__floordiv__ == 'function') return arg1.__floordiv__(arg2);
    }
    if (arg2_t == 'function'){
        if (typeof arg2.__rfloordiv__ == 'function') return arg2.__rfloordiv__(arg1);
    }
    if ((arg1_t == 'string') || (typeof arg2 == 'string')){
           throw TypeError("unsupported operand type(s) for //: '"+arg1_t+"' and '"+arg2_t+"'")
    }
    if (arg2 == 0){
        throw ZeroDivisionError("floor division or modulo by zero")
    }
    if ((arg1_t== 'bigint') && (arg2_t == 'bigint')){
        return arg1 / arg2
    }
    if ((arg1_t == 'bigint') && (arg2_t == 'boolean')){
        return arg1 / BigInt(arg2)
    }
    if ((arg1_t == 'boolean') && (arg2_t == 'bigint')){
        return BigInt(arg1) / arg2
    }

    return Math.floor( Number(arg1) / Number(arg2))
    
}

function js__modulo__(arg1,arg2){
    var arg1_t = typeof arg1;
    var arg2_t = typeof arg2;
    if (arg1_t == 'function'){
        if (typeof arg1.__modulo__ == 'function') return arg1.__modulo__(arg2);
    }
    if (arg2_t == 'function'){
        if (typeof arg2.__modulo__ == 'function') return arg2.__modulo__(arg1);
    }
    if (arg2 == 0){
        throw ZeroDivisionError("floor division or modulo by zero")
    }
    if ((arg1_t == 'string') || (typeof arg2 == 'string')){
           throw Error(" modulo on string not implemented", arg1,arg2)
    }
    if ((arg1_t== 'bigint') && (arg2_t == 'bigint')){
        if (arg1 >= 0){
            return arg1 % arg2
        }else{
            return arg1 - (arg1/arg2-1n) * arg2
        }
    }
    if ((arg1_t == 'bigint') && (arg2_t == 'boolean')){
        return arg1 % BigInt(arg2)
    }
    if ((arg1_t == 'boolean') && (arg2_t == 'bigint')){
        return BigInt(arg1) % arg2
    }
    return Number(arg1) - Math.floor( Number(arg1) / Number(arg2)) * Number(arg2)
    
}

function js__iadd__(arg1,arg2){
    var arg1_t = typeof arg1;
    var arg2_t = typeof arg2;
    
    if (arg1_t == 'function'){
        if (typeof arg1.__iadd__ == 'function') return arg1.__iadd__(arg2);
        if (typeof arg1.__add__ == 'function') return arg1.__add__(arg2);
    }
    if (arg2_t == 'function'){
        if (typeof arg2.__radd__ == 'function') return arg2.__radd__(arg1);
    }
    if ((arg1_t == 'string') && (arg2_t == 'string')){
        return arg1+arg2
    }
    if ((arg1_t == 'string') || (arg2_t == 'string')){
           throw Error("can't add string and nonstring", arg1,arg2)
    }
    if ((arg1_t == 'bigint') && (arg2_t == 'bigint')){
        return arg1+arg2
    }
    if ((arg1_t == 'bigint') && (arg2_t == 'boolean')){
        return arg1+BigInt(arg2)
    }
    if ((arg1_t == 'boolean') && (arg2_t == 'bigint')){
        return BigInt(arg1)+arg2
    }
    return Number(arg1) + Number(arg2)


}

function js__imul__(arg1,arg2){
    var arg1_t = typeof arg1;
    var arg2_t = typeof arg2;
    if (arg1_t == 'function'){
        if (typeof arg1.__imul__ == 'function') return arg1.__imul__(arg2);
        if (typeof arg1.__mul__ == 'function') return arg1.__mul__(arg2);

    }
    if (arg2_t == 'function'){
        if (typeof arg2.__rmul__ == 'function') return arg2.__rmul__(arg1);
    }
    if ((arg1_t == 'string') && ((arg2_t == 'bigint') || (arg2_t == 'boolean'))){
        return arg1.repeat(Number(arg2))
    }
    if (((arg1_t == 'bigint') || (arg1_t == 'boolean')) && (typeof arg2 == 'string')){
        return arg2.repeat(Number(arg1))
    }
    if ((arg1_t == 'string') || (arg2_t == 'string')){
           throw Error("can't mul string and nonint", arg1,arg2)
    }
    if ((arg1_t == 'bigint') && (arg2_t == 'bigint')){
        return arg1*arg2
    }
    if ((arg1_t == 'bigint') && (arg2_t == 'boolean')){
        return arg1*BigInt(arg2)
    }
    if ((arg1_t == 'boolean') && (arg2_t == 'bigint')){
        return BigInt(arg1)*arg2
    }
    return Number(arg1) * Number(arg2) 
}

function js__isub__(arg1,arg2){
    var arg1_t = typeof arg1;
    var arg2_t = typeof arg2;
    if (arg1_t == 'function'){
        if (typeof arg1.__isub__ == 'function') return arg1.__isub__(arg2);
        if (typeof arg1.__sub__ == 'function') return arg1.__sub__(arg2);
    }
    if (arg2_t == 'function'){
        if (typeof arg2.__rsub__ == 'function') return arg2.__rsub__(arg1);
    }
    
    if ((arg1_t == 'string') || (arg2_t == 'string')){
           throw Error("can't sub string", arg1,arg2)
    }
    if ((arg1_t == 'bigint') && (arg2_t == 'bigint')){
        return arg1-arg2
    }
    if ((arg1_t == 'bigint') && (arg2_t == 'boolean')){
        return arg1-BigInt(arg2)
    }
    if ((arg1_t == 'boolean') && (arg2_t == 'bigint')){
        return BigInt(arg1)-arg2
    }
    return Number(arg1) - Number(arg2)
}

function js__truediv__(arg1,arg2){
    var arg1_t = typeof arg1;
    var arg2_t = typeof arg2;
    if (arg1_t == 'function'){
        if (typeof arg1.__itruediv__ == 'function') return arg1.__itruediv__(arg2);
        if (typeof arg1.__truediv__ == 'function') return arg1.__truediv__(arg2);
    }
    if (arg2_t == 'function'){
        if (typeof arg2.__rtruediv__ == 'function') return arg2.__rtruediv__(arg1);
    }
    if ((arg1_t == 'string') || (arg2_t == 'string')){
           throw Error("can't div string", arg1,arg2)
    }
    if (arg2 == 0){
           throw Error("ZeroDivisionError", arg1,arg2)
    }
    return Number(arg1) / Number(arg2)
}


function js__floordiv__(arg1,arg2){
    var arg1_t = typeof arg1;
    var arg2_t = typeof arg2;
    if (arg1_t == 'function'){
        if (typeof arg1.__ifloordiv__ == 'function') return arg1.__ifloordiv__(arg2);
        if (typeof arg1.__floordiv__ == 'function') return arg1.__floordiv__(arg2);
    }
    if (arg2_t == 'function'){
        if (typeof arg2.__rfloordiv__ == 'function') return arg2.__rfloordiv__(arg1);
    }
    if ((arg1_t == 'string') || (typeof arg2 == 'string')){
           throw Error("can't div string", arg1,arg2)
    }
    if ((arg1_t== 'bigint') && (arg2_t == 'bigint')){
        return arg1 / arg2
    }
    if ((arg1_t == 'bigint') && (arg2_t == 'boolean')){
        return arg1 / BigInt(arg2)
    }
    if ((arg1_t == 'boolean') && (arg2_t == 'bigint')){
        return BigInt(arg1) / arg2
    }
    return Math.floor( Number(arg1) / Number(arg2))
    
}