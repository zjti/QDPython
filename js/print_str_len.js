function len(a){
    if (typeof a == 'string'){
        return BigInt(a.length)
    }
    if (typeof a.__len__ == 'function'){
        return BigInt(a.__len__());
    }
    throw Error('len not available for:',a)
    
}

function str(a){
    if (a == null){
        return 'None';
    }
    if (typeof a.__str__ == 'function'){
        return a.__str__();
    }
    if (typeof a == 'function'){
        return "<function '"+ a.name  + "' "+ a.__qualname__ +">";
    }
    if (typeof a == 'string'){
        return "'" + a +"'";
    }
    
    if (typeof a == 'boolean'){
        if (a){return 'True';}
        else {return 'False';}
    }
    if (typeof a == 'number'){
        var v = String(a)
        if (v.includes('.')){
            return  v
        }
        return v + '.0'
    }
    return String(a);
}

function print(){
    var s = [];
    for (var i = 0; i < arguments.length; i++) {
        s += str(arguments[i])
        if (i != arguments.length-1){
            s += ',';
        }
    }
    output.value+=s +'\n'
    console.log(s,'!');
}