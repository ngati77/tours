from django.db import models
import datetime
from django.utils import timezone
from django.db.models import Q






TRIP_DAYS = (
    ('Non', 'None'),    
    ('Sun', 'ראשון'),  
    ('Mon', 'שני'),  
    ('Tue', 'שלישי'),  
    ('Wed', 'רביעי'),  
    ('Thu', 'חמישי'),  
    ('Fri', 'שישי'),  
    ('Sat', 'שבת'), 
    ('All', 'כל יום'), 
)

TRIP_GUIDE = (
    ('PE', 'Pending'),
    ('YR', 'YaelR'),
    ('GS', 'Gui'),
    ('YG', 'YaelG'),
)

TRIP_TYPE = (
        ('C', 'Classic'),
        ('F', 'Family'),
        ('W', 'Winter'),
        ('B', 'Bus'),
        ('P', 'Punting'),
        ('A', 'All'),
        )
#TRIP_TYPE_HEB = {'C': 'סיור קלאסי','F': 'סיור משפחות','B': 'אוטובוס מלונדון','P': 'סיור פרטי'} 

STATUS_TRIP = (
    ('n', 'New'),
    ('a', 'Confirmed'),
    ('b', 'Canceled'),
    ('d', 'Done'),
    ('e', 'Completed'),
)

hebmonthdic = {'Jan': 'ינואר', 'Feb' : 'פברואר' , 'Mar' : 'מרץ', 'Apr': 'אפריל' , 'May' : 'מאי' , 'Jun' : 'יוני' , 'Jul' : 'יולי' , 'Aug' : 'אוגוסט' , 'Sep' : 'ספטמבר' , 'Oct' : 'אוקטובר' , 'Nov' : 'נובמבר' , 'Dec' : 'דצמבר' }

class Guide(models.Model):
    first_name         = models.CharField(max_length=20)
    last_name          = models.CharField(max_length=20)
    image              = models.ImageField(blank = True, null = True, upload_to = 'Guide/%Y/%m/')
    order              = models.IntegerField(default=0)
    general_info       = models.TextField(max_length=600)
    confirm            = models.BooleanField(default=True)

class Guide_Background(models.Model):
    question       = models.TextField(max_length=600)
    answer         = models.TextField(max_length=600)
    trip           = models.ForeignKey(Guide, on_delete=models.CASCADE)
    
    

class TripAvailabilty(models.Model):
    ava_trip_type   = models.CharField(
        max_length=1,
        choices=TRIP_TYPE,
        default='C',
    )
    ava_select_day   = models.CharField(
        max_length=3,
        choices=TRIP_DAYS,
        default='Non',
    )
    ava_time = models.TimeField('If every day trip enter time', blank=True, null=True)

    ava_no_trip_day  = models.DateTimeField('Cancel trip option on this day',blank=True, null=True)
    
              
        
class GuideVacation(models.Model):
    
    guide_vacation = models.CharField(
        max_length=2,
        choices=TRIP_GUIDE,
        default='YR',
    )
    vac_start_date    = models.DateField('First day guide on holiday') 
    vac_end_date      = models.DateField('Last day guide on holiday') 
    vac_cancel_classy = models.BooleanField(default=False)
    vac_cancel_family = models.BooleanField(default=False)
    vac_cancel_all    = models.BooleanField(default=False)


class Review(models.Model):
   
    first_name       = models.CharField(max_length=200)
    
    title            = models.CharField(max_length=200)
    review_text      = models.TextField(max_length=600)
    
    create_date      = models.DateTimeField(default=timezone.now)
    confirm          = models.BooleanField(default=False)
    
class OurTours(models.Model):

    title              = models.CharField(max_length=200)
    headerShort1       = models.CharField(max_length=200)
    descriptionShort1  = models.TextField(max_length=600)
    whoCanDoIt         = models.CharField(max_length=200)

    description1       = models.TextField(max_length=600)
    description2       = models.TextField(max_length=600)
    description3       = models.TextField(max_length=600)
    duration           = models.TextField(max_length=200)
    price              = models.IntegerField(default=0)
    priceChild         = models.IntegerField(default=0)
    deposit            = models.IntegerField(default=0)
    img                = models.ImageField(blank = True, null = True, upload_to = 'Tours/%Y/%m/')
    confirm            = models.BooleanField(default=False)
    trip_type          = models.CharField(
                                        max_length=1,
                                        choices=TRIP_TYPE,
                                        default='C',
                                        )
    order              = models.IntegerField(default=0)
    
   
    
