import pytest
from ductus2.podcasts.models import PodcastPage, PodcastRevision

pytestmark = pytest.mark.django_db

@pytest.mark.django_db
class TestPodcast:

    def create_new_podcast(self, json):
        p = PodcastPage()
        p.save(**json)
        return p

    def test_create_new_podcast_with_title_only(self):
        json_podcast = {
            'page_type': 'podcast',
            'title': 'a test podcast'
        }
        self.create_new_podcast(json_podcast)
        assert PodcastPage.objects.count() == 1
        assert PodcastRevision.objects.count() == 1

    def test_create_podcast_and_modify_description(self):
        json_podcast = {
            'page_type': 'podcast',
            'title': 'a test podcast',
            'description': 'some long text about the content of the podcast'
        }
        p = self.create_new_podcast(json_podcast)
        assert PodcastPage.objects.count() == 1
        assert PodcastRevision.objects.count() == 1
        # now amend the description
        json_podcast['description'] = 'a shorter description'
        p.save(**json_podcast)
        assert PodcastPage.objects.count() == 1
        assert PodcastRevision.objects.count() == 2

    def test_create_podcast_with_one_row_no_audio(self):
        pass

