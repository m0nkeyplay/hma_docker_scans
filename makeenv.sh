#!/bin/bash
#   Create the docker images needed
cd image_create/scan
pwd
ls
echo 'Creating docker image now'
./create_image.sh
