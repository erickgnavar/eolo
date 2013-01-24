from django.conf.urls import patterns, url

from main.views import HomeView, ReportView

urlpatterns = patterns('',

    url(
        regex=r'^$',
        view=HomeView.as_view(),
        name='home'
    ),
    url(
        regex=r'^report/$',
        view=ReportView.as_view(),
        name='report'
    )

)
