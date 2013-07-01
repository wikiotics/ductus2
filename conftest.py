# this somehow is needed by py.test to pick up the settings module
# see: http://stackoverflow.com/questions/15199700/django-py-test-does-not-find-settings-module for details

import os
import sys

sys.path.append(os.path.dirname(__file__))
