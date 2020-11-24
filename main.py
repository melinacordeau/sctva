import nipype.pipeline.engine as pe
from nipype.interfaces import IdentityInterface
from nipype import SelectFiles, Node

from sctva.pipelines.full import create_study_pipeline
from configuration import (
    PRIMAVOICE,
    CENTER,
    MODALITY,
    ACQUISITION,
    CORRECTION,
    SUBJECTS,
)


def create_main_pipeline(subject_list=SUBJECTS):
    RADIUS = 5  # selection sphere radius (mm)

    # create node that contains meta-variables about data
    inputnode = Node(
        IdentityInterface(
            fields=["subject_id", "center", "modality", "acquisition", "correction"]
        ),
        name="inputnode",
    )
    inputnode.inputs.center = CENTER
    inputnode.inputs.modality = MODALITY
    inputnode.inputs.acquisition = ACQUISITION
    inputnode.inputs.correction = CORRECTION
    inputnode.iterables = [("subject_id", subject_list)]

    #
    templates = {
        "diffusion_volume": "DTI/{center}/{subject_id}/{modality}/{acquisition}/{"
        "correction}/corrected_dwi_{subject_id}.nii.gz",
        "bvals": "DTI/{center}/{subject_id}/{modality}/{acquisition}/raw_bvals_{subject_id}.txt",
        "bvecs": "DTI/{center}/{subject_id}/{modality}/{acquisition}/{correction}/corrected_bvecs_{subject_id}.txt",
        "t1_volume": "analysis_{subject_id}/anat/{"
                     "subject_id}_ses-01_T1w_denoised_debiased_in-MNI152.nii.gz",
        "func_contrast_volume": "analysis_{subject_id}/spm_realign/results_8WM_9CSF_0mvt/In-MNI152_{subject_id}_res-8WM_9CSF_0mvt_human_vs_all_t.nii.gz",
    }
    datagrabber = pe.Node(SelectFiles(templates), name="datagrabber")
    datagrabber.inputs.base_directory = PRIMAVOICE

    study_pipeline = create_study_pipeline(radius=RADIUS)

    main_pipeline = pe.Workflow(name="main_pipeline")


    main_pipeline.connect(
        [
            (
                inputnode,
                datagrabber,
                [
                    ("subject_id", "subject_id"),
                    ("center", "center"),
                    ("modality", "modality"),
                    ("acquisition", "acquisition"),
                    ("correction", "correction"),
                ],
            )
        ]
    )
    main_pipeline.connect(
        [
            (
                datagrabber,
                study_pipeline,
                [
                    ("diffusion_volume", "inputnode.diffusion_volume"),
                    ("bvals", "inputnode.bvals"),
                    ("bvecs", "inputnode.bvecs"),
                    ("t1_volume", "inputnode.t1_volume"),
                    ("func_contrast_volume", "inputnode.func_contrast_volume"),
                ],
            )
        ]
    )
    return main_pipeline
