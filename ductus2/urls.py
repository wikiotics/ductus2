from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from ductus2.podcasts.views import view_all_podcasts, create_new_podcast
from rest_framework import routers
from ductus2.podcasts import views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
router = routers.DefaultRouter()
router.register(r'podcasts', views.PodcastPageViewSet)
router.register(r'revs', views.PodcastRevisionViewSet)


urlpatterns = patterns('',
    # Examples:
    #url(r'^$', TemplateView.as_view(template_name="base_ductus2.html")),
    # url(r'^$', 'ductus2.views.home', name='home'),
    # url(r'^ductus2/', include('ductus2.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
