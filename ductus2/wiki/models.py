# This file is part of Ductus2
# Copyright (C) 2013 Laurent Savaëte <laurent@wikiotics.org>
#                    Jim Garrison <garrison@wikiotics.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from django.contrib.auth.models import User
from django.db import models

class WikiPage(models.Model):
    """This model creates a db table, and all descendants are proxies which do not have their own table, since all content is in the revision.
    See https://docs.djangoproject.com/en/1.5/topics/db/models/#abstract-base-classes for details."""

    name = models.CharField(max_length=16)   # an md5hash-like identifier

    def get_latest_rev(self, rev_class):
        query = rev_class.objects.filter(page=self).order_by('-timestamp')
        try:
            return query[0]
        except IndexError:
            return None

class WikiPageRevision(models.Model):
    """This model is an abstract one, it does not generate a db table, only its descendants do"""

    page = models.ForeignKey(WikiPage)
    urn = models.CharField(max_length=16)
    author = models.ForeignKey(User)
    timestamp = models.DateTimeField(auto_now_add=True)
    author_ip = models.GenericIPAddressField(blank=True, null=True)

    class Meta:
        abstract = True
