"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('accounts/', include('allauth.urls')),
    
    # Gestion (ne pas dupliquer)
    path('gestion/', include('main_apps.gestion.urls')),
    
    # Pages publiques
    path('universities/', views.universities, name='universities'),
    path('bourses/', views.bourses, name='bourses'),
    path('services/', views.services, name='services'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    
    # Authentification (redondant avec allauth, à supprimer si tu utilises allauth)
    # path('login/', views.login_view, name='login'),
    # path('register/', views.register_view, name='register'),
    
    # URLs pour les demandes d'admission
    path('application/new/', views.application_create, name='application_create'),
    path('applications/', views.application_list, name='application_list'),
    path('application/<int:pk>/', views.application_detail, name='application_detail'),
    path('application/success/<int:pk>/', views.application_success, name='application_success'),
    
    # URLs pour les examens physiques
    path('physical-exam/new/', views.physical_exam_create, name='physical_exam_create'),
    path('physical-exam/<int:pk>/', views.physical_exam_detail, name='physical_exam_detail'),
    path('physical-exam/success/<int:pk>/', views.physical_exam_success, name='physical_exam_success'),
    
    # URLs pour les paiements (AJOUTER CES LIGNES)
    path('payment/<int:application_id>/', views.payment_page, name='payment_page'),
    path('payment/create-intent/<int:application_id>/', views.create_payment_intent, name='create_payment_intent'),
    path('payment/success/<int:application_id>/', views.payment_success, name='payment_success'),
    path('payment/cancel/<int:application_id>/', views.payment_cancel, name='payment_cancel'),
    path('payment/webhook/', views.payment_webhook, name='payment_webhook'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)