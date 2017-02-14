#!/bin/bash
# @program: wrapper for ytsync
# @author: abhisek.de@live.com

init()
{
export PLIST='https://www.youtube.com/playlist?list=PLoxmm7yUEsogvB9nc6zX6dWWk5aPQi5YI'
export M_DIR='/home/ubuntu/Music'
export PL_NAME='Music_ADE'
}

sync()
{
# sync YouTube playlist
/home/ubuntu/Music/ytsync.py $PLIST $M_DIR
}

validate()
{
# delete faulty files with 22K HTML content
while [ `ls *.mp3 -hl | grep 22K | cut -d ' ' -f10 | wc -l` != 0 ]
do
	for fname in `ls *.mp3 -hl | grep 22K | cut -d ' ' -f10`
	do 
		rm ${fname}
	done
	sync
done
}

main()
{
init
sync
validate
date
echo "${PL_NAME} sync complete. Check ${M_DIR} for new music files."
}

# main()
main
