function js_is_op(arg1,arg2){
    if (Object.is(arg1,arg2)){
           return true;
    }else{
        if ((arg1 instanceof tuple)  && (arg2 instanceof tuple)){
            if (js_hash4map(arg1) == js_hash4map(arg2)){
                return true;
            }
        }
    }
    return false;
}