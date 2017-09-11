import re
import glob
import os

"""
Author: Jack Baker
Date: 11/09/17
Contains: Class: ConquestParser
"""

class ConquestParser(object):

    def __init__(self, CQWD, CQOutFile="Conquest_out", coordFile="*.in"):
        self.CQOut = open('/'.join([CQWD, CQOutFile]), 'r')
        if coordFile == "*.in":
            os.chdir(CQWD)
            dotInFiles = []
            for CQWD_file in glob.glob(coordFile):
                dotInFiles.append(CQWD_file)
            if len(dotInFiles) > 1:
                print("More than one .in file in working directory,")
                print("Specify the full file name with coordFile.")
                exit()
            else:
                os.chdir('../')
                coordFile = dotInFiles[0]
                self.coords = open('/'.join([CQWD, coordFile]), 'rw')
        else:
            self.coords = open('/'.join([CQWD, coordFile]), 'rw')

    def getTotalEnergy(self):
        self.E = []
        for line in self.CQOut:
            if re.search("DFT total energy", line):
                self.E.extend(line.split())
        # No matter how many energies in CQ out, choose last one        
        self.E = float(self.E[-2])


    def getNumAtoms(self):
        # This method may seem pointless but is the most robust as 
        # there may be blank lines...
        self.numAtoms = 0
        for line in self.coords:
            if line.strip():
                self.numAtoms += 1
        # Take away four (3 for lattice vectors, 1 for atom count)    
        self.numAtoms -= 4

    def close(self):
        self.CQOut.close()
        self.coords.close()

Conquest_out = ConquestParser('SZ')
Conquest_out.getTotalEnergy()
Conquest_out.getNumAtoms()
print(Conquest_out.numAtoms)
Conquest_out.close()
