#!/bin/sh

if [ $# -eq 0 ]; then
  echo "Usage"
  echo " 1. Provide experiment directory"
  exit 1
fi

dir=$1

if [ -d "$dir" ]; then 
  echo "Already exist. Abort."
  exit 1
fi

mkdir -p "$dir"/config/resnet
mkdir -p "$dir"/features/resnet/val
mkdir "$dir"/features2
mkdir "$dir"/list
mkdir "$dir"/log
mkdir -p "$dir"/model/resnet
mkdir -p "$dir"/res/resnet
