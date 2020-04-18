from libs.tractography_pipeline import processing_pipeline_subject
from conf import SUBJECTS


if __name__ == '__main__':

    for subject in SUBJECTS:
        processing_pipeline_subject() #to be completed
