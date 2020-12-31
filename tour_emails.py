# -*- coding: utf-8 -*-
"""
Created on Thu Dec  6 22:17:48 2018

@author: Tamuz
"""

from django.conf import settings
from django.core.mail import EmailMultiAlternatives

class tour_emails:
    def send_email(msg_html, msg_plain, to, title,cc):
        
        msg  = EmailMultiAlternatives(subject = title, body= msg_plain, from_email=settings.EMAIL_YAEL, to=to,cc=cc ,bcc=settings.BCC_EMAIL)
        msg.attach_alternative(msg_html, "text/html")
        
        try:
            success = msg.send()
        except: 
            success = False
            print('Error sending email')    
        return success
 
    def send_email_pdf(to, file, file_name):
        
        msg_plain = 'Cambridge in hebrew invoice'
        title     = 'Cambridge In Hebrew'
        
        msg             = EmailMultiAlternatives(subject=title, body= msg_plain, from_email=settings.EMAIL_YAEL, to=to, bcc=settings.BCC_EMAIL)
        #msg.attach_alternative(msg_html, "text/html")
        
        attachment = open(file[1], 'rb')
        msg.attach(file_name, attachment.read(), 'text/plain')
        
        
        try:
            success = msg.send()
        except: 
            print('Error sending email')    
            success = False
        return success
 
    def send_email_msg_pdf(to, msg_html, msg_plain, file, file_name, cc, title): 
        
        
        msg             = EmailMultiAlternatives(subject=title, body= msg_plain, from_email=settings.EMAIL_YAEL, to=to ,bcc=settings.BCC_EMAIL, cc=cc)
        #msg.attach_alternative(msg_html, "text/html")
        
        attachment = open(file[1], 'rb')
        msg.attach(file_name, attachment.read(), 'text/plain')
        msg.attach_alternative(msg_html, "text/html") 
        
        try:
            success = msg.send()
        except: 
            print('Error sending email')   
            success = False
        return success
