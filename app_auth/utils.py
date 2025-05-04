import os
import uuid
import jwt
import datetime
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

def get_unique_filename(instance, filename):
    model_name = instance.__class__.__name__.lower()
    folder_mapping = {
        'user': 'profile/',
        'product': 'products/',
        'productimage': 'product_images/',
        'default': 'others/',
    }
    try:
        folder = folder_mapping[model_name]
    except:
        folder = folder_mapping['default']

    ext = filename.split('.')[-1]
    unique_filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join(folder, unique_filename)

def generate_token(user):
    exp = datetime.datetime.now() + datetime.timedelta(minutes=30)
    payload = {
        'user_email': user.email,
        'exp': exp.timestamp()
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token

def verify_token(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        return payload, True
    except jwt.ExpiredSignatureError:
        return None, False 
    except jwt.InvalidTokenError:
        return None, False

def send_verification_email(user,url):
    subject = f'Verifica tu correo electrónico en {settings.SITE_NAME}'
    context = {
        "url":url,
        "user":user,
        "site_name":settings.SITE_NAME
    }
    to_email=[user.email]
    from_email=settings.DEFAULT_FROM_EMAIL
    html_content = render_to_string('utils/email_verification.html', context)
    text_content = strip_tags(html_content)
    
    email = EmailMultiAlternatives(subject, text_content, from_email, to_email)
    email.attach_alternative(html_content, 'text/html')
    email.send()
    return True
