"""

"""


import nipype.pipeline.engine as pe
from nipype.interfaces.utility import Function

from sctva.scripts.extract_functional_peaks import extract_local_maxima


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


def select_between_spheres(input_tracks, centers, output_tracks, radius=5):
    """
    Dirty python wrapping of the tckedit MRtrix3 command to select streamlines whose 
    extremities are located inside two spheres of a given radius
    """
    import subprocess
    from distutils import spawn

    def center_to_sphere(center, radius):
        sphere = center + tuple(radius)
        return sphere

    spheres = [center_to_sphere(c, radius) for c in centers]

    def sphere_to_string(sphere):
        return str(sphere)[1:-1]

    tckedit = spawn.find_executable("tckedit")
    cmd = (
        tckedit
        + " "
        + input_tracks
        + " "
        + "-include"
        + " "
        + sphere_to_string(spheres[0])
        + " "
        + "-include"
        + sphere_to_string(spheres[1])
        + " "
        + "-ends_only"
        + " "
        + output_tracks
    )
    subprocess.run(cmd)
    pass


def create_functional_max_extraction_node():
    extract_local_max = pe.Node(
        interface=Function(
            input_names=["path_volume", "distance", "nb_peaks"],
            output_names=["path_text_file"],
            function=extract_local_maxima,
        ),
        name="extract_local_max"
    )
    return extract_local_max


def create_get_pairs_node():
    get_pairs = pe.Node(
        interface=Function(
            input_names=["path_text_file"],
            output_names=["pairs"],
            function=extract_pairs,
        ),
        name="get_pairs"
    )
    return get_pairs


def create_tracks_selection_node():
    """
    :return:
    """
    tracks_selection = pe.MapNode(
        interface=Function(
            input_names=["input_tracks", "pairs"],
            output_names=["output_tracks"],
            function=select_between_spheres,
        ),
        name="tracks_selection",
        iterfield=["pairs"]
    )
    return tracks_selection
