"""


"""

import argparse
import numpy as np
import os


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
    p.add_argument("tractogram", metavar="tractogram", help="path of the whole brain "
                                                            "tractogram ("
                                                           ".tck)")
    p.add_argument("volume", metavar="volume", help="path of the (functionnal volume) "
                                                    "registered in the diffusion space")
    p.add_argument("output_dir", metavar="output_dir", help="path of the directory "
                                                            "where to store the "
                                                            "selected streamlines and the extracted_maxima")
    p.add_argument("nb_peaks", metavar="nb_peaks", nargs="?", default=NB_PEAKS,
                   help="number of peaks to extract")
    p.add_argument("dist", metavar="dist", nargs="?", default=DIST, help="size in "
                                                                         "voxel "
                                                                       "of the "
                                                                       "neighbourhoud on which to look for a peak")
    p.add_argument("sphere_radius", metavar="shepre_radius",nargs="?", default=RADIUS,
                   help="radius of the selection spheres in mmm")
    return p


def local_max_to_txt(img, path_text_file, distance, num_peaks):
    """
    Extract the first num_peaks th most important local maxima from a multidimensionnal discrete scalar function
    and store their coordinates into a txt file
    :param img: nd volume (nd scalar function)
    :param path_text_file: txt file to store peaks coordinates
    :param distance: neighbourhood in voxel on which to look for a maxima
    :param num_peaks: number of peaks to retrieve (to avoid spurious peaks)
    :return:
    """
    import numpy as np
    import nibabel as nib
    from skimage.feature import peak_local_max

    # retrieve voxel to RAS mm space transform
    affine = img.affine
    volume = img.get_fdata()
    voxels_coord = peak_local_max(volume, min_distance=distance, num_peaks=num_peaks)
    mm_coord = nib.affines.apply_affine(affine, voxels_coord)
    #sort maxima according to their first and second coordinate (Left Right Axis,
    # then Antero-Posterior Axis)
    sorted_coords = np.sort(mm_coord.view('f4','f4','f4'), order=['f0', 'f1'],
                         axis=0).view(np.float32)
    np.savetxt(path_text_file, sorted_coords)


def extract_local_maxima(path_volume, path_text_file, distance, nb_peaks):
    """ Load a nifti volume and extract its local maxima """
    import nibabel as nib

    nii = nib.load(path_volume)
    local_max_to_txt(nii, path_text_file, distance, nb_peaks)
    pass


def extract_pairs(path_text_file):
    """
    From a list of peaks generate all unique combinations and return them as a list of
    pairs
    :param path_text_file:
    :return: pairs (list)
    """
    import numpy as np


    def generate_pairs(array):
        """"""
        pairs = [
            (tuple(p), tuple(array[j]))
            for i, p in enumerate(array)
            for j in range(i, len(array))
        ]
        return pairs

    txt = np.loadtxt(path_text_file)
    pairs = generate_pairs(txt)
    return pairs


def select_between_spheres(input_tracks, center1, center2, output_tracks, radius=5):
    """
    Dirty python wrapping of the tckedit MRtrix3 command to select streamlines whose
    extremities are located inside two spheres of a given radius
    """
    import subprocess
    from distutils import spawn

    def center_to_sphere(center, radius):
        sphere = center + tuple(radius)
        return sphere

    centers = [center1, center2]
    spheres = [center_to_sphere(c, radius) for c in centers]

    def sphere_to_string(sphere):
        return str(sphere)[1:-1]

    tckedit = spawn.find_executable("tckedit")
    cmd = [tckedit, input_tracks, "-include", sphere_to_string(spheres[0]),
           "-include", sphere_to_string(spheres[1]), "-ends_only", output_tracks]
    subprocess.run(cmd)
    pass

def main():
    """
    :return:
    """
    parser = build_argparser()
    args = parser.parse_args()

    path_txt = os.path.join(args.output_dir, 'functionnal_maxima.txt')
    extract_local_maxima(args.volume, path_txt, distance=args.dist,
                             nb_peaks=args.nb_peaks)
    maxima = np.loadtxt(path_txt)
    for i in range(len(maxima)):
        for j in range(i, len(maxima)):
            path_selected_streamlines = os.path.join(args.output_dir, str(i) + '_' +
                                                     str(j) + '_streamlines.tck')
            select_between_spheres(args.tractogram, maxima[i], maxima[j], path_selected_streamlines)


if __name__ == "__main__":
    main()
