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
    path('book-tour/<int:pYear>/<int:pMonth>/<str:trip_abc_name>', views.bookTour, name='book-tour'),
    path('book-tour', views.bookTour, name='book-tour'),
    
    path('book_tour_today/<str:trip_abc_name>', views.bookTourToday, name='book_tour_today'),
    path('book_tour_today', views.bookTourToday, name='book_tour_today'),
    
    path('tour_details/<str:trip_abc_name>', views.tour_details, name='tour_details'),
    path('tour_details', views.tour_details, name='tour_details'),

    
    path('reviewes',       views.reviewes, name='reviewes'),
    path('gallery',        views.gallery, name='gallery'),
    path('team',           views.team, name='team'),
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
    path('links',            views.links, name="links"),
    path('privacy',          views.privacy, name="privacy"),
    path('cant_make_it/<int:pk>/',     views.CantMakeIt, name="cant_make_it"),
    path('can_make_it/<int:pk>/',      views.CanMakeIt, name="can_make_it"),
    
    path('tour_confirm/<int:pk>/',            views.tour_confirm, name="tour_confirm"),
    path('tour_complete/<int:pk>/',            views.tour_complete, name="tour_complete"),
    path('contact_confirm/<int:pk>/',            views.contact_confirm, name="contact_confirm"),
    path('contact_not_spam/<int:pk>/',            views.contact_not_spam, name="contact_not_spam"),
    path('contact_spam/<int:pk>/',               views.contact_spam, name="contact_spam"),
    path('review_confirm/<int:pk>/',            views.review_confirm, name="review_confirm"),


]