"""
    Standard Python initialiser handling imports from modules and version number
"""


from importlib.metadata import version
try:
    __version__ = version("ham-plots")
except:
    __version__ = ""
print(f"\nStealthContest {__version__} by Dr Alan Robinson G1OJS\n\n")

