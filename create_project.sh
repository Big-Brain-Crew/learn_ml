#!/bin/bash

# Creates a project directory and generates example model and pipelines.

mkdir project
rm -r project/*
touch project/__init__.py
cp learn_ml/common/* project/
python3 tests/example_project_2.py
python3 project/train.py