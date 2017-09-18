from input import *
import re
import glob
import os
import numpy as np

"""
Author: Jack Baker
Date: 11/09/17
Contains: Class: ConquestReader
"""


class ConquestReader(object):

    def __init__(self, CQWD, CQOutFile="Conquest_out", coordFile="*.in"):
        self.CQWD = CQWD
        self.CQOutFile = CQOutFile
        self.coordFile = coordFile

    def openFiles(self, openCQOut=True, openCoords=True):
        if openCQOut:
            self.CQOut = open('/'.join([self.CQWD, self.CQOutFile]), 'r')
        if openCoords:
            if self.coordFile == "*.in":
                os.chdir(self.CQWD)
                dotInFiles = []
                for CQWD_file in glob.glob(self.coordFile):
                    dotInFiles.append(CQWD_file)
                if len(dotInFiles) > 1:
                    print("More than one .in file in working directory,")
                    print("Specify the full file name with coordFile.")
                    exit()
                else:
                    os.chdir('../')
                    self.coordFile = dotInFiles[0]
                    self.coords = open('/'.join([self.CQWD, self.coordFile]), 'r+')
            else:
                self.coords = open('/'.join([CQWD, coordFile]), 'r+')

    def getTotalEnergy(self):
        self.openFiles(openCoords=False)
        E = []
        for line in self.CQOut:
            if re.search("DFT total energy", line):
                E.extend(line.split())
        # No matter how many energies in CQ out, choose last one        
        self.E = float(E[-2])

    def getCoords(self):
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
        # Probably redundant due to garbage collection
        if closeCQOut:
            self.CQOut.close()
        if closeCoords:
            self.coords.close()

    def getForces(self):
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
