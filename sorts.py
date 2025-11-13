from randomize import RandomizedIteratorFactory
import numpy as np

class Record:
    def __init__(self):
        self._operation_counts = {
            "<" : 0,
            ">" : 0,
            ">=" : 0,
            "<=" : 0,
            "==" : 0
        }
    def scratch(self, string: str):
        self._operation_counts[string] += 1
    def get_counts(self):
        return self._operation_counts


class Term(float):
    _value = None

    def __init__(self, value, record):
        self._value = value
        self._record = record

    def __new__(cls, value, record):
        return super().__new__(cls, value)

    def __eq__(self, other) -> bool:
        self._record.scratch("==")
        return float.__eq__(self, other)

    def __lt__(self, other) -> bool:
        self._record.scratch("<")
        return float.__lt__(self, other)

    def __gt__(self, other) -> bool:
        self._record.scratch(">")
        return float.__gt__(self, other)


    def __le__(self, other) -> bool:
        self._record.scratch("<=")
        return float.__le__(self, other)

    def __ge__(self, other) -> bool:
        self._record.scratch(">")
        return float.__ge__(self, other)


arrayR = np.random.uniform(size=1000)
arrayS = []
for i in range(1000):
    arrayS.append(i)

randomize = RandomizedIteratorFactory.get_randomized_iterator("cocktail",arrayS)

for n in range(20):
    randomize.set_randomization(5*n)

    terms = []
    myRecord = Record()
    for rand in randomize:
        terms.append(Term(rand, myRecord))
    #
    # print(terms)
    sorted(terms)

    print(str(5*n)+"% Random: "+ str(myRecord.get_counts()))