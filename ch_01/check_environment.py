"""Check environment for following along with the text."""

from distutils.version import LooseVersion as Version
import importlib
import sys
import re


OK = '\x1b[42m[ OK ]\x1b[0m'
FAIL = '\x1b[41m[FAIL]\x1b[0m'

github_package_pattern = re.compile(r'(?:\/)([\w*\-*]*)(?:\.git)')

def run_checks(raise_exc=False):
    """
    Check that the packages we need are installed and the Python version is good.

    Parameters
    ----------
    raise_exc : bool, default ``False``
        Whether to raise an exception if any of the packages doesn't
        match the requirements (used for GitHub Action).
    """
    failures = []

    # check the python version
    print('Using Python in %s:' % sys.prefix)
    if Version(sys.version) >= '3.7.1' and Version(sys.version) < '3.10.0':
        print(OK, 'Python is version %s\n' % sys.version)
    else:
        print(FAIL, 'Python version >= 3.7.1 and < 3.10.0 is required, but %s is installed.\n' % sys.version)
        failures.append('Python')

    # read in the requirements
    with open('../requirements.txt', 'r') as file:
        requirements = {}
        for line in file.read().splitlines():
            github_package = re.search(github_package_pattern, line)
            if github_package:
                pkg = github_package.group(1).replace('-', '_')
                version = None
            else:
                if line.startswith('./'):
                    line = line.replace('./', '')
                try:
                    if '>=' in line:
                        pkg, versions = line.split('>=')
                        version = versions.split(',<=')
                    else:
                        pkg, version = line.split('==')
                except ValueError:
                    pkg, version = line, None
                if pkg == 'imbalanced-learn':
                    pkg = 'imblearn'
                elif pkg == 'scikit-learn':
                    pkg = 'sklearn'

            requirements[pkg.replace('-', '_')] = version

    # check the requirements
    for pkg, req_version in requirements.items():
        try:
            mod = importlib.import_module(pkg)
            if req_version:
                version = mod.__version__
                if isinstance(req_version, list):
                    min_version, max_version = req_version
                    if Version(version) < min_version or Version(version) > max_version:
                        print(FAIL, '%s version >= %s and <= %s is required, but %s installed.' % (pkg, min_version, max_version, version))
                        failures.append(pkg)
                        continue
                else:
                    if Version(version) != req_version:
                        print(FAIL, '%s version %s is required, but %s installed.' % (pkg, req_version, version))
                        failures.append(pkg)
                        continue
            print(OK, '%s' % pkg)
        except ImportError:
            print(FAIL, '%s not installed.' % pkg)
            failures.append(pkg)

    if failures and raise_exc:
        raise Exception(
            'Environment failed inspection due to incorrect versions '
            f'of {len(failures)} item(s): {", ".join(failures)}.'
        )

if __name__ == '__main__':
    run_checks(raise_exc=True)
