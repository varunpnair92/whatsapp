#!/bin/bash

# Set input file and chunk size
input_file=$1
chunk_size=3000

# Set initial chunk counter and file counter
chunk_counter=1
file_counter=3000

# Function to create vCard file
create_vcard() {
    local file_name="$1.vcf"
    local chunk_data="$2"
    echo -e "$chunk_data" > "cbse$file_name"
}

# Initialize variables to store chunk data
chunk_data=""

# Read the input file line by line
while IFS=, read -r name phone_number; do
    # Create vCard data for the current entry
    vcard_data="BEGIN:VCARD\nVERSION:2.1\nN:;$name.keem25;;;\nFN:$name.keem25\nTEL;CELL;PREF:$phone_number\nEND:VCARD"

    # Append vCard data to chunk data
    chunk_data="$chunk_data$vcard_data\n"

    # If chunk size is reached, create vCard file and reset chunk data
    if (( $((++counter)) % $chunk_size == 0 )); then
        create_vcard $file_counter "$chunk_data"
        chunk_data=""
        ((chunk_counter++))
        ((file_counter+=3000))
    fi
done < "$input_file"

# If there are remaining entries, create vCard file for the last chunk
if [ -n "$chunk_data" ]; then
    create_vcard $file_counter "$chunk_data"
fi

