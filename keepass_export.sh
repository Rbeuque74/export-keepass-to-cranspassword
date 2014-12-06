#!/bin/sh


cd /tmp/aurorePasswords
for D in `find . -type d`
do
    if [ $D = "." ]; then continue; fi
    arr=$(echo $D | tr "/" "\n")
    for x in $arr
    do
        test=1;
    done
    #echo $x

    for DD in `find ./$x -type f`
    do
        value=`cat $DD`
	#echo "bin/passwords/"
	echo $x
        echo "$value" | ~/bin/aurorepasswords --roles aurore -f -e $x
    done
done
