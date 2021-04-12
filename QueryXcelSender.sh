#!/bin/bash

# declare py script path variable
PYSCRIPT=~/Documents/pythonCollection/queryDB/user*.py

# start to loop py script
for dotpy in $PYSCRIPT
do
  echo "Output log for $dotpy"
  python3 "$dotpy" "$1" "$2"
  echo ""
done
