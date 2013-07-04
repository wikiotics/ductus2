from ductus2.podcasts.models import PodcastPage, PodcastRevision
from rest_framework import serializers

class PodcastRevisionSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = PodcastRevision
        fields = ('id', 'timestamp', 'podcast', 'author_ip', 'title', 'description', 'rows')

class PodcastPageSerializer(serializers.ModelSerializer):

    class Meta:
        model = PodcastPage
        fields = ()
