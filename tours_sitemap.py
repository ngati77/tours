# -*- coding: utf-8 -*-
"""
Created on Sat Apr  6 19:59:27 2019

@author: Tamuz
"""

from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from datetime import datetime


from tours.models import OurTours

class OurToursSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return OurTours.objects.filter(confirm=True)

    def lastmod(self, obj):
        return datetime.now()
    
    def location(self, obj):
        return '/tour_details/' + obj.trip_abc_name



class SiteSitemap(Sitemap):
        
    def items(self):
        return ['tour:team','tour:reviewes','tour:home','tour:gallery']
    
    def changefreq(self, obj):
        return 'weekly'
    
    def lastmod(self, obj):
        return datetime.now()
    
    def location(self, obj):
        return reverse(obj)
