from django.contrib import admin

from .models import Trip, Clients, TripAvailabilty, GuideVacation, FoundUs
from .models import Review, Gallery, OurTours, Guide, Guide_Background, Transaction, Location, Instruction
from .models import Contact

from django.contrib.admin import AdminSite
from django.http import HttpResponse
from .tour_emails import tour_emails 
from django.shortcuts import get_object_or_404
from django.conf import settings




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
        (None,               {'fields': ['foundUs']}),
        ('Payments',         {'fields': ['pre_paid']}),
        (None,               {'fields': ['total_payment']}),
        (None,               {'fields': ['text']}),
        (None,               {'fields': ['status']}),
        ('Admin',            {'fields': ['admin_comment']}),
        ('Trip',             {'fields': ['trip']}),
        
        
    ]
    inlines         = [TransactionInline]
    list_display    = ('id','first_name', 'last_name', 'email' ,'number_of_people' , 'number_of_children', 'pre_paid', 'total_payment', 'confirm_use', 'send_emails','foundUs','text','status','admin_comment')
    list_filter     = ['first_name']
    search_fields   = ['first_name','last_name']
    
    def send_success_email(self, request, queryset):
        emailTitle = "סיור בקיימברידג' - אישור הזמנה"
        emailType = 'emails/email_success.html'
        for client in queryset:
            message = tour_emails.send_email_again(request=request, emailTitle=emailTitle, client=client, emailType=emailType)
            self.message_user(request, message)

            
    def send_update_trip_email(self, request, queryset):
        emailTitle = "סיור בקיימברידג' - עידכון הזמנה "
        emailType = 'emails/email_update.html'
        for client in queryset:
            message = tour_emails.send_email_again(request=request, emailTitle=emailTitle, client=client, emailType=emailType)
            self.message_user(request, message)

            
    def send_cancelaion_trip_email(self, request, queryset):
        emailTitle = "סיור בקיימברידג' - ביטול סיור"
        emailType = 'emails/email_cancelation.html'
        for client in queryset:
            message = tour_emails.send_email_again(request=request, emailTitle=emailTitle, client=client, emailType=emailType)
            self.message_user(request, message)
            
    # def send_email_again(self, request, emailTitle, client, emailType):
    #     trip = client.trip
    #     NotFree = (trip.ourTour.price != 0)
    #     #if len(OurToursQuery)!=1:
    #     #    print('Raise exception')
    #     #title = OurToursQuery[0].title
    #     msg_plain   = 'DUMMY ONE'
    #     children    = (client.number_of_children > 0)
    #     more_to_pay =(client.total_payment-client.pre_paid)
    #     dayHeb      = hebdict[client.trip.trip_date.strftime('%a')]
    #     try:
    #         msg_html = render_to_string(emailType, {
    #                                               'emailTitle':emailTitle,
    #                                               'client':client, 
    #                                               'print_children':children, 
    #                                               'more_to_pay':more_to_pay,
    #                                               'day_in_hebrew':dayHeb,
    #                                               'NotFree':NotFree})
    #         #emailSuccess = tour_emails.send_success(trip_date=trip_date.strftime("%d-%m-%Y"), trip_time=trip_time.strftime("%H:%M"), deposit=deposit, more_to_pay=(paymentSum-deposit), idx=transaction.id, trip_type=tripType,first=first_name, last=last_name)
    #         #emailTitle = "סיור בקיימברידג' - אישור הזמנה"
    #         #cc =['yael.gati@cambridgeinhebrew.com']
    #         emailSuccess = tour_emails.send_email(msg_html=msg_html, msg_plain=msg_plain, to=[client.email], title=emailTitle, cc=settings.CC_EMAIL)
    #     except:
    #         print('Got an error... sending email...')

    #     self.message_user(request, "%s successfully send email to ." % client.email)
 
    send_success_email.short_description        = "Resending confirmation email to a specific client"   
    send_update_trip_email.short_description    = "Update client details"   
    send_cancelaion_trip_email.short_description    = "Cancel trip email"
    actions = [send_success_email, send_update_trip_email, send_cancelaion_trip_email]
    
class LocationAdmin(admin.ModelAdmin):
    fieldsets = [
        
        (None,            {'fields': ['title']}),
        (None,            {'fields': ['text_html_style']}), 
        (None,            {'fields': ['text']}), 
        (None,            {'fields': ['default']}), 
        
    ]
    list_display    = ('id','title','text_html_style','default')
    
    def set_default(self, request, queryset):
        objects = Location.objects.all()
        the_obj_id = queryset[0].id
        for obj in objects:
            if obj.id == the_obj_id:
                obj.default = True
            else:
                obj.default = False
            obj.save()

    set_default.short_description        = "Set it to be the default"   
    actions = [set_default]    
    
