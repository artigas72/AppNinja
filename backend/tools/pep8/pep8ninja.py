import sys
from os import walk
from os.path import isdir, join
import pep8


class NinjaChecker(pep8.Checker):

    def __init__(self, filename):
        pep8.Checker.__init__(self, filename)

    def report_error(self, line_number, offset, text, check):
        return pep8.Checker.report_error(self, line_number, offset, text, check)


if __name__ == '__main__':
    def usage():
        print('Usage: python pep8ninja.py <file_or_folder_to_check>*')
        print('Folders will be checked recursively.')
        sys.exit(1)

    if len(sys.argv) < 2:
        usage()
    if sys.argv == 2:
        targets = sys.argv[-1]
    else:
        targets = sys.argv[-1].split()

    def check(fn):
        try:
            checker = NinjaChecker(fn)
        except IOError:
            # File couldn't be opened, so was deleted apparently.
            # Don't check deleted files.
            return 0
        return checker.check_all()

    errors = 0
    exclude_dirs = ['account/migrations']
    exclude_files = []

    for target in targets:
        if isdir(target):
            for dirpath, dirnames, filenames in walk(target):
                cont = False
                for pat in exclude_dirs:
                    if pat in dirpath:
                        cont = True
                        break
                if cont:
                    continue
                for filename in filenames:
                    if not filename.endswith('.py'):
                        continue
                    cont = False
                    complete_filename = join(dirpath, filename)
                    for pat in exclude_files:
                        if complete_filename.endswith(pat):
                            cont = True
                    if cont:
                        continue

                    errors += check(complete_filename)
        else:
            # Got a single file to check
            for pat in exclude_dirs + exclude_files:
                if pat in target:
                    break
            else:
                if target.endswith('.py'):
                    errors += check(target)

    # If errors is 0 we return with 0. That's just fine.
    sys.exit(errors)