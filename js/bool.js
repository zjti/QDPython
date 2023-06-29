function bool(arg){
    if (arg === true){return true}
    if (arg === false){return false}
    if (typeof arg.__bool__ == 'function'){return arg.__bool__();}
    if (typeof arg.__len__ == 'function'){
        if (arg.__len__() > 0){return true;}
        else{return false;}  
    }
    if(typeof arg.length == 'number'){
        if(arg.length>0){return true;}
    }
    if (arg != 0)return true;
    return false;
}