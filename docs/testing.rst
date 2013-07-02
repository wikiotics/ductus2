Testing ductus2
===============

Python unit tests use pytest-django.

Under ``ductus2`` folder run::

   $ ../venv-ductus2/local/bin/py.test

You can also run the command one level up, but this will pick up all dependencies tests (i.e. django...) and take a while.

Make sure your tests files are named like ``test_*.py`` or they won't be picked up by py.test (read: the default django tests.py doesn't work).
