# Conquest Structure Optimizer
This code acts as a python interface for Conquest into the 
[SciPy minimization](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.minimize.html#scipy.optimize.minimize)
algorithms. Currently functioning methods include:

* BFGS (Broyden-Fletcher-Goldfarb-Shanno)
* L-BFGS-B (Limited memory BFGS bounded). We use no constraints so this becomes Simply L-BFGS.
* CG (Conjugate Gradients: Polak-Ribiere version as opposed to the Conquest-native Fletcher-Reeves version)
* Newton-CG (A quasi-newton CG method)

The code works from extracting energies, forces and stresses from static Conquest simulations.

## How-to
This code requires a Python 3 installation with numpy and scipy installed.

1. Perform a static calculation on the initial structure to be relaxed. Keep the .chden* files in the directory. Ensure your
coordinate file has the extension ".in" and that output is directed to Conquest_out.
2. Set the parameters you desire in input.py. Comments in this file should help you.
3. Run python main.py. If on a computing platform operating with .sh job-scripts, ensure the python module with scipy and numpy has been loaded before 
the run along with any libraries/modules required to run the Conquest binary.

Energies and gradient information will be printed in the working directory to structureOptimizer.out. 
Coordinates will be appended to UpdatedAtoms.dat.

## Contact
Please contact me on jack.baker.16@ucl.ac.uk with any bugs/suggestions. 
