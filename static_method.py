class Adam(object):
    """docstring for Adam"""
    def __init__(self, name):
        self.name = name


class Cain(Adam):
    """docstring for Cain"""
    def __init__(self, age, *args):
        super(Cain, self).__init__(*args)
        self.age = age

    @staticmethod
    def stat():
        print "Creation"

    def clsm(self):
        print "Made"

# print '>>>>', type(Adam), dir(Adam)
# print '>>>>', type(Cain), dir(Cain)

a = Adam('Eve')
c = Cain(12, 'Eve')
print a.name, c.age, c.name, '\n', id(a.name), id(c.age), id(c.name), id(a), id(c)
a.name = 'Abel'
print a.name, c.age, c.name, '\n', id(a.name), id(c.age), id(c.name), id(a), id(c)

print Cain(12, 'Eve').stat()
print c.clsm()
# OutPut
# Eve 12 Eve
# 140113833811568 22422064 140113833811568 140113833817296 140113833817360
# Abel 12 Eve
# 140113833811760 22422064 140113833811568 140113833817296 140113833817360
