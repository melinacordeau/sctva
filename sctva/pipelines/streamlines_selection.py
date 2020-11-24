"""


"""


import nipype.pipeline.engine as pe
from nipype.interfaces import utility

from sctva.nodes.custom_nodes import (
    create_get_pairs_node,
    create_tracks_selection_node,
)


def create_streamline_selection_from_functional_contrast_pipeline(radius):
    """

    :return:
    """

    # Pipeline nodes
    inputnode = pe.Node(
        utility.IdentityInterface(
            fields=["tractogram", "functional_contrast"], mandatory_inputs=False
        ),
        name="inputnode",
    )

    get_func_max_peaks_node = create_functional_max_extraction_node()
    pair_func_max_peaks_node = create_get_pairs_node()
    select_stream_from_spheres = create_tracks_selection_node(radius)

    outputnode = pe.Node(
        utility.IdentityInterface(
            fields=["peaks", "tractograms"], mandatory_inputs=False
        ),
        name="outputnode",
    )
    select_stream_from_func_contrast = pe.Workflow(
        name="select_stream_from_func_contrast"
    )
    # Pipeline structure
    select_stream_from_func_contrast.connect(
        inputnode, "functional_contrast", get_func_max_peaks_node, "path_volume"
    )
    select_stream_from_func_contrast.connect(
        get_func_max_peaks_node,
        "path_text_file",
        pair_func_max_peaks_node,
        "path_text_file",
    )
    select_stream_from_func_contrast.connect(
        pair_func_max_peaks_node, "pairs", select_stream_from_spheres, "pairs"
    )
    select_stream_from_func_contrast.connect(
        inputnode, "tractogram", select_stream_from_spheres, "input_tracks"
    )
    select_stream_from_func_contrast.connect(
        select_stream_from_spheres, "output_tracks", outputnode, "tractograms"
    )
    select_stream_from_func_contrast.connect(
        get_func_max_peaks_node, "path_text_file", outputnode, "peaks"
    )

    return select_stream_from_func_contrast
