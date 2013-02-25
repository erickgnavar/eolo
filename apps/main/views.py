import math
from datetime import timedelta
from decimal import Decimal

from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse

from main.forms import ConsultForm, ResumeForm
from weather.models import Measurement
from weather.models import Variable


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
        to_excel = []
        for variable in Variable.objects.all():
            qs = Measurement.objects.exclude(value=None).filter(variable=variable)
            values = get_data(qs, date, length)
            data = prepare_data(values)
            to_excel.append({
                'variable': variable,
                'real': data,
                'simulate': random_data(data)
            })
        xls = create_excel(to_excel)
        return xls_to_response(xls, 'resume.xls')


def get_data(qs, date, length):
    values = []
    # values before date selected
    for delta in range(-length, 0):
        delta_date = date + timedelta(days=delta)
        filters = {
            'date__day': delta_date.day,
            'date__month': delta_date.month,
            'date__lte': date
        }
        values += [measurement.value for measurement in qs.filter(**filters)]
        # values for date selecte before one year
    filters = {
        'date__day': date.day,
        'date__month': date.month,
        'date__lt': date + timedelta(days=-365)
    }
    values += [measurement.value for measurement in qs.filter(**filters)]
    # values above date selected
    for delta in range(1, length + 1):
        delta_date = date + timedelta(days=delta)
        filters = {
            'date__day': delta_date.day,
            'date__month': delta_date.month,
            'date__lte': date
        }
        values += [measurement.value for measurement in qs.filter(**filters)]
    values.sort()
    return values


def prepare_data(values):
    import math
    length = len(values)
    quantity = int(round(1 + (3.3 * math.log(length))))
    amplitude = (max(values) - min(values)) / Decimal(quantity)
    limit_decimal = 7
    data = {
        'length': length,
        'intervals': [],
        'amplitude': round(amplitude, limit_decimal),
        'max': max(values),
        'min': min(values)
    }
    m = min(values)
    for i in range(quantity):
        interval = {
            'index': 0,
            'min': round(m, limit_decimal),
            'max': round(m + amplitude, limit_decimal),
            'values': []
        }
        data['intervals'].append(interval)
        m += amplitude
    # insert first data
    min_value = min(values)
    for i in range(values.count(min_value)):
        data['intervals'][0]['values'].append(min_value)
    # insert rest data
    for value in values:
        for interval in data['intervals']:
            if value > interval['min'] and value <= interval['max']:
                interval['values'].append(value)
    count = 0
    for interval in data['intervals']:
        count += 1
        interval['index'] = count
        interval['class_marker'] = (interval['max'] + interval['min']) / 2
        interval['fi'] = len(interval['values'])
        interval['hi'] = round(float(interval['fi']) / float(data['length']), limit_decimal)
        interval['Fi'] = 0
        interval['Hi'] = 0

    data['intervals'][0]['Fi'] = data['intervals'][0]['fi']
    data['intervals'][0]['Hi'] = round(data['intervals'][0]['hi'], limit_decimal)
    for i in range(1, quantity):
        data['intervals'][i]['Fi'] += data['intervals'][i - 1]['Fi'] + data['intervals'][i]['fi']
        data['intervals'][i]['Hi'] += round(data['intervals'][i - 1]['Hi'] + data['intervals'][i]['hi'], limit_decimal)

    data = calculate_stadistics(data, limit_decimal)
    return data


def calculate_stadistics(data, limit_decimal=5):
    a = 0
    modal_class_index = 0
    b = 0
    for interval in data['intervals']:
        a += interval['fi'] * interval['class_marker']
        if interval['fi'] > b:
            b = interval['fi']
            modal_class_index = interval['index'] - 1
    # Median
    median = data['intervals'][modal_class_index]['min']
    if modal_class_index == 0:
        before_value = data['intervals'][0]['Fi']
    else:
        before_value = data['intervals'][modal_class_index - 1]['Fi']

    median += (((data['length'] / 2) - before_value) / data['intervals'][modal_class_index]['fi']) * float(data['amplitude'])
    # Median end
    data['median'] = round(median, limit_decimal)

    # Average
    data['average'] = round(a / data['length'], limit_decimal)

    # Mode
    if modal_class_index - 1 <= 0:
        x = data['intervals'][modal_class_index]['fi'] - float(data['intervals'][modal_class_index]['min'])
    else:
        x = data['intervals'][modal_class_index]['fi'] - float(data['intervals'][modal_class_index - 1]['fi'])
    if modal_class_index + 1 >= data['length']:
        y = data['intervals'][modal_class_index]['fi'] - float(data['intervals'][modal_class_index]['max'])
    else:
        y = data['intervals'][modal_class_index]['fi'] - float(data['intervals'][modal_class_index + 1]['fi'])
    mode = data['intervals'][modal_class_index]['min'] + ((x / (x + y)) * float(data['amplitude']))

    data['mode'] = round(mode, limit_decimal)
    # Mode end
    #Quartile
    data['q1'] = quartile(data, 1, 4)
    data['q2'] = quartile(data, 2, 4)
    data['q3'] = quartile(data, 3, 4)
    for i in range(1, 10):
        data['d' + str(i)] = quartile(data, i, 10)
    for i in range(1, 100):
        data['p' + str(i)] = quartile(data, i, 100)
    # End Quartile

    # Variance
    variance = 0
    for interval in data['intervals']:
        # variance += (interval['class_marker'] ** 2) * interval['fi']
        variance += ((interval['class_marker'] - data['average']) ** 2) * interval['fi']
    variance /= data['length']
    # variance -= data['average'] ** 2
    data['variance'] = variance
    # End Variance
    data['standard_deviation'] = math.sqrt(data['variance'])
    data['asymmetry_coefficient'] = 3 * (data['average'] - data['median']) / data['standard_deviation']
    data['inter_quartile_deviation'] = (data['q3'] - data['q1']) / 2
    return data


