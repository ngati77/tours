from django.shortcuts import render
from django.shortcuts import render_to_response

# Create your views here.
from django.http import HttpResponse

from django.views import generic


from django.utils import timezone

from .models import Trip, Clients, Review, Gallery, Calendar, ReportEntry,ClientReportEntry
from .models import OurTours, Guide, Transaction, Contact, GuideVacation, FoundUs

from .tour_emails import tour_emails 
import datetime
from django.template.loader import render_to_string



from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse

from .forms import BookingForm, ContactForm, ReviewForm, ReportForm, PaymentForm

from django.contrib.auth.decorators import login_required


import stripe

from django.conf import settings
from django.contrib import messages

from .render import Render
# import the logging library
import logging

from threading import Thread, activeCount

from django.db.models import Q


# Get an instance of a logger
logger = logging.getLogger(__name__)




#def index(request):
#    return HttpResponse("Hello, world. You're at the polls index.")
#hebmonthdic = {'Jan': 'ינואר', 'Feb' : 'פברואר' , 'Mar' : 'מרץ', 'Apr': 'אפריל' , 'May' : 'מאי' , 'Jun' : 'יוני' , 'Jul' : 'יולי' , 'Aug' : 'אוגוסט' , 'Sep' : 'ספטמבר' , 'Oct' : 'אוקטובר' , 'Nov' : 'נובמבר' , 'Dec' : 'דצמבר' }

monthStr = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul' , 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

hebdict = {'Sun':'ראשון', 'Mon':'שני', 'Tue':'שלישי', 'Wed':'רביעי', 'Thu':'חמישי', 'Fri':'שישי', 'Sat':'שבת'}


#hebdaydic   = {'Sun': 'ראשון','Mon': 'שני','Tue': 'שלישי','Wed': 'רביעי','Thu': 'חמישי','Fri': 'שישי','Sat': 'שבת'}
        
