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


class D(B):
    """docstring for D"""
    def where(self):
        print "I am in D"


class E(C):
    """docstring for D"""
    def where(self):
        print "I am in D"


class F(D, E):
    """docstring for D"""
    def where(self):
        print "I am in D"


pprint.pprint(F.__mro__)

#     A
# B       C
# D       E
#     F
