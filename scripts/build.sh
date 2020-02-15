#!/bin/bash

export PYTHONPATH=`pwd`:$PYTHONPATH

scriptdir=`dirname $0`
scriptdir=`realpath $scriptdir`

rootdir=`dirname $0`/..
rootdir=`realpath $rootdir`

(cd $rootdir/docs/src; $scriptdir/example.sh; )

for folder in common containers map_layers charts
do
	subfolders=$rootdir/docs/src/$folder/*
	for subfolder in $subfolders
	do
		if [ -f "$subfolder/example.py" ]; then
                        echo building $subfolder
                        (cd $subfolder; $scriptdir/example.sh; )
		fi
        done
done

for examplefolder in $rootdir/examples/*
do
	if [ -f "$examplefolder/example.py" ]; then
		echo building $examplefolder
		(cd $examplefolder; $scriptdir/example.sh; )
	fi
done

(cd $rootdir/docs; make clean; make html; cp -r $rootdir/docs/src $rootdir/docs/_build/html/src; cp -r $rootdir/examples $rootdir/docs/_build/html/src)

