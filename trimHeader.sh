#! /usr/bin/env bash
# Inputs: 
#   1- yaml that has a key "headerLines" with a value that lists number of lines
#   2- the .csv file to trim   
echo  "$(tail -n +"$(yq read "$1" headerLines)" $2)"
