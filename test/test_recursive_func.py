 
print(sys.version)
t0 = time()

def fibonacci(n): 
    """ recursive fibonacci """
    if n < 2:
        return 1
    return fibonacci(n - 1) + fibonacci(n - 2)  

s=fibonacci(25)

t=time()-t0
print(t,s)
print(fibonacci.__doc__)


 