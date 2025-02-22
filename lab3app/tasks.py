import schedule
import time
from . import models
from django.core.mail import send_mass_mail, mail_admins
from django.db.models import F
def delete_users():
    unconfirmed_users = models.CustomUser.objects.filter(email_confirmat=False).exclude(username_in=['george', 'Georgeee'])
    unconfirmed_users.delete()

def send_newsletter():
    email_list = models.CustomUser.objects.filter(email_confirmat=True).values_list('email', flat=True)
    send_mass_mail(('Watch Store Newsletter', 
                    "Hello! Here is the weekly newsletter. Thank you for being subscribed.",
                     'geoserb13@gmail.com',
                      email_list ), fail_silently=False)
    
def fill_stock():
    stocks = models.Stock.objects.all()
    stocks.objects.update(quantity=F('quantity') + 10)

def check_stock():
    stocks = models.Stock.objects.filter(quantity__lt=3).values_list('watch', 'quantity')
    if stocks.count() == 0: return
    stocks_string = "\n".join([f"{watch} -> {quantity}" for watch, quantity in stocks])
    mail_admins("Stocks running out of watches",
                stocks_string)


schedule.every(3).minute.do(delete_users)

schedule.every().monday.at('18:00').do(send_newsletter)

schedule.every().monday.at('6:00').do(fill_stock)

schedule.every(10).minute.do(check_stock)

    
    

