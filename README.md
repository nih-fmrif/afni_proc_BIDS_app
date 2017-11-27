## Prototype AFNI preprocessing app

### Description
This is a prototype AFNI bids app implmenting participant level preprocessing with afni_proc.py.
This pipeline is currently doing temporal alignment, nonlinear registration to standard space,
 bluring of 4 mm, masking, and scaling for all epis in the input bids dataset using the following 
 afni proc command:
```afni_proc.py -subj_id {subj_id} \
 -script proc.bids -scr_overwrite -out_dir {out_dir} \
-blocks tshift align tlrc volreg blur mask scale \
-copy_anat {anat_path} -tcat_remove_first_trs 2 \
-dsets {epi_paths} -volreg_align_to third \
-volreg_align_e2a -volreg_tlrc_warp -blur_size 4.0 -bash```

### Documentation
Documenation for afni_proc.py is available [here](https://afni.nimh.nih.gov/pub/dist/doc/program_help/afni_proc.py.html).

### How to report errors
Specific issues with this BIDS App should be reported on its [issues page](https://github.com/nih-fmrif/afni_proc_BIDS_app/issues).
AFNI issues should be posted to the [AFNI Message Board](https://afni.nimh.nih.gov/afni/community/board/list.php?1)

### Acknowledgements
Please cite the 1996 paper if you use AFNI:
 Cox RW (1996) AFNI: Software for analysis and visualization of functional magnetic resonance neuroimages. Comput Biomed Res 29(3):162–173

### Usage
This App has the following command line arguments:

		usage: run.py [-h]
		              [--participant_label PARTICIPANT_LABEL [PARTICIPANT_LABEL ...]]
		              bids_dir output_dir

		Example BIDS App entry point script.

		positional arguments:
		  bids_dir              The directory with the input dataset formatted
		                        according to the BIDS standard.
		  output_dir            The directory where the output files should be stored.
		                        If you are running a group level analysis, this folder
		                        should be prepopulated with the results of
		                        the participant level analysis.

		optional arguments:
		  -h, --help            show this help message and exit
		  --participant_label PARTICIPANT_LABEL [PARTICIPANT_LABEL ...]
		                        The label(s) of the participant(s) that should be
		                        analyzed. The label corresponds to
		                        sub-<participant_label> from the BIDS spec (so it does
		                        not include "sub-"). If this parameter is not provided
		                        all subjects will be analyzed. Multiple participants
		                        can be specified with a space separated list.

To run it in participant level mode (for one participant):

    docker run -i --rm \
		-v /Users/filo/data/ds005:/bids_dataset:ro \
		-v /Users/filo/outputs:/outputs \
		bids/example \
		/bids_dataset /outputs participant --participant_label 01

### Special considerations
This is a very early prototype. More functionality is likely coming. Expect breaking changes.