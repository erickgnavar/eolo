from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib import messages

from main.forms import ConsultForm, ResumeForm
from weather.models import Measurement
from main.util import get_data, prepare_data, random_data
from weather import tasks


class HomeView(FormView):

    template_name = 'main/home.html'
    form_class = ConsultForm

    def form_valid(self, form):
        data = form.cleaned_data
        date = data['date']
        length = data['length']
        variable = data['variable']
        qs = Measurement.objects.filter(variable=variable).exclude(value=None)
        values = get_data(qs, date, length)
        context = {
            'real_data': prepare_data(values),
            'variable': variable,
            'length': len(values)
        }
        context['simulate_data'] = random_data(context['real_data'])
        params = ('main/report.html', context, RequestContext(self.request))
        return render_to_response(*params)


class ReportView(TemplateView):

    template_name = 'main/report.html'


class FullReportView(FormView):

    template_name = 'main/full_report.html'
    form_class = ResumeForm

    def form_valid(self, form):
        data = form.cleaned_data
        date = data['date']
        length = data['length']
        email = data['email']
        kwargs = {
            'email': email,
            'length': length,
            'date': date
        }
        tasks.generate_report.delay(**kwargs)
        messages.success(self.request, 'The report will be generated and will be sent to your email')
        return super(FullReportView, self).form_valid(form)
        # return xls_to_response(xls, 'resume.xls')

    def get_success_url(self):
        return reverse('full_report')
