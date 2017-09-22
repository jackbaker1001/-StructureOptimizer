"""
CONQUEST WRITER
Author: Jack S. Baker
Date: 12/09/17
Description:
           Contains a class for writing coordinates to the
           conquest coordinate file. I tiwll in future be able
           to edit flags in Conquest_input.
"""

from input import *
from src.CQReader import ConquestReader
import numpy as np
import os


class ConquestWriter(ConquestReader):
    """
    Contains methods for writing to Conquest_input and coordinate
    files.

    ...

    Attributes
    ----------
    inherited from ConquestReader

    """

    def __init__(self):
        """
        __init__(self)

        constructor method for inheriting from ConquestReader.

        ...

        """
        super(ConquestWriter, self).__init__(wd)

    def writeCoord(self, dynamics, writeBoxDims=True, writeAtomPos=True,
                   latVec=None, newCoord=None, appendCoords=True, funcCall=None):
        """
        writeCoord(self, dynamics, writeBoxDims=True, writeAtomPos=True,
                   latVec=None, newCoord=None, appendCoords=True, funcCall=None)

        Writes new coordinates and simulation box dimensions to coordinate file.
        Keeps a history of old coordinate files in UpdatedAtoms.dat.

        Parameters
        ----------
        dynamics: ndarray(dtype=bool, shape=(numAtoms, 3))
        writeBoxDims: bool
            choose to write new simulation box dimensions
        writeAtomsPos: bool
            choses to write new atomic positions
        latVec: ndarray(dtype=np.float64, shape=(3, 1))
            array containing simulation box dimensions to be written
        newCoord: ndarray(dtype=np.float64, shape=(numAtoms, 3))
            new coordinates to be written
        appendCoords: bool
            choose to append to old coordinates into UpdatedAtoms.dat
        funcCall: int
            number of function calls in optimizer. Written as header to
            coordinates in UpdatedAtoms.dat

        ...

        """
        
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
            with open("UpdatedAtoms.dat", "a") as UAD:
                oldLines = lines
                if funcCall is not None:
                    UAD.write("Coordinates for function call %d:\n\n" % (funcCall))
                UAD.writelines(oldLines)
                UAD.writelines(["\n", "\n"])


if __name__ == "__main__":
    CQw = ConquestWriter()
    CQw.writeCoord(latVec = [10.00000, 10.00000, 10.00000],
                   newCoord = np.array([[0.23, 0.5, 0.5], [0.24, 0.5, 0.5], [0.25, 0.5, 0.5],
                                       [0.26, 0.5, 0.5], [0.27, 0.5, 0.5], [0.28, 0.5, 0.5]
                                   , [0.29, 0.5, 0.5], [0.30, 0.2, 0.5]]))

