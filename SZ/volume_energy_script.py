import numpy as np
from os import system, popen
import re

"""
Author: Jack Baker
Date: 26/01/17
Description: A script to automate a volume/energy calculation for a
             perovskite crystal in its paraelectric-cubic phase.
             This minumum of the curve is a good place to begin a
             relxation for the optimal lattice parameter.
"""

def find_opt_lattice_param(exp_param, max_factor, min_factor,
                           output_file, num_proc, coord_file,
                           steps=50):
    """
    INPUT: exp_param: The experimental lattice parameter in Bohr.
           max_factor: The maximum factor of exp_param to perform
                       a calculation on.
           min_factor: The minumum factor of exp_param to perform
                       a calculation on.
           output_file: A string containing the name of the output
                        file.
           num_proc: The number of processors used for a single run.
           coord_file: The name of the coordinate file referenced in
                       Conquest_input.
           steps: The total number of calcualtions performed between
                  min_factor and max_factor.
     RETURNS: Null (writes to output file instead)
           """
    system(" ".join(["touch ", output_file]))
    param_array = exp_param*np.linspace(min_factor, max_factor, steps)
    for a in param_array:
        print("Running DFT total energy simulation for cubic cell a = %.4f Bohr" % (a))
        with open(coord_file, "w") as coordinates:
            coordinates.writelines(["    %.10f     0.000000     0.000000\n" % (a),
                                    "    0.000000     %.10f     0.000000\n" % (a),
                                    "    0.000000     0.000000     %.10f\n" % (a),
                             "8\n",
  "0.000000000000E+00  0.000000000000E+00  0.000000000000E+00   1 T T T\n",
  "0.500000000000E+00  0.500000000000E+00  0.000000000000E+00   1 T T T\n",
  "0.500000000000E+00  0.000000000000E+00  0.500000000000E+00   1 T T T\n",
  "0.000000000000E+00  0.500000000000E+00  0.500000000000E+00   1 T T T\n",
  "0.250000000000E+00  0.250000000000E+00  0.250000000000E+00   1 T T T\n",
  "0.250000000000E+00  0.750000000000E+00  0.750000000000E+00   1 T T T\n",
  "0.750000000000E+00  0.250000000000E+00  0.750000000000E+00   1 T T T\n",
  "0.750000000000E+00  0.750000000000E+00  0.250000000000E+00   1 T T T\n"])
        system("mpirun -np " + str(num_proc) +
               " ~jbaker/Documents/ConquestSource/Conquest")
        try:
            DFT_tot_en = float(re.sub("[ |*DFTtotalenergy=-Ha]",
                               "", popen("grep \"DFT total energy\" Conquest_out").read()))
            output_line = (" ".join([str(a), str(DFT_tot_en) + "\n"]))
            with open(output_file, "a") as output:
                output.write(output_line)
        except ValueError:
            pass


if __name__ == "__main__":
    find_opt_lattice_param(exp_param=10.544, max_factor=1.1, min_factor=0.9,
                           output_file="cubic_param_vs_DFTen.out", num_proc=5,
                           coord_file="StretchSiCell.in")
