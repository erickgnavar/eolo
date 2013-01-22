from django.conf.urls import patterns, url

from admin.views import variable, measurement, region, station, user,\
                HomeView, UploadMeasurementFileView, filter

urlpatterns = patterns('',

    url(r'^$', HomeView.as_view(), name='admin_home'),
    url(
        regex=r'upload_measurement_file/$',
        view=UploadMeasurementFileView.as_view(),
        name='upload_measurement_file'
    ),
    # User
    url(
        regex=r'^user/$',
        view=user.UserListView.as_view(),
        name='admin_user_list'
    ),
    url(
        regex=r'^user/create/$',
        view=user.UserCreateView.as_view(),
        name='admin_user_create'
    ),
    url(
        regex=r'^user/(?P<pk>\d+)/edit/$',
        view=user.UserUpdateView.as_view(),
        name='admin_user_edit'
    ),
    url(
        regex=r'^user/(?P<pk>\d+)/delete/$',
        view=user.UserDeleteView.as_view(),
        name='admin_user_delete'
    ),
    # Variable
    url(
        regex=r'^variable/$',
        view=variable.VariableListView.as_view(),
        name='admin_variable_list'
    ),
    url(
        regex=r'^variable/create/$',
        view=variable.VariableCreateView.as_view(),
        name='admin_variable_create'
    ),
    url(
        regex=r'^variable/(?P<pk>\d+)/edit/$',
        view=variable.VariableUpdateView.as_view(),
        name='admin_variable_edit'
    ),
    url(
        regex=r'^variable/(?P<pk>\d+)/delete/$',
        view=variable.VariableDeleteView.as_view(),
        name='admin_variable_delete'
    ),
    #Measurement
    url(
        regex=r'^measurement/$',
        view=measurement.MeasurementListView.as_view(),
        name='admin_measurement_list'
    ),
    url(
        regex=r'^measurement/create/$',
        view=measurement.MeasurementCreateView.as_view(),
        name='admin_measurement_create'
    ),
    url(
        regex=r'^measurement/(?P<pk>\d+)/edit/$',
        view=measurement.MeasurementUpdateView.as_view(),
        name='admin_measurement_edit'
    ),
    url(
        regex=r'^measurement/(?P<pk>\d+)/delete/$',
        view=measurement.MeasurementDeleteView.as_view(),
        name='admin_measurement_delete'
    ),
    #region
    url(
        regex=r'^region/$',
        view=region.RegionListView.as_view(),
        name='admin_region_list'
    ),
    url(
        regex=r'^region/create/$',
        view=region.RegionCreateView.as_view(),
        name='admin_region_create'
    ),
    url(
        regex=r'^region/(?P<pk>\d+)/edit/$',
        view=region.RegionUpdateView.as_view(),
        name='admin_region_edit'
    ),
    url(
        regex=r'^region/(?P<pk>\d+)/delete/$',
        view=region.RegionDeleteView.as_view(),
        name='admin_region_delete'
    ),
    #Estacion
    url(
        regex=r'^station/$',
        view=station.StationListView.as_view(),
        name='admin_station_list'
    ),
    url(
        regex=r'^station/create/$',
        view=station.StationCreateView.as_view(),
        name='admin_station_create'
    ),
    url(
        regex=r'^station/(?P<pk>\d+)/edit/$',
        view=station.StationUpdateView.as_view(),
        name='admin_station_edit'
    ),
    url(
        regex=r'^station/(?P<pk>\d+)/delete/$',
        view=station.StationDeleteView.as_view(),
        name='admin_station_delete'
    ),
    #Estacion
    url(
        regex=r'^filter/$',
        view=filter.FilterListView.as_view(),
        name='admin_filter_list'
    ),
    url(
        regex=r'^filter/create/$',
        view=filter.FilterCreateView.as_view(),
        name='admin_filter_create'
    ),
    url(
        regex=r'^filter/(?P<pk>\d+)/edit/$',
        view=filter.FilterUpdateView.as_view(),
        name='admin_filter_edit'
    ),
    url(
        regex=r'^filter/(?P<pk>\d+)/delete/$',
        view=filter.FilterDeleteView.as_view(),
        name='admin_filter_delete'
    ),

)
