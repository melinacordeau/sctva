import argparse

import numpy as np
from soma import aims, aimsalgo


def peaks_as_spheres(path_peaks_volume, path_spheres, radius=2):
    """
    Generate sphere of radius radius centered on detected peaks
    :param path_peaks_volume:
    :param radius:
    :return:
    """
    volume = aims.read(path_peaks_volume)
    data = np.array(volume)[..., 0]

    voxel_size = volume.header()['voxel_size'] + [1]
    scaling = aims.AffineTransformation3d()
    scaling.fromMatrix(np.diag(voxel_size))
    peaks_vol_coord = np.transpose(np.vstack(np.where(data != 0)))
    centers = [aims.Point3df(p) for p in peaks_vol_coord]

    for i, center in enumerate(centers):
        center = scaling.transform(center)
        sphere = aims.SurfaceGenerator.sphere(center, radius,300)
        if i == 0:
            spheres = sphere
        else:
            aims.SurfaceManip.meshMerge(spheres, sphere)
    aims.write(spheres, path_spheres)


def build_argparser():
    """
    :return:
    """
    DESCRIPTION = "Generate spheres from a mask volume"
    p = argparse.ArgumentParser(description=DESCRIPTION)
    p.add_argument(
       "volume", metavar="volume", help=" path of the 3D volume(.nii|.nii.gz.)"
    )
    p.add_argument("spheres", metavar="spheres", help="path of the spheres as mesh "
                                                           ".gii")
    p.add_argument("radius", metavar="radius", nargs="?", default=2, help="spheres "
                                                                          "radius")
    return p



def main():
    """
    :return:
    """
    parser = build_argparser()
    args = parser.parse_args()

    peaks_as_spheres(args.volume, args.spheres, args.radius)


if __name__ == "__main__":
    main()