class Gallery(models.Model):
    img                = models.ImageField(blank = True, null = True, upload_to = 'Gallery/%Y/%m/')
    title              = models.CharField(max_length=200)
    text               = models.TextField(max_length=600)
    confirm            = models.BooleanField(default=True)
    

class Trip(models.Model):
    '''
    This class hold the information regarding Tour date, time and the guide.
    Clients will be refernce to those trips
    '''
    trip_text   = models.CharField(max_length=200, blank=True)
    trip_date   = models.DateField('Tour date')
    trip_time   = models.TimeField('Tour time', blank=True)
    create_date = models.DateTimeField(default=timezone.now)
    
    
    
    trip_type   = models.CharField(
        max_length=1,
        choices=TRIP_TYPE,
        default='C',
    )
    
    trip_guide = models.CharField(
        max_length=2,
        choices=TRIP_GUIDE,
        default='YR',
    )
    
    status = models.CharField(
            max_length=1, 
            choices=STATUS_TRIP,
            default='n',
            )
    
    def __str__(self):
        print('Trip indo')
        print('Trip date: ')
        print(self.trip_date)
        print('Trip time: ')
        print(self.trip_time)
        print(type(self.trip_time))
        return self.trip_text
    
    
 
    def nearby_trips(self, date):
        # now = timezone.now()
        if (( date - datetime.timedelta(days=1) <= self.trip_date) and
        ( date + datetime.timedelta(days=1) >= self.trip_date )):
            return True
        else:
            return False
    @staticmethod
    def get_event(date):
        return Trip.objects.filter(trip_date=date)
     
    #was_published_recently.admin_order_field = 'pub_date'
    #was_published_recently.boolean = True
    #was_published_recently.short_description = 'Published recently?'
   
class Clients(models.Model):
    '''
    This class hold the information regarding clients it has a pointer to Trip 
    object. It holds the details of number of people, children and email.  
    '''
    STATUS_CLIENT = (
    ('a', 'Confirmed'),
    ('b', 'Canceled'),
    ('c', 'Canceled and refund'),
)
    trip             = models.ForeignKey(Trip, on_delete=models.CASCADE)
    first_name       = models.CharField(max_length=200)
    last_name        = models.CharField(max_length=200)
    phone_number     = models.CharField(max_length=20) 
    email            = models.EmailField(blank=True, default="")
    number_of_people = models.IntegerField(default=0)
    number_of_children = models.IntegerField(default=0)
    total_payment      = models.IntegerField(default=0)
    pre_paid           = models.IntegerField(default=0)
    create_date        = models.DateTimeField(default=timezone.now)
    confirm_use        = models.BooleanField(default=False)
    send_emails        = models.BooleanField(default=False)
    status             = models.CharField(
                                        max_length=1,
                                        choices=STATUS_CLIENT,
                                        default='a',
                                        )
    
    #create_date      = models.DateTimeField('date create')
    
    def __str__(self):
        return self.first_name
    
# create a transaction
class Transaction(models.Model):
    client            =  models.ForeignKey(Clients, on_delete=models.CASCADE)
    create_date       =  models.DateTimeField(default=timezone.now)
    token             =  models.CharField(max_length=200)
    amount            =  models.IntegerField(default=0)
    charge_id         =  models.CharField(max_length=200)
    success           =  models.BooleanField(default=True)
    
    def __str__(self):
        return str(self.client_id)

  
                
class Contact(models.Model):
    '''
    This class hold the information regarding contact
    '''
    create_date      = models.DateTimeField(default=timezone.now)
    first_name       = models.CharField(max_length=200)
    last_name        = models.CharField(max_length=200)
    email            = models.EmailField(blank=True, default="")
    text             = models.TextField(max_length=600)
    confirm          = models.BooleanField(default=False)
    
    #create_date      = models.DateTimeField('date create')

