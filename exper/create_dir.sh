#!/bin/sh

if [ $# -eq 0 ]; then
    echo "Usage"
    echo " 1. Provide experiment directory"
    exit 1
fi

dir=$1
mkdir "$dir"/config
mkdir "$dir"/features
mkdir "$dir"/features2
mkdir "$dir"/list
mkdir "$dir"/log
mkdir "$dir"/model
mkdir "$dir"/res
