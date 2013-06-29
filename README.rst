Requires Python >= 3.2.

Bootstrap a virtualenv::

    $ pyvenv-3.3 venv-ductus2
    $ source venv-ductus2/bin/activate
    $ wget http://python-distribute.org/distribute_setup.py
    $ python3 distribute_setup.py
    $ venv-ductus2/local/bin/easy_install pip

Install the relevant dependencies::

    $ venv-ductus2/local/bin/pip-3.3 install -r requirements.txt

Create a local settings file::

    $ touch ductus2_local_settings.py

Run the development server::

    $ ./manage.py runserver
