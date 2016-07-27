class OptIf(object):
    """docstring for OptIf"""

    def opt_me(self, ext):
        if ext == 'CM':
            rec = self.call_cm()
        if ext == 'MM':
            rec = self.call_mm()
        if ext == 'DM':
            rec = self.call_dm()
        return rec

    def opt_me_for(self, ext):
        md_ap = {'CM': self.call_cm, 'DM': self.call_dm, 'MM': self.call_mm}
        print md_ap[ext](1, 2)

    def call_cm(self, cm, ad):
        print 'I am in CM'

    def call_mm(self, mm, ax):
        print "I am in MM"

    def call_dm(self, dm, md):
        print "I am in DM"


o = OptIf()
o.opt_me_for('CM')