class Calendar:
    
    def __init__(self, request, year, month, view):
        daydict = {'Sun':1, 'Mon':2, 'Tue':3, 'Wed':4, 'Thu':5, 'Fri':6, 'Sat':7}
        
        dayInCalendar = []
        self.Pack7Days     = []
        monthCount = 'PrevMonth';
        
        today           = datetime.datetime.now()
        today           = datetime.date(today.year,today.month,today.day)
        firstDayOfMonth = datetime.date(year, month, 1)
        self.monthStr        = hebmonthdic[firstDayOfMonth.strftime("%b")]
        self.yearStr         = str(firstDayOfMonth.year)
        self.view            = view
            
        # Find the last day of the month,
        # If Decmber than moving to the next year
        if (month == 12):
            firstDayOfNextMonth = datetime.date(year+1, 1, 1);
        else:
            firstDayOfNextMonth = datetime.date(year, month+1, 1);
        lastDayInMonth = firstDayOfNextMonth - datetime.timedelta(days=1)
        # use firstDayOfNextMonth as href to move to the nextmont
        self.nextMonth      = firstDayOfNextMonth.month
        self.nextMonthYear  = firstDayOfNextMonth.year
        
        self.thisYear       = today.year
        self.thisMonth      = today.month
        
        # Find the last day ofthe previous month
        LastDayInPrevMonth  = firstDayOfMonth - datetime.timedelta(days=1)
        # Subtract how many days from previous month we need to use 
        self.prevMonth      = LastDayInPrevMonth.month
        self.prevMonthYear  = LastDayInPrevMonth.year
        
        #Start from previous month
        dayCount = LastDayInPrevMonth.day - daydict[firstDayOfMonth.strftime("%a")] + 2
        _month =   LastDayInPrevMonth.month
        _year  =   1977
        
        for i in range (1,43):
            # Moving to current month
            if (i==daydict[firstDayOfMonth.strftime("%a")]):
                monthCount = 'thisMonth'
                dayCount =1
                _month =   month
                _year  =   year
            # Endsup with next month
            elif (dayCount==(lastDayInMonth.day+1) and monthCount== 'thisMonth' ):
                monthCount = 'nextMonth'
                dayCount =1
                _month =   self.nextMonth
                _year  =   1977
            
            dayInMonth = datetime.date(_year, _month, dayCount)
                
            dayInCalendar.append(DayInCalendar(request=request, dateInCalendar=dayInMonth, today= today, view=view))
            
            # Every 7 days pack in new list, and also revered the order to be from right to left for the hebrew calendar
            if (i%7==0):
                if (monthCount == 'nextMonth') and (dayCount >6):
                    pass
                else:
                    self.Pack7Days.append(dayInCalendar)  
                    dayInCalendar = []
            # Increment counter if we have started counting
            dayCount += 1
                
    def __str__(self):
        
        for day7 in self.Pack7Days.dayInCalendar:
            for day in day7:
                print('fill: ' + day.fill)
                print('dayNumStr: ' + day.dayNumStr)
        
        return 'Here is my calendatr:'
                

class DayInCalendar:
    
    def __init__(self, request, dateInCalendar, today, view):
        self.events=[]
        hebdict = {'Sun':'ראשון', 'Mon':'שני', 'Tue':'שלישי', 'Wed':'רביעי', 'Thu':'חמישי', 'Fri':'שישי', 'Sat':'שבת'}
        
        self.year  = dateInCalendar.year
        self.month = dateInCalendar.month
        self.day   = dateInCalendar.day 
        
        # If client then bring the relevant day of avliable tours
        # Remove days were guide is on vacation and tour isn't possible
        
        if (dateInCalendar < today):
            self.fill =    ""
        elif (dateInCalendar == today):
           self.fill =    "active"
        else:
           self.fill =    ""
        