def quartile(data, pos, type):
    q1 = (data['intervals'][len(data['intervals']) - 1]['Fi'] * pos) / type
    i = 0
    while q1 > data['intervals'][i]['Fi']:
        i += 1
    if i == 0:
        qa = 0
    else:
        qa = data['intervals'][i - 1]['Fi']
    q_value = data['intervals'][i]['min'] + (((q1 - qa) / data['intervals'][i]['fi']) * data['amplitude'])
    return q_value


def random_data(real_data):
    from random import random
    values = []
    limit_decimal = 5
    data = {
        'amplitude': real_data['amplitude'],
        'intervals': []
    }

    for i in range(100000):
        rand = random()
        tmp = 0
        for j in range(len(real_data['intervals'])):
            if rand < real_data['intervals'][j]['Hi']:
                tmp = real_data['intervals'][j]['class_marker']
                break
        values.append(tmp)

    data['length'] = len(values)
    data['max'] = max(values)
    data['min'] = min(values)

    for i in range(len(real_data['intervals'])):
        interval = {
            'index': 0,
            'min': real_data['intervals'][i]['min'],
            'max': real_data['intervals'][i]['max'],
            'values': []
        }
        data['intervals'].append(interval)

    min_value = min(values)
    for i in range(values.count(min_value)):
        data['intervals'][0]['values'].append(min_value)
    # insert rest data
    for value in values:
        for interval in data['intervals']:
            if value > interval['min'] and value <= interval['max']:
                interval['values'].append(value)

    count = 0
    for interval in data['intervals']:
        count += 1
        interval['index'] = count
        interval['class_marker'] = (interval['max'] + interval['min']) / 2
        interval['fi'] = len(interval['values'])
        interval['hi'] = round(float(interval['fi']) / float(data['length']), limit_decimal)
        interval['Fi'] = 0
        interval['Hi'] = 0

    data['intervals'][0]['Fi'] = data['intervals'][0]['fi']
    data['intervals'][0]['Hi'] = round(data['intervals'][0]['hi'], limit_decimal)
    for i in range(1, len(data['intervals'])):
        data['intervals'][i]['Fi'] += data['intervals'][i - 1]['Fi'] + data['intervals'][i]['fi']
        data['intervals'][i]['Hi'] += round(data['intervals'][i - 1]['Hi'] + data['intervals'][i]['hi'], limit_decimal)
    data = calculate_stadistics(data, limit_decimal)
    return data


def create_excel(data):
    from xlwt import Workbook
    workbook = Workbook()
    sheet = workbook.add_sheet('test', cell_overwrite_ok=True)
    i = 0
    for item in data:
        sheet.write_merge(0, 0, i + 1, i + 2, item['variable'].name)
        sheet.write(1, i + 1, 'Real')
        sheet.write(1, i + 2, 'Simulate')
        i += 2

    stadistics = [
        ('Average', 'average'),
        ('Mode', 'mode'),
        ('Min', 'min'),
        ('Max', 'max'),
        ('Median', 'median'),
        ('Q1', 'q1'),
        ('Q2', 'q2'),
        ('Q3', 'q3'),
        ('Variance', 'variance'),
        ('Standard Deviation', 'standard_deviation'),
        ('Asymmetry Coefficient', 'asymmetry_coefficient'),
        ('Inter Quartile Deviation', 'inter_quartile_deviation')
    ]
    for i in range(1, 10):
        stadistics.append(('D' + str(i), 'd' + str(i)))
    for i in range(1, 100):
        stadistics.append(('P' + str(i), 'p' + str(i)))
    i = 2
    for statistic in stadistics:
        sheet.write(i, 0, statistic[0])
        i += 1

    c = 1
    for item in data:
        j = 2
        for stadistic in stadistics:
            sheet.write(j, c, item['real'][stadistic[1]])
            sheet.write(j, c + 1, item['simulate'][stadistic[1]])
            j += 1
        c += 2
    return workbook


def xls_to_response(xls, fname):
    response = HttpResponse(mimetype="application/ms-excel")
    response['Content-Disposition'] = 'attachment; filename=%s' % fname
    xls.save(response)
    return response
