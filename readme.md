# Coding test for Bioinformatics DevOps1

## Folder contents
The python scripts address each of the 3 Bioinformatics tasks. Sample input files to be used with scripts.

## Directions
All the scripts have a '-h' switch for more information on how to run. Some examples below:

$ python3 task1_fastq.py

$ python3 task2_fasta.py -input /sample_files-2/fasta/sample.fasta

$ python3 task3_annotation.py -targets sample_files-2/annotate/coordinates_to_annotate.txt -gtf sample_files-2/gtf/hg19_annotations.gtf > output.txt

## Comments
The gtf folder in this repo is missing the gtf file due to Github file size constraints (>100MB).
No modules were imported for these scripts except for built-in parsing and OS interfacing.
Annotations were interpreted to be the "gene and transcript description" column.