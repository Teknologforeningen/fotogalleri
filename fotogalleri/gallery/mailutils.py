from django.core.mail import send_mail
from django.conf import settings


def mail_feedback(context):
    subject = context['title']
    message = '''
    {text}

    FROM: {sender}
    '''.format(text=context['text'], sender=context['email'])
    sender = settings.FEEDBACK_EMAIL_SENDER
    receiver = settings.FEEDBACK_EMAIL_RECEIVER

    return send_mail(subject, message, sender, [receiver], fail_silently=False)
