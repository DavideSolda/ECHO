from dataclasses import dataclass

@dataclass(frozen = True)
class Interval:

    min : int
    max : int

    def __init__(self, _min, _max):
        if (_min > _max):
            raise Exception(f"min value {_min} > max value{_max}.\n")
        object.__setattr__(self, "min", _min)
        object.__setattr__(self, "max", _max)

    def overlaps(self, i : 'Interval'):
        return min(self.max, i.max) - max(self.min, i.min) >= 0

    def __eq__(self, i : 'Interval'):
        return self.min == i.min and self.max == i.max
        

def main():
    i = Interval(2, 5)
    j = Interval(3, 6)
    print(i.overlaps(j))
    k = Interval(10, 15)
    print(i.overlaps(k))
    l = Interval(5, 7)
    print(l.overlaps(i))
    print("isinstance")
    print(isinstance(l, Interval))
    Interval(3, 1)
if __name__ == "__main__":
    main()
