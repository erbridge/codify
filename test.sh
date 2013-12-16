#!/bin/sh

./codify.py -i "Test string" && [ -f "output.svg" ]
