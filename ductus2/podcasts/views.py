from django.http import Http404
from django.shortcuts import get_object_or_404, render_to_response
from ductus2.podcasts.models import PodcastPage, PodcastRevision
from rest_framework import viewsets, response
from ductus2.podcasts.serializers import PodcastPageSerializer, PodcastRevisionSerializer, PodcastPageDetailSerializer, PodcastPageHistorySerializer, PodcastListSerializer

def start(request):
    """the base page under /wiki/, loads the javascript machinery which then interacts with the api."""

    return render_to_response('podcasts/base.html', {})

#
# API views
#

class PodcastPageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows podcasts to be viewed or edited.
    """
    queryset = PodcastPage.objects.all()
    serializer_class = PodcastPageSerializer

    def list(self, request):
        """ GET /api/podcast/ lists limited info for the latest revision of all podcasts.
        """
        queryset = PodcastPage.objects.all()
        serializer = PodcastListSerializer(queryset)
        return response.Response(serializer.data)

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

