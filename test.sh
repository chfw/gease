pip freeze
nosetests --with-coverage --cover-package gease --cover-package tests tests --with-doctest --doctest-extension=.rst README.rst  gease