#        if (dateInCalendar.day==1):
#            self.dayNumStr     =  str(dateInCalendar.day) + '    .....   ' + hebmonthdic[dateInCalendar.strftime("%b")]
#        else:
        if self.year == 1977:
            self.dayNumStr     =  ""
        else:
            self.dayNumStr     =  str(dateInCalendar.day)
            
        # Querey guide holiday
        guideVacationQuery   = GuideVacation.objects.filter(vac_start_date__lte=dateInCalendar,
                                                        vac_end_date__gte=dateInCalendar) 
        self.attr = False
        self.vac = False
        
        if (request.user.is_authenticated and view == 'A'):
#        if (False):
            # If user then bring relevant data of:
            # Planned trips for user
            # Days off for user
            tripQuery = Trip.objects.filter(trip_date=dateInCalendar)
            
            #for trip in tripQuery:
            #Check if we have a trip this day
            if len(tripQuery)>0:
            # Check for unconfirmed trips
                
                self.attr = True
                self.id   = dateInCalendar.strftime('%d_%m_%Y')
                self.id   += "-"+ tripQuery[0].trip_time.strftime('%H_%M')
            
            if len(guideVacationQuery)>0:
                self.vac = True
            # Now print day off    
#            for vac in guideVacationQuery:
#                attr = "event d-block p-1 pl-2 pr-2 mb-1 rounded text-truncate small bg-info text-white"
#                text  = 'Vaction ' + vac.guide_vacation
#                link  = None  
#                self.events.append(EventAttr(attr=attr, text=text, link=link, hour=11, trip_type='C', trip_id =1))
            
        
        elif (dateInCalendar > today):
            
            # Check specific day in the week
            availableDateQuery0     = TripAvailabilty.objects.filter(Q(ava_select_day    =   dateInCalendar.strftime('%a')))
            # Check for all days
            availableDateQuery1     = TripAvailabilty.objects.filter(Q(ava_select_day    =   'All'))
            availableDateQuery = availableDateQuery1 | availableDateQuery0
            
                   
            for tripAvailabilty in availableDateQuery:
                #print(tripAvailabilty.ava_trip_type)
                if (tripAvailabilty.ava_trip_type != 'A' and tripAvailabilty.ava_trip_type != view):
                    continue
                canceled = False
                # Check if the trip was canceld
                noneAvailableDateQuery = TripAvailabilty.objects.filter(ava_no_trip_day__year  = dateInCalendar.year,
                                                                        ava_no_trip_day__month = dateInCalendar.month,
                                                                        ava_no_trip_day__day   = dateInCalendar.day,
                                                                        ava_no_trip_day__hour  = tripAvailabilty.ava_time.hour
                                                                        )
                for noneAvailableDate in noneAvailableDateQuery:
                    #print(noneAvailableDate.ava_no_trip_day.strftime("%Y-%M-%D-%H"))
                    if noneAvailableDate.ava_trip_type == 'A' or noneAvailableDate.ava_trip_type == tripAvailabilty.ava_trip_type:
                        #print("TRUE")
                        # Break from nearset for
                        canceled = True
                        break
                # As it was canceled move to the next item in the lisy
                if (canceled):
                    continue
                
                for vac in guideVacationQuery:
                    if (vac.vac_cancel_all) or (vac.vac_cancel_family and view=='F') or (vac.vac_cancel_classy and view=='C'):
                        canceled = True
                        break
                # Guide on holiday there is no tour on this day
                if (canceled):
                    continue
                    
                # Check if their is already a different trip on this day, we don't want two trips on the same day
                tripQuery = Trip.objects.filter(trip_date__year  = dateInCalendar.year,
                                                trip_date__month = dateInCalendar.month,
                                                trip_date__day   = dateInCalendar.day,
                                                trip_time__hour  = tripAvailabilty.ava_time.hour,
                                                
                                                )
              
                # We found a trip let's check if it is a different one.
                for trip in tripQuery:
                    if (trip.trip_type != view):
                        canceled = True
                        break
                if (canceled):
                    continue
                    
                bg_color = 'bg-success'    
                #attr = "event d-block p-1 pl-2 pr-2 mb-1 rounded text-truncate small "+ bg_color + " text-white"
                self.attr = True
                self.id   = dateInCalendar.strftime('%d_%m_%Y')
                self.id   += "-"+ tripAvailabilty.ava_time.strftime('%H_%M')
                
            
                
                



    
    def __str__(self):
        return self.first_name
    

