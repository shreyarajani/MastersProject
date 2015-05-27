from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       (r'^criteria/$', 'ThruLine.views.criteria'),
                       (r'^results/$', 'ThruLine.views.results'),
                       (r'^results/results_user/$', 'ThruLine.views.results_user'),
                       (r'^intermediate_function', 'ThruLine.views.intermediate_function'),
                       (r'^requests/$', 'ThruLine.views.requests'),
                       (r'^request/(?P<id>[0-9]+)/$', 'ThruLine.views.request'),
                       (r'^video/(?P<request_id>[0-9]+)/$', 'ThruLine.views.serve_video'),
                       (r'^download/(?P<request_id>[0-9]+)/$', 'ThruLine.views.download_video'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
