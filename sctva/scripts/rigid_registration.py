"""

Python script to estimate a rigid transformation between a FA volume and a T1 volume
and use
This is a rustine script written to overcome difficulties with niyppe pipeline

"""

import argparse


def build_argparser():
    """
    :return:
    """
    DESCRIPTION = "Perform a rigid registration between the FA volume (dwi space) and the T1 volume and transport the associated functionnal volume into the diffusion space"

    p = argparse.ArgumentParser(description=DESCRIPTION)
    p.add_argument(
       "fa", metavar="fa", help=" path of the Fractionnal Anistotropy (fa) volume"
    )
    p.add_argument("t1", metavar="t1", help="path of the t1 volume")
    p.add_argument("dwi_to_t1", metavar="dwi_to_t1",help=" path of the text "
                                                         "file to store the diffusion ("
                                                         "dwi) "
                                                         "to t1 space rigid transform")
    p.add_argument("func_contrast_t1", metavar="func_contrast_t1", help="functionnal "
                                                                 "constrast volume in t1 space"
    )
    p.add_argument("t1_dwi", metavar="t1_dwi", help="path of the t1 volume aligned on "
                                                    "fa volume ("
                                                    "dwi space)")
    p.add_argument("func_contrast_dwi", metavar="func_contrast_dwi",
                   help="path of the functionnal contrast volume aligned on fa volume ("
                        "dwi space)")

    return p


def mrregister_rigid(image, template, transform):
    """
    Dirty wrapping of the Mrtrix3 mrregister command that estimate rigid transformation
    between a volume  and template

    See mrregister documentation for further details
    (https://mrtrix.readthedocs.io/en/latest/reference/commands/mrregister.html)

    :param image: path of the volume to register
    :param template: path of the reference volume
    :param transform: path of the text file containing the estimated rigid transform
    :return:
    """
    import subprocess
    from distutils import spawn

    mrregister = spawn.find_executable("mrregister")
    cmd = [mrregister, '-type', 'rigid', '-rigid', transform, image, template, '-f']
    subprocess.run(cmd)
    pass


def mrtransform_linear(in_file, out_file, transform):
    """
    Dirty wrapping of the mrtransform command to apply linear transform to a volume.

    The transform is applied by modfying the affine transform in the header of the
    volume (see https://mrtrix.readthedocs.io/en/latest/reference/commands
    /mrtransform.html) for further details)

    :param in_file: path of the input volume
    :param out_file: path of the transformed volume
    :param transform: path of the text file storing the rigid transform
    :return: None
    """
    import subprocess
    from distutils import spawn

    mrtransform = spawn.find_executable("mrtransform")
    # inverse option is passed to take into account reverse convention (see Mrtrix doc)
    cmd = [mrtransform, '-linear', transform, '-inverse', in_file, out_file, '-force']
    subprocess.run(cmd)
    pass


def main():
    """
    Estimate a rigid transform between an FA volume and a T1 volume and apply this
    transform to transport other volumes (functionnal contrast aligned with T1) into
    the FA (diffusion) space
    :return:
    """
    parser = build_argparser()
    args = parser.parse_args()

    mrregister_rigid(args.fa, args.t1, args.dwi_to_t1)
    # apply transform to t1 volume
    mrtransform_linear(args.t1, args.t1_dwi,  args.dwi_to_t1)
    # apply_transform to functionnal contrast
    mrtransform_linear(args.func_contrast_t1, args.func_contrast_dwi, args.dwi_to_t1)


if __name__ == "__main__":
    main()
