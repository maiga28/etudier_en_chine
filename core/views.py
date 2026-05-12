from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from main_apps.gestion.models import StudentApplication, PhysicalExamination
import json
import stripe
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from main_apps.gestion.models import StudentApplication, Payment

# Configuration Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

def index(request):
    return render(request, 'index.html')
def universities(request):
    """Page des universités"""
    return render(request, 'universities/universities.html')

def bourses(request):
    """Page des bourses"""
    return render(request, 'bourses/bourses.html')

def services(request):
    """Page des services"""
    return render(request, 'services/services.html')

def about(request):
    """Page à propos"""
    return render(request, 'about/about.html')

def contact(request):
    """Page de contact"""
    return render(request, 'contact/contact.html')




# ... vos autres vues ...

def login_view(request):
    """Page de connexion"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Identifiants invalides')
    return render(request, 'auth/login.html')

def register_view(request):
    """Page d'inscription"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Compte créé avec succès !')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'auth/register.html', {'form': form})



amount = 500.00  # Montant fixe pour les frais de dossier
def application_create(request):
    if request.method == 'POST':
        try:
            # Récupération des données JSON
            education_history = json.loads(request.POST.get('education_history', '[]'))
            work_experience = json.loads(request.POST.get('work_experience', '[]'))
            family_members = json.loads(request.POST.get('family_members', '[]'))
            
            # Création de l'application
            application = StudentApplication.objects.create(
                # Informations personnelles
                family_name=request.POST.get('family_name'),
                given_name=request.POST.get('given_name'),
                chinese_name=request.POST.get('chinese_name', ''),
                gender=request.POST.get('gender'),
                marital_status=request.POST.get('marital_status'),
                nationality=request.POST.get('nationality'),
                country_of_birth=request.POST.get('country_of_birth'),
                birth_date=request.POST.get('birth_date'),
                place_of_birth=request.POST.get('place_of_birth'),
                native_language=request.POST.get('native_language'),
                highest_education=request.POST.get('highest_education'),
                religion=request.POST.get('religion', ''),
                employer_or_institution=request.POST.get('employer_or_institution', ''),
                occupation=request.POST.get('occupation', ''),
                health_status=request.POST.get('health_status'),
                is_emigrant_from_china=request.POST.get('is_emigrant_from_china') == 'on',
                hobby=request.POST.get('hobby', ''),
                
                # Passeport
                passport_number=request.POST.get('passport_number'),
                passport_expiration_date=request.POST.get('passport_expiration_date'),
                
                # Historiques JSON
                education_history=education_history,
                work_experience=work_experience,
                family_members=family_members,
                
                # Soutien financier
                guarantor_name=request.POST.get('guarantor_name'),
                guarantor_address=request.POST.get('guarantor_address'),
                guarantor_tel=request.POST.get('guarantor_tel'),
                guarantor_relationship=request.POST.get('guarantor_relationship'),
                guarantor_organization=request.POST.get('guarantor_organization', ''),
                guarantor_email=request.POST.get('guarantor_email', ''),
                
                # Adresses
                home_address_street=request.POST.get('home_address_street'),
                home_address_city_province=request.POST.get('home_address_city_province'),
                home_address_country=request.POST.get('home_address_country'),
                home_address_phone=request.POST.get('home_address_phone'),
                home_address_mobile=request.POST.get('home_address_mobile', ''),
                home_address_zipcode=request.POST.get('home_address_zipcode', ''),
                same_current_as_home=request.POST.get('same_current_as_home') == 'on',
                current_address=request.POST.get('current_address', ''),
                personal_email=request.POST.get('personal_email'),
                
                # Réseaux sociaux
                facebook_account=request.POST.get('facebook_account', ''),
                wechat_account=request.POST.get('wechat_account', ''),
                linkedin_account=request.POST.get('linkedin_account', ''),
                twitter_account=request.POST.get('twitter_account', ''),
                qq_account=request.POST.get('qq_account', ''),
                msn_account=request.POST.get('msn_account', ''),
            )
            
            # Créer automatiquement l'objet Payment associé
            from main_apps.gestion.models import Payment
            Payment.objects.create(
                application=application,
                amount=amount,
                currency='EUR',
                status='PENDING'
            )
            
            messages.success(request, 'Votre demande a été créée avec succès ! Veuillez procéder au paiement.')
            
            # ✅ REDIRECTION UNIQUE VERS LE PAIEMENT
            return redirect('payment_page', application_id=application.pk)
            
        except Exception as e:
            messages.error(request, f'Erreur lors de la soumission: {str(e)}')
            return redirect('application_create')
    
    return render(request, 'gestion/application_form.html')

# Vue pour la page de paiement
def payment_page(request, application_id):
    application = get_object_or_404(StudentApplication, id=application_id)
    
    # Vérifier si un paiement existe déjà
    payment, created = Payment.objects.get_or_create(
        application=application,
        defaults={'amount': amount}  # Frais de dossier
    )
    
    context = {
        'application': application,
        'payment': payment,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
    }
    return render(request, 'gestion/payment.html', context)
