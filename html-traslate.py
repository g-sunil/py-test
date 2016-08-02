"""
For Linux: Script to parse the html and report the missed translates for the free text
"""

import os
import re

from glob import iglob
from lxml import etree
from optparse import OptionParser
from collections import defaultdict
from itertools import chain
from yattag import Doc


def main():
    repo_dict = defaultdict(dict)
    partials_path = "/*/*/*/src/partials/*.html"
    sub_partials_path = "/*/*/*/ui/src/*/partials/*.html"

    partials = chain(iglob(options.source + partials_path), iglob(options.source + sub_partials_path))
    for file_path in partials:
        html_dict = defaultdict(set)
        parsed_doc = etree.parse(file_path, etree.HTMLParser(remove_blank_text=True))
        file_name = file_path.split('/')[-1]
        repo_name = file_path.split('src')[1].split('/')[1]
        try:
            # Gets all the spans in the modal-header div
            all_text_tags = parsed_doc.getroot().xpath('//text()')  # Gets all the text tags
            # filter out the \n and interpolations '{{' and '}}' new lines -- EOL and get the parent tag
            # Ignore text in script and style tags
            # re.sub('[^A-Za-z]+', '', txt) -- remove all the special charators and numbers which needs no translations
            free_text_tags = map(lambda tag: tag.getparent(),
                                 filter(lambda tst: re.sub('[^A-Za-z]+', '', tst),
                                        filter(lambda txt: txt.strip() and
                                               '{{' not in txt and
                                               txt.getparent().tag not in ('style', 'script') and
                                               isinstance(txt, str),
                                               all_text_tags)))

            for tag in free_text_tags:
                if 'translate' not in tag.attrib:
                    html_dict[file_name].add(etree.tostring(tag).strip())
        except:
            pass
        repo_dict[repo_name].update(html_dict) if html_dict else None
    write_to_file(**repo_dict)


def write_to_file(**result_data):
    # Final_dict = {'jivabase.ace': {'view.html': ['tag1', 'tag1'] } }
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
                    text('Translate Report - %s' % repo)
                with tag('table',
                         ('style', table_style)
                         ):
                    with tag('tr'):
                        with tag('th',
                                 ('style', td_th_style + 'width:30%')
                                 ):
                            text('File Name')
                        with tag('th',
                                 ('style', td_th_style)
                                 ):
                            text('Tag Content')
                    for _file, _data in result_data[repo].iteritems():
                        with tag('tr'):
                            with tag('td',
                                     ('style', td_th_style)
                                     ):
                                text(_file)
                            with tag('td',
                                     ('style', td_th_style)
                                     ):
                                for v in _data:
                                    with tag('p'):
                                        text(str(v))

    with open(os.getcwd() + os.sep + 'reports' + os.sep + 'jtrans-report.html', 'w') as file_buffer:
        file_buffer.write(doc.getvalue().decode("utf-8"))
        ###############################

if __name__ == '__main__':
    parser = OptionParser(usage="usage: %prog [options] filename",
                          version="%prog 1.0")
    parser.add_option("-s", "--source", action="store", help="Input directory path till src", default="temp")
    (options, args) = parser.parse_args()
    if not os.path.exists(options.source):
        parser.error("wrong path - Enter a valid path")
    main()
