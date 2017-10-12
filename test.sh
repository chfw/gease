pip freeze
nosetests --with-coverage --cover-package gease --cover-package tests  tests docs/source gease && flake8 . --exclude=.moban.d --builtins=unicode,xrange,long
