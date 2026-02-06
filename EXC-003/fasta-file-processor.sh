		# print header
echo -e "FASTA File Statistics:\n----------------------"
		

		# assess number of sequences:
num_sequences=$(grep '>' $1 | wc -l)
echo "Number of sequences: $num_sequences"


		# assess total length of sequences
len_sequences=$(grep -v '>' $1 | wc -c)
len_sequences=$((len_sequences-$(grep -v '>' $1 | wc -l)))
		# substracts num_lines in sequences. Gets rid of linebreak-bias.
echo "Total length of sequences: $len_sequences"


#Length of the longest sequence: ______
#Length of the shortest sequence: ______
#Average sequence length: ______
#GC Content (%): ______