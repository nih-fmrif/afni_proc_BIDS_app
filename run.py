#!/usr/bin/env python3
import argparse
import os
import subprocess
from glob import glob

__version__ = open(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                'version')).read()

def run(command, env={}):
    merged_env = os.environ
    merged_env.update(env)
    process = subprocess.Popen(command, stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT, shell=True,
                               env=merged_env)
    while True:
        line = process.stdout.readline()
        line = str(line, 'utf-8')[:-1]
        print(line)
        if line == '' and process.poll() != None:
            break
    if process.returncode != 0:
        raise Exception("Non zero return code: %d"%process.returncode)

parser = argparse.ArgumentParser(description='Example BIDS App entrypoint script.')
parser.add_argument('bids_dir', help='The directory with the input dataset '
                    'formatted according to the BIDS standard.')
parser.add_argument('output_dir', help='The directory where the output files '
                    'should be stored. If you are running group level analysis '
                    'this folder should be prepopulated with the results of the'
                    'participant level analysis.')
parser.add_argument('--participant_label', help='The label(s) of the participant(s) that should be analyzed. The label '
                   'corresponds to sub-<participant_label> from the BIDS spec '
                   '(so it does not include "sub-"). If this parameter is not '
                   'provided all subjects should be analyzed. Multiple '
                   'participants can be specified with a space separated list.',
                   nargs="+")
parser.add_argument('-v', '--version', action='version',
                    version='BIDS-App example version {}'.format(__version__))



cmd_skeleton = """python /opt/afni/afni_proc.py -subj_id {subj_id} \
 -script proc.bids -scr_overwrite -out_dir {out_dir} \
-blocks tshift align tlrc volreg blur mask scale \
-copy_anat {anat_path} -tcat_remove_first_trs 2 \
-dsets {epi_paths} -volreg_align_to third \
-volreg_align_e2a -volreg_tlrc_warp -blur_size 4.0 -bash"""

args = parser.parse_args()

run('bids-validator %s'%args.bids_dir)

subjects_to_analyze = []
# only for a subset of subjects
if args.participant_label:
    subjects_to_analyze = args.participant_label
# for all subjects
else:
    subject_dirs = glob(os.path.join(args.bids_dir, "sub-*"))
    subjects_to_analyze = [subject_dir.split("-")[-1] for subject_dir in subject_dirs]

# find all T1s and skullstrip them
for subject_label in subjects_to_analyze:
    anat_path = list(glob(os.path.join(args.bids_dir, "sub-%s"%subject_label,
                                             "anat", "*_T1w.nii*")) + glob(os.path.join(args.bids_dir,"sub-%s"%subject_label,"ses-*","anat", "*_T1w.nii*")))[0]
    epi_paths = ' '.join(list(glob(os.path.join(args.bids_dir, "sub-%s"%subject_label,
                                             "func", "*bold.nii*")) + glob(os.path.join(args.bids_dir,"sub-%s"%subject_label,"ses-*","func", "*bold.nii*"))))
    subj_out_dir = os.path.join(args.output_dir,"sub-%s"%subject_label)
    cmd = cmd_skeleton.format(subj_id = subject_label, out_dir = subj_out_dir, anat_path = anat_path, epi_paths = epi_paths)
    print(cmd)
    run(cmd)
    print("tcsh -xef proc.bids 2>&1 | tee output.proc.bids")
    run("tcsh -xef proc.bids 2>&1 | tee output.proc.bids")
