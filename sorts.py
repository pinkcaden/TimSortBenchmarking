
from randomize import RandomizedIteratorFactory
import numpy as np



class Term(float):
    _value = None
    def __init__(self, value):
        _value = value
    def __eq__(self, other):
        self.__scratch_record("==")
    def __lt__(self, other):
        self.__scratch_record("<")
    def __gt__(self, other):
        self.__scratch_record(">")
    def __le__(self, other):
        self.__scratch_record("<=")
    def __ge__(self, other):
        self.__scratch_record(">")


    def __scratch_record(self, sout):
        print(sout)


class SortBehaviorFactory:

    def __init__(self):
        pass


array = np.random.uniform(size = 100)
randomize = RandomizedIteratorFactory.get_randomized_iterator(array)



randomize.set_randomization(100)

terms = []
for n in randomize:
    terms.append(Term(n))

print(terms)

print(terms[0] > 5 or terms[1] == 4)
