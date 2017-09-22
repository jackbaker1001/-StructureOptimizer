"""
CONQUEST READER
Author: Jack Baker
Date: 11/09/17
Description: contains a class with methods for extracting information from
             both Conquest_out and the coordinate file (default *.in file).
"""

from input import *
import re
import glob
import numpy as np


class ConquestReader(object):
    """
    A base class for reading in energies, forces and stresses
    and coordinates from Conquest_out and the coordinate (.in)
    file.

    ...

    Attributes
    ----------
    CQWD: string
        absolute path to the Conquest working directory.
    CQOutFile: string
        name of output file in Conquest working directory.
        defaults to Conquest_out.
    coordFile: string
        name of coordinate file in Conquest working directory.
        defaults to file extension *.in.
    coords: open() file object
        object with methods for extracting information from
        coordFile.
    CQOut: open() file object
        object with methods for extracting information from
        CQOutFile.
    coordArray: ndarray(dtype=np.float64, shape=(numAtoms, 3))
        array containing coorinates read from coordFile
    dynamics: ndarray(dtype=bool, shape=(numAtoms, 3))
        array constaining boolean information about whether
        atoms can move in optimization or not.
    numAtoms: int
        number of atoms read from coordFile
    E: float
        total DFT energy read from Conquest_out
    forces: ndarray(dtype=np.float64, shape=(numAtoms, 3))
        forces in Ha/Bohr on each atom read from Conquest_out
    stress: ndarray(dtpe=np.float64, shape=(1, 3))

    """

    def __init__(self, CQWD, CQOutFile="Conquest_out", coordFile="*.in"):
        """
        __init__(self, CQWD, CQOutFile="Conquest_out", coordFile="*.in")

        Constructor method for loading relevant filenames in the Conquest
        working directory.

        ...

        Parameters
        ----------
        CQWD: string
        CQOutFile: string
        coordFile: string

        """
        self.CQWD = CQWD
        self.CQOutFile = CQOutFile
        self.coordFile = coordFile

    def openFiles(self, openCQOut=True, openCoords=True):
        """
        openFiles(self, openCQOut=True, openCoords=True)

        Opens the Conquest_out and coordinate files into
        open() objects.

        ...

        Parameters
        ----------
        openCQOut: bool
            choose to open the ouput file
        openCoords: bool
            choose to open the coordinate file

        """

        if openCQOut:
            self.CQOut = open(self.CQOutFile, 'r')
        if openCoords:
            if self.coordFile == "*.in":
                dotInFiles = []
                for CQWD_file in glob.glob(self.coordFile):
                    dotInFiles.append(CQWD_file)
                if len(dotInFiles) > 1:
                    print("More than one .in file in working directory,")
                    print("Specify the full file name with coordFile.")
                    exit()
                else:
                    self.coordFile = dotInFiles[0]
                    self.coords = open(self.coordFile, 'r+')
            else:
                self.coords = open(self.coordFile, 'r+')

    def getTotalEnergy(self):
        """
        getTotalEnergy(self)

        Gets the total DFT energy from the Conquest_out file

        ...

        """
        self.openFiles(openCoords=False)
        E = []
        for line in self.CQOut:
            if re.search("DFT total energy", line):
                E.extend(line.split())
        # No matter how many energies in CQ out, choose last one        
        self.E = float(E[-2])

    def getCoords(self):
        """
        getCoords(self)

        Gets the coordinate array from the coordinate file
        as well as selective dynamics information and the total
        number of atoms.

        ...

        """
        self.openFiles(openCQOut=False)
        allCoords = []
        for iline, line in enumerate(self.coords):
            if iline == 0:
                self.rCellX = float(line.split()[0])
            elif iline == 1:
                self.rCellY = float(line.split()[1])
            elif iline == 2:
                self.rCellZ = float(line.split()[2])
            elif iline == 3:
                self.numAtoms = int(line)
                self.dynamics = np.ones((self.numAtoms, 3), dtype=bool)
            else:
                coordAndDyn = line.split()
                coord = coordAndDyn[:3]
                dyns = coordAndDyn[4:]
                for idyn in range(len(dyns)):
                    if dyns[idyn] == 'T':
                        self.dynamics[iline-4, idyn] = True
                    else:
                        self.dynamics[iline-4, idyn] = False
                allCoords.append(coord)
        self.coordArray = np.array(allCoords, dtype=float)

    def close(self, closeCQOut=True, closeCoords=True):
        """
        close(self, closeCQOut=True, closeCoords=True)

        Closes Conquest_out and the coordinate file.

        ...

        Parameters
        ----------
        closeCQOut: bool
            choose to close Conquest_out
        closeCoords: bool
            choose to close the coordinate file

        """
        # Probably redundant due to garbage collection
        if closeCQOut:
            self.CQOut.close()
        if closeCoords:
            self.coords.close()

    def getForces(self):
        """
        getForces(self)

        Gets the forces on atoms from Conquest_out

        ...

        """
        self.openFiles(openCoords=False)
        allForceComps = np.zeros([self.numAtoms, 3])
        forceComps = []
        for ilnum, line in enumerate(self.CQOut):
            if "Atom   X              Y              Z" in line.strip():
                for iatom in range(self.numAtoms):
                    forces = next(self.CQOut)
                    forces = forces.split()[1:]
                    for iforce in range(len(forces)):
                        force = float(forces[iforce])
                        allForceComps[iatom, iforce] = force
                        if self.dynamics[iatom, iforce] == True:
                            forceComps.append(force)
        self.allForces = -allForceComps
        self.forces = -np.array(forceComps, dtype=np.float64)


    def getStress(self):
        """
        getStress(self)

        Gets the stress components from Conquest_out

        ...

        """
        self.openFiles(openCoords=False)
        stressComps = np.zeros([3])
        for ilnum, line in enumerate(self.CQOut):
            if "Total stress:" in line.strip():
               stress = line.split()[2:-1]
               for istress in range(len(stress)):
                   stressComps[istress] = float(stress[istress])
        self.stress = stressComps


if __name__ == "__main__":
    CQr = ConquestReader(wd)
    CQr.getTotalEnergy(); CQr.getCoords(); CQr.getForces(); CQr.getStress()
    CQr.close()
    print("\n\n Conquest Reader - Jack S. Baker, 2017 \n\n")
    print("Simulation box dimensions:\n a = %.5f a0, b = %.5f a0, c = %.5f a0"
          % (CQr.rCellX, CQr.rCellY, CQr.rCellZ))
    print("%d total atoms in simulation" % (CQr.numAtoms))
    print("Atomic fractional coordinates (x, y, z):\n", CQr.coordArray)
    print("Atomic forces (Ha/a0) (Fx, Fy, Fz):\n", CQr.forces)
    print("Stress (Ha) (Sx, Sy, Sz):\n", CQr.stress)
