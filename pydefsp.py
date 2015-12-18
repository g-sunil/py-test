import sys


class PytestCase(object):
    """docstring for PytestCase"""
    def __init__(self, arg):
        print 'safdsdfsd'
        super(PytestCase, self).__init__()
        self.arg = arg

    def __call__(self):
        print 'mmmm>>>>>>m'
        return

    def get_name(self):
        print sys._getframe().f_code.co_name

    def set_name(self):
        print

c = PytestCase(1)
c()
c.get_name()
