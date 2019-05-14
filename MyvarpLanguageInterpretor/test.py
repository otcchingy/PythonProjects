from collections import namedtuple, defaultdict, Counter


Person = namedtuple("Person",["name", "age", "school"])

ben = Person("Bernard", 21, "Jubilee Academy")
print(ben)
print(ben.name, ben.age, ben.school)

def is_even(x):
     return (x % 2) == 0

list(filter(is_even, range(10)))

f = open('data.txt', 'r')
for i, line in enumerate(f):
    if line.strip() == '':
        print('Blank line at line #%i' % i)


zip(['a', 'b', 'c'], (1, 2, 3)) # ('a', 1), ('b', 2), ('c', 3)
















"""
# itertools.count()# itertools.cycle()# itertools.chain()# itertools.repeat()# itertools.islice()# itertools.tee( itertools.count() )
itertools.starmap(os.path.join,
                  [('/bin', 'python'), ('/usr', 'bin', 'java'),
                   ('/usr', 'bin', 'perl'), ('/usr', 'bin', 'ruby')])


itertools.filterfalse(is_even, itertools.count())

def less_than_10(x):
    return x < 10

itertools.takewhile(less_than_10, itertools.count())

itertools.dropwhile(less_than_10, itertools.count()) =>
  10, 11, 12, 13, 14, 15, 16, 17, 18, 19, ...

itertools.dropwhile(is_even, itertools.count()) =>
  1, 2, 3, 4, 5, 6, 7, 8, 9, 10, ...itertools.permutations([1, 2, 3, 4, 5], 2)
itertools.permutations([1, 2, 3, 4, 5], 2) =>
  (1, 2), (1, 3), (1, 4), (1, 5),
  (2, 1), (2, 3), (2, 4), (2, 5),
  (3, 1), (3, 2), (3, 4), (3, 5),
  (4, 1), (4, 2), (4, 3), (4, 5),
  (5, 1), (5, 2), (5, 3), (5, 4)

itertools.permutations([1, 2, 3, 4, 5]) =>
  (1, 2, 3, 4, 5), (1, 2, 3, 5, 4), (1, 2, 4, 3, 5),
  ...
  (5, 4, 3, 2, 1)
If you don’t supply a value for r the length of the iterable is used, meaning that all the elements are permuted.

Note that these functions produce all of the possible combinations by position and don’t require that the contents of iterable are unique:

itertools.permutations('aba', 3) =>
  ('a', 'b', 'a'), ('a', 'a', 'b'), ('b', 'a', 'a'),
  ('b', 'a', 'a'), ('a', 'a', 'b'), ('a', 'b', 'a')


city_list = [('Decatur', 'AL'), ('Huntsville', 'AL'), ('Selma', 'AL'),
             ('Anchorage', 'AK'), ('Nome', 'AK'),
             ('Flagstaff', 'AZ'), ('Phoenix', 'AZ'), ('Tucson', 'AZ'),]"""