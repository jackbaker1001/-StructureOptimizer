from input import *
import os

"""
Author: Jack Baker
Date: 13/09/17
Contains: class: ConquestWrapper
"""

class ConquestWrapper(object):

    def __init__(self, binPath, numProc, wd):
        self.binPath = binPath
        self.numProc = numProc
        self.wd = wd

    def runConquest(self):
        os.chdir(wd)
        os.system("mpirun -np %d -map-by node %s" % (self.numProc, self.binPath))
        os.chdir("../")

if __name__ == "__main__":
    CQrun = ConquestWrapper(binPath, numProc, wd)
    CQrun.runConquest()
