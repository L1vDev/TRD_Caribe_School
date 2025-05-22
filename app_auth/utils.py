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

def badge_callback(request):
    from app_config.models import ContactRequest
    request_count=ContactRequest.objects.filter(answered=False).all().count()
    return request_count
    
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
    try:
        email.send()
        return True
    except Exception as e:
        print(f"Error enviando email: {str(e)}")
    return False

def send_reset_password_email(user,url):
    subject = f'Reinicia tu contraseña en {settings.SITE_NAME}'
    context = {
        "url":url,
        "user":user,
        "site_name":settings.SITE_NAME
    }
    to_email=[user.email]
    from_email=settings.DEFAULT_FROM_EMAIL
    html_content = render_to_string('utils/reset_password.html', context)
    text_content = strip_tags(html_content)
    
    email = EmailMultiAlternatives(subject, text_content, from_email, to_email)
    email.attach_alternative(html_content, 'text/html')
    try:
        email.send()
        return True
    except Exception as e:
        print(f"Error enviando email: {str(e)}")
    return False

def send_invoice_email(invoice):
    try:
        subject = f'Estado de entrega de pedido en {settings.SITE_NAME}'
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = [invoice.email]
        if invoice.status == "canceled":
            email_subject="Su pedido ha sido cancelado"
            text=f"Tu pedido {invoice.id} ha sido cancelado. Sentimos mucho cualquier molestia ocasionada y quedamos a tu disposición para cualquier consulta o para ayudarte con una nueva compra. Gracias por confiar en nosotros."
        elif invoice.status == "completed":
            email_subject="¡Pedido entregado!"
            text=f"Tu pedido {invoice.id} ha sido entregado con éxito. ¡Gracias por elegirnos! Esperamos verte pronto de nuevo."
        elif invoice.status == "sended":
            email_subject="¡Tu pedido está en camino!"
            text=f"Nos alegra informarte que tu pedido {invoice.id} ya está en camino. Pronto lo tendrás en tus manos. Gracias por comprar con nosotros."
        else:
            email_subject="¡Su compra ha sido completada!"
            text=""
        context = {
            'invoice': invoice,
            'site_name':settings.SITE_NAME,
            'delivery_message':text,
            'email_subject': email_subject,
        }

        html_content = render_to_string('utils/invoice_email.html', context)
        text_content = strip_tags(html_content)
    
        email = EmailMultiAlternatives(subject, text_content, from_email, to_email)
        email.attach_alternative(html_content, "text/html")
        email.attach(f'{settings.SITE_NAME}-{invoice.first_name} {invoice.last_name}-{invoice.id}.pdf', invoice.invoice_file.file.read(), 'application/pdf')
        
        try:
            email.send()
            return True
        except Exception as e:
            # Log the error or handle it appropriately
            print(f"Failed to send email: {str(e)}")
    except Exception as e:
          print(str(e))
    
    return False