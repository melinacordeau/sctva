def peaks_to_rois(peaks_volume):
    """
    Generate a
    :param peaks_volume:
    :return:
    """
    import numpy as np
    peaks_index = np.where(peaks_volume !=0)
    nb_peaks = len(peaks_index[0])
    peaks_rois = np.zeros((nb_peaks,) + peaks_volume.shape, dtype=bool)
    for i in range(nb_peaks):
        peaks_rois[i, peaks_index[0][i], peaks_index[1][i],peaks_index[2][i]] = 1
    return peaks_rois


def select_streamlines_between_peaks_from_spheres(streamlines, peaks_rois,affine,
                                                index_peak1,
                                    index_peak2, radius=5):
    from dipy.tracking.streamline import select_by_rois
    import numpy as np
    roi1 = peaks_rois[index_peak1]
    roi2 = peaks_rois[index_peak2]
    roi = roi1 + roi2
    roi = np.expand_dims(roi, axis=0)
    selected_tracks = select_by_rois(streamlines, affine=affine,rois=roi, \
                                                                   mode='both_end',
                                     include=np.array([True]),
                                     tol=radius)
    return selected_tracks
