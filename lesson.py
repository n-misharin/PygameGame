class Summator:
    def __init__(self):
        pass

    def transform(self, n):
        return n

    def sum(self, n):
        g = 0
        for i in range(1, n + 1):
            g += self.transform(i)

        return g


class SquareSummator(Summator):
    def transform(self, n):
        return n ** 2


class CubeSummator(Summator):
    def transform(self, n):
        return n ** 3


a = CubeSummator()
print(a.sum(3))