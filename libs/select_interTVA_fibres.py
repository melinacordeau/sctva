import os
import numpy as np
from libs.mrtrix_wrapping import select_tracks_between_peaks


def select_interTVA_fibres(path_input_tracts, path_functional_peaks_coord, radius=5):
    '''
    Given a tractogram and associated locations of interest (functionnal peaks) extract streamlines passing by all pairs of locations
    :param path_input_tracts:
    :param path_functional_peaks_coord:
    :param radius:
    :return:
    '''
    #load functionnal peaks coordinates (RAS-mm)
    func_peaks = np.loadtxt(path_functional_peaks_coord)
    #sort func_peaks according to their antero-posterior coordinate (axis=1 according to nifti conventions)
    sorted_peaks = np.sort(func_peaks, axis=1)
    #try all peaks 2 peaks combination avoiding redenduncy (tractography is not symmetric but no directionnality associated with streamlines)
    for i, p1 in enumerate(sorted_peaks):
        for j in range(i, len(sorted_peaks)):
            p2 = sorted_peaks[j]
            path_selected_tracts = os.path.join(os.path.basename(path_input_tracts), str(i) + '-' + str(j) + '.tck')
            select_tracks_between_peaks(path_input_tracts, path_selected_tracts, p1, p2, radius)
    pass



