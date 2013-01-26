from django.views.generic import RedirectView
from django.views.generic.edit import FormView
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from accounts.forms import LoginForm, RegisterForm
from common.mail import Email


class LoginView(FormView):

    template_name = 'accounts/login.html'
    form_class = LoginForm

    def form_valid(self, form):
        data = form.cleaned_data
        user = auth.authenticate(
            username=data.get('email', ''),
            password=data.get('password', '')
        )
        if user is not None:
            auth.login(self.request, user)
            return super(LoginView, self).form_valid(form)
        else:
            from django.contrib import messages
            messages.error(self.request, 'Wrong')
            return self.form_invalid(form)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('admin_home'))
        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        if self.request.GET.get('next'):
            return self.request.GET.get('next')
        return reverse('admin_home')


class LogoutView(RedirectView):

    url = settings.LOGIN_URL

    def get(self, request, *args, **kwargs):
        auth.logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


class RegisterView(FormView):

    template_name = 'accounts/register.html'
    form_class = RegisterForm

    def form_valid(self, form):
        User = get_user_model()
        data = form.cleaned_data
        params = {
            'email': data['email'],
            'first_name': data['first_name'],
            'last_name': data['last_name']
        }
        user = User(**params)
        import uuid
        user.password = uuid.uuid4().hex
        user.save()
        email_data = {
            'to': [user.email],
            'subject': 'Registration Successful',
            'context': {'user': user},
            'template_name': 'accounts/email/register_notification.html'
        }
        Email.send_mail(**email_data)
        return super(RegisterView, self).form_valid(form)

    def get_success_url(self):
        return '/'
