#!/bin/sh
# Simply run all the tests in this dir
# Run this from the project root; i.e. tests/test_all.sh

jython tests/inftype_tests.py

jython tests/parser_tests.py

jython tests/pytown_tests.py
