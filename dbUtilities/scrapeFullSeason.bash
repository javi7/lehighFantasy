#!/bin/bash

for week in {1..12}
do
	python parseTesting.py -w $week >> log.out
done
