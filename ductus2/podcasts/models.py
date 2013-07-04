import random
import string
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

podcast_page_name_length = 16
podcast_revision_name_length = podcast_page_name_length

class PodcastPage(models.Model):
    """
    The PodcastPage doesn't hold any info about the content beyond the url, everything else is in the PodcastRevision object.

    A podcast is exposed as a JSON object structured like:
     {
      page_type: 'podcast',
      url: '<url>',   // 16 chars, empty if podcast not yet saved
      timestamp: '<revision_timestamp>',   // not set if podcast not yet saved (see line above)
      title: '<512 chars max>',    // mandatory
      description: '<text>',       // can be empty string
      rows: ''                  // a string of text for now
     }

    The rows attribute should be valid JSON (for future use) formatted like:
    [
        {"text": "the text in the row", "audio": "some ID for the audio file"},
        ...
    ]
    """

    def __str__(self):
        return self.get_latest_revision().title

    def get_latest_revision(self):
        query = PodcastRevision.objects.filter(podcast=self).order_by('-timestamp')
        try:
            return query[0]
        except IndexError:
            return None

    def save(self, *args, **kwargs):
        """When saving a podcast page, create a new revision and make the page point to it"""
        podcast_id = super(PodcastPage, self).save()    # give new pages an id for create below to work
        rev = PodcastRevision(podcast=self, timestamp=timezone.now())
        for key in kwargs:
            setattr(rev, key, kwargs[key])
        rev.save()
        return podcast_id


class PodcastRevision(models.Model):
    """Each revision is saved here. Each modification of the content leads to a new revision."""

    podcast = models.ForeignKey(PodcastPage)
    author = models.ForeignKey(User, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    author_ip = models.GenericIPAddressField(blank=True, null=True)

    title = models.CharField(max_length=512)
    description = models.TextField()
    rows = models.TextField()   # for now, store the content as a raw JSON string

    def __str__(self):
        return self.title
