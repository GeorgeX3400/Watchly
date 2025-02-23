from django.urls import path
from . import views
from django.contrib.sitemaps.views import sitemap
from .sitemaps import WatchSitemap, StaticViewsSitemap

sitemaps = {
    'watch': WatchSitemap,
    'static': StaticViewsSitemap,
}

urlpatterns = [
    path("", views.index, name="index"),
    path("contact/", views.ContactFormView.as_view(), name='contact'),
    path('watches/', views.WatchListView.as_view(), name='watches'),  
    path('watches/<int:id>', views.watch_view, name='watch'),
    path('add_watch', views.add_watch),
    path('register', views.register_view, name='register'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('home', views.home_view, name='home'),
    path('change-password/', views.change_password_view, name='change_password'),
    path('confirm_mail/<str:cod>/', views.confirm_mail_view, name='confirm_mail'),
    path('promotii/', views.promotions_view, name='promotions'),
    path('oferta/', views.offer_view, name='oferta'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('cart/', views.cart_view, name='cart'),
    path('order/', views.place_order, name='order'),
]
handler403 = 'ecommerceapp.views.custom_403_view'
