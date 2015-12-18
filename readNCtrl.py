# Read js files and log the Controllers
import re
import sys


def capture_js_ctrl_medthods(cnt):
    if re.findall('Controller/([a-zA-Z]*)', cnt):
        if 'views' not in cnt.strip():
            jsm = cnt.split('/')[-1].split("'")
            jssm = jsm[0].split('"')[0].split('?')[0]
            with open('jsCtrlMethods.txt', 'a+') as myfile:
                if jssm+'\n' not in myfile.readlines():
                    myfile.write(jssm+'\n')


def capture_ctrl_medthods(cnt):
    if re.findall('def ([a-zA-Z]*)', cnt):
        jsm = cnt.split("(")[0].split(' ')[-1]
        with open('ctrlMethods.txt', 'a+') as myfile:
            if jsm+'\n' not in myfile.readlines():
                myfile.write(jsm+'\n')


def read_file(fname):
    with open(fname, 'r') as fobj:
        cnt = fobj.readlines()
    return cnt


def main():
    fname = sys.argv[1:]  # file names
    for echf in fname:
        cnt = read_file(echf)
        if '.js' in echf:
            for echline in cnt:
                capture_js_ctrl_medthods(echline)
        else:
            for echline in cnt:
                capture_ctrl_medthods(echline)

if __name__ == '__main__':
    main()
