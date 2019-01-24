# -*- coding: utf-8 -*-
"""
Created on Sat Jul  7 22:48:55 2018

@author: ngati
"""

from django.urls import path

from . import views
app_name = 'tour'
urlpatterns = [
    path('',               views.home, name='home'),
    path('calendar/<int:pYear>/<int:pMonth>/<str:view>', views.new_calendar_view, name='new_calendar_view'),
    path('<int:pYear>/<int:pMonth>/<int:pDay>/<int:pHour>/<str:tripType>', views.booking, name='booking'),
    
    path('reviewes',       views.reviewes, name='reviewes'),
    path('ourTours',       views.ourTours, name='ourTours'),
    path('find_your_day/<str:view>', views.find_your_day, name='find_your_day'),
    path('find_your_day',  views.find_your_day, name='find_your_day'),
    path('gallery',        views.gallery, name='gallery'),
    path('team',           views.team, name='team'),
    path(r'guideview',     views.GuideView.as_view(), name='guideview'),
    path('clientview/<int:pk>/',    views.ClientView.as_view(), name='clientview'),
    path('success',         views.success, name="success"),
    path('failure',         views.failure, name="failure"),
    path('contact',         views.contactUs, name="contact"),
    path('give_review',     views.GiveReview, name="give_review"),
    path('report-viewn',    views.reportView, name="report-view"),

]