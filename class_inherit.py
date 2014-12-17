class A(object):
    """docstring for A"""

    def __init__(self):
        # self.x = x
        # self.y = y
        super(A, self).__init__()

    def add(self, x, y):
        return x+y


class B(A):
    """docstring for B"""

    def __init__(self):
        super(B, self).__init__()
        # self.x = x
        # self.y = y

    def add(self, x, y):
        return x*y

b = B()
a = A()
print b.add(3, 3), '<--- Overiding the add method of class A'
print a.add(3, 3)
