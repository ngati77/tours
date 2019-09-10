from django.contrib import admin

from .models import Trip, Clients, TripAvailabilty, GuideVacation
from .models import Review, Gallery, OurTours, Guide, Guide_Background, Transaction
from .models import Contact

from django.contrib.admin import AdminSite
from django.http import HttpResponse
from .tour_emails import tour_emails 
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from django.conf import settings

# Create your models here.


class MyAdminSite(AdminSite):

     def get_urls(self):
         from django.conf.urls import url
         urls = super(MyAdminSite, self).get_urls()
         urls += [
             url(r'^my_view/$', self.admin_view(self.my_view))
         ]
         return urls

     def my_view(self, request):
         return HttpResponse("Hello!")

class TransactionInline(admin.TabularInline):
    model = Transaction
    extra = 3


    
    
    
    



class ClientAdmin(admin.ModelAdmin):
   
    fieldsets = [
        
        ('Client details',   {'fields': ['first_name']}),
        (None,               {'fields': ['last_name']}),
        (None,               {'fields': ['email']}),
        (None,               {'fields': ['number_of_people']}),
        (None,               {'fields': ['number_of_children']}),
        (None,               {'fields': ['found_us']}),
        
        ('Payments',         {'fields': ['pre_paid']}),
        (None,               {'fields': ['total_payment']}),
        (None,               {'fields': ['text']}),
        (None,               {'fields': ['status']}),
        ('Admin',            {'fields': ['admin_comment']}),
        ('Trip',             {'fields': ['trip']}),
        
        
    ]
    inlines         = [TransactionInline]
    list_display    = ('id','first_name', 'last_name', 'email' ,'number_of_people' , 'number_of_children', 'pre_paid', 'total_payment', 'confirm_use', 'send_emails','found_us','text','status','admin_comment')
    list_filter     = ['first_name']
    search_fields   = ['first_name','last_name']
    
    def send_success_email(self, request, queryset):
        emailTitle = "סיור בקיימברידג' - אישור הזמנה"
        emailType = 'emails/email_success.html'
        for client in queryset:
            self.send_email_again(request, emailTitle, client, emailType)
            
    def send_update_trip_email(self, request, queryset):
        emailTitle = "סיור בקיימברידג' - עידכון פרטים: "
        emailType = 'emails/email_success.html'
        for client in queryset:
            emailTitle = emailTitle + client.admin_comment 
            self.send_email_again(request, emailTitle, client,emailType)
            
    def send_cancelaion_trip_email(self, request, queryset):
        emailTitle = "סיור בקיימברידג' - ביטול סיור"
        emailType = 'emails/email_cancelation.html'
        for client in queryset:
            emailTitle = emailTitle   
            self.send_email_again(request, emailTitle, client,emailType)
            
    def send_email_again(self, request, emailTitle, client, emailType):
        trip = client.trip
        #OurToursQuery = OurTours.objects.filter(trip_type=trip.trip_type)
        ourTours = get_object_or_404(OurTours, trip_type=trip.trip_type)
        NotFree = (ourTours.price != 0)
        #if len(OurToursQuery)!=1:
        #    print('Raise exception')
        #title = OurToursQuery[0].title
        msg_plain= 'DUMMY ONE'
        children = (client.number_of_children > 0)
        more_to_pay=(client.total_payment-client.pre_paid)
        try:
            msg_html = render_to_string(emailType, {'trip_date':trip.trip_date, 
                                                                      'trip_time':trip.trip_time, 
                                                                      'trip_type':ourTours.title, 
                                                                      'client':client, 
                                                                      'print_children':children, 
                                                                      'more_to_pay':more_to_pay,
                                                                      'NotFree':NotFree})
            #emailSuccess = tour_emails.send_success(trip_date=trip_date.strftime("%d-%m-%Y"), trip_time=trip_time.strftime("%H:%M"), deposit=deposit, more_to_pay=(paymentSum-deposit), idx=transaction.id, trip_type=tripType,first=first_name, last=last_name)
            #emailTitle = "סיור בקיימברידג' - אישור הזמנה"
            #cc =['yael.gati@cambridgeinhebrew.com']
            emailSuccess = tour_emails.send_email(msg_html=msg_html, msg_plain=msg_plain, to=[client.email], title=emailTitle, cc=settings.CC_EMAIL)
        except:
            print('Got an error... sending email...')

        self.message_user(request, "%s successfully send email to ." % client.email)
# 
    send_success_email.short_description        = "Resending confirmation email to a specific client"   
    send_update_trip_email.short_description    = "Update client details"   
    send_cancelaion_trip_email.short_description    = "Cancel trip email"
    actions = [send_success_email, send_update_trip_email, send_cancelaion_trip_email]
    
    
class TransactionAdmin(admin.ModelAdmin):
   
    fieldsets = [
        
        ('transaction details',   {'fields': ['charge_id']}),
        (None,               {'fields': ['create_date']}),
        (None,               {'fields': ['amount']}),
        (None,               {'fields': ['token']}),
        (None,               {'fields': ['success']}),
        (None,               {'fields': ['client']}),
        
    ]
    list_display    = ('id','charge_id', 'create_date', 'amount' ,'success','client')
    list_filter     = ['create_date']
    search_fields   = ['create_date']
    
class ClientsInline(admin.TabularInline):
    model = Clients
    extra = 3
    
