import os
import sys
import ast
import glob
import requests
from lxml import etree
from BeautifulSoup import BeautifulSoup as Parser
from ConfigParser import SafeConfigParser


class Partial(object):

    def __init__(self, repo, html_path, jivaLabels):
        self.repo = repo
        self.filepath = html_path
        self.html = Parser(open(self.filepath).read())
        self.name = self.filepath[self.filepath.find(self.repo):]
        self.criteria = jivaLabels.values() + jivaLabels.keys()
        self.issues = {}
        self.parserissues = {}
        self.issue_count = 0

    def get_issues(self):
        self._find_in_anchor_tags()
        self._find_in_tabs()
        self._find_in_table()
        self._find_in_labels()
        self._find_in_buttons()

    def _find_issues(self, tag):
        l = []
        if tag.string:
            s_clean = tag.string.strip()
            if not (len(s_clean) == 1 and ord(s_clean) > 128):
                contents = str(s_clean).split(' ')
                l = [tag for content in contents if content in self.criteria]
                self.issue_count += len(l)
        elif tag.contents:
            for content in tag.contents:
                if isinstance(content, unicode):
                    content = content.strip()
                    if str(content.strip()) in self.criteria:
                        l.extend(tag)
                        self.issue_count += 1
                elif content.span:
                    l += self._find_issues(content.span)

        return l

    def _append_to_issue_list(self, issue_type, tags):
        for tag in tags:
            try:
                issues = self._find_issues(tag)
                if issues:
                    self.issues.setdefault(issue_type, []).extend(issues)
            except Exception:
                self.parserissues.setdefault(issue_type, []).extend(tag)

    def _find_in_anchor_tags(self):
        tags = self.html.findAll('a')
        self._append_to_issue_list('anchor-tags', tags)

    def _find_in_tabs(self):
        tabs = self.html.findAll('tab')
        issues = []
        for tab in tabs:
            try:
                heads = str(tab['heading']).split()
            except:
                # import pdb; pdb.set_trace()
                heads = []
            issues += [tab for head in heads if head in self.criteria]

        if issues:
            self.issue_count += len(issues)
            self.issues.setdefault('tab-headings', []).extend(issues)

    def _find_in_table(self):
        tables = self.html.findAll('table')
        for table in tables:
            headers = table.findAll('th')
            for header in headers:
                if header.span:
                    issues = self._find_issues(header.span)
                    if issues:
                        self.issues.setdefault('table-header-spans', []).extend(issues)

            bodies = table.findAll('tbody')
            for body in bodies:
                gear_spans = body.findAll('span')
                self._append_to_issue_list('table-body-gear-icon-spans', gear_spans)

    def _find_in_labels(self):
        labels = self.html.findAll('label')
        self._append_to_issue_list('labels', labels)

    def _find_in_buttons(self):
        buttons = self.html.findAll('button')
        self._append_to_issue_list('buttons', buttons)


def get_jivaLabels(ip, port):
    """
        Get the jivaLabels for a specified JIVA instance.
        Defaults to dev-instance IP/port.
        Fires query via the REQUESTS module.
        Username/password need to be provided in such cases
        (Application login credentials)
    """
    user = raw_input('Enter app Username for the server (E.g.,zeadmin): ')
    import getpass
    pwd = getpass.getpass()
    path = 'ZeCache/getAllLabels'
    url = 'http://%s:%s/cms/ZeUI/views/%s' % (ip, port, path)

    try:
        response = requests.get(url, auth=(user, pwd))
    except Exception:
        raise Exception("Check if IP/Port is correct with a valid username and/or password")

    return ast.literal_eval(response.content)


def process(repos=[]):
    """
        Returns all the partials for a specified repository.
        Extended to supply via a configuration to check for all configured repos
    """

    partials_loc = 'src/%s/*/*/ui/src/*/'

    if repos:
        versions = repos
    else:
        app_versions = os.path.join(os.getcwd(), 'etc/jiva_app_versions.cfg')
        parser = SafeConfigParser()
        parser.read(app_versions)
        versions = parser.options('versions')

    issues = {}
    for version in versions:
        print "Looking into", version
        partial_path = partials_loc % (version)

        # __dir__ must be where the jiva_buildout resides!
        partials_dir = glob.glob(os.path.join(os.getcwd(), partial_path, 'partials/*.html'))
        partials_sub_dirs = glob.glob(os.path.join(os.getcwd(), partial_path, '*/partials/*.html'))
        partials = partials_dir + partials_sub_dirs

        for partial in partials:
            f = Partial(version, partial, jLabels)
            f.get_issues()

            if f.issues:
                issues.setdefault(version, {}).setdefault(f.name, {}).update({
                    'count': f.issue_count,
                    'anchor-tags': f.issues.get('anchor-tags', None),
                    'buttons': f.issues.get('buttons', None),
                    'labels': f.issues.get('labels', None),
                    'tab-headings': f.issues.get('tab-headings', None),
                    'table-body-gear-icon-spans': f.issues.get('table-body-gear-icon-spans', None),
                    'table-header-spans': f.issues.get('table-header-spans', None),
                    'parser-problems': f.parserissues
                })

    return issues


if __name__ == '__main__':
    sys.path[0:0] = [os.path.dirname(__file__)]
    if sys.argv[1:]:
        jLabels = get_jivaLabels(ip=sys.argv[1:][0], port=sys.argv[1:][1])
    else:
        tree = etree.parse('/home/gsunil/Desktop/scripts/jivaLabel.xml', etree.XMLParser())
        jLabels = dict((ele.tag, ele.text) for ele in tree.getroot().getchildren())
        jLabels.update({'claimant': 'Member', 'member': 'Member', 'encounter': 'Episode'})
    # repos = raw_input('Enter Repo(s) for which j-Label is to be checked. Press enter for all repos:')
    # if repos:
    #     repos = repos.split(' ')

    issues = process()
    import pdb; pdb.set_trace()
    from report_file import ReportWriter
    report = ReportWriter('j-Label Checks', 'j-label-issues.html')
    report.write_to_html(issues)
