from django import forms

from weather.models import Variable


class ConsultForm(forms.Form):

    date = forms.DateField()
    length = forms.IntegerField()
    variable = forms.ModelChoiceField(
        queryset=Variable.objects.all()
    )

    def __init__(self, *args, **kwargs):
        super(ConsultForm, self).__init__(*args, **kwargs)
        self.fields['date'].widget.attrs['class'] = 'datepicker'


class ResumeForm(forms.Form):

    date = forms.DateField()
    length = forms.IntegerField()
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super(ResumeForm, self).__init__(*args, **kwargs)
        self.fields['date'].widget.attrs['class'] = 'datepicker'
