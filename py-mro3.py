import pprint


class A(object):
    pass


class B(A):
    pass


class C(A):
    pass


class D(B, C):
    pass


class E(D):
    pass


class F(D):
    pass


class G(E, F):
    pass


#     A
# B       C
#     D
# E       F
#     G
pprint.pprint(G.__mro__)

# output:

# (<class '__main__.G'>,
#  <class '__main__.E'>,
#  <class '__main__.F'>,
#  <class '__main__.D'>,
#  <class '__main__.B'>,
#  <class '__main__.C'>,
#  <class '__main__.A'>,
#  <type 'object'>)
