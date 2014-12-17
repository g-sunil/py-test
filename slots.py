class python_slot(object):
    """docstring for python_slot
    @ http://tech.oyster.com/save-ram-with-python-slots/"""
    __slots__ = ['x', 'y']

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def prints(self, x):
        """"""
        print x, "<=--- prints"

a = python_slot(4, 6)
a.prints("python's style of print")
print dir(a)
