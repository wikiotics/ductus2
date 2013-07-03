from ductus2.podcasts.models import PodcastPage, PodcastRevision, PodcastRow, PodcastRowOrder
from rest_framework import serializers

class PodcastPageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PodcastPage
        fields = ()

class PodcastRowOrderSerializer(serializers.HyperlinkedModelSerializer):

    id = serializers.Field(source='row.id')
    text = serializers.Field(source='row.text')

    class Meta:
        model = PodcastRowOrder
        fields = ('id', 'text', 'order', )

class PodcastRevisionSerializer(serializers.HyperlinkedModelSerializer):
    rows = PodcastRowOrderSerializer(source='podcastroworder_set', many=True)
    class Meta:
        model = PodcastRevision
        fields = ('id', 'timestamp', 'podcast', 'author_ip', 'title', 'description', 'rows')

class PodcastRowSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PodcastRow
        fields = ('text')

