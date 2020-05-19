#!/bin/bash

# cd to the docs directory
cd docs

# Build API docs from the docstrings
sphinx-apidoc --implicit-namespaces -f -o . .. docs
# Generate the html
make html
cd ..
