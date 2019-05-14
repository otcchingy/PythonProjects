<<<<<<< HEAD
import unittest
from sorted_set import SortedSet


class TestConstruction(unittest.TestCase):

    def empty(self):
        s = SortedSet([])

    def none(self):
        s = SortedSet()

    def filled(self):
        s = SortedSet([1,2,3,4])

    def filled_with_duplicates(self):
        s = SortedSet([2,2,2,34])
=======
import unittest
from sorted_set import SortedSet


class TestConstruction(unittest.TestCase):

    def empty(self):
        s = SortedSet([])

    def none(self):
        s = SortedSet()

    def filled(self):
        s = SortedSet([1,2,3,4])

    def filled_with_duplicates(self):
        s = SortedSet([2,2,2,34])
>>>>>>> c45a9c38d692dc08ca320eb779636442c0f89b3f
