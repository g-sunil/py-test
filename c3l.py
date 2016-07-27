class A(object):
    pass


class B(A):
    pass


class C(A):
    pass


class D(B, A, C):
    pass


# class E(C, B, A):
#     pass

# class F(B, C, A):
#     pass





# C3 wants to enforce two incompatible constraints in this case:

# It wants to put C before A because A is a base class of C
# It wants to put A before C because of D's base class ordering
