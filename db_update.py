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
sys.path.append('/Users/owner/cambridge')
os.environ['DJANGO_SETTINGS_MODULE'] = 'cambridge.settings'

# This is needed
#sys.path.append('/home/ngati/cambridge')
#os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings.production'
django.setup()

from django.shortcuts import get_object_or_404
from django.conf import settings

from tours.models import  Trip, Guide, OurTours

def main():
    
    # Find all trips tomorrow
    tripQuery = Trip.objects.all()
    print (len(tripQuery))

    ourToursClassic = get_object_or_404(OurTours, trip_abc_name='Classic')
    ourToursWinter = get_object_or_404(OurTours,  trip_abc_name='Winter')
    ourToursFree = get_object_or_404(OurTours,    trip_abc_name='Free')
    ourToursFamily = get_object_or_404(OurTours,  trip_abc_name='Family')

    guideg    = get_object_or_404(Guide, user_name='yaelg')
    guider    = get_object_or_404(Guide, user_name='yaelr')

    # Now find the clients and send an email 
    for trip in tripQuery:
        if trip.get_trip_type_display() == 'Classic':
            trip.ourTour = ourToursClassic
        elif trip.get_trip_type_display() == 'Winter':
            trip.ourTour = ourToursWinter
        elif trip.get_trip_type_display() == 'Free':
            trip.ourTour = ourToursFree
        elif trip.get_trip_type_display() == 'Family':
            trip.ourTour = ourToursFamily
        
        if trip.get_trip_guide_display() == 'YaelR':
            trip.guide = guider
        elif trip.get_trip_guide_display() == 'YaelG':
            trip.guide = guideg
        trip.save()
        


if __name__ == "__main__":
    main()    
