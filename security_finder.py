"""
For Linux: Script to find the method without security declaration.
"""

import re
import glob
import os
from optparse import OptionParser
from collections import defaultdict

final_dict = defaultdict(list)


def main():
    # generator, search immediate subdirectories
    for file_path in glob.iglob(options.source + "/*/Products/*/*.py"):
        if file_path.endswith("Controller.py") or file_path.endswith("Ctrl.py"):
            with open(file_path, 'r') as file:
                file_content = file.read()
                # regex patterns
                pattern_security = re.compile(r'security.\w+\(\'\w+\s\w+\s\w+\'\,\s*\'\w+\'\)', re.I | re.M)
                pattern_private = re.compile(r'security.\w+\(\'\w+\'\)', re.I | re.M)
                pattern_method = re.compile(r'^\s{4}def\s\w+\(self.*\)\:', re.I | re.M)  # Ignore inner methods

                # search/get exact method name - private security
                # security.declarePrivate('_xxx')
                private_securities = map(lambda i: re.search(r'(\w+).(\w+)..(\w+)', i).group(3),
                                         re.findall(pattern_private, file_content))

                # search/get exact method name - protected security
                # security.declareProtected('Xx xxx xxxxxx', 'xxx_xxx')
                all_securities = map(lambda i: re.search(r'\w+', i.split(',')[-1]).group(),
                                     map(lambda w: re.sub(r'\n\s*', ' ', w), re.findall(pattern_security,
                                                                                        file_content)))
                all_defs = map(lambda v: v.group(2), map(lambda i: re.search(r'(def)\s(\w+)', i),
                                                         re.findall(pattern_method, file_content)))
                all_securities.extend(private_securities)

                # remove magic methods and zope methods. - Securities doesn't apply
                all_defs = filter(lambda f: not (f.startswith('__') or f.startswith('manage_')), all_defs)

                repo_name = file_path.split('/')[6]
                final_dict[repo_name].extend(set(all_defs) - set(all_securities))

    for repo, defs in final_dict.iteritems():
        if defs:
            with open(options.dest + '/' + str(repo) + '.txt', 'w+') as write_to_file:
                write_to_file.write(str(defs) + '\n')

if __name__ == '__main__':
    parser = OptionParser(usage="usage: %prog [options] filename",
                          version="%prog 1.0")
    parser.add_option("-s", "--source", action="store", help="Input directory path till src", default="temp")
    parser.add_option("-d", "--dest", action="store", help="Output directory path", default="temp")
    (options, args) = parser.parse_args()
    if not os.path.exists(options.source):
        parser.error("wrong path - Enter a valid path")
    if not os.path.exists(options.dest):
        try:
            os.makedirs(options.dest)
        except OSError as Exception:
            parser.error("wrong path - Enter a valid path")
    main()
