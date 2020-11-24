"""


"""

import argparse



def build_argparser():
    """
    :return:
    """
    DESCRIPTION = "Extract local maxima of a ndimensionnal nifti volume and store " \
                  "their location as boolean mask volume"
    DIST = 5
    NB_PEAKS = 10
    p = argparse.ArgumentParser(description=DESCRIPTION)
    p.add_argument(
       "volume", metavar="volume", help=" path of the 3D volume(.nii|.nii.gz.)"
    )
    p.add_argument("peaks_volume", metavar="peaks_volume", help="path of the volume "
                                                                "containing peaks as "
                                                                "position ("
                                                           ".nii|.nii.gz)")
    p.add_argument("num_peaks", metavar="num_peaks", nargs="?", default=NB_PEAKS,
                   help="number of peaks to extract")
    p.add_argument("dist", metavar="dist", nargs="?", default=DIST, help="size in "
                                                                         "voxel "
                                                                       "of the "
                                                                       "neighbourhood on which to look for a peak")
    return p


def local_max_to_volume(path_volume, path_max_mask_volume,  distance, num_peaks):
    """


    """
    import nibabel as nib
    from skimage.feature import peak_local_max
    volume = nib.load(path_volume)
    data = volume.get_fdata()
    peaks_mask = peak_local_max(data, min_distance=distance, num_peaks=num_peaks,
                                  indices=False)
    peaks_volume = nib.Nifti1Image(peaks_mask, volume.affine, volume.header)
    nib.save(peaks_volume, path_max_mask_volume)





def main():
    """
    :return:
    """
    parser = build_argparser()
    args = parser.parse_args()


    local_max_to_volume(args.volume, args.peaks_volume, distance=args.dist,
                        num_peaks=args.num_peaks)


if __name__ == "__main__":
    main()
