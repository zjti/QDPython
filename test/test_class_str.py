class A:
    def __init__(self,a,*args):
        print(a,args)
        self.a =a
        self.args = args

    def k(self):
        print(self.a,self.args)

    def __str__(self):
        return f'Obj A({self.a}) '
    def __call__(self):
        print('its called')


a = A(*[2,2])
b = A(1)
c = A(None,1,2,3,4,5,6,7)
print(a,b,c)
a()
b.__call__ = lambda self: print('its lambda')

b()
b.__call__()
