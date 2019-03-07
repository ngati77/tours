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
#    path('calendar/<int:pYear>/<int:pMonth>/<str:view>', views.new_calendar_view, name='new_calendar_view'),
#    path('<int:pYear>/<int:pMonth>/<int:pDay>/<int:pHour>/<str:tripType>', views.booking, name='booking'),
    path('<int:pYear>/<int:pMonth>/<str:tripType>', views.bookTour, name='book-tour'),
    
    path('book_tour_today/<str:tripType>', views.bookTourToday, name='book_tour_today'),
    path('book_tour_today', views.bookTourToday, name='book_tour_today'),
    
    path('tour_details/<str:tripType>', views.tour_details, name='tour_details'),
    path('tour_details', views.tour_details, name='tour_details'),

    
    path('reviewes',       views.reviewes, name='reviewes'),
    path('ourTours',       views.ourTours, name='ourTours'),
#    path('find_your_day/<str:view>', views.find_your_day, name='find_your_day'),
#    path('find_your_day',  views.find_your_day, name='find_your_day'),
    path('gallery',        views.gallery, name='gallery'),
    path('team',           views.team, name='team'),
#    path(r'guideview',     views.GuideView.as_view(), name='guideview'),
    path('clients_in_tour/<int:pk>/',    views.ClientView.as_view(), name='clientview'),
    path('success',         views.success, name="success"),
    path('failure',         views.failure, name="failure"),
    path('contact',         views.contactUs, name="contact"),
    path('give_review',     views.GiveReview, name="give_review"),
    path('report-view',     views.reportView, name="report-view"),
    path('trip_view',       views.tripView, name="trip_view"),
    path('trip_pdf/<int:pk>/', views.tripPdf, name='trip_pdf'),
    path('payment',          views.payment, name="payment"),
    path('tasks',            views.tasks, name="tasks"),
    
    path('tour_confirm/<int:pk>/',            views.tour_confirm, name="tour_confirm"),
    path('tour_complete/<int:pk>/',            views.tour_complete, name="tour_complete"),
    path('contact_confirm/<int:pk>/',            views.contact_confirm, name="contact_confirm"),
    path('review_confirm/<int:pk>/',            views.review_confirm, name="review_confirm"),


]