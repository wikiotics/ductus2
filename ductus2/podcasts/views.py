import hashlib
import json
from django.http import HttpResponse
from django.utils import timezone
from ductus2.podcasts.models import PodcastPage, PodcastRevision
#from ductus2.wiki.models import WikiPage, WikiPageRevision
from rest_framework import viewsets
from ductus2.podcasts.serializers import PodcastPageSerializer, PodcastRevisionSerializer

class PodcastPageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = PodcastPage.objects.all()
    serializer_class = PodcastPageSerializer

class PodcastRevisionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = PodcastRevision.objects.all()
    serializer_class = PodcastRevisionSerializer


class PodcastRevisionJSONEncoder(json.JSONEncoder):
    def encode_row(self, row):
        return "{text: '" + row.text + "' }"

    def default(self, p):
        """encode a podcast revision object to a JSON string, order not guaranteed"""
        #output = '{' +
        #"'page_type':'podcast'," +
        #"url: '" + p.podcast.url + "'" +
        #"rev_urn: '" + p.urn "'" +
        j = ["page_type:'podcast'"]
        for key in p.__dict__:
            if key != 'rows':
                j.append(str(key) + ":'" + str(getattr(p, key)) + "'")
        j.append('[')
        for row in p.rows.all():
            j.append(self.encode_row(row))
        j.append(']')
        return '{' + ','.join(j) + '}'



def build_JSON_object_for_revision(rev):
    """build a JSON object from the python object"""
    #import json
    #text = json.dumps(rev.__dict__)
    #from django.core import serializers
    #text = serializers.serialize("json", [rev])
    text = PodcastRevisionJSONEncoder().encode(rev)
    return text

def build_JSON_object_for_urn(urn):
    rev = PodcastRevision.objects.get(urn=urn)
    return build_JSON_object_for_revision(rev)

def build_JSON_object_for_url(url):
    p = PodcastPage.objects.get(url=url)
    return build_JSON_object_for_revision(p.get_latest_rev())

def view_all_podcasts(request):
    p = PodcastPage.objects.all()
    l = [repr(it) for it in p]

    return HttpResponse(str(l), content_type='text/plain; charset=utf-8')

def create_new_podcast(request):
    from django.utils.encoding import force_str
    now = str(timezone.now()).encode('ascii')
    url = now[0:15] #hashlib.md5(now).digest()
    #url = hashlib.md5(now).digest()
    p = PodcastPage(url=url)
    pid = p.save()

    return HttpResponse(str(pid), content_type='text/plain; charset=utf-8')


