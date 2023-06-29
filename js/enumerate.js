function enumerate(iter){
    e = {'iter_obj':iter.__iter__()}
    e.__iter__ = function(){
        function* iter(iter_obj){
            var i = BigInt(0);
            for (const v of iter_obj){
                yield new pytuple([i,v]);
                i++;
            }
        }
        iter_obj = iter(this.iter_obj)
        iter_obj.__next__ = iter_obj.next
        return iter_obj
    }
    return e
}
