from src.CQReader import ConquestReader
from input import *
import numpy as np
import os

"""
Author: Jack S. Baker
Date: 12/09/17
Contains: Class: ConquestWriter
"""

# Rough version, only writes coordinates for now.

class ConquestWriter(ConquestReader):

    def __init__(self):
        super(ConquestWriter, self).__init__(wd)

    def writeCoord(self, dynamics, writeBoxDims=True, writeAtomPos=True,
                   latVec=None, newCoord=None, appendCoords=True, funcCall=None):
        # Deals only with fractional coordinates
        self.openFiles(openCQOut=False)
        lines = np.array(self.coords.readlines(), dtype=object)
        if writeBoxDims:
            lines[0] = str(latVec[0]) + "  0.00000  0.00000\n"
            lines[1] = "0.00000  " + str(latVec[1]) + "  0.00000\n"
            lines[2] = "0.00000  0.00000  " + str(latVec[2]) + "\n"
        if writeAtomPos:
            for ilnum in range(len(lines)):
                if ilnum > 3:
                    currLine = lines[ilnum]
                    currLine = currLine.split()
                    for ipos in range(3):
                        if dynamics[ilnum - 4, ipos] == True:
                            currLine[ipos] = str(newCoord[ilnum - 4, ipos]/latVec[ipos])
                    currLine.append("\n")
                    currLine = "  ".join(currLine)
                    lines[ilnum] = currLine
        self.coords.truncate(0)
        self.coords.seek(0)
        self.coords.writelines(lines)
        self.close(closeCQOut=False)
        if appendCoords:
            os.chdir(wd)
            with open("UpdatedAtoms.dat", "a") as UAD:
                oldLines = lines
                if funcCall is not None:
                    UAD.write("Coordinates for function call %d:\n\n" % (funcCall))
                UAD.writelines(oldLines)
                UAD.writelines(["\n", "\n"])
            os.chdir("../../StructureOptimizer")


if __name__ == "__main__":
    CQw = ConquestWriter()
    CQw.writeCoord(latVec = [10.00000, 10.00000, 10.00000],
                   newCoord = np.array([[0.23, 0.5, 0.5], [0.24, 0.5, 0.5], [0.25, 0.5, 0.5],
                                       [0.26, 0.5, 0.5], [0.27, 0.5, 0.5], [0.28, 0.5, 0.5]
                                   , [0.29, 0.5, 0.5], [0.30, 0.2, 0.5]]))

