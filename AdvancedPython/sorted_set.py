<<<<<<< HEAD
from collections.abc import Sequence, Set
from bisect import bisect_left
from itertools import chain

class SortedSet(Sequence, set):

    def __init__(self, items = None):
        self._items = sorted(set(items)) if items is not None else []

    def __contains__(self , item):
        try:
            self.index(item)
            return True
        except ValueError:
            return False
        #return item in self._items

    def __len__(self):
        return len(self._items)

    def __str__(self):
        return str(self._items)

    def __repr__(self):
        return 'SortedSet({})'.format(str(self._items))

    def __getitem__(self, index : int):
       result = self._items[index]
       return SortedSet(result) if isinstance(index, slice) else result

    def __iter__(self):
        return iter(self._items)

    # will be automatically implemeted if __getitem__ is implemented
    # def __reversed__(self):
    #    self.items.__reveresed__()

    def __add__(self, obj):
        return SortedSet(chain(self._items, obj._items))

    def __mul__(self, number):
        return self if number > 0 else SortedSet()

    def __rmul__(self, number):
        return self * number

    def issubset(self, obj):
        return self <= SortedSet(obj)

    def issuperset(self, obj):
        return self >= SortedSet(obj)

    def intersection(self, obj):
        return self & SortedSet(obj)

    def union(self, obj):
        return self | SortedSet(obj)

    def symmetric_differnce(self, obj):
        return self ^ SortedSet(obj)

    def difference(self, obj):
        return self - SortedSet(obj)

    def __eq__(self, obj):
        if not isinstance(obj, SortedSet):
            return NotImplemented
        return self._items == obj._items

    def __ne__(self, obj):
        if not isinstance(obj, SortedSet):
            return NotImplemented
        return self._items != obj._items

    def is_unique_and_sorted(self):
        return all(self[i] < self[i+1] for i in range(len(self)-1))


    # def __gt__(self, obj):
    #     if not isinstance(obj, SortedSet):
    #         return NotImplemented
    #     return self._items > obj._items
    #
    # def __ge__(self, obj):
    #     if not isinstance(obj, SortedSet):
    #         return NotImplemented
    #     return self._items >= obj._items
    #
    # def __lt__(self, obj):
    #     if not isinstance(obj, SortedSet):
    #         return NotImplemented
    #     return self._items < obj._items
    #
    # def __le__(self, obj):
    #     if not isinstance(obj, SortedSet):
    #         return NotImplemented
    #     return self._items <= obj._items
    #
    # def __and__(self, obj):
    #     if not isinstance(obj, SortedSet):
    #         return NotImplemented
    #     return self._items and obj._items
    #
    # def __or__(self, obj):
    #     if not isinstance(obj, SortedSet):
    #         return NotImplemented
    #     return self._items or obj._items
    #
    # def __xor__(self, obj):
    #     if not isinstance(obj, SortedSet):
    #         return NotImplemented
    #     return self._items ^ obj._items
    #
    # def __sub__(self, obj):
    #     if not isinstance(obj, SortedSet):
    #         return NotImplemented
    #     return self._items - obj._items

    def index(self, item):
        assert self.is_unique_and_sorted()
        index = bisect_left(self._items, item)
        if (index != len(self._items) and self._items[index] == item):
            return index
        raise ValueError('The item {} is not in the Set'.format(item))


    def remove(self, index : int):
        assert self.is_unique_and_sorted()
        self._items.pop(index)


    def count(self, item):
        assert self.is_unique_and_sorted()
        return int(item in self)


class SomeException(Exception):
    pass


