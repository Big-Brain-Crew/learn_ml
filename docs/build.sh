#!/bin/bash

cd docs

sphinx-apidoc -o . ..
make html
