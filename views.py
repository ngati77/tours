from django.shortcuts import render
from django.shortcuts import render_to_response

# Create your views here.
from django.http import HttpResponse

from django.views import generic


from django.utils import timezone

from .models import Trip, Clients, NewCalendar, Review, Gallery
from .models import OurTours, Guide, Transaction, Contact

from .tour_emails import tour_emails 
import datetime
from django.template.loader import render_to_string



from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from .forms import Booking1Form, ContactForm, ReviewForm

from django.contrib.auth.decorators import login_required


import stripe

from django.conf import settings
from django.contrib import messages

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)




#def index(request):
#    return HttpResponse("Hello, world. You're at the polls index.")
hebmonthdic = {'Jan': 'ינואר', 'Feb' : 'פברואר' , 'Mar' : 'מרץ', 'Apr': 'אפריל' , 'May' : 'מאי' , 'Jun' : 'יוני' , 'Jul' : 'יולי' , 'Aug' : 'אוגוסט' , 'Sep' : 'ספטמבר' , 'Oct' : 'אוקטובר' , 'Nov' : 'נובמבר' , 'Dec' : 'דצמבר' }

hebdaydic   = {'Sun': 'ראשון','Mon': 'שני','Tue': 'שלישי','Wed': 'רביעי','Thu': 'חמישי','Fri': 'שישי','Sat': 'שבת'}


        
def home(request):
    """
    Show home page
    """
    #return render(request, 'tour/index.html', {'page_title':'home'})

    OurToursQuery = OurTours.objects.filter(confirm=True).order_by('order')
    reviewesQuery = Review.objects.filter(confirm=True).order_by('create_date')[:3]
    logger.info('home page')
    meta_des_heb = "סיורים בקיימברידג' אנגליה, סיור בעיר יפיפיה מחוץ ללונדון. סיור חד יומי  "
    meta_des_en  = "Cambridge in hebrew - Guided tours in Hebrew. In the beautiful city Cambridge. This is a one day tour outside London "
    meta_des = meta_des_heb + meta_des_en
    meta_key_heb = "סיור קיימברידג' קימברידג' קמברידג' אנגליה מחוץ ללונדון  "
    meta_key_en  = "Cambridge hebrew Guided tours"
    meta_key     = meta_key_heb + meta_key_en
    return render(request, 'tour/index.html', {'page_title':"קיימברידג' - סיור בעברית מחוץ ללונדון", 
                                               'meta_des':meta_des,
                                               'meta_key':meta_key,
                                               'ourTours':OurToursQuery,
                                               'reviewes':reviewesQuery})

def team(request):
    """
    Show home page
    """
    teamQuery = Guide.objects.filter(confirm=True)
    logger.info('team page')
    meta_des_heb = "סיורים בקיימברידג' אנגליה - הצוות שלנו  "
    meta_des_en  = "Cambridge in hebrew - The team "
    meta_des = meta_des_heb + meta_des_en
    meta_key_heb = "סיור קיימברידג' קימברידג' קמברידג' הצוות  "
    meta_key_en  = "Cambridge hebrew Guided tours - Team"
    meta_key     = meta_key_heb + meta_key_en
    return render(request, 'tour/team.html', {'page_title':'מי אנחנו',
                                              'meta_des':meta_des,
                                              'meta_key':meta_key,
                                              'guides' : teamQuery})

def gallery(request):
    """
    Show the gallery page
    """
    galleryQuery = Gallery.objects.filter(confirm=True)
    logger.info('gallery page')
    meta_des_heb = "סיורים בקיימברידג' אנגליה - קיימברידג' בתמונות  "
    meta_des_en  = "Cambridge in hebrew -Beautiful cambridge in the pictures "
    meta_des = meta_des_heb + meta_des_en
    meta_key_heb = "תמונות קיימברידג' אנגליה  "
    meta_key_en  = "Beautiful Cambridge pictures"
    meta_key     = meta_key_heb + meta_key_en
    return render(request, 'tour/gallery.html', {'page_title':'גלריית תמונות',
                                                 'meta_des':meta_des,
                                                 'meta_key':meta_key,
                                                 'images':galleryQuery})

