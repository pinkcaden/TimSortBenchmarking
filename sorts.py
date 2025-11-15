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

terms = []
rec = Record()
for n in [15,3,2,191,17]:
    terms.append(Term(n, rec))

for n in terms:
    sorted(terms[:])

newArr = []
for n in terms:
    newArr.append(n)

leftArr = newArr
leftAr = newArr


sorted(leftArr)

print(rec.get_counts())