##!/bin/bash
#
#echo -e "Inferring assignments...\n\n"
#rm logs/*
#jython main.py tests/src/assignment.py
#cat logs/*
#
#echo -e "Enter to continue...\n\n"
#read x
#
#
echo -e "Inferring function definitions and calls...\n\n"
rm logs/*
jython main.py tests/src/functions.py
cat logs/*

echo -e "Enter to continue...\n\n"
read x

#echo -e "Inferring class definitions and usage...\n\n"
#rm logs/*
#jython main.py tests/src/classes.py
#cat logs/*
#
#echo -e "Enter to continue...\n\n"
#read x
