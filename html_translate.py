import os
import re
from glob import iglob
from lxml import etree, html
from optparse import OptionParser
from collections import defaultdict

final_dict = defaultdict(list)

# No LXML fails
# if class is altered - added - path fails

def jhelp():
    # /home/gsunil/instances/jiva_poc_old/src/jivabase.notes/jivabase/notes/ui/src/notes/partials/widgets/view-all-notes.html
    if 1:
    # for file_path in iglob(options.source + "/*/*/*/ui/src/*/partials/*.html"):
        # print file_path
        file_content = html.parse('/home/gsunil/Desktop/scripts/test.html')
        import pdb; pdb.set_trace()
        # repo_name = file_path.split('/')[6]
        try:
            # span_list = file_content.find("//div[@class='modal-header']/span")
            file_content.findAll("//div[@class='modal-header']/span")
            import pdb; pdb.set_trace()
        except AssertionError:
            # Incorrect htmls
            span_list = div_list = []
        if div_list and span_list:
            print file_path
            print etree.tostring(div_list[0])
            import pdb; pdb.set_trace()
            jtag = filter(lambda jt: 'j-help' in jt.attrib and jt.attrib['j-help'], span_list)
        # if not jtag or span_list:
        #     import pdb; pdb.set_trace()

def main():
    for file_path in iglob(options.source + "/*/*/*/ui/src/*/partials/*.html"):
        file_content = html.parse(file_path)
        try:
            span_list = file_content.xpath("//div[@class='modal-header']/span")
        except AssertionError:
            span_list = []
        for span in span_list:
            if not ('j-help' in span.attrib and span.attrib['j-help']):
                if options.fix:
                    import pdb; pdb.set_trace()
                    parent_div = span_list[0].getparent()
                    parent_div.insert(-1, etree.DIV("<span j-help='%s'></span>" % file_path.split('src')[-1]
                                                        .replace('.html', '').replace('/', '', 1)))
                    # etree.ElementTree(parent_div).write(file_content, pretty_print=True)
                    with open(file_path, 'w') as f:
                        f.write(etree.tostring(file_content, pretty_print=True))
                else:
                    repo_name = file_path.split('/')[6]
                    final_dict[repo_name].append(file_path)

    for repo, defs in final_dict.iteritems():
        if defs:
            with open(options.dest + '/' + str(repo) + '.txt', 'w+') as write_to_file:
                write_to_file.write(str(defs) + '\n')


def regs():
    for file_path in iglob(options.source + "/*/*/*/ui/src/*/partials/*.html"):
        old_data = new_data = pin_me = None
        with open(file_path, 'r') as file:
            file_buffer = file.read()
            tag_pattrn = re.compile(r'<div\sclass=(\'|\")[\s,\w]*modal-header[\s,\w]*(\'|\")>(.|\n)*?</div>',
                                    re.I | re.M)
            # <span ng-if="!mbrAbstractCtrl.printAbstract" j-help="member/partials/member-abstract"></span>

            jtag_pattrn = re.compile(r'\s*<span(.)*j-help=', re.I)
            matched = re.search(tag_pattrn, file_buffer)
            if matched:  # HTML has modal-header
                old_data = matched.group()  # Div container
                jtag_old = filter(lambda i: re.search(jtag_pattrn, i), old_data.split('\n'))
                if jtag_old:
                    jtag_old = jtag_old[0]
                else:
                    pin_me = 1
                    jspan = "%s<span j-help='%s'></span>" %\
                        (' '*12, file_path.split('src')[-1].replace('.html', '').replace('/', '', 1))
                    new_data = re.sub(r'</button>',
                                      '</button>\n%s' % jspan, old_data)

        if old_data and new_data and pin_me:
            with open(file_path, 'w') as file:
                file.write(file_buffer.replace(old_data, new_data))

if __name__ == '__main__':
    parser = OptionParser(usage="usage: %prog [options] filename",
                          version="%prog 1.0")
    parser.add_option("-s", "--source", action="store", help="Input directory path till src", default="temp")
    parser.add_option("-d", "--dest", action="store", help="Output directory path", default="temp")
    parser.add_option("-f", "--fix", action="store_true", help="Output directory path", default=False)
    (options, args) = parser.parse_args()
    if not os.path.exists(options.source):
        parser.error("wrong path - Enter a valid path")
    if not os.path.exists(options.dest):
        try:
            os.makedirs(options.dest)
        except OSError as Exception:
            parser.error("wrong path - Enter a valid path")
    regs()
    # jhelp()
