#!/bin/bash

# cd to the docs directory
cd docs

sphinx-apidoc -f -o . ../learn_ml/ ../docs/*

# Generate the html
make html O=-W || { echo 'make html failed' ; exit 1; }
cd ..