# Vue pour créer une intention de paiement Stripe
def create_payment_intent(request, application_id):
    """Créer une intention de paiement Stripe"""
    application = get_object_or_404(StudentApplication, id=application_id)
    payment = Payment.objects.get(application=application)
    
    try:
        intent = stripe.PaymentIntent.create(
            amount=int(payment.amount * 100),  # Stripe utilise les centimes
            currency=payment.currency.lower(),
            metadata={
                'application_id': application.id,
                'student_name': f"{application.family_name} {application.given_name}",
                'payment_id': payment.id
            },
        )
        
        payment.payment_intent_id = intent.id
        payment.save()
        
        return JsonResponse({
            'clientSecret': intent.client_secret,
            'paymentIntentId': intent.id
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

# Vue pour gérer le succès du paiement
def payment_success(request, application_id):
    """Page après paiement réussi"""
    application = get_object_or_404(StudentApplication, id=application_id)
    payment = get_object_or_404(Payment, application=application)
    
    # Vérifier le statut du paiement avec Stripe
    if payment.payment_intent_id:
        try:
            intent = stripe.PaymentIntent.retrieve(payment.payment_intent_id)
            if intent.status == 'succeeded':
                payment.mark_as_paid(intent.id)
                messages.success(request, 'Votre paiement a été confirmé avec succès !')
            else:
                messages.warning(request, 'Le paiement est en cours de vérification.')
        except Exception as e:
            messages.error(request, f'Erreur: {str(e)}')
    
    return render(request, 'gestion/payment_success.html', {'application': application})

# Vue pour annuler le paiement
def payment_cancel(request, application_id):
    """Page après annulation du paiement"""
    application = get_object_or_404(StudentApplication, id=application_id)
    return render(request, 'gestion/payment_cancel.html', {'application': application})

# Webhook Stripe pour confirmer les paiements asynchrones
def payment_webhook(request):
    """Webhook Stripe pour confirmer les paiements asynchrones"""
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        return JsonResponse({'error': 'Invalid payload'}, status=400)
    except stripe.error.SignatureVerificationError:
        return JsonResponse({'error': 'Invalid signature'}, status=400)
    
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        payment_id = payment_intent['metadata'].get('payment_id')
        
        if payment_id:
            try:
                payment = Payment.objects.get(id=payment_id)
                payment.mark_as_paid(payment_intent['id'])
            except Payment.DoesNotExist:
                pass
    
    return JsonResponse({'status': 'success'})
def application_list(request):
    applications = StudentApplication.objects.all().order_by('-application_date')
    return render(request, 'gestion/application_list.html', {'applications': applications})

def application_detail(request, pk):
    application = get_object_or_404(StudentApplication, pk=pk)
    return render(request, 'gestion/application_detail.html', {'application': application})

def application_success(request, pk):
    app = get_object_or_404(StudentApplication, pk=pk)
    return render(request, 'gestion/application_success.html', {'app': app})

# Vues pour les examens physiques
def physical_exam_create(request):
    application_id = request.GET.get('application_id')
    if not application_id:
        messages.error(request, 'Veuillez d\'abord créer une demande d\'admission.')
        return redirect('application_create')
    
    application = get_object_or_404(StudentApplication, pk=application_id)
    
    if request.method == 'POST':
        try:
            physical_exam = PhysicalExamination.objects.create(
                application=application,
                name=request.POST.get('name'),
                gender=request.POST.get('gender'),
                birth_date=request.POST.get('birth_date'),
                present_mailing_address=request.POST.get('present_mailing_address', ''),
                nationality=request.POST.get('nationality'),
                birth_place=request.POST.get('birth_place', ''),
                blood_type=request.POST.get('blood_type') or None,
                
                # Signes vitaux
                height_cm=request.POST.get('height_cm') or None,
                weight_kg=request.POST.get('weight_kg') or None,
                blood_pressure_systolic=request.POST.get('blood_pressure_systolic') or None,
                blood_pressure_diastolic=request.POST.get('blood_pressure_diastolic') or None,
                
                # Vision
                vision_left=request.POST.get('vision_left', ''),
                vision_right=request.POST.get('vision_right', ''),
                corrected_vision_left=request.POST.get('corrected_vision_left', ''),
                corrected_vision_right=request.POST.get('corrected_vision_right', ''),
                colour_sense=request.POST.get('colour_sense', ''),
                
                # Examens physiques
                development=request.POST.get('development', ''),
                nourishment=request.POST.get('nourishment', ''),
                heart=request.POST.get('heart', ''),
                lungs=request.POST.get('lungs', ''),
                abdomen=request.POST.get('abdomen', ''),
                skin=request.POST.get('skin', ''),
                other_findings=request.POST.get('other_findings', ''),
                
                # Examens complémentaires
                ecg_result=request.POST.get('ecg_result', ''),
                chest_xray_result=request.POST.get('chest_xray_result', ''),
                hiv_test_result=request.POST.get('hiv_test_result') or None,
                syphilis_test_result=request.POST.get('syphilis_test_result') or None,
                
                # Avis médical
                medical_opinion=request.POST.get('medical_opinion', ''),
                is_medically_fit=request.POST.get('is_medically_fit') == 'on',
                physician_signature=request.POST.get('physician_signature', ''),
                examination_date=request.POST.get('examination_date') or None,
            )
            
            messages.success(request, 'L\'examen physique a été enregistré avec succès !')
            return redirect('physical_exam_success', pk=physical_exam.pk)
            
        except Exception as e:
            messages.error(request, f'Erreur lors de l\'enregistrement: {str(e)}')
    
    return render(request, 'gestion/physical_exam_form.html', {'application': application})

def physical_exam_detail(request, pk):
    physical_exam = get_object_or_404(PhysicalExamination, pk=pk)
    return render(request, 'gestion/physical_exam_detail.html', {'physical_exam': physical_exam})

def physical_exam_success(request, pk):
    physical_exam = get_object_or_404(PhysicalExamination, pk=pk)
    return render(request, 'gestion/physical_exam_success.html', {'physical_exam': physical_exam})