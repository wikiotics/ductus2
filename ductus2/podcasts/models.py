import random
import string
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
      rev_urn: '<urn>',        // 16 chars, empty if podcast not yet saved, will be ignored when saving, we always create a new rev if there are changes
      timestamp: '<revision_timestamp>',   // not set if podcast not yet saved (see line above)
      title: '<512 chars max>',    // mandatory
      description: '<text>',       // can be empty string
      rows: [
        { ... },    // TODO: to be defined
      ]
     }
    """


    #url = models.CharField(max_length=podcast_page_name_length)

    def __str__(self):
        return 'podcast stuff'

    def get_latest_rev(self):
        query = PodcastRevision.objects.filter(podcast=self).order_by('-timestamp')
        try:
            return query[0]
        except IndexError:
            return None

    def save(self, *args, **kwargs):
        """When saving a podcatpage, create a new revision and make the page point to it"""
        podcast_id = super(PodcastPage, self).save()    # give new pages an id for create below to work
        now = timezone.now()

        #try:    # FIXME: put this in validator
        #    title = kwargs['title']
        #except KeyError:
        #    raise Exception('Title required for Podcast lessons')

        #try:
        #    self.url = kwargs['url']
            #TODO: check for changes before saving a rev
        #except KeyError:
            # set a random url if none exists
        #    self.url = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(podcast_page_name_length))

        #del kwargs['page_type']
        rev = PodcastRevision(podcast=self, timestamp=now)
        rev.save(**kwargs)
        return podcast_id


class PodcastRow(models.Model):
    """A row in a podcast, containing text, audio. Order info is held in an intermediate structure."""
    text = models.CharField(max_length=512)
    # TODO: add language

class PodcastRevision(models.Model):

    #urn = models.CharField(max_length=podcast_revision_name_length)
    podcast = models.ForeignKey(PodcastPage)
    #author = models.ForeignKey(User)
    timestamp = models.DateTimeField(auto_now_add=True)
    author_ip = models.GenericIPAddressField(blank=True, null=True)

    title = models.CharField(max_length=512)
    description = models.TextField()
    rows = models.ManyToManyField(PodcastRow, through='PodcastRowOrder')

    def save(self, *args, **kwargs):
        for key in kwargs:
            if key != 'rows':
                setattr(self, key, kwargs[key])
        rev = super(PodcastRevision, self).save()
        try:
            for rank, row in enumerate(kwargs['rows']):
                row_obj = PodcastRow(text=row['text'])
                row_obj.save()
                self.podcastroworder_set.create(revision=self, order=rank, row=row_obj)
        except KeyError:
            pass

class PodcastRowOrder(models.Model):
    """The intermediate class used to tell a revision in which order are its rows."""

    revision = models.ForeignKey(PodcastRevision)
    row = models.ForeignKey(PodcastRow)
    order = models.IntegerField()
