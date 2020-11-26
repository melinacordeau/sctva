import numpy as np
import nibabel as nib
from skimage.feature import peak_local_max


def get_local_peaks(array, type_peak, distance, num_peaks):
    """
    Extract local peak from a n-dimensional array
    :param array:
    :param type_peak:
    :param distance:
    :param num_peaks:
    :return:
    """
    if type_peak == 'optima':
        array = np.abs(array)
    elif type_peak == 'minima':
        array = -array
    if num_peaks is None:
        num_peaks = np.inf
    peaks_mask = peak_local_max(array, min_distance=distance, num_peaks=num_peaks,
                                indices=False)
    return peaks_mask


def local_peak_to_volume(path_volume, path_peak_mask_volume, type_peak, distance, \
                         num_peaks):
    """ Extract local peak from a n-dimensional scalar nifti volume

    Local maxima are searched within a distance voxel radius neighbourhood and only
    the num_peaks th most important maxima (in magnitude) are returned


    :param path_volume: path of the input n-dimensional scalar nifti volume (
    .nii|.nii.gz)
    :param path_peak_mask_volume: path of the output n-dimensional boolean nifti
    volume containing maxima location (.nii|.nii.gz)
    :param distance: size in voxel (int)
    :param num_peaks: maximum number of peaks to return based on their magnitude
    :return: None
    """
    volume = nib.load(path_volume)
    data = volume.get_fdata()
    peaks_mask = get_local_peaks(data, type_peak, distance, num_peaks)
    peaks_volume = nib.Nifti1Image(peaks_mask, volume.affine, volume.header)
    nib.save(peaks_volume, path_peak_mask_volume)
    pass