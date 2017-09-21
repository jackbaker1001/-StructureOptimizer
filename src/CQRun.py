from input import *
import os

"""
Author: Jack Baker
Date: 13/09/17
Contains: class: ConquestWrapper
"""

class ConquestWrapper(object):

    def __init__(self, binPath, numProc, wd, platform):
        self.binPath = binPath
        self.numProc = numProc
        self.wd = wd
        self.platform = platform

    def runConquest(self):
        os.chdir(wd)
        if self.platform == "cluster":
            os.system("mpirun -np %d -map-by node %s" % (self.numProc, self.binPath))
        elif self.platform == "Thomas":
            os.system("gerun %s" % (self.binPath))

if __name__ == "__main__":
    CQrun = ConquestWrapper(binPath, numProc, wd)
    CQrun.runConquest()
