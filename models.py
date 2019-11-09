from django.db import models
import datetime
from django.utils import timezone
from django.db.models import Q
from django.shortcuts import get_object_or_404

TRIP_DAYS = (
    ('Sun', 'ראשון'),  
    ('Mon', 'שני'),  
    ('Tue', 'שלישי'),  
    ('Wed', 'רביעי'),  
    ('Thu', 'חמישי'),  
    ('Fri', 'שישי'),  
    ('Sat', 'שבת'), 
    ('All', 'כל יום'), 
)

#TRIP_GUIDE = (
#    ('PE', 'Pending'),
#    ('YR', 'YaelR'),
#    ('GS', 'Gui'),
#    ('YG', 'YaelG'),
#)

#TRIP_TYPE = (
#        ('C', 'Classic'),
#        ('F', 'Family'),
#        ('W', 'Winter'),
#        ('B', 'Bus'),
#        ('P', 'Punting'),
#        ('A', 'All'),
#        ('E','Free'),
#        )
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
    first_name         = models.CharField(max_length=20, default="")
    last_name_en       = models.CharField(max_length=20, default="")
    first_name_en      = models.CharField(max_length=20, default="")
    last_name          = models.CharField(max_length=20, default="")
    user_name          = models.CharField(max_length=20, default="")
    phone              = models.CharField(max_length=20, default="")
    email              = models.EmailField(blank=True, default="")
    image              = models.ImageField(blank = True, null = True, upload_to = 'Guide/%Y/%m/')
    order              = models.IntegerField(default=0)
    general_info       = models.TextField(max_length=600)
    confirm            = models.BooleanField(default=True)

    def __str__(self):
        return self.user_name

class Guide_Background(models.Model):
    question       = models.TextField(max_length=600)
    answer         = models.TextField(max_length=600)
    trip           = models.ForeignKey(Guide, on_delete=models.CASCADE)
    
  
        



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
    #trip_type          = models.CharField(
    #                                    max_length=1,
    #                                    choices=TRIP_TYPE,
    #                                    default='C',
    #                                    )
    trip_abc_name     = models.CharField(max_length=20,default='Classic')

    order              = models.IntegerField(default=0)

    def __str__(self):
        return self.trip_abc_name
    
class GuideVacation(models.Model):
    guide           = models.ForeignKey(Guide,    on_delete=models.SET_NULL, blank=True, null=True)
    ourTour         = models.ForeignKey(OurTours, on_delete=models.SET_NULL,  blank=True, null=True)
    #guide_vacation = models.CharField(
    #    max_length=2,
    #    choices=TRIP_GUIDE,
    #    default='YR',
    #)
    vac_start_date    = models.DateField('First day guide on holiday',default=datetime.date.today) 
    vac_end_date      = models.DateField('Last day guide on holiday', default=datetime.date.today) 
    #vac_cancel_classy = models.BooleanField(default=False)
    #vac_cancel_family = models.BooleanField(default=False)
    vac_cancel_all    = models.BooleanField(default=False)    
   

