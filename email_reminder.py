# -*- coding: utf-8 -*-
"""
Created on Sun Dec 16 07:38:21 2018

@author: Tamuz
"""


import sys, os, django
import datetime
# append root folder of django project
# could be solved with a relative path like 
#os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..') which corresponds to the parent folder of the actual file.
# Used locally
#sys.path.append('/Users/owner/cambridge')
#os.environ['DJANGO_SETTINGS_MODULE'] = 'cambridge.settings'

# This is needed
sys.path.append('/home/ngati/cambridge')
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings.production'
django.setup()

from tours.tour_emails import tour_emails
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from django.conf import settings

from tours.models import  Trip, Clients, OurTours

def main():
    # Search for trips tomorrw
    tomorrow      = datetime.datetime.now() + datetime.timedelta(days=1)
    
    # Find all trips tomorrow
    tripQuery = Trip.objects.filter(trip_date__year  = tomorrow.year,
                                     trip_date__month = tomorrow.month,
                                     trip_date__day   = tomorrow.day,
                                     status           = 'a',
                                     
                                    )
    
    # Now find the clients and send an email 
    for trip in tripQuery:
        if (trip.guide):
            email_guide = trip.guide.email
        else:
            email_guide = ''
        NotFree = (trip.ourTour.price != 0)
        clientQuerey = trip.clients_set.filter(status = 'a')
        for client in clientQuerey:
            msg_plain= 'תזכורת לסיור מחר'
            more_to_pay=str(client.total_payment-client.pre_paid)
            
            try:
                msg_html = render_to_string('emails/email_reminder.html', { 
                                                                      'trip_time':trip.trip_time, 
                                                                      'client':client, 
                                                                      'more_to_pay':more_to_pay,
                                                                      'NotFree':NotFree})
                emailTitle = "תזכורת לסיור מחר"
                #cc =['yael.gati@cambridgeinhebrew.com']
                emailSuccess = tour_emails.send_email(msg_html=msg_html, msg_plain=msg_plain, to=[client.email,email_guide], title=emailTitle, cc=settings.CC_EMAIL)
            except:
                print('Got an error... sending email...')



if __name__ == "__main__":
    main()    
