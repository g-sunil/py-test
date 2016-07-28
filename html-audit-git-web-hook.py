"""
For Linux: Script to parse the html and report the missed jvars for <select> tags
{file_name: 'Line No - line'}
"""

import os
import re

from optparse import OptionParser
from lxml import etree as ET
from glob import iglob
from collections import defaultdict
from collections import OrderedDict

log_result = defaultdict(list)
msgs = {
    'translate': 'Translate is missed',
    'jvar': 'Jvar is missed',
    'jlabel': 'Jlabel is missed',
    'jhelp': 'Jhelp is missed'
}


def _jvar(parsed_cnt):
    all_select_tags = []
    try:
        # Gets all the select tags in the HTML
        all_select_tags = parsed_cnt.getroot().findall('.//select')
    except:
        pass
    return [str(tag.sourceline) + ' : ' + msgs['jvar'] for tag in all_select_tags]


def _get_free_text_tags(parsed_cnt):
    all_text_tags = parsed_cnt.getroot().xpath('//text()')  # Gets all the text tags
    # filter out the \n and interpolations '{{' and '}}' new lines -- EOL and get the parent tag
    return map(lambda tag: tag.getparent(), filter(lambda txt: txt.strip() and
                                                   not (txt.startswith('{{') or txt.endswith('}}')),
                                                   all_text_tags))


def _jlabel(parsed_cnt):
    # Needs to refer the valid jlabels
    tree = ET.parse('/home/gsunil/Desktop/scripts/jivaLabel.xml', ET.XMLParser())
    j_label_dict = dict((ele.tag, ele.text) for ele in tree.getroot().getchildren())
    missed_jlable_tag = OrderedDict()
    try:
        text_tags = _get_free_text_tags(parsed_cnt)
        for jkey, jval in j_label_dict.iteritems():
            for tag in text_tags:
                if re.search(r'^\b%s\b' % jval.strip().lower(), tag.text.strip().lower()) \
                   and tag.attrib.get('jname', '') != jkey:
                    missed_jlable_tag[tag.sourceline] = msgs['jlabel']

    except:
        pass
    return [str(line) + ' : ' + msg for line, msg in missed_jlable_tag.items()]


def _jhelp(parsed_cnt):
    span_tags = []
    try:
        # Get all span tags in `modal-header` class
        all_span_tags = parsed_cnt.getroot().findall(".//div[@class='modal-header']//span")
        span_tags = filter(lambda tag: not tag.attrib.get('j-help'), all_span_tags)
    except:
        pass
    return [str(tag.sourceline) + ' : ' + msgs['jhelp'] for tag in span_tags]


def _translate(parsed_cnt):
    text_tags = []
    try:
        text_tags = _get_free_text_tags(parsed_cnt)
    except:
        pass
    return [str(tag.sourceline) + ' : ' + msgs['translate'] for tag in text_tags if 'translate' not in tag.attrib]


def main():
    partials_path = "%s/*.html" % options.source
    for file_path in iglob(partials_path):
        parsed_doc = ET.parse(file_path, ET.HTMLParser())
        file_name = file_path.split('/')[-1]
        log_result[file_name].extend(_jvar(parsed_doc) + _jlabel(parsed_doc) +
                                     _translate(parsed_doc) + _jhelp(parsed_doc))
    print_to_console(log_result)


def print_to_console(log_result):
    for _file, _data in log_result.iteritems():
        for d in _data:
            print _file, d  # Need to print this to console


if __name__ == '__main__':
    parser = OptionParser(usage="usage: %prog [options] filename",
                          version="%prog 1.0")
    parser.add_option("-s", "--source", action="store", help="Input Directory Path")
    (options, args) = parser.parse_args()
    if not os.path.exists(options.source):
        parser.error("wrong path - Enter a valid path")
    main()
