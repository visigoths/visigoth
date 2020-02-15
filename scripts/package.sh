
rootdir=`dirname $0`/..

(cd $rootdir;python3 setup.py clean)
(cd $rootdir;python3 setup.py sdist)

# now run twine upload dist/*
