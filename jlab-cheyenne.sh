#!/bin/bash

echo "ssh -N -L 8877:`hostname`:8877 $USER@cheyenne.ucar.edu"
jupyter lab --no-browser --ip=`hostname` --port=8877
