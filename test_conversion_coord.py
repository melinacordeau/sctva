from soma import aims

path_vol = '/hpc/banco/VOICELOC/nifti_raw/sub-ACE12/ses-01/anat/sub-ACE12_ses-01_T1w.nii'

x = -45
y = 18
z = -36

input = aims.Point3df(x, y, z)
vol = aims.read(path_vol)
aims_mm_to_ras_mm = aims.AffineTransformation3d(vol.header()['transformations'][0])
output = aims_mm_to_ras_mm.transform(input)

print output