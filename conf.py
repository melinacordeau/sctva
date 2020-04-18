"""
Configuration file used to store global variables like subjects name, database structure and locations
Avoid to have multiple definitions into scripts files.
Example : BANCO ='/hpc/banco'
        from conf import BANCO (in scripts)
"""

import os

N = 10
SUBJECTS_PREFIX = 'sub-'
SUBJECTS = (SUBJECTS_PREFIX + '0' + str(i) if i < 10 else SUBJECTS_PREFIX + str(i) for i in range(1, N, 1))

BANCO = '/hpc/banco'
BRAINVISA_DB = os.path.join(BANCO, 'tobecompleted')   # a completer
CENTER = 'subjects'
ACQUISITION = 'default_acquisition'
CORRECTION = 'default_analysis'

#Generate dictionnaries containing path of the files
CORRECTED_DWI = {subject: os.path.join(BRAINVISA_DB, CENTER, subject, 'dmri', ACQUISITION, CORRECTION) for subject in SUBJECTS}

