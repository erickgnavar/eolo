from django.core.mail import EmailMultiAlternatives
from django.core.mail.message import EmailMessage
from django.conf import settings
from django.template import Context, loader


class Email(object):

    @staticmethod
    def send_mail(*args, **kwargs):
        context = Context(kwargs.get('context', {}))
        template = loader.get_template(kwargs.get('template_name'))
        html_content = template.render(context)
        subject = kwargs.get('subject')
        from_email = kwargs.get('from_email', settings.DEFAULT_FROM_EMAIL)
        to = kwargs.get('to')
        body = kwargs.get('body', '')

        message = EmailMultiAlternatives(subject, body, from_email, to)
        message.attach_alternative(html_content, 'text/html')
        message.send(fail_silently=True)

    @staticmethod
    def send_email_attach(*args, **kwargs):
        email = EmailMessage()
        email.subject = kwargs['subject']
        email.body = kwargs['body']
        email.from_email = settings.DEFAULT_FROM_EMAIL
        email.to = [kwargs['email']]
        email.attach_file(kwargs['path'])
        email.send()
