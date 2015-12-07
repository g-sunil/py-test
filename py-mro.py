import pprint


class A(object):
    """docstring for A"""
    def where(self):
        print "I am in A"


class B(A):
    """docstring for B"""
    def where(self):
        print "I am in B"


class C(A):
    """docstring for C"""
    def where(self):
        print "I am in C"


class D(B, C):
    """docstring for D"""
    def where(self):
        print "I am in D"


# a = A()
# d = D()
pprint.pprint(D.__mro__)
# d.where()

#     A
# B       C
#     D


# output:

# (<class '__main__.D'>,
#  <class '__main__.B'>,
#  <class '__main__.C'>,
#  <class '__main__.A'>,
#  <type 'object'>)
