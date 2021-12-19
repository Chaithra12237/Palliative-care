from .models import *
from django.core.mail import send_mail


def AdminCheck(request):
    user = request.user
    if user.is_authenticated:
        try:
            u = Users.objects.get(user=user)
            if u.type == 'admin':
                return (True)
            else:
                return (False)
        except:
            return (False)
    else:
        return (False)

def ProviderCheck(request):
    user = request.user
    if user.is_authenticated:
        try:
            u = Users.objects.get(user=user)
            if u.type == 'service_provider':
                return (True)
            else:
                return (False)
        except:
            return (False)
    else:
        return (False)

def UserCheck(request):
    user = request.user
    if user.is_authenticated:
        try:
            u = Users.objects.get(user=user)
            if u.type == 'public':
                return (True)
            else:
                return (False)
        except:
            return (False)
    else:
        return (False)


def MailSend(request,subject,message,to):
    send_mail(
        subject,
        message,
        'palliativecare197@gmail.com',
        [to],
        fail_silently=False,
    )
    