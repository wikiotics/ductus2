Requirements:
  * Python >= 3.2.
  * Postgresql (9.x?)

Bootstrap a virtualenv::

    $ pyvenv-3.3 venv-ductus2
    $ source venv-ductus2/bin/activate
    $ wget http://python-distribute.org/distribute_setup.py
    $ python3 distribute_setup.py
    $ venv-ductus2/local/bin/easy_install pip

Install the relevant dependencies::

    $ venv-ductus2/local/bin/pip-3.3 install -r requirements.txt

Create a database in postgresql, name it whatever you want.

Create a local settings file::

    $ touch ductus2_local_settings.py

and update it to point to the database you just created::

   DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '',        # the DB name to use
        'USER': '',        # postgresql username
        'PASSWORD': '',    # postgresql password
        'HOST': '',        # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',        # Set to empty string for default.
     }
   }

Run the development server::

    $ ./manage.py runserver
