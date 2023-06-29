function range(start, end, step= 1n){
    if (arguments.length==1){
        end = start
        start = 0n
    }
    r = {'start':start ,'end':end, 'step':step}
    // print(start,end,step)
    r.__getitem__ = function (i){
        v = this.start + i * this.step
        if (v >= this.end){
            throw Error('range out of bonds')
        }
        return v
    }
    r.__len__ = function (){
        return Math.floor((this.end - this.start - 1) / (this.step)) + 1
    }
    r.__iter__ = function (){
        function* iter(start,end,step){
            for (let i = start; i < end; i += step) {
                yield i;
            }
        }
        iter_obj = iter(this.start,this.end,this.step)
        iter_obj.__next__ = iter_obj.next
        return iter_obj
    }
    return r
}
