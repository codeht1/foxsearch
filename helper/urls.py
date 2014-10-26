from django.conf.urls import patterns, include, url
#from django.conf.urls.static import static
#from django.conf.urls import handler404,handler400,handler500,handler403

from django.contrib import admin
admin.autodiscover()

# handler404 = 'searchreqs.views.error404'
# handler400 = 'searchreqs.views.error400'
# handler500 = 'searchreqs.views.error500'
# handler403 = 'searchreqs.views.error403'
urlpatterns = patterns('',
    # Examples:
    url(r'^result/', 'searchreqs.views.result', name='result'),
    url(r'^home/', 'searchreqs.views.home', name='home'),
    url(r'^about/', 'searchreqs.views.about', name='about'),
    url(r'^contact/', 'searchreqs.views.contact', name='contact'),
    url(r'^$', 'searchreqs.views.home', name='home'),
    #url(r'^.*$','searchreqs.views.home', name='home')
    # url(r'^blog/', include('blog.urls')),

    url(r'^djangoadmindev1/', include(admin.site.urls)),
)
