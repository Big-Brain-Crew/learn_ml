#!/bin/bash

# cd to the docs directory
cd docs

# Build API docs from the docstrings
sphinx-apidoc -W --implicit-namespaces -f -o . .. ../docs/* || { echo 'sphinx-apidoc failed' ; exit 1; }
# Generate the html
make html || { echo 'make html failed' ; exit 1; }
cd ..