class TripAvailabilty(models.Model):
    
    ourTour         = models.ForeignKey(OurTours, on_delete=models.SET_NULL,  blank=True, null=True)

    #ava_trip_type   = models.CharField(
    #    choices=TRIP_TYPE,
    ##    max_length=1,
    #    default='C',
    #)
    ava_select_day   = models.CharField(
        max_length=3,
        choices=TRIP_DAYS,
        default='All',
    )
    ava_time = models.TimeField('If every day trip enter time')


    ava_trip_start_day  = models.DateField('Start day',blank=True, null=True)
    ava_trip_end_day  = models.DateField('End day',blank=True, null=True)

                 
   
    
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
    trip_time   = models.TimeField('Tour time')
    create_date = models.DateTimeField(default=timezone.now)
    
    guide              = models.ForeignKey(Guide,    on_delete=models.SET_NULL, blank=True, null=True)
    ourTour            = models.ForeignKey(OurTours, on_delete=models.SET_NULL, blank=True, null=True)
    
    #trip_type   = models.CharField(
    #    max_length=1,
    #    choices=TRIP_TYPE,
    #    default='C',
    #)
    
    #trip_guide = models.CharField(
    #    max_length=2,
    #    choices=TRIP_GUIDE,
    #    default='YR',
    #)
    
    status = models.CharField(
            max_length=1, 
            choices=STATUS_TRIP,
            default='n',
            )
    total_payment      = models.IntegerField(default=0, blank=True, null=True)
    def __str__(self):
        return str(self.id)
    
    
 
    def nearby_trips(self, date):
        # now = timezone.now()
        if (( date - datetime.timedelta(days=1) <= self.trip_date) and
        ( date + datetime.timedelta(days=1) >= self.trip_date )):
            return True
        else:
            return False
        
    def get_trip_sum(self):
        '''
        This function summerise the total incomne of a trip
        
        '''
        #reportEntry = ReportEntry(self.ourTour.title, self.trip_date.strftime("%d.%m.%y"), self.guide.name())
        reportEntry = ReportEntry(self.ourTour.trip_abc_name, self.trip_date.strftime("%d.%m.%y"), self.guide.user_name)
        # Get all cilents from a trip hopefully more than one
        clientQuerey = self.clients_set.all()
        # Scan all clients, in the futrue need to scan the invoice
        reportEntry.trip_id         = self.id
        for client in clientQuerey:
            if client.status != 'a':
                continue
            reportEntry.total_people    += client.number_of_people
            reportEntry.total_children  += client.number_of_children
            reportEntry.total_deposit   += client.pre_paid
            reportEntry.total_gross     += client.total_payment
        
        # If it is a free tour, then the anount is in the trip total amount
        if (reportEntry.total_gross == 0):
            reportEntry.total_gross = self.total_payment
        # If Yael Gati is the guide for this tour. then we don't need to pay her!!!
        if (self.guide.user_name == 'yaelg'):
            reportEntry.total_guide_exp = 0
            reportEntry.total_neto      = reportEntry.total_gross - reportEntry.other_expense
            reportEntry.guide_payback = 0
        else:
            
            # How much the guide earn from this tour
            reportEntry.total_guide_exp = reportEntry.calc_guide_payment(
                                                                    adult     = reportEntry.total_people,
                                                                    children  = reportEntry.total_children,
                                                                    ourTour   = self.ourTour)
            # how much we earend
            reportEntry.total_neto      = reportEntry.total_gross - reportEntry.other_expense - reportEntry.total_guide_exp
            # Now that we know how much the guide earn we can calculate home amount he needs to return
            reportEntry.guide_payback   = reportEntry.total_neto - reportEntry.total_deposit
        
        
        
        return reportEntry
        
        
        
    @staticmethod
    def get_event(date,trip_abc_name):
        trip_abc_name
        ourTour = get_object_or_404(OurTours, trip_abc_name=trip_abc_name)

        return Trip.objects.filter(
                                ~Q(status='b'),
                                trip_date=date,
                                ourTour=ourTour)
     
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
    
    FOUND_US = (
    ('a', 'גוגל'),
    ('b', 'פייסבוק'),
    ('c', 'שאל לונדוני'),
    ('g', 'ארטנטיבי'),
    ('d', 'כתבה'),
    ('e', 'המלצה מחבר/ה'),
    ('f', 'אחר'),
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
    found_us             = models.CharField(
                                        max_length=1,
                                        choices=FOUND_US,
                                        default='f',
                                        )
    
    text                = models.TextField(max_length=600, blank=True)
    admin_comment       = models.TextField(max_length=120, blank=True)
    
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
    STATUS_MESSAGE = (
    ('n', 'New'),
    ('c', 'Confirmed'),
    ('d', 'Done'),
    )
    confirm             = models.CharField(
                                        max_length=1,
                                        choices=STATUS_MESSAGE,
                                        default='n',
                                        )

    
    #create_date      = models.DateTimeField('date create')


# This class is used in the report.html
class ReportEntry: 
    def __init__(self, trip_abc_name, trip_date, guide):
        self.trip_text   = trip_abc_name
        self.trip_date   = trip_date
        self.trip_guide  = guide

        self.trip_time       = ''
        self.trip_id         = 0
        self.total_people    = 0
        self.total_children  = 0

        self.total_deposit   = 0
        self.total_gross     = 0
        self.total_guide_exp = 0
        self.other_expense   = 0
        self.guide_payback   = 0
        self.total_neto      = 0
        
    """
    Return report between range of guides and according to the guide
    """
    # This function calculate how much money the guide owe the company
    def calc_guide_payment(self ,adult, children, ourTour):
        # Before calculating Guide salary check if children are paying

        # If it is a payed our then
        if ourTour.price > 0:
            ChildAccount    = ourTour.priceChild > 0
            # If children are account take the number of them otherwise set it to zero
            childNum        = children if ChildAccount else 0
            # Just add chidren to people
            totalPeople     = adult +  childNum
            # if more than 2 peole than we have extra to add
            extraPeople     = (totalPeople-2) if totalPeople > 2 else 0
            # Base amount 40 + 5 Pound per person
            return (40 + 5 * extraPeople)
        # It is a free tour, guide ge 50% with minimum of 40
        
        else:
            if (self.total_gross < 80):
                return 40
            else:
                return self.total_gross/2.0
            

    def __add__(self, reportEntry):
        '''
        New operator to add 
        '''
        self.total_people      += reportEntry.total_people
        self.total_children    += reportEntry.total_children
        self.total_deposit     += reportEntry.total_deposit
        self.total_gross       += reportEntry.total_gross
        self.guide_payback     += reportEntry.guide_payback   
        self.total_guide_exp   += reportEntry.total_guide_exp
        self.total_neto        += reportEntry.total_neto
        return self
        

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
        # Only gor Managment
        if (request.user.is_authenticated and view == 'All'):
#        if (False):
            # If user then bring relevant data of:
            # Planned trips for user
            # Days off for user
            tripQuery = Trip.objects.filter(trip_date=dateInCalendar)
            
            #for trip in tripQuery:
            #Check if we have a trip this day
            if len(tripQuery)>0:
            # Check for unconfirmed trips
                if (tripQuery[0].status  != 'b'):
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
            
            # Check specific day in the week (Sun/Mon/Tue/...)
            #availableDateQuery0     = TripAvailabilty.objects.filter(ava_select_day = dateInCalendar.strftime('%a'))
            # Check for all days
            #availableDateQuery1     = TripAvailabilty.objects.filter(ava_select_day    =   'All')
            #availableDateQuery2     = TripAvailabilty.objects.filter(ava_trip_day__lte =   dateInCalendar)
            #availableDateQuery      = availableDateQuery2 | availableDateQuery1 | availableDateQuery0
            
            # Bring all relevant tours
            availableDateQuery       = TripAvailabilty.objects.filter(ourTour__trip_abc_name = view)
            #print("view: " + view)       
            for tripAvailabilty in availableDateQuery:
                # Check if on the day we have either all tours or the specific tour that we need
                #if (tripAvailabilty.ourTour.trip_abc_name != view):
                #    #print("Skip this tour")
                #    continue

                # Check if start day is bigger than the day in the calendar
                if (tripAvailabilty.ava_trip_start_day != None and tripAvailabilty.ava_trip_start_day > dateInCalendar ):
                    continue
                # Check if end day is smaller than the day in the calendar
                if (tripAvailabilty.ava_trip_end_day != None and tripAvailabilty.ava_trip_end_day < dateInCalendar ):
                    continue
                # Now that we know trip is in the right dates, check if it run every day or on a prticular day
                if (tripAvailabilty.ava_select_day != 'All' and tripAvailabilty.ava_select_day != dateInCalendar.strftime('%a') ):
                    continue

                canceled = False
                

                for vac in guideVacationQuery:                     
                    if ((vac.vac_cancel_all) or (vac.ourTour != None and vac.ourTour.trip_abc_name == view)):
                        canceled = True
                        break
                # Guide on holiday there is no tour on this day
                if (canceled):
                    #print("Skip this tour no guides")
                    continue
                    
                # Check if their is already a different trip on this day, we don't want two trips on the same day
                tripQuery = Trip.objects.filter(trip_date__year  = dateInCalendar.year,
                                                trip_date__month = dateInCalendar.month,
                                                trip_date__day   = dateInCalendar.day,
                                                trip_time__hour  = tripAvailabilty.ava_time.hour,
                                                trip_time__minute  = tripAvailabilty.ava_time.minute,
                                                trip_time__second  = tripAvailabilty.ava_time.second
                                                
                                                )
                # We found a trip let's check if it is a different one.
                for trip in tripQuery:
                    #print("trip type: "+ trip.get_trip_type_display())
                    #print("view2 : "+ view)
                    if (trip.status  != 'b' and trip.ourTour.trip_abc_name != view):
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
    

