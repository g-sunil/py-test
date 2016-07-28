"""
For Linux: Script to parse the html and report the missed jlabels
# <j-label jname="encounter"></j-label> Start Date
"""

import os
import re
import requests
import ast

from optparse import OptionParser
from lxml import etree
from glob import iglob
from collections import defaultdict
from itertools import chain
from yattag import Doc


def remote_jlables():
    ip_port = raw_input('Enter app IP with port no (E.g., 127.0.0.1:4547): ')
    user = raw_input('Enter app Username for the server (E.g.,zeadmin): ')
    import getpass
    pwd = getpass.getpass()
    path = 'ZeCache/getAllLabels'
    url = 'http://%s:%s/cms/ZeUI/views/%s' % (ip_port.split(':')[0], ip_port.split(':')[1], path)
    try:
        response = requests.get(url, auth=(user, pwd))
    except Exception:
        raise Exception("Check if IP/Port is correct with a valid username and/or password")
    return ast.literal_eval(response.content)


def local_jlables():
    tree = etree.parse('/home/gsunil/Desktop/scripts/jivaLabel.xml', etree.XMLParser())
    return dict((ele.tag, ele.text) for ele in tree.getroot().getchildren())


def get_jlabels():
    to_get_rmt = raw_input('Get J-lables from remote IP? (y/n): ')
    if not to_get_rmt or not ('y' in to_get_rmt or 'n' in to_get_rmt):
        get_jlabels()
    if 'y' in to_get_rmt:
        return remote_jlables()
    else:
        return local_jlables()


def main():
    repo_dict = defaultdict(dict)
    j_label_dict = get_jlabels()
    # src/jivacore.ngui/jivacore/ngui/src/partials/
    # src/jivabase.ace/jivabase/ace/ui/src/ace/partials/
    partials_path = "/*/*/*/src/partials/*.html"
    sub_partials_path = "/*/*/*/ui/src/*/partials/*.html"

    partials = chain(iglob(options.source + partials_path), iglob(options.source + sub_partials_path))
    for file_path in partials:
        html_dict = defaultdict(dict)
        tags_dict = defaultdict(set)
        parsed_doc = etree.parse(file_path, etree.HTMLParser())
        file_name = file_path.split('/')[-1]
        repo_name = file_path.split('src')[1].split('/')[1]
        try:
            get_all_tags = parsed_doc.getroot().findall('.//')  # Gets all the tags in the HTML
        except:
            pass
        for tag in get_all_tags:
            if tag.text and tag.text.strip():  # strip(), returns '' if new line is encountred
                if '{{' in tag.text:  # Interpolations were used to parse the text in htmls
                    continue
                for jkey, jval in j_label_dict.iteritems():
                    if re.search(r'^\b%s\b' % jval.strip().lower(), tag.text.strip().lower()) \
                       and tag.attrib.get('jname', '') != jkey:
                        tags_dict[jval.strip()].add(etree.tostring(tag).strip())
        html_dict[file_name].update(tags_dict) if tags_dict else None
        repo_dict[repo_name].update(html_dict) if html_dict else None
    write_to_file(**repo_dict)


def write_to_file(**result_data):
    # Final_dict = {'jiva.ace': {'view.html': {'Episode': ['tag1', 'tag1']} } }
    ###############################
    # yattag code for creating htmls
    ###############################
    doc, tag, text = Doc().tagtext()
    doc.asis('<!DOCTYPE html>')
    td_th_style = 'border: 1px solid #dddddd; text-align: left; padding: 8px;'  # th, td style
    table_style = 'font-family: arial, sans-serif; border-collapse:collapse; width:100%'  # table style
    with tag('html'):
        with tag('body'):
            for repo in result_data:
                with tag('h2'):
                    text('Jlabel Report - %s' % repo)
                    for _file, _data in result_data[repo].iteritems():
                        with tag('h4'):
                            text(_file)
                        with tag('table',
                                 ('style', table_style)
                                 ):
                            with tag('tr'):
                                with tag('th',
                                         ('style', td_th_style + 'width:30%')
                                         ):
                                    text('J-Label')
                                with tag('th',
                                         ('style', td_th_style)
                                         ):
                                    text('Tag Content')
                            for key, val in _data.iteritems():
                                with tag('tr'):
                                    with tag('td',
                                             ('style', td_th_style)
                                             ):
                                        text(str(key))
                                    with tag('td',
                                             ('style', td_th_style)
                                             ):
                                        for v in val:
                                            with tag('p'):
                                                text(str(v))

    with open(os.getcwd() + os.sep + 'result.html', 'w') as file_buffer:
        file_buffer.write(doc.getvalue())
        ###############################

if __name__ == '__main__':
    parser = OptionParser(usage="usage: %prog [options] filename",
                          version="%prog 1.0")
    parser.add_option("-s", "--source", action="store", help="Input directory path till src", default="temp")
    parser.add_option("-i", "--server", action="store", help="Server IP:Port No", default="0.0.0.0:4547")
    # parser.add_option("-d", "--dest", action="store", help="Output directory path", default="temp")
    (options, args) = parser.parse_args()
    if not os.path.exists(options.source):
        parser.error("wrong path - Enter a valid path")
    main()
