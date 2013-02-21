from django.conf.urls import patterns, url

from main.views import HomeView, ReportView, FullReportView

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
    ),
    url(
        regex=r'^full_report/$',
        view=FullReportView.as_view(),
        name='full_report'
    )

)
