"""
Extraction of local maxima, minima ou optima from a n-dimensional scalar nifti volume

"""

import argparse

from ..core.extract_local_peaks import local_peak_to_volume



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
