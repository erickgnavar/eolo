from django.conf.urls import patterns, url, include

urlpatterns = patterns('',

    url(r'^', include('main.urls')),
    url(r'^', include('accounts.urls')),
    url(r'admin/', include('admin.urls'))

)
