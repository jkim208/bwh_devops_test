#!/usr/bin/env python3
# Program: task1_fastq.py
import argparse  # Command line argument parser
import os  # Operating system interface module


# Function: Return the percentage of sequences that have > 30 nucleotides
def processFastqSeqs(fastq):
        i = 1
        total_seqs = 0
        long_seqs = 0
        for line in fastq:
            line = line.rstrip()
            if i == 2:  # Sequence line is the 2nd line in a fastq record
                total_seqs += 1
                if len(line) > 30:
                    long_seqs += 1
            if i == 4:  # End of record --> reset i to 1
                i = 1
            else:
                i += 1

        percentG30 = round(100 * (long_seqs / total_seqs), 2)
        return(percentG30)           

# Function: Check if the the fastq file has the correct header.
def checkFastqHeader(fastq):
    with open(fastq, 'r') as f:
        if not f.readline().startswith('@'):
            print("First line in", fastq, "does not have a Fastq header. File skipped.\n")
            return False
        else:
            return True

def main():
    # Grab command line arguments if any. Default input is current directory.
    parser = argparse.ArgumentParser(description='Recursively find all FASTQ files in a directory '
                                                 'and report each file\'s name and the percent of '
                                                 'sequences in the file that are > 30 nucleotides')
    group = parser.add_argument_group('required arguments')
    group.add_argument('-input', help='Folder to check for FASTQ files', required=False, default='.')
    args = parser.parse_args()

    # Recursive search of directories and files for FASTQs
    for root, dirs, files in os.walk(str(args.input)):
        for file in files:
            if file.endswith(".fastq"):
                print("File name:", file)
                if checkFastqHeader(fastq = os.path.join(root, file)) == True:
                    with open(os.path.join(root, file)) as f:
                        percentG30 = processFastqSeqs(fastq = f)
                        print("This FASTQ file has", str(percentG30), \
                            "% of its sequences that are > 30 nucleotides long\n")
    return

if __name__ == '__main__':
    main()
