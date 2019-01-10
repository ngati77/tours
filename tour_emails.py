# -*- coding: utf-8 -*-
"""
Created on Thu Dec  6 22:17:48 2018

@author: Tamuz
"""

from django.conf import settings
from django.core.mail import EmailMultiAlternatives

class tour_emails:
    def send_email(msg_html, msg_plain, to, title,cc):
        
        msg             = EmailMultiAlternatives(subject=title, body= msg_plain, from_email=settings.EMAIL_YAEL, to=to,cc=settings.CC_EMAIL ,bcc=settings.BCC_EMAIL)
        msg.attach_alternative(msg_html, "text/html")
        try:
            success = msg.send()
        except: 
            print('Error sending email')    
        return success
 
