#!/bin/bash
for filename in $( find . -type f -name "*.mp3" )
do
	rm ${filename} 
	touch ${filename}
done