def reviewes_old(request):
    """
    Show home reviewes
    """
    reviewList = []
    review3List = []
    reviewesQuery = Review.objects.filter(confirm=True)
    for i, reviewEntry in enumerate(reviewesQuery):
        review3List.append(reviewEntry)
        
       
        if i%3==2:
            if i==2:
                first3 = review3List
            else:
                reviewList.append(review3List)
            review3List = []
    reviewList.append(review3List)    
    print (len(first3))    
    print (len(reviewList)) 
    return render(request, 'tour/reviewes.html', {'page_title':'reviewes', 
                                                  'first_review':first3, 'reviewes':reviewList})
def reviewes(request):
    """
    Show home reviewes
    """
    meta_des_heb = "סיורים בקיימברידג' אנגליה - ממליצים עליינו. חוות דעת ממטילים  "
    meta_des_en  = "Cambridge in hebrew - Reviewes. Our reputation  "
    meta_des = meta_des_heb + meta_des_en
    meta_key_heb = "מה חושבים עלינו המלצות  "
    meta_key_en  = "Reviewes reputation"
    meta_key     = meta_key_heb + meta_key_en
    reviewesQuery = Review.objects.filter(confirm=True).order_by('create_date')
    return render(request, 'tour/reviewes.html', {'page_title':'ממליצים עלינו', 
                                                   'meta_des':meta_des,
                                                 'meta_key':meta_key,
                                                  'reviewes':reviewesQuery})
def ourTours(request):
    """
    Show home reviewes
    """
    OurToursQuery = OurTours.objects.filter(confirm=True)
    meta_des_heb = "סיורים בקיימברידג' אנגליה - נטייל בשוק, נכנס לעיר עם אווירה של 800 שנה, נכנס לקולג'ים המפוארים, נבלה בשוק העתיק ועוד  "
    meta_des_en  = "Cambridge in hebrew - We will go back 800 years, visit in the magnificent colleges, and the old city market"
    meta_des = meta_des_heb + meta_des_en
    meta_key_heb = "קולג'ים קולג' קיימברידג' שוק "
    meta_key_en  = " cambridge college old market"
    meta_key     = meta_key_heb + meta_key_en
    return render(request, 'tour/our_tours.html', {'page_title':'הסיורים שלנו', 
                                                   'meta_des':meta_des,
                                                   'meta_key':meta_key,
                                                   
                                                  'ourTours':OurToursQuery})
    
    
    
def find_your_day(request, view):
    """
    Show calendar of events this month
    """
    today = datetime.date.today()
    #return calendar(request, lToday.year, lToday.month)
    return new_calendar_view(request=request,  pYear=today.year, pMonth=today.month, view=view)

  

def new_calendar_view(request, pYear, pMonth, view):
    """
    Show calendar of events this month
    """
   
    #return calendar(request, lToday.year, lToday.month)
    newCalendar= NewCalendar(request=request, year=pYear,  month=pMonth , view=view)
    if view == 'A':
        OurTour = ''
    else:
        OurToursQuery = OurTours.objects.filter(trip_type=view)
        if len(OurToursQuery)!=1:
            print('Raise exception')
        OurTour = OurToursQuery[0]
#    print(newCalendar)
    meta_des_heb = "סיורים בקיימברידג' אנגליה - נטייל בשוק, נכנס לעיר עם אווירה של 800 שנה, נכנס לקולג'ים המפוארים, נבלה בשוק העתיק ועוד  "
    meta_des_en  = "Cambridge in hebrew - We will go back 800 years, visit in the magnificent colleges, and the old city market"
    meta_des = meta_des_heb + meta_des_en
    meta_key_heb = "קולג'ים קולג' קיימברידג' שוק "
    meta_key_en  = " cambridge college old market"
    meta_key     = meta_key_heb + meta_key_en
    return render(request, 'tour/calendar.html', {'page_title':OurTour.title,
                                                   'meta_des':meta_des,
                                                   'meta_key':meta_key,
                                                  'newCalendar':newCalendar,'ourTour':OurTour})

    

