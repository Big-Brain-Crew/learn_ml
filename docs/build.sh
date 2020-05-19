#!/bin/bash

# cd to the docs directory
cd docs

# Build API docs from the docstrings
sphinx-apidoc -o . ..
# Generate the html
make html
