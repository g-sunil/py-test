class A:
    def who_am_i(self):
        print("I am a A")


class B(A):
    def who_am_i(self):
        print("I am a B")
    pass


class C(A):
    def who_am_i(self):
        print("I am a C")


class D(B, C):
    def who_am_i(self):
        print("I am a D")
    pass

d1 = D()
d1.who_am_i()


# Python 2.2 instead does not raise an exception, but chooses an ad hoc ordering (CABXYO in this case).
