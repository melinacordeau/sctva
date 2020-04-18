import subprocess
from distutils import spawn

#Immutable list of Mrtrix commands and scripts (partially) wrapped hereunder
MRTRIX_CMDS = ('mrconvert', 'dwi2mask', 'dwi2tensor','tensor2metrics', 'dwi2response', 'dwi2fod','5ttgen','5tt2gmwmi','tckgen', 'tckedit' )
#Absolute path of the Mrtrix commands to avoid setting path in bash scripts (should not be necessary if mrtrix path set properly)
mrtrix = {cmd: spawn.find_executable(cmd) for cmd in MRTRIX_CMDS}

def convert_volume(path_input_volume, path_output_volume, path_gradient=None):
    '''
    :param path_input_volume:
    :param path_gradient:
    :param path_output_volume:
    :return:
    '''
    if path_gradient is not None:
        cmd = mrtrix['mrconvert'] + ' ' + path_input_volume + ' -fslgrad ' + path_gradient + ' ' + path_output_volume
    else:
        cmd = mrtrix['mrconvert'] + ' ' + path_input_volume + ' ' + path_output_volume
    subprocess.run(cmd)
    pass

def create_mask(path_input_volume, path_mask):
    '''
    :param path_input_volume:
    :param path_mask:
    :return:
    '''
    cmd = mrtrix['dwi2mask'] + ' ' + path_input_volume + ' ' + path_mask
    subprocess.run(cmd)
    pass

def tensor(path_dwi_volume, path_tensor_coeff):
    '''
    :param path_dwi_volume:
    :param path_tensor_coeff:
    :return:
    '''
    cmd = mrtrix['dwi2tensor'] + ' ' + path_dwi_volume + ' ' + path_tensor_coeff
    subprocess.run(cmd)
    pass

def tensor_metrics(path_tensor_coeff, path_metrics):
    cmd = mrtrix['tensor2metrics'] + ' ' + path_tensor_coeff + ' -vec ' + path_metrics
    subprocess.run(cmd)
    pass

def msmt_response (path_dwi_volume, path_mask_volume, path_wm_response, path_gm_response, path_csf_response, path_voxels_volume):
    cmd = mrtrix['dwi2response'] + ' dhollander ' + path_dwi_volume + ' ' + path_wm_response + ' ' + path_gm_response + ' ' + path_csf_response + ' -voxels ' + path_voxels_volume  + ' -mask ' + path_mask_volume
    subprocess.run(cmd)

def msmt_csd (path_dwi_volume, path_wm_response, path_gm_response, path_csf_response, path_wm_fod, path_gm_fod, path_csf_fod):
    cmd = mrtrix['dwi2fod'] + ' ' + 'msmt_csd ' + path_dwi_volume + ' ' + path_wm_response + ' ' + path_wm_fod + ' ' +  path_gm_response + ' ' +  path_gm_fod + ' ' + path_csf_response + '  ' + path_csf_fod
    subprocess.run(cmd)
    pass

def tissue_classification(path_t1_volume, path_tissue_classes_volume):
    cmd = mrtrix['5ttgen'] + ' fsl ' + path_t1_volume + ' ' + path_tissue_classes_volume
    subprocess.run(cmd)
    pass

def gmwm_interface(path_5tt_volume, path_gmwmi_volume):
    cmd = mrtrix['5tt2gmwmi'] + ' ' + path_5tt_volume + ' ' + path_gmwmi_volume
    subprocess.run(cmd)
    pass

def probabilistic_tractography( path_wm_fod_volume, path_tissue_constraint_volume, path_gmwmi_volume, path_tracks, number_seeds=1000000  ):
    cmd = mrtrix['tckgen'] + ' -act ' + path_tissue_constraint_volume + ' -seed_gmwmi ' + path_gmwmi_volume + ' -select ' + str(number_seeds) + ' ' + path_wm_fod_volume + ' ' + path_tracks
    subprocess.run(cmd)
    pass

def select_tracks_between_peaks(path_input_tracks, path_selected_tracks, first_peak, second_peak, radius='5'):
    first_sphere = str(first_peak[0]) + ',' + str(first_peak[1]) + ',' + str(first_peak[2]) + ',' + radius
    second_sphere = str(second_peak[0]) + ',' + str(second_peak[1]) + ',' + str(second_peak[2]) + ',' + radius
    cmd = mrtrix['tckedit'] + ' -select ' + first_sphere + ' -select ' + second_sphere + ' -ends_only ' + path_input_tracks + '  ' + path_selected_tracks
    subprocess.run(cmd)
    pass





