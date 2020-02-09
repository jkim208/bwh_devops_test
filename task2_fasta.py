#!/usr/bin/env python3
# Program: task2_fasta.py
import argparse  # Command line argument parser


# Function: Keep track of sequences and how many times they appear in the file
def processFastaSeqs(fasta):
    seq_counts = {}
    for line in fasta:
        line = line.rstrip()
        if not line.startswith('>'):  # Grab sequences, not headers
            if line in seq_counts:
                seq_counts[line] += 1
            else:
                seq_counts[line] = 1
    return(seq_counts)

# Function: Check if the file is a fasta. End program if not.
def checkIfFasta(file):
    if not file[-6:] == ".fasta":
        raise Exception("Input file does not end with .fasta")
    with open(file, 'r') as f:
        if not f.readline().startswith('>'):
            raise Exception("First line in file does not have a Fasta header")

def main():
    # Grab command line arguments if any. Default input is current directory.
    parser = argparse.ArgumentParser(description='Take a FASTA file with DNA sequences and find the '
                                                 '10 most frequent sequences and return the sequence '
                                                 'and their counts in the file')
    group = parser.add_argument_group('required arguments')
    group.add_argument('-input', help='Fasta file', required=True)
    args = parser.parse_args()

    checkIfFasta(file = args.input)

    with open(args.input, 'r') as f:
        seq_counts = processFastaSeqs(fasta = f)
        # Itemize the dictionary into key-val pairs to make them sortable
        seq_counts_items = seq_counts.items()
        # Sort the seq_counts in desc order based on its counts via the key argument
        top10_seqs = sorted(seq_counts_items, key=lambda x: x[1], reverse = True)[:10]
        print("The top 10 most frequent sequences in", args.input,  "are...")
        print("Sequence : Count")
        for x in range(len(top10_seqs)): 
            print(top10_seqs[x][0], ":", top10_seqs[x][1])
    return

if __name__ == '__main__':
    main()
