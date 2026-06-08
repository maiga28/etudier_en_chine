"""
URL configuration for core project.
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
from . import views as core_views
from .views import index
from main_apps.gestion import views as gestion_views

urlpatterns = [
    # Administration
    path('admin/', admin.site.urls),
    
    # Pages principales
    path('', core_views.index, name='index'),
    
    # Allauth (pour l'authentification sociale)
    path('accounts/', include('allauth.urls')),
    path('accounts/profile/<int:pk>/', include('allauth.urls')),
    
    # Authentification personnalisée (désactiver les doublons avec allauth si nécessaire)
    path('login/', core_views.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', core_views.register_view, name='register'),
    # core/urls.py

    path('accounts/profile/', core_views.profile_redirect, name='profile_redirect'),

    # Redirection après connexion
    path('dashboard-redirect/', gestion_views.dashboard_redirect, name='dashboard_redirect'),
    
    # Tableaux de bord
    path('dashboard/user/', gestion_views.user_dashboard, name='user_dashboard'),
    path('dashboard/admin/', gestion_views.admin_dashboard, name='admin_dashboard'),
    
    # Gestion (admin seulement)
    path('gestion/', include('main_apps.gestion.urls')),
    # path('gestion/', gestion_views.gestion, name='gestion'),  # Vue alternative
    
    # Pages publiques
    path('universities/', core_views.universities, name='universities'),
    path('bourses/', core_views.bourses, name='bourses'),
    path('services/', core_views.services, name='services'),
    path('about/', core_views.about, name='about'),
    path('contact/', core_views.contact, name='contact'),
    
    # URLs pour les demandes d'admission
    path('application/new/', core_views.application_create, name='application_create'),
    path('applications/', core_views.application_list, name='application_list'),
    path('application/<int:pk>/', core_views.application_detail, name='application_detail'),
    path('application/<int:id>/update-status/<str:new_status>/', core_views.update_application_status, name='update_application_status'),
    path('application/success/<int:pk>/', core_views.application_success, name='application_success'),
    path('my-applications/', core_views.my_applications, name='my_applications'),
    path('application/<int:id>/update-status/', core_views.update_application_status,name='update_application_status'),
    path('application/<int:pk>/', core_views.application_detail, name='application_detail'),
    path('physical-exam/<int:pk>/', core_views.physical_exam_detail, name='physical_exam_detail'),
    # URLs pour les examens physiques
    path('physical-exam/new/', core_views.physical_exam_create, name='physical_exam_create'),
    path('physical-exam/<int:pk>/', core_views.physical_exam_detail, name='physical_exam_detail'),
    path('physical-exam/success/<int:pk>/', core_views.physical_exam_success, name='physical_exam_success'),
    path('physical_exam_list/', core_views.physical_exam_list, name='physical_exam_list'),

    
    # URLs pour les paiements
    path('payment/<int:application_id>/', core_views.payment_page, name='payment_page'),
    path('payment/create-intent/<int:application_id>/',
         core_views.create_payment_intent,
         name='create_payment_intent'
    ),
    path('payment_list', core_views.payment_list, name="payment_list"),
    path('payment/success/<int:application_id>/', core_views.payment_success, name='payment_success'),
    path('payment/cancel/<int:application_id>/', core_views.payment_cancel, name='payment_cancel'),
    path('payment/webhook/', core_views.payment_webhook, name='payment_webhook'),
]

# Gestion des fichiers statiques et médias en mode debug
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)