def home(request):
    """
    Show home page
    """
    #return render(request, 'tour/index.html', {'page_title':'home'})

    OurToursQuery = OurTours.objects.filter(confirm=True).order_by('order')
    reviewesQuery = Review.objects.filter(confirm=True).order_by('-create_date')[:5]
    logger.info('home page')
    meta_des_heb = "סיורים בקיימברידג' אנגליה, סיור בעיר יפיפיה מחוץ ללונדון. סיור חד יומי  "
    meta_des_en  = "Cambridge in hebrew - Guided tours in Hebrew. In the beautiful city Cambridge. This is a one day tour outside London "
    meta_des = meta_des_heb + meta_des_en
    meta_key_heb = "סיור קיימברידג' קימברידג' קמברידג' אנגליה מחוץ ללונדון  "
    meta_key_en  = "Cambridge hebrew Guided tours"
    meta_key     = meta_key_heb + meta_key_en
    return render(request, 'tour/index.html', {'page_title':"Cambridge In Hebrew טיול בקיימברידג", 
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
    meta_des_heb = "טיול בקיימברידג' אנגליה - הצוות שלנו  "
    meta_des_en  = "Cambridge in hebrew - The team "
    meta_des = meta_des_heb + meta_des_en
    meta_key_heb = "טיול קיימברידג' קימברידג' קמברידג' הצוות  "
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
    return render(request, 'tour/gallery.html', {'page_title':'Tour Gallery',
                                                 'meta_des':meta_des,
                                                 'meta_key':meta_key,
                                                 'images':galleryQuery})


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
    reviewesQuery = Review.objects.filter(confirm=True).order_by('-create_date')
    return render(request, 'tour/reviewes.html', {'page_title':'ממליצים עלינו', 
                                                   'meta_des':meta_des,
                                                 'meta_key':meta_key,
                                                  'reviewes':reviewesQuery})

    
def create_new_trip_client(*args):
    ''' This function create trip if needed and create a client 
    '''
    title, trip_date, trip_time, trip_abc_name, first_name, last_name, phone, email, number_adults, number_child, deposit, paymentSum, confirm_use, send_emails, foundUs ,text = args
    date         = [int(x) for x in trip_date.split("-")]
    dateClass    = datetime.date(date[0],date[1],date[2])
    tripQuerySet = Trip.get_event(dateClass, trip_abc_name)
    guide        = get_object_or_404(Guide, user_name='yaelr')
    ourTour      = get_object_or_404(OurTours, trip_abc_name = trip_abc_name)
    foundUsPointer      = get_object_or_404(FoundUs, pk = foundUs)

    # If need a new trip
    if (len(tripQuerySet)==0):
        trip = Trip(trip_text='', trip_date=dateClass, trip_time=trip_time, guide=guide, ourTour=ourTour)
        trip.save()
    # Repeat to solve the time format in the email    
    tripQuerySet = Trip.get_event(dateClass, trip_abc_name)    
    trip = tripQuerySet[0]
    # Create new client           
    client = Clients(trip=trip,first_name=first_name,last_name=last_name, phone_number=phone, email=email, number_of_people=int(number_adults), 
                     number_of_children=int(number_child), pre_paid = deposit, total_payment = int(paymentSum), confirm_use = confirm_use, send_emails = send_emails, text = text, foundUs = foundUsPointer)
#            
    client.save()
    return client

def send_succes_email(request,client):
    ''' This function send email confirmation to a new client
    '''
    NotFree     = (client.trip.ourTour.price != 0)
    msg_plain   = 'DUMMY ONE'
    children    = (client.number_of_children > 0)
    more_to_pay = (client.total_payment-client.pre_paid)
    dayHeb      = hebdict[client.trip.trip_date.strftime('%a')]
    try:
        msg_html = render_to_string('emails/email_success.html', { 
                                                                  'client':client, 
                                                                  'print_children':children, 
                                                                  'more_to_pay':more_to_pay,
                                                                  'day_in_hebrew':dayHeb,
                                                                  'NotFree':NotFree})

        emailTitle = "סיור בקיימברידג' - אישור הזמנה"
        emailSuccess = tour_emails.send_email(msg_html=msg_html, msg_plain=msg_plain, to=[client.email], title=emailTitle, cc=settings.CC_EMAIL)
    except:
        print('Got an error... sending email...')
    #print(f'Debug {emailSuccess}')
    meta_des_heb = "סיורים בקיימברידג' אנגליה - ההרשמה לסיור הסתיימה בהצלחה  "
    meta_des_en  = ""
    meta_des = meta_des_heb + meta_des_en
    meta_key_heb = "הרשמה הצלחה "
    meta_key_en  = " "
    meta_key     = meta_key_heb + meta_key_en
    #print(trip)
    return render(request,'tour/success.html', {'title':'תשלום הצליח', 'page_title':'ההרשמה הסתיימה בהצלחה', 
                                                      'meta_des':  meta_des,
                                                      'meta_key':  meta_key,
                                                      'client':    client,
                                                      'more_to_pay':more_to_pay, 
                                                      'day_in_hebrew':dayHeb
                                                      })
            
def payment(request):
    form = PaymentForm(request.POST)
    if request.method == 'POST':
        title, trip_date, trip_time, trip_abc_name, first_name, last_name, phone, email, number_adults, number_child, deposit, paymentSum, confirm_use, send_emails, foundUs, text = form.get_data() 
        stripe.api_key = settings.STRIPE_SECRET_KEY
        deposit = int(deposit)
        try:
            token  = request.POST['stripeToken']
            charge = stripe.Charge.create(
                amount=deposit*100,
                currency='gbp',
                description='Advance payment',
                source=token,
                receipt_email = email
            )
        except stripe.error.CardError as e:
            messages.info(request, "Your card has been declined.")
            return render(request, 'tour/failure.html', {'title':'failure', 'page_title':'failure'})
        
        # We made a payment, greaty lat's create trip and client
        client = create_new_trip_client(title, trip_date, trip_time, trip_abc_name, first_name, last_name, phone, email, number_adults, number_child, deposit, paymentSum, confirm_use, send_emails, foundUs ,text)
               
        transaction = Transaction(client=client,
                            token=token, 
                            charge_id = charge.id,
                            amount=client.pre_paid,
                            success=True)
            # save the transcation (otherwise doesn't exist)
        transaction.save()
        return send_succes_email(request, client)

    return render(request, 'tour/failure.html', {'title':'failure payment end', 'page_title':'failure'})
    

def tour_details(request, trip_abc_name='Classic'):
    
    ourTours = get_object_or_404(OurTours, trip_abc_name=trip_abc_name)

    meta_des_heb = "סיורים בקיימברידג' אנגליה"
    meta_des_en  = "סיורים בעברית בקיימברידג'- סיור מחוץ ללונדון"
    meta_des = meta_des_heb + meta_des_en
    meta_key_heb = "קולג'ים קולג' קיימברידג' שוק "
    meta_key_en  = " cambridge college old market"
    meta_key     = meta_key_heb + meta_key_en
    print_child = (ourTours.priceChild) > 0
    NotFree = (ourTours.price != 0)
    return render(request, 'tour/tour_details.html', {'page_title':ourTours.title,
                                                   'meta_des':meta_des,
                                                   'meta_key':meta_key,
                                                   'print_child':print_child,
                                                   'ourTour':ourTours,
                                                   'NotFree':NotFree})
    
def bookTourToday(request, trip_abc_name ):
     today = datetime.date.today()
     return bookTour(request,today.year, today.month, trip_abc_name )
            
def bookTour(request,pYear=1977, pMonth=1, trip_abc_name='Classic' ):
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        form = BookingForm(request.POST)
        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            #book_inst.due_back = form.cleaned_data['renewal_date']
           # Get all infortamtion from form
            title, trip_date, trip_time, trip_abc_name, first_name, last_name, phone, email, number_adults, number_child, deposit, paymentSum, confirm_use, send_emails, foundUs ,text  = form.get_data()
           
            # If it is  a free tour, no need to go to payment
            ourTours = get_object_or_404(OurTours, trip_abc_name=trip_abc_name)
            if (ourTours.price==0):
                client = create_new_trip_client(title, trip_date, trip_time, trip_abc_name, first_name, last_name, phone, email, number_adults, number_child, deposit, paymentSum, confirm_use, send_emails, foundUs ,text)
                return send_succes_email(request, client)
            meta_des_heb = "סיורים בקיימברידג תשלום על סיור  "
            meta_des_en  = "cambridge in hebrew payment"
            meta_des = meta_des_heb + meta_des_en
            meta_key_heb = "תשלום "
            meta_key_en  = "payment "
            meta_key     = meta_key_heb + meta_key_en

            form = PaymentForm(initial={       'title':title,
                                               'trip_date':trip_date,
                                               'trip_time':trip_time,
                                               'trip_type':trip_abc_name,
                                               'first_name':first_name,
                                               'last_name':last_name,
                                               'phone':phone,
                                               'email':email,
                                               'number_adults':number_adults,
                                               'number_child':number_child,
                                               
                                               'confirm_use': confirm_use, 
                                               'send_emails': send_emails,
                                               'foundUs'   : foundUs,
                                               'text'       : text,
                                               'deposit':deposit,
                                               'paymentSum':paymentSum})

            return render(request, 'tour/payment.html', {'title':title, 'page_title' : 'תשלום עבור סיור',
                                                  'meta_des':meta_des,
                                                  'meta_key':meta_key,
                                                  'form':form,
                                                 'tripdate': trip_date, 
                                                 'triptime': trip_time, 
                                                 'price':paymentSum, 
                                                 'deposit':deposit, 
                                                 'stripe_public_key':settings.STRIPE_PUBLISHABLE_KEY,
                                                 })
           
    newCalendar= Calendar(request=request, year=pYear,  month=pMonth , view=trip_abc_name)
    # If this is a POST request then process the Form data
    # Bring the trip name in hebrew from db
    TripTypeQuery = OurTours.objects.filter(trip_abc_name=trip_abc_name)
    
    if (len(TripTypeQuery)>0):
        ourTours    = TripTypeQuery[0]
        NotFree     = (ourTours.price != 0)
        title       = ourTours.title
        deposit     = ourTours.deposit
        price       = ourTours.price
        priceChild  = ourTours.priceChild
        print_child = ourTours.priceChild > 0
    else:
        title   = ''
        deposit = 0
        price =  0
        priceChild =  0
        print_child = 0
        NotFree     = True

    form = BookingForm(initial={'title':title, 'trip_type':trip_abc_name,  'price':price, 'priceChild':priceChild, 'deposit':deposit})

    pageTitle=  'הזמנת ' +  title 
    meta_des_heb = "הזמנת סיור בקיימברידג בעברית  "
    meta_des_en  = "book your tour in Hebrew in Cambridge UK"
    meta_des = meta_des_heb + meta_des_en
    meta_key_heb = "הזמנת סיור עברית קיימברידג' "
    meta_key_en  = "book tour cambridge hebrew "
    meta_key     = meta_key_heb + meta_key_en
    return render(request, 'tour/book-tour.html', {'title':title, 'page_title' : pageTitle,
                                                  'meta_des':meta_des,
                                                  'meta_key':meta_key,
                                                 'form': form, 
                                                 'price':price, 
                                                 'priceChild':priceChild, 
                                                 'deposit':deposit, 
                                                 'print_child': print_child,
                                                 'newCalendar':newCalendar,
                                                 'NotFree':NotFree})


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
                msg_plain = str(contact.id) + "מישהו יצר קשר פניה "
                emailTitle = "מישהו יצר קשר"
                emailSuccess = tour_emails.send_email(msg_html=msg_html, msg_plain=msg_plain, to=settings.BCC_EMAIL, title=emailTitle, cc=[])
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
            meta_des_heb = "משוב טיול בקיימברידג"
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



# 
class ClientView(generic.DetailView):
    template_name = 'tour/clients_in_tour.html'
    model = Trip


#######################################################
def reportView(request):

    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        form = ReportForm(request.POST)
        # We get field called 'rating' a number from 1 to 10
        # Check if the form is valid:
        report = []
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            #book_inst.due_back = form.cleaned_data['renewal_date']
           # Get all infortamtion from form
            start_month, end_month, start_year, end_year, guide, foundUs,order, output= form.get_data()
            check_guide = (guide != None)        
            tripQuerey = Trip.objects.filter(
                trip_date__month__gte  = start_month,
                trip_date__month__lte  = end_month,
                trip_date__year__gte   = start_year,
                trip_date__year__lte   = end_year,
                ).order_by(order)

            # At the moment there are two filters the guide and the 'found us'
            # They give different report as 'found us' is per client.... while the guide is per trip
            # Check if need a specific guide
            # If we need a specific guide and it is not this one...
            sum_commision = 0
            if (foundUs != None):
                for trip in tripQuerey: 
                    for client in trip.clients_set.all():
                        if client.foundUs == foundUs:
                            report.append(ClientReportEntry(client,foundUs.precentage))
                            # If the client didn't cancel then we add it to the final sum
                            if (report[-1].client.status == 'a'):
                                sum_commision += report[-1].comission
            
            else:
                reportsum = ReportEntry("sum", "sum", "sum")
                
                check_guide = (guide != None)

                for trip in tripQuerey:
                    if ((check_guide == False or trip.guide==guide) and trip.get_status_display()=='Completed'):

                    # Gather the sum here
                        reportEntry = trip.get_trip_sum()
                        reportsum   += reportEntry
                  
                        report.append(reportEntry)
                
                report.append(reportsum)
          
            # If requested view is html  
            if (output=='html'):
                return render(request, 'tour/report.html', {'title':'Report view',
                                                     'page_title' : 'דוח',
                                                     'meta_des':'',
                                                     'meta_key':'',
                                                     'form': form,
                                                     'report': report,
                                                     'found_us':(foundUs != None),
                                                     'filter_check_guide': check_guide
                                                     })
            
            # The view is pdf, therefore Create param dictionary for the pdf
            #print(list(hebmonthdic.keys())[int(month)-1])
            if (int(end_month) == 12):
                firstDayOfNextMonth = datetime.date(int(end_year)+1, 1, 1);
            else:
                firstDayOfNextMonth = datetime.date(end_year, int(end_month) +1, 1);
            lastDayInMonth = firstDayOfNextMonth - datetime.timedelta(days=1)
            if (foundUs == None):
                report_pdf=  report[:-1]
                sum_pdf   =   report[-1]
            else:
                report_pdf=  report
                sum_pdf   =  sum_commision

            params = {
                'report': report_pdf,
                'sum':   sum_pdf,
                'filter_check_guide'    : check_guide,
                'start_month'           : monthStr[int(start_month)-1],
                'end_month'             : monthStr[int(end_month)-1],
                'start_year'            : start_year,
                'end_year'              : end_year,
                'end_day'               : lastDayInMonth.day,
                'request'               : request
            }
            # Check if need to send the pdf    
            if (output=='send_pdf'):
                file_name='Report_' +  monthStr[int(start_month)-1] + '_' + str(start_year)  + '.pdf'
                if (foundUs == None):
                    file = Render.render_to_file('pdf/report.html', file_name, params)
                else:
                    file = Render.render_to_file('pdf/found_us.html', file_name, params)
                tour_emails.send_email_pdf(to=['noam.gati@gmail.com'],file=file, file_name=file_name)
                
            if (foundUs == None):
                return Render.render('pdf/report.html', params)    
            else:    
                return Render.render('pdf/found_us.html', params)    
    else:
        today   = datetime.date.today()
        form    = ReportForm(initial={'start_year' : today.year, 'start_month' : today.month, 'end_year' : today.year, 'end_month' : today.month})
        report  = []
        check_guide = False
        return render(request, 'tour/report.html', {'title':'Report view',
                                                     'page_title' : 'דוח',
                                                     'meta_des':'קיימברידג בעברית דוחות',
                                                     'meta_key':'קמברידג',
                                                     'form': form,
                                                     'report': report,
                                                     'filter_check_guide': check_guide
                                                     })
            

        # If this is a GET (or any other method) create the default form.
        # TODO, Double check date as avialable one, or already has a trip on that day. 
    
def tripView(request):

    if request.method == 'POST':
        report = []
        # Create a form instance and populate it with data from the request (binding):
        form = ReportForm(request.POST)
        # We get field called 'rating' a number from 1 to 10
        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            # Get all infortamtion from form
            #month, year, check_guide, guide, order, output  = form.get_data()
            start_month, end_month, start_year, end_year, guide, foundUs, order, output= form.get_data()
                    
            tripQuerey = Trip.objects.filter(
                trip_date__month__gte  = start_month,
                trip_date__month__lte  = end_month,
                trip_date__year__gte   = start_year,
                trip_date__year__lte   = end_year,
                ).order_by(order)

            # At the moment there are two filters the guide and the 'found us'
            # They give different report as 'found us' is per client.... while the guide is per trip
            # Check if need a specific guide
            # If we need a specific guide and it is not this one...
            
            #if (found_us != 'f'):
            #    trip in tripQuereyand 
            #    report = [client for client in trip.clients_all.objects() if client.found_us == found_us]
            # Bring the whole trip
            #else:
            
            check_guide = (guide != None)

            report = [trip for trip in tripQuerey if (check_guide == False or trip.guide==guide)]
             
            # If we need a specific 'Found us' then we need to bring the client and this report will be per client.

            # If requested view is html  
            if (output=='html'):
                return render(request, 'tour/trip_view.html', {'title':'טיולים לחודש',
                                                     'page_title' : 'טיולים לחודש',
                                                     'meta_des':'',
                                                     'meta_key':'',
                                                     'form': form,
                                                     'report': report,
                                                     'filter_check_guide': check_guide
                                                     })
            
            # The view is pdf, therefore Create param dictionary for the pdf
            #print(list(hebmonthdic.keys())[int(month)-1])
            if (end_month == 12):
                firstDayOfNextMonth = datetime.date(int(end_year)+1, 1, 1);
            else:
                firstDayOfNextMonth = datetime.date(end_year, int(end_month) +1, 1);
            lastDayInMonth = firstDayOfNextMonth - datetime.timedelta(days=1)
            params = {
                'report': tripQuerey,
                'filter_check_guide': check_guide,
                'start_month'           : monthStr[int(start_month)-1],
                'end_month'             : monthStr[int(end_month)-1],
                'start_year'            : start_year,
                'end_year'              : end_year,
                'end_day'               : lastDayInMonth.day,

                'request': request
            }
            # Check if need to send the pdf    
            if (output=='send_pdf'):
                file_name='Trips_' +  monthStr[int(start_month)-1] + '_' + str(start_year) + '.pdf'
                file = Render.render_to_file('pdf/trip.html', file_name, params)
                tour_emails.send_email_pdf(to=['noam.gati@gmail.com'],file=file, file_name=file_name)
                
            
            return Render.render('pdf/trip.html', params)    
    else:
        today           = datetime.date.today()
        form = ReportForm(initial={'start_year' : today.year, 'end_year' : today.year, 'start_month' : today.month, 'end_month' : today.month})
        tripQuerey = []
        check_guide = False
        return render(request, 'tour/trip_view.html', {'title':'טיולים לחודש',
                                                     'page_title' : 'טיולים לחודש',
                                                     'meta_des':'קיימברידג בעברית ',
                                                     'meta_key':'קמברידג',
                                                     'form': form,
                                                     'report': tripQuerey,
                                                     'filter_check_guide': check_guide
                                                     })
                
def tripPdf(request, pk):
    '''
    This function generate a pdf document  - there is a problem with the name in hebrew...
    '''
    trip = Trip.objects.filter(id=pk)[0]
                        
    params = {
        'trip': trip,
        'request': request
    }
                
            
    return Render.render('pdf/trip_details.html', params)    


def links(request): 
     return render(request, 'tour/links.html')

def privacy(request): 
     return render(request, 'tour/privacy.html', {'title':'מדיניות פרטיות',
                                                     'page_title' : 'מדיניות פרטיות',
                                                     'meta_des':'מדיניות פרטיות ',
                                                     'meta_key':'מדיניות פרטיות'
                                                     })
    
def tasks(request):
    today           = datetime.date.today()
    new_tours =  Trip.objects.filter(
                         status  = 'n'
                        ).order_by('trip_date')
    
    complete_tours = Trip.objects.filter(
                         status  = 'a',
                         trip_date__lte  = today
                        ).order_by('trip_date')
    
    check_contact_spam = Contact.objects.filter(confirm = 'n')
    
    new_contact = Contact.objects.filter(confirm = 'c')
    
    new_review = Review.objects.filter(confirm = False)
    
    next_tours =  Trip.objects.filter(
                        ~Q(status='b'),
                        trip_date__gte  = today
                        ).order_by('trip_date')
    
    next_vacations = GuideVacation.objects.filter(
            vac_end_date__gte = today
            ).order_by('vac_start_date')
         
    return render(request, 'tour/tasks.html', {'title':'Tasks',
                                                     'page_title' : 'משימות',
                                                     'meta_des':'קיימברידג בעברית משימות',
                                                     'meta_key':'קמברידג',
                                                     'new_tours': new_tours,
                                                     'complete_tours': complete_tours,
                                                     'check_contact_spam' : check_contact_spam,
                                                     'new_contact':new_contact,
                                                     'new_review':new_review,
                                                     'next_tours':next_tours,
                                                     'next_vacations':next_vacations
                                                     
                                                     })


def tour_confirm(request, pk):
    '''
    This function change trip status to confirm
    '''
    tours_query =  Trip.objects.filter(id  = pk)
    if (len(tours_query)>0):
        tour = tours_query[0]
        tour.status = 'a'
        tour.save()
    return  redirect('tour:tasks')

# This class is used in the report.html
class TransactionEntry: 
    def __init__(self, payment_type, payment_date, payment_amount, payment_id):
        self.payment_type      = payment_type
        self.payment_date      = payment_date
        self.payment_amount    = payment_amount
        self.payment_id        = payment_id

    



def tour_complete(request, pk):
    '''
    This function change trip status to complete:
        1. Create transaction cache
        2. Create invice
        3. Send email with request for feedback
    '''
    trip = get_object_or_404(Trip, pk=pk)
    
    #tours_query =  Trip.objects.filter(id  = pk)
    #if (len(tours_query)>0):
    #    trip = tours_query[0]
    if trip.get_status_display() == 'Confirmed':
        # First thing to avoid races -  Change trip status to complete    
        trip.status = 'e'
        trip.save()
        
        CreateInvoice = (trip.ourTour.price != 0)
        #Let's see if it is a free tour
        
        clientQuerey = trip.clients_set.all()
        
        # If it is a free tour, we don't need to send invoice to the clients
        # We just need to send the email....
        
        
        # This isn't  a free tour we are going to make invice and send email with attachment
        # Scan all clients
        for client in clientQuerey:
            transactionArray = []
            if client.status != 'a':
                continue
            # Free tour will skip this if statement 
            if client.total_payment > client.pre_paid:
                # Create Cache transaction  
                try:
                    transaction = Transaction(
                                    client          =  client,
                                    token           =  'Cash',
                                    amount          =  (client.total_payment - client.pre_paid),
                                    charge_id       =  'Cash',
                                    success         =  True)
                    transaction.save()
                except:
                    print ('problem creating transaction')
                        
            #'Now create the invoice'
            # Prepare the email content
            msg_plain = "תודה שטיילתם איתנו בקיימברדיג' היה לנו כייף"
            msg_html = render_to_string('emails/email_feedback.html', {'first_name':client.first_name})
            title = "קיימברידג' בעברית- תודה שטיילתם איתנו"
            if (CreateInvoice):
                transactionQuerey = client.transaction_set.all()
                amount = 0
                for tran in transactionQuerey:
                    tType = 'Card / אשראי'
                    if tran.token == 'Cash':
                        tType = 'Cash / מזומן'
                    elif tran.token == 'bank':
                        tType = 'Bank Payment / העברה בנקית'
                    amount += tran.amount
                    tranEntry = TransactionEntry(payment_type   = tType,
                                                 payment_date   = tran.create_date,
                                                 payment_amount = tran.amount ,
                                                 payment_id     = tran.id )  
                    
                    transactionArray.append(tranEntry)
                # create sum 
                tranEntry = TransactionEntry(payment_type   = 'סיכום',
                                                 payment_date   = datetime.datetime.now(),
                                                 payment_amount = amount ,
                                                 payment_id     = trip.id )
                # Ready to create invoice
                params = {
                    'report'   : transactionArray,
                    'sum'      : tranEntry, 
                    'client'   : client,
                    'children' : (client.number_of_children > 0),
                    'request'  : request
                }
                # Check if need to send the pdf    
                try:
                    file_name='Cambridge_in_hebrew_invoice_' + str(client.id)  + '.pdf'
                    file = Render.render_to_file('pdf/client.html', file_name, params)
                except:
                    print("Can't create pdf")
                try:
                
                    tour_emails.send_email_msg_pdf( to=[client.email],
                                                   msg_html=msg_html, 
                                                   msg_plain=msg_plain, 
                                                   file=file, 
                                                   file_name=file_name, 
                                                   cc=[settings.EMAIL_YAEL], 
                                                   title=title)
                except:
                    print("Can't send email")
            else:
                try:
                    
                    emailSuccess = tour_emails.send_email(msg_html=msg_html, msg_plain=msg_plain, to=[client.email], title=title, cc=[settings.EMAIL_YAEL])
                except:
                    print('Got an error... sending email...')
        
    
    # Bring back the tasks        
    return  redirect('tour:tasks')

def contact_not_spam(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    #if (len(contact_query)>0):
    contact.confirm = 'c'
    contact.save()
    # Now send email to adminstrator            
    try:
        msg_html = render_to_string('emails/email_contact.html', {'first_name':contact.first_name,'last_name':contact.last_name, 'email':contact.email, 'id': contact.id, 'text':contact.text})
        msg_plain = str(contact.id) + "תודה שיצרתם קשר "
        emailTitle = "סיור בקיימברידג' - צור קשר"
        emailSuccess = tour_emails.send_email(msg_html=msg_html, msg_plain=msg_plain, to=[contact.email], title=emailTitle, cc=settings.EMAIL_GMAIL_YAEL)
    except:
        print('Got an error...')
        # Save contact here
        

    return  redirect('tour:tasks')

def contact_spam(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    #if (len(contact_query)>0):
    contact.delete()
    # Now send email to adminstrator            
    return  redirect('tour:tasks')

def contact_confirm(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    contact.confirm = 'd'
    contact.save()
    return  redirect('tour:tasks')


def review_confirm(request, pk):
    review_query = Review.objects.filter(id  = pk)
    if (len(review_query)>0):
        review = review_query[0]
        review.confirm = True
        review.save()
    return  redirect('tour:tasks')


def CanMakeIt(request, pk ):
    return CanMakeItFuncion(request, pk, True )
def CantMakeIt(request, pk ):    
    return CanMakeItFuncion(request, pk, False )

def CanMakeItFuncion(request, pk, canMakeit ):
    clients = get_object_or_404(Clients, pk=pk)
    title = 'שגיאה'
    try:
        msg_html = render_to_string('emails/email_free_tour_confirmation.html', {'first_name':clients.first_name,'last_name':clients.last_name, 'email':clients.email, 'id': clients.id, 'canMakeit':canMakeit})
        if (canMakeit):
            msg_plain = str(clients.id) + "בטח מגיע לסיור "
            emailTitle = clients.first_name + " בטח מגיע לסיור"
            title = " בטח מגיע לסיור"
        else:
            msg_plain = str(clients.id) + "לא מגיע לסיור "
            emailTitle = clients.first_name + " לא מגיע לסיור"
            title = "  לא מגיע לסיור"
        emailSuccess = tour_emails.send_email(msg_html=msg_html, msg_plain=msg_plain, to=settings.CC_EMAIL, title=emailTitle, cc=[])
    except:
        print('Got an error...')
        # Save contact here
    meta_des_heb = "קיימברידג בעברית אישור הגעה  "
    meta_des_en  = "confirmation Cambridge in Hebrew"
    meta_des = meta_des_heb + meta_des_en
    meta_key_heb = "אישור הגעה קיימברידג' "
    meta_key_en  = "confirmaion cambridge hebrew "
    meta_key     = meta_key_heb + meta_key_en
    
    return render(request, 'tour/free_tour_confirmation.html', {'title':title, 
                                                               'meta_des':meta_des,
                                                               'meta_key':meta_key,
                                                               'page_title':title,
                                                               'canMakeit':canMakeit
                                                               
                                                               })
