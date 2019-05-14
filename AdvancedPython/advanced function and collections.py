<<<<<<< HEAD
#collection   
#abc 
#yield # pauses and returns a value from an iterable like object then continues over the iterable 
#all # return true if all elements in an iterable return true
#any # return true if any of the elements in an iterable return true
#filter  #takes function that return bool and run it over an iterable and return an new iterable of true values
#map  #takes function and run it over an iterable and return an new iterable of  function(values)
#lambda # lambda x: function(x) return x when the function operates on it function lambda retun a function
#comprehension ..generators() and list[]
#enumerate
# def func(a:int,b:int) -> float:
#counter
#defaultdict  # return a default value for any keyerror ..its init takes a function can be lambda
#eg.defaultdict(list) to change the default value u can do ddict.default_factory = int || or any type
#ordereddict  # keeps the order they were entered
#namedtuple #
#deque #like list but has more methods ..popleft, appendleft
"""
to create a generator class you need to create the  __next__() method ## this creates an iterator
to create and iterable __iter__() method that returns an iterator or a generator
or create __len__() and __getitem__ # creates an iterable 

argument unpacking
"""

class genClass:
    ### this is an iterator
    def __init__(self):
        self.number = 0

    def __next__(self):
        num = self.number
        self.number += 1
        return num

    def __iter__(self):
        ## this makes the class an iterable can use for and while
        return self

g = genClass()

print(next(g))
print(next(g))
print(next(g))
print(next(g))


# class _while_:

#     def __init__(self, f):
#         self.function = f

#     def __next__(self):
#         if self.function():
#             return True
#         else:
#             return False

def counter(max):
    i = 0
    while i < max:
        yield i
        i+=1


c = counter(10)

for i in range(11):
=======
#collection   
#abc 
#yield # pauses and returns a value from an iterable like object then continues over the iterable 
#all # return true if all elements in an iterable return true
#any # return true if any of the elements in an iterable return true
#filter  #takes function that return bool and run it over an iterable and return an new iterable of true values
#map  #takes function and run it over an iterable and return an new iterable of  function(values)
#lambda # lambda x: function(x) return x when the function operates on it function lambda retun a function
#comprehension ..generators() and list[]
#enumerate
# def func(a:int,b:int) -> float:
#counter
#defaultdict  # return a default value for any keyerror ..its init takes a function can be lambda
#eg.defaultdict(list) to change the default value u can do ddict.default_factory = int || or any type
#ordereddict  # keeps the order they were entered
#namedtuple #
#deque #like list but has more methods ..popleft, appendleft
"""
to create a generator class you need to create the  __next__() method ## this creates an iterator
to create and iterable __iter__() method that returns an iterator or a generator
or create __len__() and __getitem__ # creates an iterable 

argument unpacking
"""

class genClass:
    ### this is an iterator
    def __init__(self):
        self.number = 0

    def __next__(self):
        num = self.number
        self.number += 1
        return num

    def __iter__(self):
        ## this makes the class an iterable can use for and while
        return self

g = genClass()

print(next(g))
print(next(g))
print(next(g))
print(next(g))


# class _while_:

#     def __init__(self, f):
#         self.function = f

#     def __next__(self):
#         if self.function():
#             return True
#         else:
#             return False

def counter(max):
    i = 0
    while i < max:
        yield i
        i+=1


c = counter(10)

for i in range(11):
>>>>>>> c45a9c38d692dc08ca320eb779636442c0f89b3f
    print(next(c))