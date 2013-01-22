from django.conf.urls import patterns, url, include

from accounts.views import LoginView, RegisterView, LogoutView

urlpatterns = patterns('',

    url(r'^login', LoginView.as_view(), name='login'),
    url(r'^logout', LogoutView.as_view(), name='logout'),
    url(r'^register', RegisterView.as_view(), name='register'),
    url(r'admin/', include('admin.urls')),

)
