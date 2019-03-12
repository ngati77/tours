# -*- coding: utf-8 -*-
"""
Created on Sun Dec 16 07:38:21 2018

@author: Tamuz
"""


import sys, os, django
import datetime
# append root folder of django project
# could be solved with a relative path like os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..') which corresponds to the parent folder of the actual file.
sys.path.append('C:\\first_web\\mysite')
os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
django.setup()

from django.core.mail import send_mail

from tours.tour_emails import tour_emails
from django.template.loader import render_to_string
from django.conf import settings

from tours.models import  Trip, Clients
def main():
    # Search for trips tomorrw
    tomorrow      = datetime.datetime.now() + datetime.timedelta(days=1)
    
    # Find all trips tomorrow
    tripQuery = Trip.objects.filter(trip_date__year  = tomorrow.year,
                                     trip_date__month = tomorrow.month,
                                     trip_date__day   = tomorrow.day,
                                     
                                    )
    
    # Now find the clients and send an email 
    for trip in tripQuery:
        clientQuerey = trip.clients_set.filter(status = 'a')
        for client in clientQuerey:
            msg_plain= 'DUMMY ONE'
#            msg_html = render_to_string('emails/email_reminder.html', {'trip_date':trip.trip_date.strftime("%d-%m-%Y"), 'trip_time':trip.trip_time.strftime("%H:%M"), 'trip_type':trip.trip_type, 'first':client.first_name, 'last':client.last_name })
#            #emailSuccess = tour_emails.send_success(trip_date=trip_date.strftime("%d-%m-%Y"), trip_time=trip_time.strftime("%H:%M"), deposit=deposit, more_to_pay=(paymentSum-deposit), idx=transaction.id, trip_type=tripType,first=first_name, last=last_name)
#            emailSuccess =tour_emails.send_email(msg_html=msg_html, msg_plain=msg_plain, to=[client.email], title=title,cc=[settings.CC_EMAIL])
#        
            more_to_pay=str(client.total_payment-client.pre_paid)
            try:
                msg_html = render_to_string('emails/email_reminder.html', { 
                                                                      'trip_time':trip.trip_time, 
                                                                      'client':client, 
                                                                      'more_to_pay':more_to_pay})
                emailTitle = "תזכורת לסיור מחר"
                #cc =['yael.gati@cambridgeinhebrew.com']
                emailSuccess = tour_emails.send_email(msg_html=msg_html, msg_plain=msg_plain, to=[client.email], title=emailTitle, cc=settings.CC_EMAIL)
            except:
                print('Got an error... sending email...')



















if __name__ == "__main__":
    main()    