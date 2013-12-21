#!/bin/sh

./codify.py -i "Test string" -o test.svg -p NaivePainter && [ -f "test.svg" ] && rm test.svg
./codify.py -i "Test string" -o test.svg -p ManchesterPainter && [ -f "test.svg" ] && rm test.svg
./codify.py -i "Test string" -o test.svg -p DifferentialManchesterPainter && [ -f "test.svg" ] && rm test.svg
