### prep

echo -e "FASTA File Statistics:\n----------------------"

fasta=$1

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

num_seq=$(wc -l <<< $seqcount | awk '{print $1}')
echo "Number of sequences: $num_seq"

### Task2

all_sequences=0
for j in $seqcount; do
	all_sequences=$all_sequences+$j
done

all_sequences="$(echo $((all_sequences)))"

echo "Total length of sequences: $((all_sequences))"

### Task3 & 4

sorted=$(sort -n <<< $seqcount)
echo "Length of the longest sequence: $(tail -1 <<< $sorted)"
echo "Length of the shortest sequence: $(head -1 <<< $sorted)"

### Task5

echo "Average sequence length: $(($((all_sequences))/$num_seq))"

### Task6

just_sequences=$(grep -v '>' $fasta)
GC_abs="$(echo $just_sequences | awk '{gc_count += gsub(/[GgCc]/, "")} END {print gc_count}')"
GC_rel="$(echo "scale=3; $GC_abs/$all_sequences*100" | bc)"
echo "GC Content (%): $GC_rel"
