#/bin/bash

# DOES NOT WORK IN PYTHON2

for f in ./not_translated/2*
do
    echo $f
    python3 translate_not_updated.py $f
done
  
for f in ./not_translated/updated/*
do
    echo $f
    python3 translate_updated.py $f
done
