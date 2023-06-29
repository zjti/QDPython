print(sys.version)
t0 = time()
s = 0
for i in range(100*100):
    if i % 2 ==0:
        s+=i
    else:
        s-=i
t = time()-t0
print(t,s)

s = 0
for i in range(1000*1000):
    if i % 2 ==0:
        s+=i
    else:
        s-=i
t = time()-t0
print(t,s)