# -*- coding: utf-8 -*-
"""
Created on Tue Aug  7 21:07:27 2018

@author: ngati
"""

from django import forms


from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from datetime import date, datetime, time
#from captcha.fields import CaptchaField

from .models import Guide, FoundUs
       
class BookingForm(forms.Form):
    
    first_name     = forms.CharField(label ='',  widget=forms.TextInput(attrs={'placeholder': 'שם פרטי'}))
    last_name      = forms.CharField(label ='',  widget=forms.TextInput(attrs={'placeholder': 'שם משפחה'}))
    phone          = forms.CharField(label ='',  widget=forms.TextInput(attrs={'placeholder': 'מספר טלפון ביום הטיול'}))
    email          = forms.CharField(max_length=100, label ='',
                                        widget= forms.EmailInput
                                        (attrs={'placeholder':'דוא"ל'}))

    number_adults  = forms.IntegerField(max_value = 20, min_value =1, initial=0, label ='מספר מבוגרים' ) 
    number_child   = forms.IntegerField(max_value = 10, min_value =0, initial=0, label ='מספר ילדים עד גיל 12')
    confirm_use    = forms.BooleanField(label ='אני מסכים שפרטי ישמרו כדי ליצור קשר לגבי הסיור',label_suffix="")
    send_emails    = forms.BooleanField(required=False, label ='אני מעוניין להצטרף לרשימת התפוצה',label_suffix="")
    foundUs        = forms.ModelChoiceField(queryset=FoundUs.objects.all(), label='מצא אותנו')
    text           = forms.CharField(required=False, label  ='', widget=forms.Textarea(attrs={'placeholder': 'שדה לא חובה - אנא הוסיפו כמה פרטים על עצמכם כדי שנדע את מי אנו פוגשים. אם ובתה / משפחה / פנסיונריות . כאן זה גם המקום לכתוב אם ישנה איזה מגבלה או משהו אחר שאנו צריכים להיות מודעים אליו. תודה'}))
    deposit        = forms.IntegerField(min_value =30,initial=0,label =' תשלום מקדמה (לפחות 30 פאונד)')
    price          = forms.IntegerField(widget = forms.HiddenInput())
    min_adult      = forms.IntegerField(widget = forms.HiddenInput())
    priceChild     = forms.IntegerField(widget = forms.HiddenInput())
    paymentSum     = forms.IntegerField(widget = forms.HiddenInput())
    title          = forms.CharField(widget = forms.HiddenInput())
    trip_date      = forms.CharField(widget = forms.HiddenInput())
    trip_time      = forms.CharField(widget = forms.HiddenInput())
    trip_type      = forms.CharField(widget = forms.HiddenInput())

    
    def get_data(self):
        title           = self.data['title']
        trip_date       = self.cleaned_data['trip_date']
        trip_time       = self.cleaned_data['trip_time']
        trip_type       = self.cleaned_data['trip_type']
        first_name      = self.cleaned_data['first_name']
        last_name       = self.cleaned_data['last_name']
        phone           = self.cleaned_data['phone']
        email           = self.cleaned_data['email']
        number_adults   = self.cleaned_data['number_adults']
        number_child    = self.cleaned_data['number_child']
        deposit         = self.cleaned_data['deposit']
        paymentSum      = self.cleaned_data['paymentSum']
        confirm_use     = self.cleaned_data['confirm_use']
        send_emails     = self.cleaned_data['send_emails']
        foundUs         = self.data['foundUs']
        text            = self.cleaned_data['text']
        
        return  [title,
                trip_date, 
                trip_time, 
                trip_type, 
                first_name, 
                last_name, 
                phone, 
                email, 
                number_adults, 
                number_child, 
                deposit, 
                paymentSum, 
                confirm_use, 
                send_emails, 
                foundUs, 
                text]



    def clean(self):
        # Then call the clean() method of the super  class
        cleaned_data = super().clean()
        # Check that if this is a new tour we have enough people.
        # If this is a new tour, we make sure the payment is above £60
        if cleaned_data['price'] !=0 and cleaned_data['min_adult']==1 and cleaned_data['paymentSum']<60 :
            raise ValidationError('סליחה, אבל כרגע אין משתתפים נוספים ולכן סכום מינימלי הוא 60 פאונד. אם ניתן נסו לשנות תאריך או צרו איתנו קשר שנוכל לעזור לכם.')
        
        return cleaned_data
      
