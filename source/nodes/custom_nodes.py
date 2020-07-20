"""

"""


import nipype.pipeline.engine as pe
from nipype.interfaces.utility import Function

from source.scripts.extract_functional_peaks import extract_local_maxima


def extract_pairs(path_text_file):
    """
    :param path_text_file:
    :param pairs: list of pairs of peaks
    :return:
    """
    import numpy as np

    def generate_pairs(array):
        """Given a multidimensionnal NxD array"""
        pairs = [
            (tuple(p), tuple(array[j]))
            for i, p in enumerate(array)
            for j in range(i, len(array))
        ]
        return pairs

    txt = np.loadtxt(path_text_file)
    pairs = generate_pairs(txt)
    return pairs


def create_functional_max_extraction_node():
    extract_local_max = pe.Node(
        interface=Function(
            input_names=["path_volume", "distance", "nb_peaks"],
            output_names=["path_text_file"],
            function=extract_local_maxima,
        ),
    )
    return extract_local_max


def create_get_pairs_node():
    get_pairs = pe.Node(
        interface=Function(
            input_names=["path_text_file"],
            output_names=["pairs"],
            function=extract_pairs,
        ),
    )
    return get_pairs
