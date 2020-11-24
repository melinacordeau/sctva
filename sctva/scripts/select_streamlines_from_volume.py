"""


"""

import argparse

import numpy as np
import nibabel as nib
from skimage.feature import peak_local_max
from dipy.tracking.metrics import inside_sphere

def build_argparser():
    """
    :return:
    """
    DESCRIPTION = "Extract streamlines connecting pairs of maxima of volume of " \
                  "interest (here functionnal contrast)"
    DIST = 5
    NB_PEAKS = 10
    RADIUS = 5
    p = argparse.ArgumentParser(description=DESCRIPTION)
    p.add_argument(
       "volume", metavar="volume", help=" path of the 3D volume (.nii|.nii.gz.)"
    )

    p.add_argument("tractogram", metavar="tractogram", help="path of tractogram "
                                                            "tractogram ("
                                                           ".tck|.trk file)")
    p.add_argument(
        "peaks_volume", metavar="peaks_volume", help=" path of the 3D volume ("
                                                 ".nii|.nii.gz.)"
    )
    p.add_argument("num_peaks", metavar="num_peaks", nargs="?", default=NB_PEAKS,
                   help="number of peaks to extract")
    p.add_argument("dist", metavar="dist", nargs="?", default=DIST, help="size in "
                                                                         "voxel "
                                                                         "of the "
                                                                         "neighbourhoud on which to look for a peak")
    p.add_argument("sphere_radius", metavar="shepre_radius", nargs="?", default=RADIUS,
                   help="radius of the selection spheres in mmm")
    p.add_argument("output_dir", metavar="output_dir", help="path of the directory "
                                                            "where to store the "
                                                            "selected streamlines and the extracted_maxima")

    return p


def local_max_to_volume(path_volume, distance, num_peaks, path_peaks_volume=None):
    """


    """

    volume = nib.load(path_volume)
    data = volume.get_fdata()
    peaks_mask = peak_local_max(data, min_distance=distance, num_peaks=num_peaks,
                                  indices=False)
    peaks_volume = nib.Nifti1Image(peaks_mask, volume.affine, volume.header)
    nib.save(peaks_volume, path_peaks_volume)
    peaks_vox_coord = np.transpose(np.vstack(np.where(peaks_mask!=0)))
    peaks_rasmm_coord = nib.affines.apply_affine(peaks_vox_coord)
    return peaks_rasmm_coord


def select_streamlines_between_peaks_from_spheres(streamlines, peak1, peak2,
                                                   radius=5):
    """
    :param streamlines:
    :param peak1:
    :param peak2:
    :param radius:
    :return:
    """

    for s in streamlines:
        start = np.expand_dims(s[0], axis=0)
        end = np.expand_dims(s[-1], axis=0)
        if inside_sphere(start, peak1, radius) and inside_sphere(end, peak2, radius):
            yield s
        elif inside_sphere(start, peak2, radius) and inside_sphere(end, peak1, radius):
            yield s



def main():
    """
    :return:
    """
    parser = build_argparser()
    args = parser.parse_args()

    peaks_coords = local_max_to_volume(args.volume, args.peaks_volume,
                               args.distance=args.dist, num_peaks=args.num_peaks)





if __name__ == "__main__":
    main()
