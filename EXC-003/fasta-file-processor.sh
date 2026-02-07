		# print header
echo -e "FASTA File Statistics:\n----------------------"
		# store file in variable
fasta=$1

		# assess number of sequences:
num_sequences=$(grep '>' $fasta | wc -l)
echo "Number of sequences: $num_sequences"


		# assess total length of sequences -
		# first solution involved "wc -c" but that was inferior
		# alternative: grep -v '>' -> for loop -> count if [ATGC]
just_sequences=$(grep -v '>' $fasta)
just_sequences="${just_sequences//[^ATGC]}"
echo "Total length of sequences: ${#just_sequences}"


#Length of the longest sequence: ______
#Length of the shortest sequence: ______
#Average sequence length: ______
#GC Content (%): ______