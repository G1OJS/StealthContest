"""
    Standard Python initialiser handling imports from modules and version number
"""

from importlib.metadata import version
try:
    __version__ = version("ham-plots")
except:
    __version__ = ""

__all__ = ["aggregator", "plotter", "datasources"]

if __name__ == "__main__":
    print(f"\nHamplots {__version__} by Dr Alan Robinson G1OJS\n\n")

