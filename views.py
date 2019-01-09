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
    return render(request, 'tour/index.html', {'page_title':'home', 
                                                  'ourTours':OurToursQuery,
                                                  'reviewes':reviewesQuery})
    
     

def team(request):
    """
    Show home page
    """
    teamQuery = Guide.objects.filter(confirm=True)
    logger.info('team page')
    return render(request, 'tour/team.html', {'page_title':'team','guides' : teamQuery})

def gallery(request):
    """
    Show the gallery page
    """
    galleryQuery = Gallery.objects.all()
    logger.info('gallery page')
    return render(request, 'tour/gallery.html', {'page_title':'gallery', 'images':galleryQuery})

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
    reviewesQuery = Review.objects.filter(confirm=True).order_by('create_date')
    return render(request, 'tour/reviewes.html', {'page_title':'reviewes', 
                                                  'reviewes':reviewesQuery})
def ourTours(request):
    """
    Show home reviewes
    """
    OurToursQuery = OurTours.objects.filter(confirm=True)
   
    return render(request, 'tour/our_tours.html', {'page_title':'Tours', 
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
    return render(request, 'tour/calendar.html', {'page_title':'calendar','newCalendar':newCalendar,'ourTour':OurTour})

    

def booking(request, pYear, pMonth, pDay, pHour, tripType):

    
    # If this is a POST request then process the Form data
    #TyprDict = {'F': 'הרשמה לסיור משפחות', 'C': 'הרשמה לסיור קלאסי', 'B': 'הרשמה לאוטובוס'}
    # Britng the trip name in hebrew from db
    TripTypeQuery = OurTours.objects.filter(trip_type=tripType)
    title =  TripTypeQuery[0].title
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
                emailSuccess = tour_emails.send_email(msg_html=msg_html, msg_plain=msg_plain, email=email, title=emailTitle, cc=['yael.gati@cambridgeinhebrew.com','yrimon@gmail.com'])
            except:
                print('Got an error...')
            #print(f'Debug {emailSuccess}')
            return render(request, 'tour/success.html', {'title':'success', 'page_title':'success', 'trip_date':trip_date.strftime("%d-%m-%Y"), 'trip_time':trip_time.strftime("%H:%M"), 'deposit':deposit, 'more_to_pay':more_to_pay, 'id': transaction.id, 'trip_type':title, 'first':first_name, 'last':last_name })
           

    # If this is a GET (or any other method) create the default form.
   # TODO, Double check date as avialable one, or already has a trip on that day. 
    proposed_date = datetime.datetime(pYear, pMonth, pDay, pHour)
    form = Booking1Form(initial={'trip_date': proposed_date.date, 'trip_time':  proposed_date.time, 'trip_type':tripType})
        
    tripdate = proposed_date.strftime("%d.%m.%Y") + ' (' +  ' יום '  +  hebdaydic[proposed_date.strftime("%a")] + ')'     
    triptime = proposed_date.strftime("%H:%M") 
    
    return render(request, 'tour/booking.html', {'title':title, 'page_title' : 'Booking', 'form': form, 'tripdate': tripdate, 'triptime': triptime})




def contactUs(request ):
    print('Hello')
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        form = ContactForm(request.POST)
        # Check if the form is valid:
        print(form)
        print(form.is_valid())
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
                emailSuccess = tour_emails.send_email(msg_html=msg_html, msg_plain=msg_plain, email='yael.gati@cambridgeinhebrew.com', title=emailTitle, cc=['yael.gati@cambridgeinhebrew.com'])
            except:
                print('Got an error...')
            # Save contact here
            return render(request, 'tour/contact_saved.html', {'title':'contact', 'page_title':'contact', 'id': contact.id})

    # If this is a GET (or any other method) create the default form.
   # TODO, Double check date as avialable one, or already has a trip on that day. 
    
    form = ContactForm()
        
    return render(request, 'tour/contact.html', {'title':'Contact', 'page_title' : 'Contact', 'form': form})

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
             
            return render(request, 'tour/review_saved.html', {'title':'Give Review', 'page_title':'Give Review'})

    # If this is a GET (or any other method) create the default form.
   # TODO, Double check date as avialable one, or already has a trip on that day. 
    
    form = ReviewForm()
        
    return render(request, 'tour/give_review.html', {'title':'Give Review', 'page_title' : 'Give Review', 'form': form})


def success (request):
    
   return render(request, 'tour/success.html', {'title':'success','page_title':'success'})


def failure (request):
    
   return render(request, 'tour/failure.html', {'title':'faiure','page_title':'failure'})





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


