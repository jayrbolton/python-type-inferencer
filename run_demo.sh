#!/bin/bash
rm logs/* ; jython main.py tests/src/demo.py ; cat logs/*
