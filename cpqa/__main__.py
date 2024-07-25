import sys
from cpqa.app import CpqaDashboard

if __name__ == '__main__':
    if not (sys.version_info.major == 3 and sys.version_info.minor >= 9):
        raise Exception("Must be using Python3.9 or later")
    CpqaDashboard().run()
