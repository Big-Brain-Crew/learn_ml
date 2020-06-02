#!/bin/bash

# Creates a project directory and generates example model and pipelines.

rm -r project/
mkdir project
mkdir project/assets
mkdir project/models
mkdir project/pipelines
mkdir project/results
touch project/__init__.py
touch project/assets/__init__.py
cp learn_ml/common/* project/
python3 tests/example_project_2.py