"""
    Standard Python initialiser handling imports from modules and version number
"""
from .pskr_utils import *
from .analysers import *
from .cli import *

from importlib.metadata import version
try:
    __version__ = version("docu-lite-kit")
except:
    __version__ = ""
print(f"\nStealthContest {__version__} by Dr Alan Robinson G1OJS\n\n")


