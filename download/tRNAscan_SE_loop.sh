#!/bin/bash

# Exit on error
set -e

# Loop over each .fasta file in the current directory
for fasta_file in *.fasta; do
    # Get filename without the .fasta extension
    base_name="${fasta_file%.fasta}"
    
    # Create results directory
    result_dir="${base_name}_results"
    mkdir -p "$result_dir"
    
    echo "Processing $fasta_file ..."

    # Run tRNAscan-SE and store results in the respective directory
    tRNAscan-SE -A -H "$fasta_file" -o "$result_dir/${base_name}_tRNAscan.txt" -a "$result_dir/${base_name}_trnas.txt" -f "$result_dir/${base_name}_ss.txt" --detail

    echo "Results stored in $result_dir"
done
