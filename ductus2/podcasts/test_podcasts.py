import pytest
from ductus2.podcasts.models import PodcastPage, PodcastRevision, PodcastRow, PodcastRowOrder

pytestmark = pytest.mark.django_db

@pytest.mark.django_db
class TestPodcast:

    def create_new_podcast(self, json):
        p = PodcastPage()
        p.save(**json)
        return p

    def test_create_new_podcast_with_title_only(self):
        """create a new podcast, save and retrieve title"""
        title = 'a test podcast'
        json_podcast = {
            'page_type': 'podcast',
            'title': title
        }
        self.create_new_podcast(json_podcast)
        assert PodcastPage.objects.count() == 1
        assert PodcastRevision.objects.count() == 1
        t = PodcastRevision.objects.all()[0].title
        assert t == title

    def test_create_podcast_and_modify_description(self):
        """create a new podcast, then change its description and check we can get it back from db"""
        new_description = 'a shorter description'
        json_podcast = {
            'page_type': 'podcast',
            'title': 'a test podcast',
            'description': 'some long text about the content of the podcast'
        }
        p = self.create_new_podcast(json_podcast)
        assert PodcastPage.objects.count() == 1
        assert PodcastRevision.objects.count() == 1
        # now amend the description
        json_podcast['description'] = new_description
        p.save(**json_podcast)
        assert PodcastPage.objects.count() == 1
        assert PodcastRevision.objects.count() == 2
        desc = p.get_latest_rev().description
        assert desc == new_description

    def test_create_podcast_with_one_text_row(self):
        json_podcast = {
            'page_type': 'podcast',
            'title': 'a test podcast',
            'description': 'some long text about the content of the podcast',
            'rows': [
                {'text': 'the first row'}
            ]
        }
        self.create_new_podcast(json_podcast)
        assert PodcastPage.objects.count() == 1
        assert PodcastRevision.objects.count() == 1
        assert PodcastRowOrder.objects.count() == 1
        assert PodcastRow.objects.count() == 1

    def test_create_podcast_with_multiple_text_rows(self):
        json_podcast = {
            'page_type': 'podcast',
            'title': 'a test podcast',
            'description': 'some long text about the content of the podcast',
            'rows': [
                {'text': 'the first row'},
            ]
        }
        p = self.create_new_podcast(json_podcast)
        json_podcast['rows'] = [
                {'text': 'the first row'},
                {'text': 'the second row'},
                {'text': 'the third row'},
                {'text': 'the fourth row'},
            ]
        p.save(**json_podcast)
        assert PodcastPage.objects.count() == 1
        assert PodcastRevision.objects.count() == 2
        assert PodcastRowOrder.objects.count() == 5
        assert PodcastRow.objects.count() == 5  # FIXME: we should get 4 here, not 5, if we reuse existing rows...

