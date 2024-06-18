import sys
import os
from pathlib import Path
os.environ['KIVY_HOME'] = str(Path(__file__).parent.parent.absolute() / 'data')

import kivy
from cpqa.app import CpqaApp

if __name__ == '__main__':
    if not (sys.version_info.major == 3 and sys.version_info.minor >= 9):
        raise Exception("Must be using Python3.9 or later")
    kivy.require('2.1.0')
    CpqaApp().run()
