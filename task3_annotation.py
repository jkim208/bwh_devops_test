#!/usr/bin/env python3
# Program: task3_annotation.py
import argparse  # Command line argument parser


# Function: Run binary search on sorted list of starting positions to find the closest one to target position
def binarySearch(gtf_list, target):
    best_idx = 0
    low_idx = 0
    high_idx = len(gtf_list) - 1
    # Indexes will come together as the sorted list is examined in half-intervals
    while low_idx <= high_idx:
        mid_idx = low_idx + ((high_idx - low_idx) // 2)  # Round down when finding mid index
        if gtf_list[mid_idx] < target:
            low_idx = mid_idx + 1
        elif gtf_list[mid_idx] > target:
            high_idx = mid_idx - 1
        else:  # Exact target value found
            best_idx = mid_idx
            break
        # Determine if the middle index is closer to the target than the current best index
        if abs(gtf_list[best_idx] - target) > abs(gtf_list[mid_idx] - target):
            best_idx = mid_idx
    return best_idx

# Function: Read through the GTF and create complex data structures for quick annotation lookups
def processGTF(gtf):
    gtf_all = {}  # Includes annotation and ending coordinates
    gtf_starts = {}  # Only has starting coordinates for sorting purposes
    for line in gtf:
        listed_line = line.rstrip().split("\t")
        chro = listed_line[0]
        start_pos = listed_line[3]
        end_pos = listed_line[4]
        annotation = listed_line[8]

        if chro in gtf_all: 
            gtf_all[chro][start_pos] = [int(end_pos), annotation]
            gtf_starts[chro].append(int(start_pos))
        else:  # Key (chromosome) missing. Initialize dictionaries
            gtf_all[chro] = {}
            gtf_all[chro][start_pos] = [int(end_pos), annotation]
            gtf_starts[chro] = []
            gtf_starts[chro].append(int(start_pos))
    return(gtf_all, gtf_starts)

def main():
    # Grab command line arguments if any. Default input is current directory.
    parser = argparse.ArgumentParser(description='Given a chromosome and coordinates, '
                                                 'look up the the genome annotations')
    group = parser.add_argument_group('required arguments')
    group.add_argument('-targets', help='File with list of chromosomes and coordinates', required=True)
    group.add_argument('-gtf', help='GTF formatted file with genome annotations', required=True)
    args = parser.parse_args()

    with open(args.gtf, 'r') as gtf:
        (gtf_all, gtf_starts) = processGTF(gtf)
    
    # Sort the start positions for each chromosome dictionary to reduce annotation lookup burden
    for chro in gtf_starts.keys():
        gtf_starts[chro].sort()

    with open(args.targets, 'r') as targets:
        for line in targets:
            listed_line = line.rstrip().split("\t")
            t_chro = listed_line[0]
            t_pos = int(listed_line[1])
            if t_chro in gtf_starts:
                # Find the closest starting position from gtf list to the target position
                idx = binarySearch(gtf_list = gtf_starts[t_chro], target = t_pos)
                t_start = gtf_starts[t_chro][idx]

                # Confirm that target_start is within a gene's start and end coordinates
                if t_start <= t_pos <= gtf_all[t_chro][str(t_start)][0]:
                    # No index adjustment needed
                    print(gtf_all[t_chro][str(t_start)][1])
                elif idx == 0:
                    # The coordinate is below any annotated coordinate range
                    print("Target position is not associated with an annotation from the GTF file")
                elif gtf_starts[t_chro][idx - 1] <= t_pos <= t_start:
                    # Target_start is closest to an end coordinate. Shift index down one.
                    t_start = gtf_starts[t_chro][idx - 1]
                    print(gtf_all[t_chro][str(t_start)][1])
                else:
                    # The coordinate is above any annotated coordinate range
                    print("Target position is not associated with an annotation from the GTF file")
            else:
                print("Target chromosome does not appear in GTF file")
    return

if __name__ == '__main__':
    main()
