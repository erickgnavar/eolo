from django.conf.urls import patterns, url

from accounts.views import LoginView, RegisterView, LogoutView

urlpatterns = patterns('',

    url(
        regex=r'^login',
        view=LoginView.as_view(),
        name='login'
    ),
    url(
        regex=r'^logout',
        view=LogoutView.as_view(),
        name='logout'
    ),
    url(
        regex=r'^register',
        view=RegisterView.as_view(),
        name='register'
    ),

)
