#!/bin/bash
#
#echo -e "Inferring assignments...\n\n"
#rm output/logs/*
#jython main.py src/tests/assignment.py
#cat output/logs/*
#
#echo -e "Enter to continue...\n\n"
#read x
#
#
#echo -e "Inferring function definitions and calls...\n\n"
#rm output/logs/*
#jython main.py src/tests/functions.py
#cat output/logs/*
#
#echo -e "Enter to continue...\n\n"
#read x

echo -e "Inferring class definitions and usage...\n\n"
rm output/logs/*
jython main.py src/tests/classes.py
cat output/logs/*

echo -e "Enter to continue...\n\n"
read x
