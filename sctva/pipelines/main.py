"""

"""

import nipype.pipeline.engine as pe
from nipype.interfaces import utility

from mrproc.pipelines.dwi_pipelines import create_diffusion_pipeline
from mrproc.nodes.custom_nodes import create_apply_linear_transform_node

from sctva.pipelines.streamlines_selection import (
    create_streamline_selection_from_functional_contrast_pipeline,
)

# Constants
N_TRACKS = 5000000
MIN_LENGTH = 10  # mm
MAX_LENGTH = 300  # mm


def create_study_pipeline():

    # Nodes composing the pipeline
    diffusion_pipeline = create_diffusion_pipeline()
    apply_rigid_transform = create_apply_linear_transform_node()
    tva_streamlines_selection = (
        create_streamline_selection_from_functional_contrast_pipeline()
    )
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
    outputnode = pe.Node(
        utility.IdentityInterface(
            fields=["corrected_diffusion_volume", "mask"], mandatory_inputs=False
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

    study_pipeline.connect([diffusion_pipeline, apply_rigid_transform,
                            [('func_contrast_volume', "in_file")] ])
    study_pipeline.connect([diffusion_pipeline, apply_rigid_transform,
                            [('func_contrast_volume', "in_file")]])