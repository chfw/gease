isort $(find gease -name "*.py"|xargs echo) $(find tests -name "*.py"|xargs echo)
black -l 79 gease
black -l 79 tests