'''  
class PaymentForm(forms.Form):
    title          = forms.CharField(widget = forms.HiddenInput())
    trip_date      = forms.CharField(widget = forms.HiddenInput())
    trip_time      = forms.CharField(widget = forms.HiddenInput())
    trip_type      = forms.CharField(widget = forms.HiddenInput())
    first_name     = forms.CharField(widget = forms.HiddenInput())
    last_name      = forms.CharField(widget = forms.HiddenInput())
    phone          = forms.CharField(widget = forms.HiddenInput())
    email          = forms.EmailField(widget = forms.HiddenInput())
    number_adults  = forms.IntegerField(widget = forms.HiddenInput()) 
    number_child   = forms.IntegerField(widget = forms.HiddenInput())
    confirm_use    = forms.BooleanField(widget = forms.HiddenInput())
    send_emails    = forms.BooleanField(required=False, widget = forms.HiddenInput())
    foundUs        = forms.ModelChoiceField(queryset=FoundUs.objects.all(), widget = forms.HiddenInput())
    text           = forms.CharField(required=False, widget = forms.HiddenInput())
    deposit        = forms.IntegerField(widget = forms.HiddenInput())
    paymentSum     = forms.IntegerField(widget = forms.HiddenInput())
    

    
    def get_data(self):
        title           = self.data['title']
        first_name      = self.data['first_name']
        trip_date       = self.data['trip_date']
        trip_time       = self.data['trip_time']
        trip_type       = self.data['trip_type']
        last_name       = self.data['last_name']
        phone           = self.data['phone']
        email           = self.data['email']
        number_adults   = self.data['number_adults']
        number_child    = self.data['number_child']
        deposit         = self.data['deposit']
        paymentSum      = self.data['paymentSum']
        confirm_use     = self.data['confirm_use']
        send_emails     = self.data['send_emails']
        foundUs        = self.data['foundUs']
        text            =self.data['text']
        return title, trip_date, trip_time, trip_type, first_name, last_name, phone, email, number_adults, number_child, deposit, paymentSum, confirm_use, send_emails, foundUs, text        

'''

class ContactForm(forms.Form):
    first_name     = forms.CharField(label  ='', widget=forms.TextInput(attrs={'placeholder': 'שם פרטי'}))
    last_name      = forms.CharField(label  ='', widget=forms.TextInput(attrs={'placeholder': 'שם משפחה'}))
    #email          = forms.EmailField(label ='', widget=forms.TextInput(attrs={'placeholder': 'דוא"ל'}))
    email          = forms.CharField(max_length=100, label ='',
                                        widget= forms.EmailInput
                                        (attrs={'placeholder':'דוא"ל'}))
    text           = forms.CharField(label  ='', widget=forms.Textarea(attrs={'cols':26,'placeholder': 'נושא הפנייה'}))
    
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

class ReportForm(forms.Form):
    MONTH = (
    ('1', 'Jan'),
    ('2', 'Feb'),
    ('3', 'Mar'),
    ('4', 'Apr'),
    ('5', 'May'),
    ('6', 'Jun'),
    ('7', 'Jul'),
    ('8', 'Aug'),
    ('9', 'Sep'),
    ('10', 'Oct'),
    ('11', 'Nov'),
    ('12', 'Dec'),
    )
    start_month      = forms.ChoiceField(choices=MONTH)
    end_month        = forms.ChoiceField(choices=MONTH)
    start_year       = forms.IntegerField(initial=2019)
    end_year         = forms.IntegerField(initial=2019)
   
    guide = forms.ModelChoiceField(queryset=Guide.objects.all(),required=False)
    foundUs       = forms.ModelChoiceField(queryset=FoundUs.objects.all(),required=False, label='מצא אותנו')

    ORDER = (
    ('trip_date', 'Date'),
    ('trip_guide', 'Guide'),
    )
    order = forms.ChoiceField(choices=ORDER)
    OUTPUT = (
    ('html', 'HTML'),
    ('pdf', 'SHOW PDF'),
    ('send_pdf', 'SHOW & SEND PDF'),
    )
    output = forms.ChoiceField(choices=OUTPUT)
    def get_data(self):
        start_month     = self.cleaned_data['start_month']
        end_month       = self.cleaned_data['end_month']
        start_year      = self.cleaned_data['start_year']
        end_year        = self.cleaned_data['end_year']
        guide           = self.cleaned_data['guide']
        foundUs        = self.cleaned_data['foundUs']
        order           = self.cleaned_data['order']
        output          = self.cleaned_data['output']
        return start_month, end_month, start_year, end_year, guide, foundUs,order, output  

    

