from django.contrib import messages
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from admin.forms import MeasurementFileForm
from common.views import LoginRequiredMixin
from weather.models import Station, Region


class HomeView(LoginRequiredMixin, TemplateView):

    template_name = 'admin/home.html'


class UploadMeasurementFileView(LoginRequiredMixin, FormView):

    template_name = 'admin/upload_measurement_file.html'
    form_class = MeasurementFileForm

    def form_valid(self, form):
        from weather.tasks import insert_measurement
        m_file = self.request.FILES['measurement_file']
        name = m_file.name
        region_code = name[:2]
        station_code = name[2:8]
        station = Station.objects.filter(code=station_code)
        region = Region.objects.filter(code=region_code)
        if station.count() > 0 and region.count() > 0:
            station = station.get()
            region = region.get()
            if station.region == region:
                content = m_file.read()
                insert_measurement.delay(content, station)
                messages.info(self.request, 'Data is inserting!')
            else:
                messages.warning(self.request, 'Dont match station with region in file name!')
        else:
            messages.error(self.request, 'station or region doesnt exists')
        return super(UploadMeasurementFileView, self).form_valid(form)

    def get_success_url(self):
        return reverse('admin_measurement_list')
