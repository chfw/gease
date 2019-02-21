pip freeze
nosetests --with-coverage --cover-package gease --cover-package tests tests --with-doctest --doctest-extension=.rst README.rst  gease && flake8 . --exclude=.moban.d,docs --builtins=unicode,xrange,long