def booking(request, pYear, pMonth, pDay, pHour, tripType):

    
    # If this is a POST request then process the Form data
    #TyprDict = {'F': 'הרשמה לסיור משפחות', 'C': 'הרשמה לסיור קלאסי', 'B': 'הרשמה לאוטובוס'}
    # Britng the trip name in hebrew from db
    TripTypeQuery = OurTours.objects.filter(trip_type=tripType)
    title   =  TripTypeQuery[0].title
    deposit =  TripTypeQuery[0].deposit
    price =  TripTypeQuery[0].price
    priceChild =  TripTypeQuery[0].priceChild
    print_child = (TripTypeQuery[0].priceChild) > 0
    #title = TyprDict[tripType]
    stripe.api_key = settings.STRIPE_SECRET_KEY
   
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        form = Booking1Form(request.POST)
        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            #book_inst.due_back = form.cleaned_data['renewal_date']
           # Get all infortamtion from form
            trip_date, trip_time, first_name, last_name, phone, email, number_audlts, number_child, deposit, paymentSum = form.get_data()
            
            #trip_date = datetime.datetime(pYear, pMonth, pDay, pHour)
            # Check iftrip exists
           
            
            try:
                token = request.POST['stripeToken']
                charge = stripe.Charge.create(
                    amount=deposit*100,
                    currency='gbp',
                    description='Advance payment',
                    source=token,
                    receipt_email = email,
                )
            except stripe.error.CardError as e:
                messages.info(request, "Your card has been declined.")
                return render(request, 'tour/failure.html', {'title':'failure', 'page_title':'failure'})
            
            # Create ne trip
            tripQuerySet = Trip.get_event(trip_date)
            if (len(tripQuerySet)==0):
                trip = Trip(trip_text='', trip_date=trip_date, trip_time=trip_time ,trip_type=tripType)
                trip.save()
            else:
                trip = tripQuerySet[0]
            
            # Create new client           
            client = Clients(trip=trip,first_name=first_name,last_name=last_name, phone_number=phone, email=email, number_of_people=number_audlts, number_of_children=number_child, pre_paid = deposit, total_payment = paymentSum)
            client.save()
            # create a transaction
            transaction = Transaction(client=client,
                            token=token, 
                            charge_id = charge.id,
                            amount=deposit,
                            success=True)
            # save the transcation (otherwise doesn't exist)
            transaction.save()
            
            # redirect to a new URL:
            #print("Added new client")
            #return HttpResponseRedirect(reverse('all-borrowed') )
            #sg_plain = render_to_string('templates/email.txt', {'some_params': some_params})
            msg_plain= 'DUMMY ONE'
            children = (client.number_of_children > 0)
            more_to_pay=(paymentSum-deposit)
            try:
                msg_html = render_to_string('emails/email_success.html', {'trip_date':trip_date.strftime("%d-%m-%Y"), 'trip_time':trip_time.strftime("%H:%M"), 'id': transaction.id, 'trip_type':title, 'client':client, 'print_children':children, 'more_to_pay':more_to_pay})
                #emailSuccess = tour_emails.send_success(trip_date=trip_date.strftime("%d-%m-%Y"), trip_time=trip_time.strftime("%H:%M"), deposit=deposit, more_to_pay=(paymentSum-deposit), idx=transaction.id, trip_type=tripType,first=first_name, last=last_name)
                emailTitle = "סיור בקיימברידג' - אישור הזמנה"
                #cc =['yael.gati@cambridgeinhebrew.com']
                emailSuccess = tour_emails.send_email(msg_html=msg_html, msg_plain=msg_plain, to=[email], title=emailTitle, cc=settings.CC_EMAIL)
            except:
                print('Got an error...')
            #print(f'Debug {emailSuccess}')
            meta_des_heb = "סיורים בקיימברידג' אנגליה - ההרשמה לסיור הסתיימה בהצלחה  "
            meta_des_en  = ""
            meta_des = meta_des_heb + meta_des_en
            meta_key_heb = "הרשמה הצלחה "
            meta_key_en  = " "
            meta_key     = meta_key_heb + meta_key_en
            return render(request, 'tour/success.html', {'title':'success', 'page_title':'ההרשמה הסתיימה בהצלחה', 
                                                          'meta_des':meta_des,
                                                          'meta_key':meta_key,
                                                         'trip_date':trip_date.strftime("%d-%m-%Y"), 'trip_time':trip_time.strftime("%H:%M"), 'deposit':deposit, 'more_to_pay':more_to_pay, 'id': transaction.id, 'trip_type':title, 'first':first_name, 'last': last_name })
           

    # If this is a GET (or any other method) create the default form.
   # TODO, Double check date as avialable one, or already has a trip on that day. 
    proposed_date = datetime.datetime(pYear, pMonth, pDay, pHour)
    form = Booking1Form(initial={'trip_date': proposed_date.date, 'trip_time':  proposed_date.time, 'trip_type':tripType,  'price':price, 'priceChild':priceChild, 'deposit':deposit})
        
    tripdate = proposed_date.strftime("%d.%m.%Y") + ' (' +  ' יום '  +  hebdaydic[proposed_date.strftime("%a")] + ')'     
    triptime = proposed_date.strftime("%H:%M") 
    
    pageTitle=  'הזמנת ' +  title 
    meta_des_heb = "הזמנת סיור בקיימברידג בעברית  "
    meta_des_en  = "book your tour in Hebrew in Cambridge UK"
    meta_des = meta_des_heb + meta_des_en
    meta_key_heb = "הזמנת סיור עברית קיימברידג' "
    meta_key_en  = "book tour cambridge hebrew "
    meta_key     = meta_key_heb + meta_key_en
    return render(request, 'tour/booking.html', {'title':title, 'page_title' : pageTitle,
                                                  'meta_des':meta_des,
                                                  'meta_key':meta_key,
                                                 'form': form, 
                                                 'tripdate': tripdate, 
                                                 'triptime': triptime, 
                                                 'price':price, 
                                                 'priceChild':priceChild, 
                                                 'deposit':deposit, 
                                                 'print_child': print_child})




