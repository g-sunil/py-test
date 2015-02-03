import re

s = "importing re testing 1"
rs = re.search(r"^\s*import\s*", s)
print rs.group(0), '\n--------------------'

dg = "dog cat dog"
dg_mct = re.match(r"dog", dg)
print dg_mct.group(), dg_mct.start(), dg_mct.end(), '\n--------------------'

dg_srh = re.search(r"cat", dg)
print dg_srh.group(), '\n--------------------'

dg_find = re.findall(r"dog", dg)
print dg_find

no = "The number that are i like are 1 and 10 and sometimes 20 also ooh oh i forgot i like 7 more"
fnd_no = re.findall('[0-9]+', no)
print fnd_no

# greedy matching
x = "From: Using the: Character"
y = re.findall('^F.+:', x)
print y, '\n--------'

# non-greedy matching
z = re.findall('^F.+?:', x)
print z

html = "<html><body><span fontface='cosmo' width='5px'>hi! you there?</span>\
        <span fontface='cosmo' width='6px'>hello! yes i am :)</span></body></html>"
txt = re.findall('<span.+?</span>', html)
print txt

# extract the phrase
frm = "From snl.job@gmail.com this is sent and sunil.techspk@gmail.com has received it"
extfrm = re.findall('\S+@\S+', frm)
print extfrm