properties = ['__add__', '__class__', '__contains__', '__delattr__', '__delitem__',
              '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__',
              '__getitem__', '__gt__', '__hash__', '__iadd__', '__imul__', '__init__',
              '__init_subclass__', '__iter__', '__le__', '__len__', '__lt__', '__mul__',
              '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__reversed__',
              '__rmul__', '__setattr__', '__setitem__', '__sizeof__', '__str__', '__subclasshook__',
=======
from collections.abc import Sequence, Set
from bisect import bisect_left
from itertools import chain

class SortedSet(Sequence, set):

    def __init__(self, items = None):
        self._items = sorted(set(items)) if items is not None else []

    def __contains__(self , item):
        try:
            self.index(item)
            return True
        except ValueError:
            return False
        #return item in self._items

    def __len__(self):
        return len(self._items)

    def __str__(self):
        return str(self._items)

    def __repr__(self):
        return 'SortedSet({})'.format(str(self._items))

    def __getitem__(self, index : int):
       result = self._items[index]
       return SortedSet(result) if isinstance(index, slice) else result

    def __iter__(self):
        return iter(self._items)

    # will be automatically implemeted if __getitem__ is implemented
    # def __reversed__(self):
    #    self.items.__reveresed__()

    def __add__(self, obj):
        return SortedSet(chain(self._items, obj._items))

    def __mul__(self, number):
        return self if number > 0 else SortedSet()

    def __rmul__(self, number):
        return self * number

    def issubset(self, obj):
        return self <= SortedSet(obj)

    def issuperset(self, obj):
        return self >= SortedSet(obj)

    def intersection(self, obj):
        return self & SortedSet(obj)

    def union(self, obj):
        return self | SortedSet(obj)

    def symmetric_differnce(self, obj):
        return self ^ SortedSet(obj)

    def difference(self, obj):
        return self - SortedSet(obj)

    def __eq__(self, obj):
        if not isinstance(obj, SortedSet):
            return NotImplemented
        return self._items == obj._items

    def __ne__(self, obj):
        if not isinstance(obj, SortedSet):
            return NotImplemented
        return self._items != obj._items

    def is_unique_and_sorted(self):
        return all(self[i] < self[i+1] for i in range(len(self)-1))


    # def __gt__(self, obj):
    #     if not isinstance(obj, SortedSet):
    #         return NotImplemented
    #     return self._items > obj._items
    #
    # def __ge__(self, obj):
    #     if not isinstance(obj, SortedSet):
    #         return NotImplemented
    #     return self._items >= obj._items
    #
    # def __lt__(self, obj):
    #     if not isinstance(obj, SortedSet):
    #         return NotImplemented
    #     return self._items < obj._items
    #
    # def __le__(self, obj):
    #     if not isinstance(obj, SortedSet):
    #         return NotImplemented
    #     return self._items <= obj._items
    #
    # def __and__(self, obj):
    #     if not isinstance(obj, SortedSet):
    #         return NotImplemented
    #     return self._items and obj._items
    #
    # def __or__(self, obj):
    #     if not isinstance(obj, SortedSet):
    #         return NotImplemented
    #     return self._items or obj._items
    #
    # def __xor__(self, obj):
    #     if not isinstance(obj, SortedSet):
    #         return NotImplemented
    #     return self._items ^ obj._items
    #
    # def __sub__(self, obj):
    #     if not isinstance(obj, SortedSet):
    #         return NotImplemented
    #     return self._items - obj._items

    def index(self, item):
        assert self.is_unique_and_sorted()
        index = bisect_left(self._items, item)
        if (index != len(self._items) and self._items[index] == item):
            return index
        raise ValueError('The item {} is not in the Set'.format(item))


    def remove(self, index : int):
        assert self.is_unique_and_sorted()
        self._items.pop(index)


    def count(self, item):
        assert self.is_unique_and_sorted()
        return int(item in self)


class SomeException(Exception):
    pass


properties = ['__add__', '__class__', '__contains__', '__delattr__', '__delitem__',
              '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__',
              '__getitem__', '__gt__', '__hash__', '__iadd__', '__imul__', '__init__',
              '__init_subclass__', '__iter__', '__le__', '__len__', '__lt__', '__mul__',
              '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__reversed__',
              '__rmul__', '__setattr__', '__setitem__', '__sizeof__', '__str__', '__subclasshook__',
>>>>>>> c45a9c38d692dc08ca320eb779636442c0f89b3f
              'append', 'clear', 'copy', 'count', 'extend', 'index', 'insert', 'pop', 'remove', 'reverse', 'sort']