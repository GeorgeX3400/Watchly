from datetime import datetime
import json
import os
import uuid
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import  login, logout
from .forms import *
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash, authenticate
from django.contrib import messages
from django.core.mail import send_mail, send_mass_mail
from django.template.loader import render_to_string
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from . import models
from django.shortcuts import render
from .models import CustomUser, Feature, Stock, Watch, Order, OrderItem, WatchFeature
import time
from django.http import JsonResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import logging
from rest_framework.response import Response
from .serializers import *
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.parsers import JSONParser
import io
from django.middleware.csrf import get_token
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect


logging = logging.getLogger('django')
def mesaj_trimis(request):
    return render("ok")
def index(request):
    return render("good")




def watch_list(request):
    form = WatchFilterForm(request.GET or None)
    watches = Watch.objects.all()
    user = request.user
    if user: 
        messages.info(request, f"{user.username} acceseaza pagina de produse.")
    
    if form.is_valid():
        name = form.cleaned_data.get('name')
        brand = form.cleaned_data.get('brand')
        min_price = form.cleaned_data.get('min_price')
        max_price = form.cleaned_data.get('max_price')
        min_water_resistance = form.cleaned_data.get('min_water_resistance')
        movement_type = form.cleaned_data.get('movement_type')
        warranty = form.cleaned_data.get('warranty')
        material = form.cleaned_data.get('material')
        feature = form.cleaned_data.get('feature')

        if name:
            watches = watches.filter(name__icontains=name)

        if brand:
            watches = watches.filter(brand=brand)

        if min_price:
            watches = watches.filter(price__gte=min_price)

        if max_price:
            watches = watches.filter(price__lte=max_price)

        if min_water_resistance:
            watches = watches.filter(water_resistance__gte=min_water_resistance)

        if movement_type:
            watches = watches.filter(movement_type=movement_type)

        if warranty:
            watches = watches.filter(warranty=warranty)

        if material:
            watches = watches.filter(materials__id=material.id)

        if feature:
            watches = watches.filter(features__id=feature.id)

    return render(request, 'watch_list.html', {'form': form, 'watches': watches})

def watch_view(request, id):
    watch = Watch.objects.filter(id=id)[0]
    user = request.user
    stock = Stock.objects.filter(watch=watch)
    watchFeatures = WatchFeature.objects.filter(watch=watch)
    features = Feature.objects.filter(id__in=watchFeatures)
    if user.is_authenticated:
        models.add_visualization(user, watch)
        
    return render(request, 'watch.html', {'watch': watch, 'stock': stock, 'features': features})


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            messages.debug(request, 'Se proceseaza formularul de contact.')
            data = form.cleaned_data
            birthdate = data.pop("birthdate")
            today = datetime.today()
            age_years = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
            age_months = (today.month - birthdate.month + 12) % 12
            age = f"{age_years} years and {age_months} months"

            message = data["message"].replace("\n", " ")
            message = " ".join(message.split())
            data["message"] = message
            data["age"] = age

            del data["confirm_email"]
            logging.critical('Nou formular de contact completat.')

            timestamp = int(datetime.timestamp(datetime.now()))
            filename = f"mesaje/mesaj_{timestamp}.json"
            os.makedirs("mesaje", exist_ok=True)
            with open(filename, "w") as f:
                json.dump(data, f, indent=4)
            messages(request, 'Formularul a fost trimis cu succes! ')
            return JsonResponse({"status": "success", "message": "Message saved successfully."})
        else:
            return render(request, 'contact.html', {'form': form})

    form = ContactForm()
    return render(request, 'contact.html', {'form': form})



class WatchListView(APIView):
    def get(self, request):
        watches = Watch.objects.all()
        if request.body:
            stream = io.BytesIO(request.body)
            data = JSONParser().parse(stream)
            filterSerializer = WatchFilterSerializer(data=data)
            if filterSerializer.is_valid():   
                name = filterSerializer.validated_data.get('name')
                brand = filterSerializer.validated_data.get('brand')
                min_price = filterSerializer.validated_data.get('min_price')
                max_price = filterSerializer.validated_data.get('max_price')
                min_water_resistance = filterSerializer.validated_data.get('min_water_resistance')
                movement_type = filterSerializer.validated_data.get('movement_type')
                warranty = filterSerializer.validated_data.get('warranty')
                material = filterSerializer.validated_data.get('material')
                feature = filterSerializer.validated_data.get('feature') 
                if name:
                    watches = watches.filter(name__icontains=name)
                if brand:
                    watches = watches.filter(brand=brand)

                if min_price:
                    watches = watches.filter(price__gte=min_price)

                if max_price:
                    watches = watches.filter(price__lte=max_price)

                if min_water_resistance:
                    watches = watches.filter(water_resistance__gte=min_water_resistance)

                if movement_type:
                    watches = watches.filter(movement_type=movement_type)

                if warranty:
                    watches = watches.filter(warranty=warranty)

                if material:
                    watches = watches.filter(materials__id=material.id)

                if feature:
                    watches = watches.filter(features__id=feature.id)

            else: 
                return JsonResponse(filterSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer = WatchSerializer(watches, many=True)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)


