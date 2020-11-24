which python
FUNC='/hpc/banco/Primavoice_Data_and_Analysis/analysis_sub-04/spm_realign/results_8WM_9CSF_0mvt/In-MNI152_sub-04_res-8WM_9CSF_0mvt_human_vs_all_t.nii.gz'
FUNC_PEAKS='/home/alex/recherche/tests/functionnal_peaks.nii.gz'
ANAT='/hpc/banco/Primavoice_Data_and_Analysis/analysis_sub-04/anat/sub-04_ses-01_T1w_denoised_debiased_in-MNI152.nii.gz'
python /home/alex/PycharmProjects/sctva/sctva/scripts/extract_local_peaks.py $FUNC $FUNC_PEAKS
