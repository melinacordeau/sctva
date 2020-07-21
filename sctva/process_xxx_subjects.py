"""

"""

if __name__ == "__main__":
    import os

    # Number of subjects included in the study (to be changed)
    N = 10
    SUBJECTS_PREFIX = "sub-"
    # Subject's ID such as sub-01 or s-10
    SUBJECTS = [
        SUBJECTS_PREFIX + "0" + str(i) if i < 10 else SUBJECTS_PREFIX + str(i)
        for i in range(1, N, 1)
    ]

    # Data structure of the study
    BANCO = "/hpc/banco"
    PRIMAVOICE = os.path.join(BANCO, "Primavoice_Data_and_Analysis")
    # BrainVISA database location
    BV_DB = os.path.join(PRIMAVOICE, "DTI")
    # BrainVISA field values
    CENTER = "cerimed"
    SUBJ_DIRS = {subject: os.path.join(BV_DB, CENTER, subject) for subject in SUBJECTS}
    MODALITY = "dmri"
    ACQUISITION = "default_acquisition"
    ACQUISITION_DIRS = {
        subject: os.path.join(SUBJ_DIRS[subject], MODALITY, ACQUISITION)
        for subject in SUBJECTS
    }
    CORRECTION = "default_analysis"
    CORRECTION_DIRS = {
        subject: os.path.join(ACQUISITION_DIRS[subject], CORRECTION)
        for subject in SUBJECTS
    }
    # Data generated through Diffuse (to check the three following paths)
    CORRECTED_DWI = {
        subject: os.path.join(
            CORRECTION_DIRS[subject], "corrected_dwi" + "_" + subject + ".nii.gz"
        )
        for subject in SUBJECTS
    }
    BVECS = {
        subject: os.path.join(
            CORRECTION_DIRS[subject], "corrected_bvecs" + "_" + subject + ".txt"
        )
        for subject in SUBJECTS
    }
    BVALS = {
        subject: os.path.join(
            ACQUISITION_DIRS[subject], "raw_bvals" + "_" + subject + ".txt"
        )
        for subject in SUBJECTS
    }
    # Added directory that contains the mrtrix generated data (no subdirs)
    PROCESSING = "Mrtrix"
    PROCESSING_DIRS = {
        subject: os.path.join(CORRECTION_DIRS[subject], PROCESSING)
        for subject in SUBJECTS
    }
    MRTRIX_CORRECTED_DWIS = {
        subject: os.path.join(PROCESSING_DIRS[subject], subject + "_" + "dwi" + ".mif")
        for subject in SUBJECTS
    }
    TENSORS = {
        subject: os.path.join(
            PROCESSING_DIRS[subject], subject + "_" + "tensor" + ".mif"
        )
        for subject in SUBJECTS
    }
    FAS = {
        subject: os.path.join(PROCESSING_DIRS[subject], subject + "_" + "fa" + ".mif")
        for subject in SUBJECTS
    }
    MASKS = {
        subject: os.path.join(
            PROCESSING_DIRS[subject], subject + "_" + "dwi_mask" + ".mif"
        )
        for subject in SUBJECTS
    }
    WM_RESPONSES = {
        subject: os.path.join(PROCESSING_DIRS[subject], subject + "_" + "wm" + ".txt")
        for subject in SUBJECTS
    }
    WM_FODS = {
        subject: os.path.join(
            PROCESSING_DIRS[subject], subject + "_" + "wm_fod" + ".mif"
        )
        for subject in SUBJECTS
    }

    TRACKS = {
        subject: os.path.join(
            PROCESSING_DIRS[subject], subject + "_" + "raw_tractogram.tck"
        )
        for subject in SUBJECTS
    }
    FILTERED_TRACKS = {
        subject: os.path.join(
            PROCESSING_DIRS[subject], subject + "_" + "sift_filtered_tractogram.tck"
        )
        for subject in SUBJECTS
    }

    # T1 is registered rigidly in the MNI152 space
    FUNCTIONAL_ANALYSIS = {
        subject: os.path.join(PRIMAVOICE, "analysis" + "_" + subject)
        for subject in SUBJECTS
    }
    T1 = {
        os.path.join(
            FUNCTIONAL_ANALYSIS[subject],
            "anat",
            subject + "_" + "ses-01_T1W_denoised_debiased_in_MNI152.nii.gz",
        )
        for subject in SUBJECTS
    }
    CONTRAST = {
        os.path.join(
            FUNCTIONAL_ANALYSIS[subject],
            "spm_realign",
            "results_8WM_9CSF_0mvt",
            "In-MNI152"
            + "_"
            + subject
            + "_"
            + "res-8WM_9CSF_0mvt_human_vs_all_t.nii.gz",
        )
        for subject in SUBJECTS
    }
    DWI_TO_T1 = {os.path.join()}

    pass
