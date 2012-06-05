#!/bin/bash
rm output/logs/*.log ; jython infer.py $1 ; less output/logs/*.log
