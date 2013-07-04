from ductus2.podcasts.models import PodcastPage, PodcastRevision
from rest_framework import serializers

class PodcastRevisionSerializer(serializers.HyperlinkedModelSerializer):
    """Give only a summary of a revision, useful for listings"""

    class Meta:
        model = PodcastRevision
        fields = ('id', 'timestamp', 'podcast', 'author_ip', 'title')

class PodcastLatestRevisionSerializer(serializers.HyperlinkedModelSerializer):
    """Give full details of the latest revision"""

    class Meta:
        model = PodcastRevision
        fields = ('id', 'timestamp', 'podcast', 'author_ip', 'title', 'description', 'rows')

class PodcastPageSerializer(serializers.ModelSerializer):
    """The default serializer, used for saving podcasts"""

    class Meta:
        model = PodcastPage
        fields = ()

class PodcastPageDetailSerializer(serializers.ModelSerializer):
    """Serialize only the latest revision of a podcast, throw in full details."""

    revision = serializers.SerializerMethodField('get_latest_revision')

    class Meta:
        model = PodcastPage
        fields = ()

    def get_latest_revision(self, obj):
        rev = obj.get_latest_revision()
        serializer = PodcastLatestRevisionSerializer(rev)
        return serializer.data

class PodcastPageHistorySerializer(serializers.ModelSerializer):
    """Serialize a podcast with its history of revisions"""

    revisions = PodcastRevisionSerializer(source='revisions', required=False)
    class Meta:
        model = PodcastPage
        fields = ()
