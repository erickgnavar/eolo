from datetime import datetime
from decimal import Decimal
import time

from weather.models import Variable, Measurement, Filter
from celery.task import task
from common.mail import Email
from main.util import prepare_data, get_data, random_data, create_excel


@task(name='insert_data')
def insert_measurement(content, station):
    print 'Inserting data...'
    content = content.replace('\r', '')
    variables = Variable.objects.all()
    filters = [filter.value for filter in Filter.objects.all()]
    lines = content.split('\n')
    variable_names = [var_name.replace('_', '').upper()\
        for var_name in lines[0].split(',')[3:]]
    lines = lines[1:]
    errors = 0
    measurements = []
    for line in lines:
        if len(line) > 0:
            values = line.split(',')
            date_txt = '%s/%s/%s' % (values[0], values[1], values[2])
            str_time = time.strptime(date_txt, '%Y/%m/%d')
            date_django = datetime.fromtimestamp(time.mktime(str_time))

            params = {
                'date': date_django,
                'station': station
            }
            i = 3
            for var_name in variable_names:
                try:
                    variable = variables.get(code=var_name)  # TODO add try except block
                    value = values[i]
                    params['variable'] = variable
                    i += 1
                    if value in filters:
                        params['value'] = None
                    else:
                        try:
                            value = Decimal(value)
                            if value >= 0:
                                params['value'] = Decimal(value)
                            else:
                                params['value'] = None
                        except:
                            params['value'] = None
                            errors += 1
                    measurement = Measurement(**params)
                    measurements.append(measurement)
                except:
                    pass
                if len(measurements) == 10000:
                    Measurement.objects.bulk_create(measurements)
                    print 'saved'
                    measurements = []
    print '%d errors' % errors
    print 'Insert done!'
    validate_data.delay()


@task(name='validate_data')
def validate_data():
    print 'Validating data!'
    variables = Variable.objects.all()
    for variable in variables:
        measurements = Measurement.objects.filter(variable=variable).order_by('date')
        flag = True
        i = 0
        while flag:
            if measurements[i].value != None:
                flag = False
            else:
                i += 1
        for measurement in measurements[:i]:
            measurement.delete()
        print 'variable %s done' % variable
    print 'Validate done!'


@task(name='generate_report')
def generate_report(*args, **kwargs):
    to_excel = []
    date = kwargs['date']
    length = kwargs['length']
    email = kwargs['email']
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
    path = 'resume.xls'
    xls.save(path)
    print 'Email sent to %s' % kwargs['email']
    email_data = {
        'email': email,
        'subject': 'Resume for date: %s' % date,
        'body': '',
        'path': path
    }
    Email.send_email_attach(**email_data)
