from __future__ import print_function
from distutils.version import LooseVersion as Version
import importlib
import sys
import re

OK = '\x1b[42m[ OK ]\x1b[0m'
FAIL = '\x1b[41m[FAIL]\x1b[0m'

pattern = re.compile(r'(?:\/)([\w*\-*]*)(?:\.git)')

def run_checks():
    """Check that the packages we need are installed and the Python version is high enough."""
    # check the python version
    print('Using Python in %s:' % sys.prefix)
    if Version(sys.version) >= '3.6':
        print(OK, 'Python is version %s\n' % sys.version)
    else:
        print(FAIL, 'Python version 3.6+ is required, but %s is installed.\n' % sys.version)

    # read in the requirements
    with open('../requirements.txt', 'r') as file:
        requirements = {}
        for line in file.read().splitlines():
            try:
                pkg, version = line.split('==')
                if pkg == 'imbalanced-learn':
                    pkg = 'imblearn'
                elif pkg == 'scikit-learn':
                    pkg = 'sklearn'
            except ValueError:
                pkg = re.search(pattern, line).group(1).replace('-', '_')
                version = None

            requirements[pkg.replace('-', '_')] = version

    # check the requirements
    for pkg, req_version in requirements.items():
        try:
            mod = importlib.import_module(pkg)
            if req_version:
                version = mod.__version__
                if Version(version) != req_version:
                    print(FAIL, '%s version %s is required, but %s installed.' % (pkg, req_version, version))
            print(OK, '%s' % pkg)
        except ImportError:
            print(FAIL, '%s not installed.' % pkg)

if __name__ == '__main__':
    run_checks()