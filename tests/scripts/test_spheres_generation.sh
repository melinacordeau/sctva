FUNC='/hpc/banco/Primavoice_Data_and_Analysis/analysis_sub-04/spm_realign/results_8WM_9CSF_0mvt/In-MNI152_sub-04_res-8WM_9CSF_0mvt_human_vs_all_t.nii.gz'
FUNC_PEAKS='/home/alex/recherche/tests/functionnal_peaks.nii.gz'
SPHERES='/home/alex/recherche/tests/spheres.gii'
ANAT='/hpc/banco/Primavoice_Data_and_Analysis/analysis_sub-04/anat/sub-04_ses-01_T1w_denoised_debiased_in-MNI152.nii.gz'
/home/alex/softs/brainvisa-4.6.1/bin/python /home/alex/PycharmProjects/sctva/sctva/scripts/generate_spheres.py $FUNC_PEAKS $SPHERES
