from django.contrib import admin

from .models import Trip, Clients, TripAvailabilty, GuideVacation
from .models import Review, Gallery, OurTours, Guide, Guide_Background, Transaction
from .models import Contact

from django.contrib.admin import AdminSite
from django.http import HttpResponse
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
        
        ('Payments',         {'fields': ['pre_paid']}),
        (None,               {'fields': ['total_payment']}),
        
    ]
    inlines         = [TransactionInline]
    list_display    = ('id','first_name', 'last_name', 'email' ,'number_of_people' , 'number_of_children', 'pre_paid', 'total_payment')
    list_filter     = ['first_name']
    search_fields   = ['first_name']


class TransactionAdmin(admin.ModelAdmin):
   
    fieldsets = [
        
        ('transaction details',   {'fields': ['charge_id']}),
        (None,               {'fields': ['create_date']}),
        (None,               {'fields': ['amount']}),
        (None,               {'fields': ['token']}),
        (None,               {'fields': ['success']}),
    ]
    list_display    = ('id','charge_id', 'create_date', 'amount' ,'success')
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
       
        
    ]
    inlines         = [ClientsInline]
    list_display    = ('id','trip_type', 'trip_date', 'trip_time' ,'trip_guide' ,'status','create_date')
    list_filter     = ['trip_date']
    search_fields   = ['trip_text']
    actions         = ['track_trip']


class TripAvailabiltyAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['ava_trip_type']}),
        ('Date information', {'fields': ['ava_time']}),
        (None,               {'fields': ['ava_select_day']}),
        ('Date information', {'fields': ['ava_no_trip_day']}),
       
    ]
    list_display    = ('ava_trip_type', 'ava_time','ava_select_day','ava_no_trip_day')
    list_filter     = ['ava_no_trip_day']
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
        (None,               {'fields': ['meetingPoint']}),
        (None,               {'fields': ['gettingThere']}),
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
