#!/bin/bash

# cd to the docs directory
cd docs

# Build API docs from the docstrings
# || { echo 'sphinx-apidoc failed' ; exit 1; }
# before=$(stat -L -c %y /proc/self/fd/2)
# if sphinx-apidoc -q --implicit-namespaces -f -o . .. ../docs/* &&
#  after=$(stat -L -c %y /proc/self/fd/2) &&
#  [ "$after" = "$before" ]
# then echo 'command ok'
# else echo 'command fail'
# fi

if { phinx-apidoc -q --implicit-namespaces -f -o 2>&1 >&3 3>&- | grep '^' >&2; } 3>&1; then
  echo there was some output on stderr
fi



# Generate the html
make html || { echo 'make html failed' ; exit 1; }
cd ..
