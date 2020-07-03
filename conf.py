"""
Configuration file used to store global variables used in this project
Avoid to have multiple definitions into scripts files.
Example : BANCO ='/hpc/banco'
        from conf import BANCO (in scripts)
"""

import os

N = 10
SUBJECTS_PREFIX = "sub-"
SUBJECTS = [
    SUBJECTS_PREFIX + "0" + str(i) if i < 10 else SUBJECTS_PREFIX + str(i)
    for i in range(1, N, 1)
]

BANCO_HPC = "/hpc/banco"  # frioul di
BANCO_LOCAL = r"L:\banco"  # local mount

if os.path.exists(BANCO_HPC):
    BANCO = BANCO_HPC
else:
    BANCO = BANCO_LOCAL

PRIMAVOICE = os.path.join(BANCO, "Primavoice_Data_and_Analysis")
PRIM_DTI = os.path.join(PRIMAVOICE, "DTI")
CERIMED = os.path.join(PRIM_DTI, "cerimed")
SUBJS_DIR = {subject: os.path.join(CERIMED, subject) for subject in SUBJECTS}


#  = os.path.join(BANCO, 'tobecompleted')   a completer
CENTER = "subjects"
ACQUISITION = "default_acquisition"
CORRECTION = "default_analysis"

# Generate dictionnaries containing path of the files
# CORRECTED_DWI = {subject: os.path.join(BRAINVISA_DB, CENTER, subject, 'dmri', ACQUISITION, CORRECTION) for subject in SUBJECTS}
