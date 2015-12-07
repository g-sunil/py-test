import pprint


class A(object):
    pass


class B(A):
    pass


class C(A):
    pass


class D(B):
    pass


class E(C):
    pass


class F(D):
    pass


class G(E):
    pass


class H(F, G):
    pass


pprint.pprint(H.__mro__)

#     A
# B       C
# D       E
# F       G
#     H
