"""

"""

import nipype.pipeline.engine as pe
from nipype.interfaces import utility

from mrproc.pipelines.diffusion import create_diffusion_pipeline
from mrproc.nodes.custom_nodes import create_apply_linear_transform_node

from sctva.pipelines.streamlines_selection import (
    create_streamline_selection_from_functional_contrast_pipeline,
)

# Constants
N_TRACKS = 5000000
MIN_LENGTH = 10  # mm
MAX_LENGTH = 300  # mm
RADIUS = 5  # selection sphere radius mm


def create_study_pipeline(radius=RADIUS):
    """
    :return:
    """

    # Nodes composing the pipeline
    # Input and Output Nodes
    inputnode = pe.Node(
        utility.IdentityInterface(
            fields=[
                "diffusion_volume",
                "bvals",
                "bvecs",
                "t1_volume",
                "func_contrast_volume",
            ],
            mandatory_inputs=False,
        ),
        name="inputnode",
    )
    diffusion_pipeline = create_diffusion_pipeline()
    apply_rigid_transform = create_apply_linear_transform_node()
    tva_streamlines_selection = create_streamline_selection_from_functional_contrast_pipeline(
        radius
    )
    outputnode = pe.Node(
        utility.IdentityInterface(
            fields=[
                "corrected_diffusion_volume",
                "wm_fod",
                "tractogram",
                "peaks",
                "sub-tractograms",
            ],
            mandatory_inputs=False,
        ),
        name="outputnode",
    )
    study_pipeline = pe.Workflow(name="sctva_pipeline")
    # Pipeline structure
    study_pipeline.connect(
        [
            (
                inputnode,
                diffusion_pipeline,
                [
                    ("diffusion_volume", "inputnode.diffusion_volume"),
                    ("bvals", "inputnode.bvals"),
                    ("bvecs", "inputnode.bvecs"),
                    ("t1_volume", "inputnode.t1_volume"),
                ],
            )
        ]
    )

    study_pipeline.connect(
        inputnode, "func_contrast_volume", apply_rigid_transform, "in_file"
    )
    study_pipeline.connect(
        diffusion_pipeline,
        "outputnode.diffusion_to_t1_transform",
        apply_rigid_transform,
        "transform",
    )
    study_pipeline.connect(
        apply_rigid_transform,
        "out_file",
        tva_streamlines_selection,
        "inputnode.functional_contrast",
    )
    study_pipeline.connect(
        diffusion_pipeline,
        "outputnode.tractogram",
        tva_streamlines_selection,
        "inputnode.tractogram",
    )
    study_pipeline.connect(
        tva_streamlines_selection, "outputnode.peaks", outputnode, "peaks"
    )
    study_pipeline.connect(
        tva_streamlines_selection,
        "outputnode.tractograms",
        outputnode,
        "sub-tractograms",
    )
    study_pipeline.connect(
        diffusion_pipeline,
        "outputnode.corrected_diffusion_volume",
        outputnode,
        "corrected_diffusion_volume",
    )
    study_pipeline.connect(
        diffusion_pipeline, "outputnode.wm_fod", outputnode, "wm_fod"
    )
    return study_pipeline
