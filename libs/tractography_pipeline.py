"""
Diffusion data processing scripts based on the Mrtrix software :
We choose to have a fully parametrable subject level and then
"""
from libs.mrtrix_wrapping import convert_volume, create_mask, tensor, tensor_metrics, msmt_response, msmt_csd, tissue_classification, gmwm_interface,probabilistic_tractography


def processing_pipeline_subject(path_input_dwi, path_input_gradients, path_input_t1, path_output_dwi,
                                    path_output_t1, path_output_mask, path_output_tensor, path_output_tensor_coeff,
                                    path_output_5tt, path_output_gmwmi, path_output_wm_response,
                                    path_output_gm_response, path_output_csf_response, path_output_wm_fod,
                                    path_output_gm_fod, path_output_csf_fod, path_output_tracks, nb_seeds=1000000):
    """
    :param path_input_dwi:
    :param path_input_gradients:
    :param path_input_t1:
    :param path_output_dwi:
    :param path_output_t1:
    :param path_output_mask:
    :param path_output_tensor:
    :param path_output_tensor_coeff:
    :param path_output_5tt:
    :param path_output_gmwmi:
    :param path_output_wm_response:
    :param path_output_gm_response:
    :param path_output_csf_response:
    :param path_output_wm_fod:
    :param path_output_gm_fod:
    :param path_output_csf_fod:
    :param path_output_tracks:
    :param nb_seeds:
    :return:
    """

    # convert .nii dwi volume into .mif file including gradients information
    convert_volume(path_input_dwi, path_output_dwi, path_input_gradients)

    #extract gross mask from dwi volume
    create_mask(path_output_dwi, path_output_mask)

    # compute tensor and derived metrics (not useful for tractography, can be skipped)
    tensor(path_output_dwi, path_output_tensor)
    tensor_metrics(path_output_tensor, path_output_tensor_coeff)

    #estimate multi-shell multi tissue (wm, gm,csf) impulsionnal response
    msmt_response(path_output_dwi,path_output_wm_response,path_output_gm_response, path_output_csf_response)
    #perform spherical deconvolution of DWI signal
    msmt_csd(path_output_dwi,path_output_wm_response, path_output_gm_response, path_output_csf_response,path_output_wm_fod,path_output_gm_fod, path_output_csf_fod)

    # convert .nii t1 volume into .mif
    convert_volume(path_input_t1, path_output_t1)

    #classify tissues into 5 types (FSL version)
    tissue_classification(path_output_t1, path_output_5tt)
    #and generate gret/white matter interface volume from classification
    gmwm_interface(path_output_5tt, path_output_gmwmi)

    #merge dwi and t1 pipeline --> perform probabilistic anatomically constraint tractography
    probabilistic_tractography(path_output_wm_fod,path_output_5tt,path_output_gmwmi,path_output_tracks,nb_seeds)

    pass



if __name__ == '__main__' :
    pass



