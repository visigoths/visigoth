#!/bin/bash

export PYTHONPATH=`pwd`:$PYTHONPATH

rootdir=`dirname $0`/..

rm -rf dist
rm -rf build
rm -rf visigoth.egg-info

rm -f $rootdir/docs/src/example.svg
rm -f $rootdir/docs/src/example.html
rm -f $rootdir/docs/src/example.png
rm -f $rootdir/docs/src/thumbnail.png

for folder in common containers map_layers charts
do
	subfolders=$rootdir/docs/src/$folder/*
	for subfolder in $subfolders
	do
		if [ -f "$subfolder/example.html" ]; then
                        echo cleaning $subfolder
			rm -f "$subfolder/example.svg"
			rm -f "$subfolder/example.html"
			rm -f "$subfolder/example.png"
			rm -f "$subfolder/thumbnail.png"
		fi
        done
done

for examplefolder in $rootdir/examples/*
do
	if [ -f "$examplefolder/example.html" ]; then
                echo cleaning $examplefolder
		rm -f "$examplefolder/example.svg"
		rm -f "$examplefolder/example.html"
		rm -f "$examplefolder/example.png"
		rm -f "$examplefolder/thumbnail.png"
	fi
done

(cd $rootdir; find . -type f -name "test_*.svg" -delete)
(cd $rootdir; find . -type f -name "test_*.html" -delete)

if [ -d "$rootdir/docs/_static/src" ]; then
  rm -Rf $rootdir/docs/_static/src
fi

if [ -d "$rootdir/docs/_static/examples" ]; then
  rm -Rf $rootdir/docs/_static/examples
fi

(cd $rootdir/docs; make clean;)

