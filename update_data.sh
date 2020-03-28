#!/bin/sh

sh ./get_data.sh
python3 parse.py
./main