def contactUs(request ):
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        form = ContactForm(request.POST)
        # Check if the form is valid:
        if form.is_valid():
            
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            #book_inst.due_back = form.cleaned_data['renewal_date']
           # Get all infortamtion from form
            first_name, last_name,  email, text = form.get_data()
            
            contact = Contact(first_name=first_name, last_name = last_name, email = email, text = text)
            contact.save()
            try:
                msg_html = render_to_string('emails/email_contact.html', {'first_name':first_name,'last_name':last_name, 'email':email, 'id': contact.id, 'text':text})
                msg_plain = str(contact.id) + "מישהו יצר קשר פניה "#emailSuccess = tour_emails.send_success(trip_date=trip_date.strftime("%d-%m-%Y"), trip_time=trip_time.strftime("%H:%M"), deposit=deposit, more_to_pay=(paymentSum-deposit), idx=transaction.id, trip_type=tripType,first=first_name, last=last_name)
                emailTitle = "מישהו יצר קשר"
                emailSuccess = tour_emails.send_email(msg_html=msg_html, msg_plain=msg_plain, to=[settings.EMAIL_YAEL], title=emailTitle, cc=settings.CC_EMAIL)
            except:
                print('Got an error...')
            # Save contact here
            meta_des_heb = "קיימברידג בעברית צור קשר  "
            meta_des_en  = "contact Cambridge in Hebrew"
            meta_des = meta_des_heb + meta_des_en
            meta_key_heb = "צור קשר קיימברידג' "
            meta_key_en  = "contact cambridge hebrew "
            meta_key     = meta_key_heb + meta_key_en
            return render(request, 'tour/contact_saved.html', {'title':'contact', 
                                                               'meta_des':meta_des,
                                                               'meta_key':meta_key,
                                                               'page_title':'נחזור אלייך בהקדם', 
                                                               'id': contact.id})

    # If this is a GET (or any other method) create the default form.
   # TODO, Double check date as avialable one, or already has a trip on that day. 
    
    form = ContactForm()
    meta_des_heb = "קיימברידג בעברית צור קשר  "
    meta_des_en  = "contact Cambridge in Hebrew"
    meta_des = meta_des_heb + meta_des_en
    meta_key_heb = "צור קשר קיימברידג' "
    meta_key_en  = "contact cambridge hebrew "
    meta_key     = meta_key_heb + meta_key_en    
    return render(request, 'tour/contact.html', {'title':'Contact', 
                                                 'page_title' : 'צור קשר', 
                                                  'meta_des':meta_des,
                                                  'meta_key':meta_key,
                                                  'form': form})

