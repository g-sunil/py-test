class list_scope(object):
    """docstring for list_scope"""
    def __init__(self, x):
        super(list_scope, self).__init__()
        self.x = x
        print x, '-- int'

    def test1(self, x):
        x.append(1)
        print x, id(x), 'test1 id'

    def test2(self, x):
        x.append(2)
        print x, id(x), 'test2 id'

    def res(self, x):
        self.test2(x)
        self.test1(x)
        return x


l = [3, 4]
a = list_scope(l)
print a.res(l)
