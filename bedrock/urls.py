# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.conf import settings
from django.conf.urls import handler404, include, url

from django.utils.module_loading import import_string

from bedrock.base import views as base_views
from watchman import views as watchman_views

# The default django 500 handler doesn't run the ContextProcessors, which breaks
# the base template page. So we replace it with one that does!
handler500 = 'bedrock.base.views.server_error_view'


urlpatterns = (
    # Main pages
    url(r'^foundation/', include('bedrock.foundation.urls')),
    url(r'^grants/', include('bedrock.grants.urls')),
    url(r'^about/legal/', include('bedrock.legal.urls')),
    url(r'^press/', include('bedrock.press.urls')),
    url(r'^privacy/', include('bedrock.privacy.urls')),
    url(r'^styleguide/', include('bedrock.styleguide.urls')),
    url(r'^security/', include('bedrock.security.urls')),
    url(r'^shapeoftheweb/', include('bedrock.shapeoftheweb.urls')),
    url(r'', include('bedrock.firefox.urls')),
    url(r'', include('bedrock.mozorg.urls')),
    url(r'', include('bedrock.newsletter.urls')),
    url(r'^etc/', include('bedrock.etc.urls')),

    url(r'^healthz/$', watchman_views.ping, name="watchman.ping"),
    url(r'^readiness/$', watchman_views.status, name="watchman.status"),
    url(r'^healthz-cron/$', base_views.cron_health_check),
    url(r'^csp-violation-capture$', base_views.csp_violation_capture,
        name='csp-violation-capture'),
    url(r'^country-code\.json$', base_views.geolocate,
        name='geolocate')
)

if settings.DEBUG:

    def show404(request):
        return import_string(handler404)(request, '')

    urlpatterns += (
        url(r'^404/$', show404),
        url(r'^500/$', import_string(handler500)),
    )
