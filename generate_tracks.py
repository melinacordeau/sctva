from distutils import spawn
import subprocess
import numpy as np

# automatically find the mrconvert command if installed and belong to path
mrconvert = spawn.find_executable('mrconvert')

def select_tracks_between_pics(path_input_tracks, path_selected_tracks, first_peak, second_peak, radius='5'):
    first_sphere = str(first_peak[0]) + ',' + str(first_peak[1]) + ',' + str(first_peak[2]) + ',' + radius
    second_sphere = str(second_peak[0]) + ',' + str(second_peak[1]) + ',' + str(second_peak[2]) + ',' + radius
    cmd = mrconvert + ' ' + ' -select ' + first_sphere + ' -select ' + second_sphere + ' -ends_only ' + path_input_tracks + ' ' + path_selected_tracks
    subprocess.run(cmd)
    pass



def select_interTVA_fibres(path_input_trakcs, path_functional_peaks_coord, radius=5):
    func_peaks = np.loadtxt(path_functional_peaks_coord)
    #sort func_peaks according to their antero_posterior coordinate (1 axis according to nifti conventions)
    sorted_peaks = np.sort(func_peaks, axis=1)
    for i, p1 in enumerate(sorted_peaks):
        for j in range(i, )
            select_tracks_between_pics(path_input_trakcs, path_selected_tracks p1,p2, radius)
    pass