class InstructionAdmin(admin.ModelAdmin):
    fieldsets = [
        
        (None,            {'fields': ['title']}),
        (None,            {'fields': ['text_html_style']}), 
        (None,            {'fields': ['text']}), 
        (None,            {'fields': ['default']}), 
        
    ]
    list_display    = ('id','title','text_html_style','default')

    def set_default(self, request, queryset):
        objects = Instruction.objects.all()
        the_obj_id = queryset[0].id
        for obj in objects:
            if obj.id == the_obj_id:
                obj.default = True
            else:
                obj.default = False
            obj.save()

    set_default.short_description        = "Set it to be the default"   
    actions = [set_default]


class FoundUsAdmin(admin.ModelAdmin):
    fieldsets = [
        
        (None,            {'fields': ['title']}),
        (None,            {'fields': ['precentage']}),    
        
    ]
    list_display    = ('id','title','precentage')


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
        
        ('Details',          {'fields': ['ourTour']}),
        (None,               {'fields': ['status']}),
        (None,               {'fields': ['total_payment']}),
        ('Date information', {'fields': ['trip_date']}),
        (None,               {'fields': ['trip_time']}),
        ('Make sure not empty',          {'fields': ['guide']}),
        (None,          {'fields': ['location']}),
        (None,          {'fields': ['instruction']}),
       
        ('Date information', {'fields': ['create_date'],'classes': ['collapse']}),
        ('Comments',         {'fields': ['trip_text']}),
       
        
    ]
    inlines         = [ClientsInline]
    list_display    = ('id','trip_date', 'trip_time'  ,'status','create_date','total_payment','ourTour','guide','location')
    list_filter     = ['trip_date']
    search_fields   = ['trip_text']
    actions         = ['track_trip']


class TripAvailabiltyAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['ourTour']}),
        ('Date information', {'fields': ['ava_time']}),
        (None,               {'fields': ['ava_select_day']}),
        ('Date information', {'fields': ['ava_trip_start_day']}),
        ('Date information', {'fields': ['ava_trip_end_day']}),
        
       
    ]
    list_display    = ('ourTour', 'ava_time','ava_select_day','ava_trip_start_day','ava_trip_end_day')
    list_filter     = ['ava_trip_start_day']
    search_fields   = ['ava_select_day']

class GuideVacationAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['guide']}),
        ('Date information', {'fields': ['vac_start_date']}),
        ('Date information', {'fields': ['vac_end_date']}),
        (None,               {'fields': ['ourTour']}),
        (None,               {'fields': ['vac_cancel_all']}),

        
       
    ]
    list_display    = ('guide', 'vac_start_date','vac_end_date','vac_cancel_all')
    list_filter     = ['vac_start_date']
    search_fields   = ['guide']
    

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
        (None,               {'fields': ['ChildAge']}),
        (None,               {'fields': ['deposit']}),
        (None,               {'fields': ['trip_abc_name']}),      
        (None,               {'fields': ['img']}),
        (None,               {'fields': ['confirm']}),
        (None,               {'fields': ['order']}),
        (None,               {'fields': ['base_payment']}),

    ]
    list_display    = ('title','price','img','confirm','order','priceChild','ChildAge','deposit','trip_abc_name','base_payment')

class GuideBackgroundInline(admin.TabularInline):
    model = Guide_Background
    extra = 3


    
class GuideAdmin(admin.ModelAdmin):
    fieldsets = [
        
        (None,               {'fields': ['first_name']}),
        (None,               {'fields': ['last_name']}),
        (None,               {'fields': ['default']}), 
        (None,               {'fields': ['first_name_en']}),
        (None,               {'fields': ['last_name_en']}),
        (None,               {'fields': ['gender_female']}),
        (None,               {'fields': ['user_name']}),
        (None,               {'fields': ['order']}),
        (None,               {'fields': ['image']}),
        (None,               {'fields': ['phone']}),
        (None,               {'fields': ['email']}),
        (None,               {'fields': ['general_info']}),
        (None,               {'fields': ['confirm']}),
       
    ]
    inlines         = [GuideBackgroundInline]
    list_display    = ('first_name', 'last_name', 'default','first_name_en', 'last_name_en','gender_female', 'user_name', 'order', 'image', 'phone' , 'email', 'confirm')
    search_fields   = ['first_name']
    def set_default(self, request, queryset):
        objects = Guide.objects.all()
        the_obj_id = queryset[0].id
        for obj in objects:
            if obj.id == the_obj_id:
                obj.default = True
            else:
                obj.default = False
            obj.save()

    set_default.short_description        = "Set it to be the default"   
    actions = [set_default] 
    
class ContactAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['create_date']}),
        (None,               {'fields': ['first_name']}),
        (None,               {'fields': ['last_name']}),
        (None,               {'fields': ['email']}),
        (None,               {'fields': ['text']}),
        (None,               {'fields': ['confirm']}),
    ]
    list_display    = ('id','create_date','first_name','last_name','email','text','confirm')
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
admin.site.register(FoundUs,FoundUsAdmin)
admin.site.register(Location,LocationAdmin)
admin.site.register(Instruction,InstructionAdmin)




admin_site = MyAdminSite()
