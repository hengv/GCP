#!/bin/bash
while IFS='' read -r line || [[ -n "$line" ]]; do
    echo "sox $line --channels=1 --rate 16k --bits 16  ./sox/$line"
#  if [[ $line == *" (1).wav" ]]; then
#    echo  "mv ${line% *}\ \(1\).wav ${line% *}.wav"
#  fi
done < "$1"
