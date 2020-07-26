#!/bin/bash

export PYTHONPATH=`pwd`:$PYTHONPATH

scriptdir=`dirname $0`
scriptdir=`realpath $scriptdir`

rootdir=`dirname $0`/..
rootdir=`realpath $rootdir`

if [ -d "$rootdir/docs/_static/src" ]; then
  rm -Rf $rootdir/docs/_static/src
fi
mkdir $rootdir/docs/_static/src

if [ -d "$rootdir/docs/_static/examples" ]; then
  rm -Rf $rootdir/docs/_static/examples
fi
mkdir $rootdir/docs/_static/examples

cp -r $rootdir/docs/src $rootdir/docs/_static
cp -r $rootdir/examples $rootdir/docs/_static

(cd $rootdir/docs; make clean; make html;)

