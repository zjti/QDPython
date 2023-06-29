class Animal:
    legs = 4
    def oink(self):
        print('Animal makes Oink')
    def count_legs(self):
        print(f'Animal has {Animal.legs} legs')
        return 4#Animal.num_legs
        
class Cat(Animal):
    def oink(self):
        print('Cat makes MIAU')
        

class Dog(Animal):
    def oink(self):
        print('Dog makes WAUWAU')
        

class DoubleDog(Dog):
    def count_legs(self):
        print('super says:')
        num_legs = super().count_legs() * 2
        
        print(f'so : DoubleDog has {num_legs} legs')
        return num_legs
        
        
a = Animal()
c = Cat()
d = Dog()
dd = DoubleDog()
print(dd.count_legs())   
        