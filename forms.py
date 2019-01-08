# -*- coding: utf-8 -*-
"""
Created on Tue Aug  7 21:07:27 2018

@author: ngati
"""

from django import forms


from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from datetime import date, datetime, time

 
    
class Booking1Form(forms.Form):
    trip_date      = forms.DateField(widget = forms.HiddenInput())
    trip_time      = forms.TimeField(widget = forms.HiddenInput())
    trip_type      = forms.CharField(widget = forms.HiddenInput())
    first_name     = forms.CharField(label ='',  widget=forms.TextInput(attrs={'placeholder': 'שם פרטי'}))
    last_name      = forms.CharField(label ='',  widget=forms.TextInput(attrs={'placeholder': 'שם משפחה'}))
    phone          = forms.CharField(label ='',  widget=forms.TextInput(attrs={'placeholder': 'טלפון לזמן הטיול'}))
    email          = forms.EmailField(label ='' ,widget=forms.TextInput(attrs={'placeholder': 'דוא"ל'}))
    number_adults  = forms.IntegerField(max_value = 10, min_value =0, label ='מספר מבוגרים' ) 
    number_child   = forms.IntegerField(max_value = 10, min_value =0, label ='מספר ילדים עד גיל 12')
    deposit        = forms.IntegerField(widget = forms.HiddenInput())
    paymentSum     = forms.IntegerField(widget = forms.HiddenInput())

    
    def get_data(self):
        first_name      = self.cleaned_data['first_name']
        trip_date       = self.cleaned_data['trip_date']
        trip_time       = self.cleaned_data['trip_time']
        trip_type       = self.cleaned_data['trip_type']
        last_name       = self.cleaned_data['last_name']
        phone           = self.cleaned_data['phone']
        email           = self.cleaned_data['email']
        number_adults   = self.cleaned_data['number_adults']
        number_child    = self.cleaned_data['number_child']
        deposit         = self.cleaned_data['deposit']
        paymentSum      = self.cleaned_data['paymentSum']
        return trip_date, trip_time, first_name, last_name, phone, email, number_adults, number_child, deposit, paymentSum 
        

class ContactForm(forms.Form):
    first_name     = forms.CharField(label  ='', widget=forms.TextInput(attrs={'placeholder': 'שם פרטי'}))
    last_name      = forms.CharField(label  ='', widget=forms.TextInput(attrs={'placeholder': 'שם משפחה'}))
    email          = forms.EmailField(label ='', widget=forms.TextInput(attrs={'placeholder': 'דוא"ל'}))
    text           = forms.CharField(label  ='', widget=forms.Textarea(attrs={'rows':8, 'cols':20,'placeholder': 'נושא הפנייה'}))

    
    def get_data(self):
        first_name      = self.cleaned_data['first_name']
        last_name       = self.cleaned_data['last_name']
        email           = self.cleaned_data['email']
        text            = self.cleaned_data['text']
        
        return first_name, last_name, email, text 

class ReviewForm(forms.Form):
    first_name     = forms.CharField(label  ='', widget=forms.TextInput(attrs={'placeholder': 'שם פרטי'}))
  
    review_title   = forms.CharField(label  ='', widget=forms.TextInput(attrs={'placeholder': 'כותרת'}))
    text           = forms.CharField(label  ='', widget=forms.Textarea(attrs={'placeholder': 'חוות דעת'}))

    
    def get_data(self):
        first_name      = self.cleaned_data['first_name']
        review_title    = self.cleaned_data['review_title']
        text            = self.cleaned_data['text']
        
        return first_name,  review_title, text