class WatchView(APIView):
    def get(self, request, id):
        query = get_object_or_404(Watch, id=id)
        serializer = WatchSerializer(query)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)

class ContactFormView(APIView):
    def post(self, request, *args, **kwargs):
        print(type(request.body)) 
        stream = io.BytesIO(request.body)
        data = JSONParser().parse(stream)
        print(data)
        serializer = ContactFormSerializer(data=data)
        print(serializer)
        print(serializer.is_valid())
        if serializer.is_valid():
            # Process the form data here, e.g., save it to the database or send an email
            data = serializer.validated_data
            birthdate = data.pop("birthdate")
            today = datetime.today()
            age_years = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
            age_months = (today.month - birthdate.month + 12) % 12
            age = f"{age_years} years and {age_months} months"

            message = data["message"].replace("\n", " ")
            message = " ".join(message.split())
            data["message"] = message
            data["age"] = age
            del data["confirm_email"]
            # create a json file and save the contact form in a "messages" folder
            timestamp = int(datetime.timestamp(datetime.now()))
            filename = f"messages/message_{timestamp}.json"
            os.makedirs("messages", exist_ok=True)
            with open(filename, "w") as f:
                json.dump(data, f, indent=4)
            
            # You can do other operations like saving the message, etc.
            return Response({"status": "success", "message": "Message sent!"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@permission_required('lab3app.add_watch', raise_exception=True)
def add_watch(request):
    if request.method == "POST":
        form = WatchForm(request.POST)
        messages.debug(request, 'Se adauga un ceas nou.')
        if form.is_valid():
            form.save()
            messages.success(request, 'Noul produs a fost adaugat cu succes.')
            return redirect('thank_you')   
        else:
            logging.error('A aparut o problema in adaugarea produsului in baza de date.')
    else:
        form = WatchForm()
    return render(request, "add_watch.html", {"form": form})


from django.shortcuts import render

def custom_403_view(request, exception):
    messages.error(request, f"Acces interzis ")
    logging.critical('Accesare interzisa a website-ului.')
    return render(request, '403.html', {
        'titlu': 'Access forbidden',
        'mesaj_personalizat': 'You\'re not allowed to access this page.'
    }, status=403)



#
#REGISTER/LOGIN:
#

#csrf-token:

class CSRFTokenView(APIView):
    
    def get(self, request):
        csrftoken = get_token(request)
        return JsonResponse({'token': csrftoken}, status=status.HTTP_200_OK)  

def register_view(request):
    if request.method == 'POST':
        print(request.POST)
        form = CustomUserCreationForm(request.POST)
        print(form)
        if form.is_valid():
            user = form.save(commit=False)
            user.cod = str(uuid.uuid4())
            user.email_confirmat = False
            user.save()
            send_mail(
                subject="Confirmare E-mail",
                message=f"Salut {user.first_name} {user.last_name},\n\n"
                        f"Pentru a confirma adresa ta de e-mail, te rugam sa accesezi urmatorul link:\n"
                        f"{settings.BASE_URL}/confirma_mail/{user.cod}/\n\n"
                        f"Multumim ca te-ai inregistrat pe site-ul nostru!",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
            messages.success(request, f"Cont creat cu succes! Nou utilizator -> {user.first_name} {user.last_name}")
            logging.info(f"Now utilizator: {user.username}")
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


class RegisterView(APIView):
    @method_decorator(csrf_protect)
    def post(self, request,):
        
        
        registerData = CustomUserSerializer(data=request.data)
        if registerData.is_valid():
            CustomUserSerializer.create(registerData, registerData.validated_data)
            return JsonResponse({'message': 'Register successful.'}, status=status.HTTP_201_CREATED)
        return JsonResponse({'error': registerData.errors}, status=status.HTTP_400_BAD_REQUEST)        


def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST, request=request)
        if form.is_valid():
            user = form.get_user() 
            login(request, user)  

            if not user.email_confirmat:
                messages.warning(request, "Confirm email before logging in.")

            if not form.cleaned_data.get('stay_logged_in'):
                request.session.set_expiry(0)  
            else:
                request.session.set_expiry(2 * 7 * 24 * 60 * 60)  

            return redirect('home') 
        else:
            messages.error(request, "Username sau parola incorecte.")
    else:
        form = CustomAuthenticationForm()

    return render(request, 'login.html', {'form': form})

class LoginView(APIView):
    @method_decorator(csrf_protect)    
    def post(self, request):
        stream = io.BytesIO(request.body)
        data = JSONParser().parse(stream)
        serializer = LoginSerializer(data=data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')

            print(serializer.validated_data.get('stay_logged_in'))

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

def confirm_mail_view(request, cod):
    user = get_object_or_404(CustomUser, cod=cod)
    if not user.email_confirmat:
        user.email_confirmat = True
        user.cod = None  
        messages.info(request, f"Email confirmat. -> {user.username}")
        user.save()
        return HttpResponse("<h1>Email confirmed successfully! You can login now.</h1>")
    else:
        messages.warning(f"Email already confirmed. -> {user.username}")
        return HttpResponse("<h1>Email has been already confirmed.</h1>")


def logout_view(request):
    logout(request)
    return redirect('login')


def home_view(request):
    
    request.session['user_data'] = {
        'username': request.user.username,
        'date_of_birth': str(request.user.date_of_birth) if request.user.is_authenticated else "N/A",
        'phone_number': str(request.user.phone_number) if request.user.is_authenticated else "N/A",
        'address': str(request.user.address) if request.user.is_authenticated else "N/A",
        'bio': str(request.user.bio) if request.user.is_authenticated else "N/A",
        'has_premium': "Da" if request.user.is_authenticated and request.user.has_premium else "Nu"
    }

    
    user_data = request.session.get('user_data')

    return render(request, 'home.html', {'user_data': user_data})


@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, request.user)  
            return redirect('home')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'change_password.html', {'form': form})



#PROMOTIONS:

def send_promotions(promotion, K=3):
    for category in promotion.categories.all():
        users = CustomUser.objects.filter(
            visualization__watch__features=category
        ).annotate(views_count=models.Count('visualization')).filter(views_count__gte=K).distinct()

        
        for user in users:
            message = render_to_string('emails/promotion_template.html', {
                'user': user,
                'promotion': promotion,
                'category': category,
            })
            send_mass_mail([(
                promotion.subject,
                message,
                'admin@example.com',  
                [user.email]
            )])

def promotions_view(request):
    if request.method == 'POST':
        form = PromotionForm(request.POST)
        if form.is_valid():
            promotion = form.save()
            send_promotions(promotion)  
            return redirect('promotions')
    else:
        form = PromotionForm()
    return render(request, 'promotions.html', {'form': form})

# offer visualize user permission:


def offer_view(request):
    content_type = ContentType.objects.get_for_model(Watch)
    vizualizeaza_oferta = Permission.objects.get(
                        codename= "vizualizeaza_oferta", 
                        content_type= content_type)
    request.user.user_permissions.add(vizualizeaza_oferta)
    print(request.user.user_permissions)
    if request.user.is_authenticated and request.user.has_perm('vizualizeaza_oferta'):
        return HttpResponse('Oferta vizualizata. :)')


def cart_view(request):
    return render(request, 'cart.html')

def place_order(request):
    if request.method == "POST":
        
        cart_data = request.body
        cart = json.loads(cart_data)

        
        user = request.user
        total_price = sum(item['quantity'] * float(item['price']) for item in cart)
        order = Order.objects.create(user=user, total_price=total_price)

        
        for item in cart:
            product = Watch.objects.get(id=item['id'])
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item['quantity'],
                price=product.price,
            )

        
        timestamp = int(time.time())
        folder_path = os.path.join(settings.MEDIA_ROOT, f"temp-invoices/{user.username}")
        os.makedirs(folder_path, exist_ok=True)
        pdf_path = os.path.join(folder_path, f"factura-{timestamp}.pdf")

        create_invoice_pdf(order, pdf_path)

        
        send_mail(
            subject="Factura comenzii tale",
            message=f"Buna {user.first_name}, atasam factura comenzii tale!",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )
        logging.info(f"Comanda noua: {user.username}")
        
        return redirect('watches')

    return JsonResponse({'success': False, 'message': 'Error processing the order.'}, status=400)

def create_invoice_pdf(order, path):
    c = canvas.Canvas(path, pagesize=letter)
    width, height = letter

    
    c.drawString(100, height - 50, f"Factura - Comanda #{order.id}")

    
    user = order.user
    c.drawString(50, height - 100, f"Utilizator: {user.first_name} {user.last_name}")
    c.drawString(50, height - 120, f"Email: {user.email}")

    
    c.drawString(50, height - 150, f"Data comenzii: {order.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
    c.drawString(50, height - 170, f"Total produse: {sum(item.quantity for item in order.items.all())}")
    c.drawString(50, height - 190, f"Total: {order.total_price} RON")

    
    y = height - 230
    for item in order.items.all():
        c.drawString(50, y, f"{item.product.name} - {item.quantity} x {item.price} RON = {item.quantity * item.price} RON")
        y -= 20

    
    c.drawString(50, y - 40, "Contact administrator: admin@example.com")

    c.save()
