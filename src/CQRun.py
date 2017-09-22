"""
CONQUEST WRAPPER
Author: Jack Baker
Date: 13/09/17
Decription:
          A simple wrapper for calling mpirun. This method may
          vary depending on the computing platform.
"""

from input import *
import os


class ConquestWrapper(object):
    """
    Command line interface to mpirun

    ...

    Attributes
    ----------
    binPath: string
        path to Conquest binary
    numProc: int
        number of MPI processes to execute on.
        Only relvant for cluster.
    wd: string
    platform: string
        name of computing platform operating on.

    """

    def __init__(self, binPath, numProc, wd, platform):
        """
        __init__(self, binPath, numProc, wd, platform)

        constructor method for setting attributes

        ...

        Parameters
        ----------
        binPath: string
        numProc: int
        wd: string
        platform: string

        """
        self.binPath = binPath
        self.numProc = numProc
        self.wd = wd
        self.platform = platform

    def runConquest(self):
        """
        runConquest(self)

        Perform a static calculation with Conquest.

        ...

        """
        os.chdir(wd)
        if self.platform == "cluster":
            os.system("mpirun -np %d -map-by node %s" % (self.numProc, self.binPath))
        elif self.platform == "Thomas":
            os.system("gerun %s" % (self.binPath))


if __name__ == "__main__":
    CQrun = ConquestWrapper(binPath, numProc, wd)
    CQrun.runConquest()
