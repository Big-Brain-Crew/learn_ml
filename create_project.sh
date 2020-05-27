#!/bin/bash

# Creates a project directory and generates example model and pipelines.

mkdir project
rm project/*
touch project/__init__.py
cp common/* project/
python3 tests/example_project.py
python3 project/train.py