"""
Extraction of local maxima, minima ou optima from a n-dimensional scalar nifti volume

"""

import argparse

import numpy as np
import nibabel as nib
from skimage.feature import peak_local_max


def build_argparser():
    """ Instanciate parser with help and scripts arguments

    :return:
    """
    description = "Extract local peaks (maxima, minima or both) from a n-dimensional " \
                  "nifti volume and " \
                  "store " \
                  "their location as a boolean n-dimensional nifti volume"

    p = argparse.ArgumentParser(description=description)
    p.add_argument(
        "volume", metavar="volume",
        help="path of the input n-dimensional nifti volume ("
             ".nii|.nii.gz)"
    )
    p.add_argument("peaks_volume", metavar="peaks_volume", help="path of the "
                                                                "output "
                                                                "n-dimensional boolean "
                                                                "volume "
                                                                "containing peaks "
                                                                "location "
                                                                " ("
                                                                ".nii|.nii.gz)")
    p.add_argument("--type_peak", metavar="type_peak", nargs="?", type=str, choices=[
        'maxima',
        'minima',
        'optima'],
                   default='maxima', help="type of peak to extract: either maxima or "
                                          "minima or optima (both), (default: %("
                        "default)s)" )
    p.add_argument("--num_peaks", metavar="num_peaks", nargs="?", type=int, default=10,
                   help="number of peaks to extract, (default: %("
                        "default)s)")
    p.add_argument("--dist", metavar="dist", nargs="?", type=int, default=5,
                   choices=range(1, 20),
                   help="size "
                        "in "
                        "voxel "
                        "of the "
                        "neighbourhood on which to look for a peak,  (default: %("
                        "default)s)")
    return p


def local_peak_to_volume(path_volume, path_peak_mask_volume, type_peak, distance, \
                         num_peaks):
    """ Extract local maxima from a n-dimensional scalar nifti volume

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
    if type_peak == 'optima':
        data = np.abs(data)
    elif type_peak == 'minima':
        data = -data
    if num_peaks is None:
        num_peaks = np.inf
    peaks_mask = peak_local_max(data, min_distance=distance, num_peaks=num_peaks,
                                indices=False)
    peaks_volume = nib.Nifti1Image(peaks_mask, volume.affine, volume.header)
    nib.save(peaks_volume, path_peak_mask_volume)
    pass


def main():
    """ Parse scripts arguments and extract local maxima
    :return: None
    """
    parser = build_argparser()
    args = parser.parse_args()
    local_peak_to_volume(args.volume, args.peaks_volume, type_peak=args.type_peak,
                         distance=args.dist,
                         num_peaks=args.num_peaks)
    pass


if __name__ == "__main__":
    main()
