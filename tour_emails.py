# -*- coding: utf-8 -*-
"""
Created on Thu Dec  6 22:17:48 2018

@author: Tamuz
"""

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


# Create your models here.
hebdict = {'Sun':'ראשון', 'Mon':'שני', 'Tue':'שלישי', 'Wed':'רביעי', 'Thu':'חמישי', 'Fri':'שישי', 'Sat':'שבת'}
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
    
    def send_email_again(request, emailTitle, client, emailType):
        trip = client.trip
        if (trip.guide):
            email_guide = trip.guide.email
        else:
            email_guide = ''
        NotFree = (trip.ourTour.price != 0)
        #if len(OurToursQuery)!=1:
        #    print('Raise exception')
        #title = OurToursQuery[0].title
        msg_plain   = 'DUMMY ONE'
        children    = (client.number_of_children > 0)
        more_to_pay =(client.total_payment-client.pre_paid)
        dayHeb      = hebdict[client.trip.trip_date.strftime('%a')]
        
        msg_html = render_to_string(emailType, {
                                                  'emailTitle':emailTitle,
                                                  'client':client, 
                                                  'print_children':children, 
                                                  'more_to_pay':more_to_pay,
                                                  'day_in_hebrew':dayHeb,
                                                  'NotFree':NotFree})
            #emailSuccess = tour_emails.send_success(trip_date=trip_date.strftime("%d-%m-%Y"), trip_time=trip_time.strftime("%H:%M"), deposit=deposit, more_to_pay=(paymentSum-deposit), idx=transaction.id, trip_type=tripType,first=first_name, last=last_name)
            #emailTitle = "סיור בקיימברידג' - אישור הזמנה"
            #cc =['yael.gati@cambridgeinhebrew.com']
        emailSuccess = tour_emails.send_email(msg_html=msg_html, msg_plain=msg_plain, to=[client.email,email_guide], title=emailTitle, cc=settings.CC_EMAIL)
        

        return f'successfully send email to {client.email}' 
