"""

"""

import nipype.pipeline.engine as pe
from nipype.interfaces.utility import Function


def select_between_spheres(input_tracks, pair, output_tracks):
    """
    Select tracks whose extremities are located inside two spheres
    :param input_tracks: path to the tck file
    :param sphere1:tuple  (x1,y1,z1,r1)
    :param sphere2: tuple (x2,y2,z2,r2)
    :param output_tracks: path to output the selected tracks
    :return: None
    """
    import subprocess
    from distutils import spawn

    sphere1, sphere2 = pair

    def sphere_to_string(sphere):
        return str(sphere)[1:-1]

    tckedit = spawn.find_executable("tckedit")
    cmd = (
        tckedit
        + " "
        + input_tracks
        + " "
        + "-include"
        + " "
        + sphere_to_string(sphere1)
        + " "
        + "-include"
        + sphere_to_string(sphere2)
        + output_tracks
    )
    subprocess.run(cmd)
    pass


def create_tracks_selection_node():
    """
    :return:
    """
    tracks_selection = pe.MapNode(
        name="tracks_selection",
        interface=Function(
            input_names=["input_tracks", "pairs"],
            output_names=["output_tracks"],
            function=select_between_spheres,
        ),
        iterfield=["pairs"],
    )
    return tracks_selection
