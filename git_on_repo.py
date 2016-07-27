import os
import sys

try:
    dir_path = sys.argv[1]
except:
    print '##############################'
    print 'Usage'
    print 'python git_on_repo <file-path>'
    print '##############################'
for dirp in os.listdir(dir_path):
    path = dir_path + '/' + dirp
    if os.path.isdir(path):
        os.chdir(path)
        print 'Checking out in ...', path
        os.popen('git co -- .')
        os.popen('git pull')
