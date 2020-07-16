"""


"""

import argparse

import numpy as np
import nibabel as nib
from skimage.feature import peak_local_max


def build_argparser():
    """
    :return:
    """
    DESCRIPTION = "Extract all local maxima of a 3D volume and save their RAS coordinate in mm in a text file"
    p = argparse.ArgumentParser(description=DESCRIPTION)
    p.add_argument(
        "3D volume path", metavar="volume", help=" path of the 3D volume(.nii|.nii.gz."
    )
    p.add_argument("textfile", metavar="textfile", help="path of the textfile (.txt)")
    return p


def local_max_to_txt(img, path_text_file, distance=5, num_peaks=10):
    """
    Extract the first num_peaks th most important local maxima from a multidimensionnal discrete scalar function
    and store their coordinates into a txt file
    :param img: nd volume (nd scalar function)
    :param path_text_file: txt file to store peaks coordinates
    :param distance: neighbourhood in voxel on which to look for a maxima
    :param num_peaks: number of peaks to retrieve (to avoid spurious peaks)
    :return:
    """
    # retrieve voxel to RAS mm space transform
    affine = img.affine
    volume = img.get_fdata()
    voxels_coord = peak_local_max(volume, min_distance=distance, num_peaks=num_peaks)
    mm_coord = nib.affines.apply_affine(affine, voxels_coord)
    np.savetxt(path_text_file, mm_coord)


def extract_local_maxima(path_volume, path_text_file):
    """ Load a nifti volume and extract its local maxima """
    nii = nib.load(path_volume)
    local_max_to_txt(nii, path_text_file)
    pass


def main():
    """
    :return:
    """
    parser = build_argparser()
    args = parser.parse_args()

    try:
        nii = nib.load(args.volume)
        local_max_to_txt(nii, args.textfile)
    except:
        parser.error("Expecting 3D volume as first argument")


if __name__ == "__main__":
    main()
