#!/bin/bash

# cd to the docs directory
cd docs

# Build API docs from the docstrings
# || { echo 'sphinx-apidoc failed' ; exit 1; }
before=$(stat -L -c %y /proc/self/fd/2)
if sphinx-apidoc --implicit-namespaces -f -o . .. ../docs/* &&
 after=$(stat -L -c %y /proc/self/fd/2) &&
 [ "$after" = "$before" ]
then echo 'Docs built successfully!'
else exit 1
fi

# echo hello
# if { sphinx-apidoc -q --implicit-namespaces -f -o . .. ../docs/* 2>&1 >&3 3>&- | grep '^' >&2; } 3>&1; then
#   exit 1
# fi
# echo goodbye



# Generate the html
make html || { echo 'make html failed' ; exit 1; }
cd ..
