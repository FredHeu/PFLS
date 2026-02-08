		# print header
echo -e "FASTA File Statistics:\n----------------------"
		# store file in variable
fasta=$1

		# split by sequences -> count them individually ->
		# save to variable as list -> count/sum/longest/shortest/avr etc.

while read i; do
  if [[ $i != ">"* ]]; then
  		seqcount+=$(echo "${#i}+")
  	else
  		seqcount+=$(echo "b")
  fi
done <$1

seqcount="${seqcount:1}"
seqcount="$(echo $seqcount | tr "b" '\n' | sed 's/$/0/g' | bc)"

### Task1

num_seq=$(wc -l <<< $seqcount)
echo "Number of sequences: $num_seq"

### Task2

all_sequences=0
for j in $seqcount; do
	all_sequences=$all_sequences+$j
done
echo "Total length of sequences: $((all_sequences))"

### Task3 & 4

sorted=$(sort -n <<< $seqcount)
echo "Length of the longest sequence: $(tail -1 <<< $sorted)"
echo "Length of the shortest sequence: $(head -1 <<< $sorted)"

### Task5

echo "Average sequence length: $(($((all_sequences))/$num_seq))"

### Task6

#GC Content (%): ______




##### --- first approach

### Task 1
		# assess number of sequences:
#num_sequences=$(grep '>' $fasta | wc -l)
#echo "Number of sequences: $num_sequences"

### Task 2
		# check total length of sequences -
		# first solution involved "wc -c" but that was inferior
		# alternative: grep -v '>' -> count [ATGC] (source: Old stackoverflow post)
		# does take a while for large files
#just_sequences=$(grep -v '>' $fasta)
#just_sequences="${just_sequences//[^ATGC]}"
#echo "Total length of sequences: ${#just_sequences}"