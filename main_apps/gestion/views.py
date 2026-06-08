from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# core/views.py
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse
from django.contrib import messages
from main_apps.gestion.models import PhysicalExamination, StudentApplication



# core/views.py - Ajoutez cette fonction


'''@login_required
def gestion(request):
    """Tableau de bord de gestion des demandes"""
    applications = StudentApplication.objects.all().order_by('-application_date')
    total_applications = applications.count()
    pending_applications = applications.filter(status='PENDING_PAYMENT').count()
    accepted_applications = applications.filter(status='ACCEPTED').count()
    physical_exams_count = PhysicalExamination.objects.count()
    
    context = {
        'applications': applications,
        'total_applications': total_applications,
        'pending_applications': pending_applications,
        'accepted_applications': accepted_applications,
        'physical_exams_count': physical_exams_count,
    }
    return render(request, 'gestion/gestion.html', context)'''


@login_required
def dashboard_redirect(request):
    """Redirige l'utilisateur vers son dashboard approprié"""
    user = request.user
    if user.is_superuser or user.is_staff:
        return redirect('admin_dashboard')
    else:
        return redirect('user_dashboard')




# core/views.py
@login_required
def user_dashboard(request):
    """Tableau de bord pour les utilisateurs normaux - uniquement leurs demandes"""
    
    # Récupérer UNIQUEMENT les demandes de l'utilisateur connecté
    applications = StudentApplication.objects.filter(
        user=request.user
    ).order_by('-application_date')
    
    # Statistiques détaillées
    total_applications = applications.count()
    pending_payment_count = applications.filter(status='PENDING_PAYMENT').count()
    pending_validation_count = applications.filter(status='PENDING').count()
    reviewing_count = applications.filter(status='REVIEWING').count()
    accepted_applications = applications.filter(status='ACCEPTED').count()
    rejected_count = applications.filter(status='REJECTED').count()
    needs_info_count = applications.filter(status='NEEDS_INFO').count()
    
    # Examens physiques de l'utilisateur
    physical_exams_count = PhysicalExamination.objects.filter(
        application__user=request.user
    ).count()
    
    context = {
        'user': request.user,
        'applications': applications,
        'total_applications': total_applications,
        'pending_payment_count': pending_payment_count,
        'pending_validation_count': pending_validation_count,
        'reviewing_count': reviewing_count,
        'accepted_applications': accepted_applications,
        'rejected_count': rejected_count,
        'needs_info_count': needs_info_count,
        'physical_exams_count': physical_exams_count,
    }
    return render(request, 'dashboard/user_dashboard.html', context)


@login_required
@staff_member_required
def admin_dashboard(request):
    """Tableau de bord pour les administrateurs"""
    applications = StudentApplication.objects.all().order_by('-application_date')
    
    # Statistiques
    total_applications = applications.count()
    pending_payment = applications.filter(status='PENDING_PAYMENT').count()
    pending_validation = applications.filter(status='PENDING').count()
    reviewing = applications.filter(status='REVIEWING').count()
    accepted = applications.filter(status='ACCEPTED').count()
    rejected = applications.filter(status='REJECTED').count()
    needs_info = applications.filter(status='NEEDS_INFO').count()
    
    # Examens physiques
    physical_exams = PhysicalExamination.objects.select_related('application').all()
    physical_exams_count = physical_exams.count()
    
    # Dernières demandes (5 dernières)
    recent_applications = applications[:10]
    
    context = {
        'applications': applications,
        'recent_applications': recent_applications,
        'total_applications': total_applications,
        'pending_payment': pending_payment,
        'pending_validation': pending_validation,
        'reviewing': reviewing,
        'accepted_applications': accepted,
        'rejected': rejected,
        'needs_info': needs_info,
        'physical_exams': physical_exams,
        'physical_exams_count': physical_exams_count,
    }
    return render(request, 'dashboard/admin_dashboard.html', context)


@login_required
@staff_member_required
def gestion(request):
    """Tableau de bord de gestion des demandes (alias pour admin_dashboard)"""
    return admin_dashboard(request)

# Gardez votre fonction gestion existante ou remplacez-la


