import nibabel as nib
import numpy as np
from skimage.feature import peak_local_max
import argparse

def build_argparser():
    DESCRIPTION = 'Extract all local maxima of a 3D volume and save their RAS coordinate in mm in a text file'
    p = argparse.ArgumentParser(description=DESCRIPTION)
    p.add_argument('3D volume path',metavar='volume', help=' path of the 3D volume(.nii|.nii.gz.')
    p.add_argument('textfile', metavar='textfile', help='path of the textfile (.txt)')
    return p


def local_maxima_2_text(img, path_text_file, distance=3, num_peaks=10):
    '''
    Extract all local maxima of an up to 3D volume and save their coordinate into RAS-mm space in a text file
    :param path_volume: the path of the input volume
    :param path__text_file: the path of the text file containing the local_maxima to store
    :return: void
    '''
    affine = img.affine
    volume = img.get_data()
    voxels_coord = peak_local_max(volume,min_distance=distance,num_peaks=num_peaks)
    mm_coord = nib.affines.apply_affine(affine, voxels_coord)
    np.savetxt(path_text_file, mm_coord)

def extract_local_maxima(path_volume, path_text_file):
    nii = nib.load(path_volume)
    local_maxima_2_text(nii, path_text_file)
    pass

def main():
    '''
    :return:
    '''
    parser = build_argparser()
    args = parser.parse_args()

    try:
        nii = nib.load(args.volume)
        local_maxima_2_text(nii, args.textfile)
    except:
        parser.error("Expecting 3D volume as first argument.")


if __name__ == '__main__':
   main()


