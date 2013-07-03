from ductus2.podcasts.models import PodcastPage, PodcastRevision
from rest_framework import viewsets
from ductus2.podcasts.serializers import PodcastPageSerializer, PodcastRevisionSerializer

class PodcastPageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows podcasts to be viewed or edited.
    """
    queryset = PodcastPage.objects.all()
    serializer_class = PodcastPageSerializer

class PodcastRevisionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows revisions to be viewed or edited.
    """
    queryset = PodcastRevision.objects.all()
    serializer_class = PodcastRevisionSerializer