def GiveReview(request ):

    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        form = ReviewForm(request.POST)
        # We get field called 'rating' a number from 1 to 10
        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            #book_inst.due_back = form.cleaned_data['renewal_date']
           # Get all infortamtion from form
            first_name, review_title, text  = form.get_data()
           # contact = Contact(first_name=first_name, last_name = last_name, email = email, text = text)
           # contact.save()
           
            review = Review(first_name=first_name, title=review_title, review_text = text)
            review.save()
            # Save contact here
            meta_des_en  = "write a review for Cambridge in hebrew"
            meta_des = meta_des_heb + meta_des_en
            meta_key_heb = "משוב קיימברידג' "
            meta_key_en  = "review Cambridge hebrew "
            meta_key     = meta_key_heb + meta_key_en   
            return render(request, 'tour/review_saved.html', {'title':'Give Review', 
                                                               'meta_des':meta_des,
                                                               'meta_key':meta_key,
                                                               'page_title':'תודה על המשוב'})

    # If this is a GET (or any other method) create the default form.
   # TODO, Double check date as avialable one, or already has a trip on that day. 
    
    form = ReviewForm()
    meta_des_heb = "תן לנו משוב  "
    meta_des_en  = "write a review for Cambridge in hebrew"
    meta_des = meta_des_heb + meta_des_en
    meta_key_heb = "משוב קיימברידג' "
    meta_key_en  = "review Cambridge hebrew "
    meta_key     = meta_key_heb + meta_key_en        
    return render(request, 'tour/give_review.html', {'title':'Give Review',
                                                     'page_title' : 'תן לנו משוב',
                                                     'meta_des':meta_des,
                                                     'meta_key':meta_key,
                                                     'form': form})


def success (request):
    meta_des_heb = "ההרשמה הסתיימה בהצלחה  "
    meta_des_en  = "Booking confirmed"
    meta_des = meta_des_heb + meta_des_en
    meta_key_heb = "ההזמנה הסתיימה קיימברידג' "
    meta_key_en  = "booking success Cambridge hebrew "
    meta_key     = meta_key_heb + meta_key_en  
    return render(request, 'tour/success.html', {'title':'success',
                                                'meta_des':meta_des,
                                                'meta_key':meta_key,
                                                'page_title':'ההרשמה הצליחה'})


def failure (request):
    meta_des_heb = "ההרשמה נכשלה  "
    meta_des_en  = "Booking failed"
    meta_des = meta_des_heb + meta_des_en
    meta_key_heb = "ההזמנה נכשלה קיימברידג' "
    meta_key_en  = "booking failed Cambridge hebrew "
    meta_key     = meta_key_heb + meta_key_en 
    return render(request, 'tour/failure.html', {'title':'faiure',
                                                'meta_des':meta_des,
                                                'meta_key':meta_key,
                                                'page_title':'ההרשמה נכשלה'})





class GuideView(generic.ListView):
    template_name = 'tour/guide_view.html'
    context_object_name = 'latest_trip_list'

    #def get_queryset(self):
    """
    Return the last five published questions (not including those set to be
    published in the future).
    """
        
        
        
    def get_queryset(self):
        filter_val = self.request.GET.get('filter', timezone.now())
        order = self.request.GET.get('orderby', 'trip_date')
        new_context = Trip.objects.filter(
                trip_date__gte=filter_val,
                ).order_by(order)
        return new_context

    def get_context_data(self, **kwargs):
        context = super(GuideView, self).get_context_data(**kwargs)
        context['filter'] = self.request.GET.get('filter', timezone.now())
        context['orderby'] = self.request.GET.get('orderby','trip_date')
        return context
 
class ClientView(generic.DetailView):
    template_name = 'tour/clients_view.html'
    model = Trip


