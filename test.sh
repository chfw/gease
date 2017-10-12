pip freeze
nosetests --with-coverage --cover-package gease --cover-package tests --with-doctest --doctest-extension=.rst README.rst tests docs/source gease && flake8 . --exclude=.moban.d --builtins=unicode,xrange,long
