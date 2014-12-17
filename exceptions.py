import sqlite3, traceback, sys


class excetions(object):
    """docstring for excetions"""
    def __init__(self, arg):
        super(excetions, self).__init__()
        self.arg = arg

    def conect(self):
        conn = sqlite3.connect('test.db')
        return conn

    def raise1(self):
        ll = []
        try:
            ll = self.raise2(ll)
            conn = self.conect()
            cr = conn.cursor()
            print cr.execute("select * from test_table").fetchall()
        except Exception as e:
            print '=======', e
            l = {'res': str(e)}
            ll.append(l)
        print 'after failer ************', ll

    def raise2(self):
        conn = self.conect()
        cr = conn.cursor()
        try:
            cr.execute("insert into test_table values('1','two')")
        except Exception as e:
            print sys.exc_info(), 'sys.exc_info()'
            print e, 'e---- \n\n'
        try:
            print "insert into test_table values(2,'two')"
            cr.execute("insert into test_table values(2,'two')")
        except Exception as e:
            print sys.exc_info(), 'sys.exc_info()'
            print e, 'e----\n\n'
        try:
            print "insert into test_table values(1,'one')"
            cr.execute("insert into test_table values(1,'one')")
        except Exception as e:
            print sys.exc_info(), 'sys.exc_info()'
            print e, 'e----\n\n'
        conn.commit()
        conn.close()
        return 1

    def raise5(self):
        for i in range(0, 10):
            print 'te'
        return None

    def raise4(self):
        (a, b) = self.raise3()
        print self.raise5()

    def raise3(self):
        try:
            int('asda')
        except Exception as e:
            return e
            # raise Exception(e)

ee = excetions(1)
ee.raise2()
