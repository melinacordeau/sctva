from scripts.extract_functional_peaks import extract_local_maxima



if __name__ == '__main__':

    import os
    from conf import SUBJS_DIR, SUBJECTS

    subject = SUBJECTS[3]  #sub-04
    dir_subject = SUBJS_DIR[subject]
    test_dir = os.path.join(dir_subject,'test_scripts')
    #if directory does not exist create it else do nothing
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)

    path_functionnal_volume =        # a completer
    path_peaks_coordinates = os.path.join(test_dir, 'functionnal_peaks.txt')

    extract_local_maxima(path_functionnal_volume, path_peaks_coordinates)