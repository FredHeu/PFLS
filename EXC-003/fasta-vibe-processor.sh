#!/bin/bash

# Error checking
if [[ ! -f "$1" ]]; then
    echo "Error: File '$1' not found or no file provided." >&2
    exit 1
fi

if [[ ! -s "$1" ]]; then
    echo "Error: File '$1' is empty." >&2
    exit 1
fi

if ! grep -q '^>' "$1"; then
    echo "Error: File '$1' does not appear to be a valid FASTA file (no header lines found)." >&2
    exit 1
fi

echo -e "FASTA File Statistics:\n----------------------"

declare -a lengths
total=0
gc_count=0
current_len=0

while IFS= read -r line; do
    if [[ $line == ">"* ]]; then
        [[ $current_len -gt 0 ]] && lengths+=($current_len) && total=$((total + current_len))
        current_len=0
    else
        current_len=$((current_len + ${#line}))
        # Faster GC counting with parameter expansion
        temp=${line//[^GCgc]}
        gc_count=$((gc_count + ${#temp}))
    fi
done < "$1"

[[ $current_len -gt 0 ]] && lengths+=($current_len) && total=$((total + current_len))

num_seq=${#lengths[@]}
echo "Number of sequences: $num_seq"
echo "Total length of sequences: $total"

IFS=$'\n' sorted=($(printf '%s\n' "${lengths[@]}" | sort -n))
echo "Length of the longest sequence: ${sorted[-1]}"
echo "Length of the shortest sequence: ${sorted[0]}"

echo "Average sequence length: $((total / num_seq))"

GC_rel=$(echo "scale=3; $gc_count*100/$total" | bc)
echo "GC Content (%): $GC_rel"

### Histogram of sequence lengths
echo -e "\nSequence Length Distribution:"
echo "----------------------------"

# Find bin width (use max/10 or at least 10)
max_len=${sorted[-1]}
bin_width=$(( max_len / 10 ))
[[ $bin_width -lt 10 ]] && bin_width=10

# Count sequences per bin
declare -A bins
for len in "${lengths[@]}"; do
    bin=$(( len / bin_width * bin_width ))
    bins[$bin]=$(( ${bins[$bin]:-0} + 1 ))
done

# Find max count for scaling
max_count=0
for count in "${bins[@]}"; do
    [[ $count -gt $max_count ]] && max_count=$count
done

# Print histogram
for bin in $(printf '%s\n' "${!bins[@]}" | sort -n); do
    count=${bins[$bin]}
    bar_len=$(( count * 50 / max_count ))
    bar=$(printf '%*s' "$bar_len" | tr ' ' '█')
    printf "%5d-%5d | %-50s %d\n" "$bin" "$((bin + bin_width - 1))" "$bar" "$count"
done