#!/bin/bash

# Combine a bunch of data cards together, giving each bin/category a nice name.
#
# Usage:
#
#   combine_cards_with_names.sh /path/to/cards/*.txt > megacard.txt
#
# Author: Evan K. Friis, UW Madison
#
# Just running combineCards.py a/bunch/of/cards/*.txt
# Destroys all the information about the bin names in the cards and replaces it
# with ch1, ch2, etc.  This script uses the file name as bin label.

MIN_ARGS=1
if [ $# -lt $MIN_ARGS ]
then
  echo "Usage: $0 /path/to/cards/*.txt > megacard.txt"
  exit 1
fi

OUTPUT_COMMAND="combineCards.py -S "

# Loop over list of input cards
for card in $@
do
  cardname=`basename $card | sed "s|.txt||"`
  #echo $cardname
  OUTPUT_COMMAND="$OUTPUT_COMMAND $cardname=$card"
done

$OUTPUT_COMMAND
