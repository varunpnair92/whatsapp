#!/bin/bash
IFS=,
while read a b
do
echo "BEGIN:VCARD
VERSION:2.1
N:;$a.keem;;;
FN:$a.keem
TEL;CELL;PREF:$b
END:VCARD"
done<$1