class TripAdmin(admin.ModelAdmin):
    def track_trip(self, request, queryset):
        rows_updated = queryset.update(status='d')
        if rows_updated == 1:
            message_bit = "1 tri was"
        else:
            message_bit = "%s trips were" % rows_updated
        self.message_user(request, "%s successfully marked as published." % message_bit)
        
    track_trip.short_description = "Mark selected trips as confirmed"
    fieldsets = [
        
        ('Date information', {'fields': ['trip_date']}),
        (None,               {'fields': ['trip_time']}),
        ('Details',          {'fields': ['trip_guide']}),
        (None,               {'fields': ['trip_type']}),
        (None,               {'fields': ['status']}),
       
        ('Date information', {'fields': ['create_date'],'classes': ['collapse']}),
        ('Comments',         {'fields': ['trip_text']}),
        (None,               {'fields': ['total_payment']}),
       
        
    ]
    inlines         = [ClientsInline]
    list_display    = ('id','trip_type', 'trip_date', 'trip_time' ,'trip_guide' ,'status','create_date','total_payment')
    list_filter     = ['trip_date']
    search_fields   = ['trip_text']
    actions         = ['track_trip']


class TripAvailabiltyAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['ava_trip_type']}),
        ('Date information', {'fields': ['ava_time']}),
        (None,               {'fields': ['ava_select_day']}),
        ('Date information', {'fields': ['ava_trip_day']}),
       
    ]
    list_display    = ('ava_trip_type', 'ava_time','ava_select_day','ava_trip_day')
    list_filter     = ['ava_trip_day']
    search_fields   = ['ava_select_day']

class GuideVacationAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['guide_vacation']}),
        ('Date information', {'fields': ['vac_start_date']}),
        ('Date information', {'fields': ['vac_end_date']}),
        (None,               {'fields': ['vac_cancel_classy']}),
        (None,               {'fields': ['vac_cancel_family']}),
        (None,               {'fields': ['vac_cancel_all']}),
       
    ]
    list_display    = ('guide_vacation', 'vac_start_date','vac_end_date','vac_cancel_classy','vac_cancel_family','vac_cancel_all')
    list_filter     = ['vac_start_date']
    search_fields   = ['guide_vacation']
    

class ReviewAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['first_name']}),
        ('Date information', {'fields': ['create_date']}),
        ('Date information', {'fields': ['review_text']}),
        (None,               {'fields': ['title']}),
        (None,               {'fields': ['confirm']}),
        
        
       
    ]
    list_display    = ('first_name', 'create_date','review_text','title','confirm')
    list_filter     = ['create_date']
    search_fields   = ['first_name']
    
class GalleryAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Date information', {'fields': ['text']}),
        (None,               {'fields': ['title']}),
        (None,               {'fields': ['img']}),
        (None,               {'fields': ['confirm']}),
        
        
       
    ]
    list_display    = ('text','title','img','confirm')
    list_filter     = ['title']
    search_fields   = ['title']

class OurTourAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['title']}),
        ('Description on home page',               {'fields': ['headerShort1']}),
        (None,               {'fields': ['descriptionShort1']}),
        (None,               {'fields': ['whoCanDoIt']}),
        (None,               {'fields': ['description1']}),
        (None,               {'fields': ['description2']}),
        (None,               {'fields': ['description3']}),
        (None,               {'fields': ['duration']}),
        (None,               {'fields': ['price']}),
        (None,               {'fields': ['priceChild']}),
        (None,               {'fields': ['deposit']}),
        (None,               {'fields': ['trip_type']}),
        (None,               {'fields': ['img']}),
        (None,               {'fields': ['confirm']}),
        (None,               {'fields': ['order']}),
    ]
    list_display    = ('title','price','trip_type','img','confirm','order','priceChild','deposit')

class GuideBackgroundInline(admin.TabularInline):
    model = Guide_Background
    extra = 3


    
class GuideAdmin(admin.ModelAdmin):
    fieldsets = [
        
        (None,               {'fields': ['first_name']}),
        (None,               {'fields': ['last_name']}),
        (None,               {'fields': ['order']}),
        (None,               {'fields': ['image']}),
        (None,               {'fields': ['general_info']}),
        (None,               {'fields': ['confirm']}),
       
    ]
    inlines         = [GuideBackgroundInline]
    list_display    = ('first_name','last_name', 'image','confirm')
    search_fields   = ['first_name']
    
    
class ContactAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['create_date']}),
        (None,               {'fields': ['first_name']}),
        (None,               {'fields': ['last_name']}),
        (None,               {'fields': ['email']}),
        (None,               {'fields': ['text']}),
        (None,               {'fields': ['confirm']}),
    ]
    list_display    = ('create_date','first_name','last_name','email','text','confirm')
    list_filter     = ['create_date']




admin.site.register(Trip, TripAdmin)
admin.site.register(TripAvailabilty, TripAvailabiltyAdmin)
admin.site.register(GuideVacation, GuideVacationAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Gallery, GalleryAdmin)
admin.site.register(OurTours, OurTourAdmin)
admin.site.register(Guide, GuideAdmin)
admin.site.register(Clients, ClientAdmin)
admin.site.register(Contact,ContactAdmin)
admin.site.register(Transaction,TransactionAdmin)




admin_site = MyAdminSite()
