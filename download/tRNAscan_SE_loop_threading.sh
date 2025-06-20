#!/bin/bash

# Exit on errors
set -e

# === Configuration ===
MAX_JOBS=4           # Number of concurrent files to process
THREADS_PER_JOB=4    # Number of threads for each tRNAscan-SE run

# === Function to process each file ===
process_fasta_file() {
    local fasta_file="$1"
    local base_name="$(basename "$fasta_file" .fasta)"
    local result_dir="${base_name}_results"

    mkdir -p "$result_dir"
    echo "Processing $fasta_file with $THREADS_PER_JOB threads..."

    tRNAscan-SE -A -H "$fasta_file" -o "$result_dir/${base_name}_tRNAscan.txt" -a "$result_dir/${base_name}_trnas.txt" -f "$result_dir/${base_name}_ss.txt"  --thread "$THREADS_PER_JOB" --detail

    echo "Finished $fasta_file"
}

export -f process_fasta_file

# === Main parallel execution ===
# Find all .fasta files and process in parallel
ls *.fasta | xargs -n 1 -P "$MAX_JOBS" bash -c 'process_fasta_file "$0"' 
