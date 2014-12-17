# File: traceback-example-3.py
import traceback
import sys


def function():
    int('df')

try:
    function()
except:
    print sys.exc_info(), '<---------- '
    # for file, lineno, function, text in traceback.extract_tb(info[2]):
        # print file, "line", lineno, "in", function
        # print "=>", repr(text)
        # pass
    # print "** %s: %s" % info[:]

## traceback-example-3.py line 8 in ?
## => 'function()'
## traceback-example-3.py line 5 in function
## => 'raise IOError, "an i/o error occurred"'
## ** exceptions.IOError: an i/o error occurred
