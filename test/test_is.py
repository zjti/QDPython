print(True is False)
print([i for i in range(3)] is None)
print([i for i in range(3)] is list)
a = dict({1:1})
b = a
print(a is b)
a = dict({1:1})
print(a,b,a is b)
a = tuple((1,2,3))
b = tuple((1,2,)) + (3,)

print(a,b,a is b, a==b)
