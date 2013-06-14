Requires Python >= 3.2.

Bootstrap a virtualenv::

    $ pyvenv-3.3 venv-ductus2
    $ source venv-ductus2/bin/activate
    $ wget http://python-distribute.org/distribute_setup.py
    $ python3 distribute_setup.py
    $ easy_install pip

Install the relevant dependencies::

    $ pip-3.3 install -r requirements.txt

Run the development server::

    $ ./manage.py runserver
