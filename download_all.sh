#!/bin/bash

rm -rf ./data/*

python download.py

gunzip ./data/*.gz

for file in ./data/*; do
    mv "$file" "${file}.csv"
done

if [ "$1" != "" ]; then
    echo "Uploading to bucket = " $1
    gsutil cp ./*.csv gs://$1/data
else
    echo "Skipping upload to storage; please specify bucket on google cloud otherwise."
fi