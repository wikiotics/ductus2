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
        """create a new podcast, save and retrieve title"""
        title = 'a test podcast'
        json_podcast = {
            'title': title
        }
        self.create_new_podcast(json_podcast)
        assert PodcastPage.objects.count() == 1
        assert PodcastRevision.objects.count() == 1
        t = PodcastRevision.objects.all()[0].title
        assert t == title

    def test_create_podcast_and_modify_description(self):
        """create a new podcast, then change its description, check we can get it back from db, and that we've got 2 revisions"""
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
        desc = p.get_latest_revision().description
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

    def test_api_get_podcast_list(self, admin_client):
        response = admin_client.get('/api/podcasts/')
        print(response.__dict__)
        assert response.status_code == 200
        assert response.data['count'] == 0

    def test_get_single_podcast(self, admin_client):
        """ GET on /api/podcasts/<id>/ should return the content of the latest revision """
        #TODO: fill this in
        pass

    def test_api_save_podcast_and_modify(self, admin_client):
        """create a podcast through the API, update it, and check the DB is correctly updated.
        Create a podcast: POST on /api/podcasts/      \
        Update a podcast: PUT on /api/podcasts/<id>/  /   both create a new revision
        """
        json_podcast = {
            'title': 'a test podcast',
            'description': 'some long text about the content of the podcast',
            'rows': [
                {'text': 'the first row'},
            ]
        }
        response = admin_client.post('/api/podcasts/', json_podcast)
        assert response.status_code == 201
        podcast_id = response.data["id"]
        assert PodcastPage.objects.count() == 1
        assert PodcastRevision.objects.count() == 1
        # now update the podcast
        json_podcast_update = {"title": "a new test podcast",
            "description": "some long text about the content of the podcast",
            "rows": [
                {"text": "the first row"},
                {"text": "more stuff"}
            ]
        }
        json_podcast_update = '{ "title": "a new test podcast", "description": "some long text about the content of the podcast", "rows": [ {"text": "the first row"}, {"text": "more stuff"} ] }'
        # django's client uses different content_types for POST and PUT, go figure... so we force json here
        response = admin_client.put('/api/podcasts/' + str(podcast_id) + '/?format=json',json_podcast_update, content_type='application/json')
        assert response.status_code == 200
        assert PodcastPage.objects.count() == 1
        assert PodcastRevision.objects.count() == 2
