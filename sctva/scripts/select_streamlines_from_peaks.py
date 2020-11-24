"""


"""

import argparse
import os

import numpy as np
import nibabel as nib
from dipy.tracking.metrics import inside_sphere



def build_argparser():
    """
    :return:
    """
    DESCRIPTION = "Extract streamlines connecting pairs of maxima "
    RADIUS = 5
    p = argparse.ArgumentParser(description=DESCRIPTION)
    p.add_argument("tractogram", metavar="tractogram", help="path of the whole brain "
                                                            "tractogram ("
                                                           ".tck)")
    p.add_argument("peaks_volume", metavar="peaks_volume", help="path of the volume "
                                                                "containing th "
                                                                "postion of the peaks"
                                                    "volume must be in the same space than the tractogram")
    p.add_argument("out_dir", metavar="out_dir", help="path of the directory "
                                                            "where to store the "
                                                            "selected streamlines and the extracted_maxima")

    p.add_argument("radius", metavar="radius",nargs="?", default=RADIUS,
                   help="radius of the selection spheres in mmm")
    return p


def get_peaks_coords(peaks_volume, affine):
    """
    Convert the individual peaks mask into
    :param peaks_volume:
    :return:
    """
    peaks_index = np.transpose(np.vstack(np.where(peaks_volume != 0)))
    peaks_coords = nib.affines.apply_affine(affine, peaks_index)
    return peaks_coords



def select_streamlines_between_peaks_from_spheres(streamlines, peak1, peak2,
                                                   radius=5):

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
    tckfile = nib.streamlines.load(args.tractogram, lazy_load=True)
    peaks_volume = nib.load(args.peaks_volume)
    peaks_coords = get_peaks_coords(peaks_volume.get_fdata(), peaks_volume.affine)
    nb_peaks = peaks_coords.shape[0]
    for i in range(nb_peaks):
        for j in range(i+1, nb_peaks,1):
            path_out = os.path.join(args.out_dir, str(i) + '_' + str(j) + '_' +
                                    'streamlines.tck')
            selected_streamlines = select_streamlines_between_peaks_from_spheres(
            tckfile.streamlines, peaks_coords[i], peaks_coords[j],
                                                  radius=args.radius)
            selected_tck_file = nib.streamlines.TckFile(nib.streamlines.Tractogram(
                selected_streamlines,
                affine_to_rasmm=tckfile.tractogram.affine_to_rasmm),
                header=tckfile.header)
            nib.streamlines.save(selected_tck_file, path_out)
    pass




if __name__ == "__main__":

    main()
