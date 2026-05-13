from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from main_apps.gestion.models import PhysicalExamination, StudentApplication

# core/views.py - Ajoutez cette fonction


@login_required
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
    return render(request, 'gestion/gestion.html', context)
