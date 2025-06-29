#!/bin/bash

# Loop over all .fasta files in the current directory
for file in *.fasta; do
    # Check if the file exists 
    [ -e "$file" ] || continue

    # Run mlocarna and capture the full output
    output=$(mlocarna --stockholm "$file")

    # Get the last line of the output
    last_line=$(echo "$output" | tail -n 1)

    # Create a new filename for the output
    output_file="${file%.fasta}_alifold_consensus.txt"

    # Save the last line to the new file
    echo "$last_line" > "$output_file"

    echo "Saved consensus to $output_file"
done