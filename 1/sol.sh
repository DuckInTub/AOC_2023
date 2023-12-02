#!/bin/bash
cat input.txt | awk '{gsub(/[^0-9]+/, "", $0); s+= 10*substr($0, 1, 1)+substr($0, length, 1)}END{print s}'
