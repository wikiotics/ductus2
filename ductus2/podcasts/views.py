from django.http import Http404
from django.shortcuts import get_object_or_404
from ductus2.podcasts.models import PodcastPage, PodcastRevision
from rest_framework import viewsets, response
from ductus2.podcasts.serializers import PodcastPageSerializer, PodcastRevisionSerializer, PodcastPageDetailSerializer, PodcastPageHistorySerializer

class PodcastPageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows podcasts to be viewed or edited.
    """
    queryset = PodcastPage.objects.all()
    serializer_class = PodcastPageSerializer

    def retrieve(self, request, pk=None):
        """ GET /api/podcasts/<id>/ returns all fields in the podcast, for the latest revision.
            GET /api/podcasts/<id>/?history returns only limited info, but for all revisions of a podcast.
            """
        try:
            podcast = PodcastPage.objects.get(pk=pk)
        except PodcastPage.DoesNotExist:
            raise Http404

        if 'history' in request.QUERY_PARAMS:
            s = PodcastPageHistorySerializer
        else:
            s = PodcastPageDetailSerializer

        serializer = s(podcast, context={'request': request})
        return response.Response(serializer.data)

class PodcastRevisionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows revisions to be viewed or edited.
    This should normally not be used much.
    """
    queryset = PodcastRevision.objects.all()
    serializer_class = PodcastRevisionSerializer

