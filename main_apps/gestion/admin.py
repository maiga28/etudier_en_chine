# main_apps/gestion/admin.py
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from .models import StudentApplication, PhysicalExamination


@admin.register(StudentApplication)
class StudentApplicationAdmin(admin.ModelAdmin):
    """
    Configuration de l'interface admin pour les demandes d'admission
    """
    
    list_display = [
        'full_name_display',
        'nationality',
        'application_date_display',
        'status_colored',
        'age',
        'passport_info',
        'has_physical_exam',
    ]
    
    list_filter = [
        'status',
        'gender',
        'marital_status',
        'nationality',
        'highest_education',
        'application_date',
        'is_emigrant_from_china',
    ]
    
    search_fields = [
        'family_name',
        'given_name',
        'chinese_name',
        'passport_number',
        'nationality',
        'personal_email',
        'guarantor_name',
    ]
    
    readonly_fields = [
        'application_date',
        'created_at',
        'updated_at',
    ]
    
    fieldsets = (
        ('Statut de la demande', {
            'fields': ('status', 'notes', 'application_date')
        }),
        ('Informations personnelles', {
            'fields': (
                'family_name', 'given_name', 'chinese_name', 'gender',
                'marital_status', 'nationality', 'country_of_birth', 'birth_date',
                'place_of_birth', 'native_language', 'highest_education',
                'religion', 'employer_or_institution', 'occupation',
                'health_status', 'is_emigrant_from_china', 'hobby'
            )
        }),
        ('Passeport et Visa', {
            'classes': ('collapse',),
            'fields': ('passport_number', 'passport_expiration_date')
        }),
        ('Formation et Expériences', {
            'classes': ('collapse',),
            'fields': ('education_history', 'work_experience')
        }),
        ('Famille', {
            'classes': ('collapse',),
            'fields': ('family_members',)
        }),
        ('Soutien financier', {
            'fields': (
                'guarantor_name', 'guarantor_address', 'guarantor_tel',
                'guarantor_relationship', 'guarantor_organization', 'guarantor_email'
            )
        }),
        ('Adresses', {
            'fields': (
                'home_address_street', 'home_address_city_province',
                'home_address_country', 'home_address_phone',
                'home_address_mobile', 'home_address_zipcode',
                'same_current_as_home', 'current_address', 'personal_email'
            )
        }),
        ('Médias sociaux', {
            'classes': ('collapse',),
            'fields': (
                'facebook_account', 'wechat_account', 'linkedin_account',
                'twitter_account', 'qq_account', 'msn_account'
            )
        }),
        ('Métadonnées', {
            'classes': ('collapse',),
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    actions = ['mark_as_accepted', 'mark_as_rejected', 'mark_as_reviewing']
    list_per_page = 25
    ordering = ['-application_date']
    list_display_links = ['full_name_display']
    
    def full_name_display(self, obj):
        """Affiche le nom complet avec un lien vers l'édition"""
        if obj.pk:
            url = reverse('admin:gestion_studentapplication_change', args=[obj.pk])
            return format_html('{}','<a href="{}">{} {}</a>', url, obj.family_name, obj.given_name)
        return f"{obj.family_name} {obj.given_name}"
    full_name_display.short_description = "Nom complet"
    full_name_display.admin_order_field = 'family_name'
    
    def application_date_display(self, obj):
        """Affiche la date de soumission formatée"""
        if obj.application_date:
            return obj.application_date.strftime('%d/%m/%Y %H:%M')
        return "N/A"
    application_date_display.short_description = "Date de soumission"
    application_date_display.admin_order_field = 'application_date'
    
    def status_colored(self, obj):
        """Affiche le statut avec une couleur"""
        colors = {
            'PENDING': '#ff9800',
            'REVIEWING': '#2196f3',
            'ACCEPTED': '#4caf50',
            'REJECTED': '#f44336',
            'NEEDS_INFO': '#9c27b0',
        }
        status_display = dict(StudentApplication._meta.get_field('status').choices).get(obj.status, obj.status)
        color = colors.get(obj.status, '#000000')
        return format_html('{}','<span style="color: {}; font-weight: bold;">{}</span>', color, status_display)
    status_colored.short_description = "Statut"
    status_colored.admin_order_field = 'status'
    
    def age(self, obj):
        """Calcule l'âge de l'étudiant"""
        if obj.pk and obj.birth_date:
            today = timezone.now().date()
            age = today.year - obj.birth_date.year
            if today.month < obj.birth_date.month or (today.month == obj.birth_date.month and today.day < obj.birth_date.day):
                age -= 1
            return f"{age} ans"
        return "N/A"
    age.short_description = "Âge"
    
    def passport_info(self, obj):
        """Affiche les informations du passeport"""
        if not obj.pk:
            return obj.passport_number or "N/A"
        
        expiration = obj.passport_expiration_date
        today = timezone.now().date()
        if expiration:
            if expiration < today:
                return format_html('{}','<span style="color: red;">⚠️ Expiré: {}</span>', expiration.strftime('%d/%m/%Y'))
            elif (expiration - today).days < 180:
                return format_html('{}','<span style="color: orange;">⚠️ Expire bientôt: {}</span>', expiration.strftime('%d/%m/%Y'))
            else:
                return format_html('{}','{}<br><small>Exp: {}</small>', obj.passport_number, expiration.strftime('%d/%m/%Y'))
        return obj.passport_number
    passport_info.short_description = "Passeport"
    
    def has_physical_exam(self, obj):
        """Indique si l'étudiant a un examen physique associé"""
        if not obj.pk:
            return format_html('{}','<span style="color: gray;">-</span>')
        
        try:
            if hasattr(obj, 'physical_examination') and obj.physical_examination:
                return format_html('{}','<span style="color: green;">✓ Complet</span>')
        except PhysicalExamination.DoesNotExist:
            pass
        return format_html('{}','<span style="color: red;">✗ Non complété</span>')
    has_physical_exam.short_description = "Examen physique"
    
    def mark_as_accepted(self, request, queryset):
        updated = queryset.update(status='ACCEPTED')
        self.message_user(request, f'{updated} demande(s) ont été acceptée(s).')
    mark_as_accepted.short_description = "Marquer comme acceptée"
    
    def mark_as_rejected(self, request, queryset):
        updated = queryset.update(status='REJECTED')
        self.message_user(request, f'{updated} demande(s) ont été rejetée(s).')
    mark_as_rejected.short_description = "Marquer comme rejetée"
    
    def mark_as_reviewing(self, request, queryset):
        updated = queryset.update(status='REVIEWING')
        self.message_user(request, f'{updated} demande(s) sont en cours d\'examen.')
    mark_as_reviewing.short_description = "Marquer comme en cours d'examen"


@admin.register(PhysicalExamination)
class PhysicalExaminationAdmin(admin.ModelAdmin):
    """
    Configuration de l'interface admin pour les examens physiques
    """
    
    list_display = [
        'name',
        'gender',
        'birth_date',
        'age_display',
        'blood_type_display',
        'health_status_badge',
        'examination_date_display',
        'linked_application'
    ]
    
    list_filter = [
        'gender',
        'blood_type',
        'hiv_test_result',
        'syphilis_test_result',
        'is_medically_fit',
        'examination_date',
    ]
    
    search_fields = [
        'name',
        'nationality',
        'physician_signature',
        'application__family_name',
        'application__given_name',
    ]
    
    readonly_fields = [
        'created_at',
        'updated_at',
    ]
    
    fieldsets = (
        ('Informations de base', {
            'fields': (
                'application', 'name', 'gender', 'birth_date',
                'present_mailing_address', 'nationality', 'birth_place', 'blood_type'
            )
        }),
        ('Signes vitaux', {
            'fields': ('height_cm', 'weight_kg', 'blood_pressure_systolic', 'blood_pressure_diastolic')
        }),
        ('Examens physiques', {
            'fields': (
                'development', 'nourishment', 'neck',
                'vision_left', 'vision_right', 'corrected_vision_left', 
                'corrected_vision_right', 'colour_sense',
                'skin', 'lymph_nodes', 'ears', 'nose', 'tonsils',
                'heart', 'lungs', 'abdomen', 'spine', 'extremities', 
                'nervous_system', 'other_findings'
            )
        }),
        ('Examens complémentaires', {
            'fields': ('ecg_result', 'chest_xray_result', 'chest_xray_report')
        }),
        ('Analyses de laboratoire', {
            'fields': ('hiv_test_result', 'syphilis_test_result', 'lab_report')
        }),
        ('Avis médical', {
            'fields': ('medical_opinion', 'is_medically_fit', 'physician_signature', 'examination_date')
        }),
        ('Métadonnées', {
            'classes': ('collapse',),
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    list_per_page = 25
    ordering = ['-examination_date']
    
    def age_display(self, obj):
        """Affiche l'âge"""
        if obj.pk and obj.birth_date:
            today = timezone.now().date()
            age = today.year - obj.birth_date.year
            if today.month < obj.birth_date.month or (today.month == obj.birth_date.month and today.day < obj.birth_date.day):
                age -= 1
            return f"{age} ans"
        return "N/A"
    age_display.short_description = "Âge"
    
    def blood_type_display(self, obj):
        """Affiche le groupe sanguin"""
        if obj.blood_type:
            return obj.blood_type
        return 'Non renseigné'
    blood_type_display.short_description = "Groupe sanguin"
    
    def examination_date_display(self, obj):
        """Affiche la date d'examen formatée"""
        if obj.examination_date:
            return obj.examination_date.strftime('%d/%m/%Y')
        return 'N/A'
    examination_date_display.short_description = "Date d'examen"
    
    def health_status_badge(self, obj):
        """Affiche un badge indiquant l'état de santé"""
        if not obj.pk:
            return format_html('{}','<span style="color: gray;">En attente</span>')
        
        if obj.is_medically_fit and obj.is_healthy():
            return format_html('{}','<span style="background-color: #4caf50; color: white; padding: 3px 8px; border-radius: 3px;">✓ APTE</span>')
        else:
            return format_html('{}','<span style="background-color: #f44336; color: white; padding: 3px 8px; border-radius: 3px;">✗ INAPTE</span>')
    health_status_badge.short_description = "Aptitude"
    
    def linked_application(self, obj):
        """Lien vers la demande associée"""
        if obj.pk and obj.application:
            url = reverse('admin:gestion_studentapplication_change', args=[obj.application.id])
            return format_html('{}','<a href="{}">{} {}</a>', url, obj.application.family_name, obj.application.given_name)
        return "Non associé"
    linked_application.short_description = "Demande associée"
    
    def save_model(self, request, obj, form, change):
        """Sauvegarde le modèle"""
        super().save_model(request, obj, form, change)


# Configuration du titre de l'administration
admin.site.site_header = "Administration Étudier En Chine"
admin.site.site_title = "Étudier En Chine"
admin.site.index_title = "Bienvenue dans l'administration"