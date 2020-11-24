TRACKS='/home/alex/recherche/tests/diffusion_pipeline/core_diffusion_pipeline/tractogram_pipeline/tractography/tracked.tck'
PEAKS='/home/alex/recherche/tests/streamlines_selection/test_fake_volume_dwi_space.nii.gz'
DIR_OUT='/home/alex/recherche/tests/streamlines_selection'
python /home/alex/PycharmProjects/sctva/sctva/scripts/select_streamlines_from_peaks.py $TRACKS $PEAKS $DIR_OUT