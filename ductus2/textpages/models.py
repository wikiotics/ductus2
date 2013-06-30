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

from django.db import models
from django.utils import timezone
from ductus2.wiki.models import WikiPage, WikiPageRevision

class TextPage(WikiPage):
    """A proxy class, which won't create a db table, only the parent class does"""

    class Meta:
        proxy = True

    def __unicode__(self):
        return u'this is a text page'

    def get_latest_rev(self):
        return super(TextPage, self).get_latest_rev(TextPageRevision)

    def save(self, *args, **kwargs):
        """When saving a textpage, create a new revision and make the page point to it"""
        super(TextPage, self).save()    # give new pages an id for create below to work
        now = timezone.now()
        from django.contrib.auth.models import User # FIXME: set the author to the superuser until we have a UI
        self.textpagerevision_set.create(title="text page created at" + str(now), timestamp=now, author=User.objects.get(pk=1))

class TextPageRevision(WikiPageRevision):

    title = models.CharField(max_length=512)
    text = models.TextField()

    def __unicode__(self):
        return self.title
