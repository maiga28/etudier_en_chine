# main_apps/gestion/forms.py
from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import StudentApplication, PhysicalExamination
import datetime


class StudentApplicationForm(forms.ModelForm):
    """
    Formulaire pour la demande d'admission
    """
    
    # Champs supplémentaires pour l'historique d'éducation (non stockés directement)
    education_entries = forms.JSONField(
        required=False,
        widget=forms.HiddenInput()
    )
    work_entries = forms.JSONField(
        required=False,
        widget=forms.HiddenInput()
    )
    family_entries = forms.JSONField(
        required=False,
        widget=forms.HiddenInput()
    )
    
    class Meta:
        model = StudentApplication
        fields = [
            # Informations personnelles
            'family_name', 'given_name', 'chinese_name', 'gender',
            'marital_status', 'nationality', 'country_of_birth', 'birth_date',
            'place_of_birth', 'native_language', 'highest_education', 'religion',
            'employer_or_institution', 'occupation', 'health_status',
            'is_emigrant_from_china', 'hobby',
            
            # Passeport
            'passport_number', 'passport_expiration_date',
            
            # Expériences
            'education_history', 'work_experience', 'family_members',
            
            # Soutien financier
            'guarantor_name', 'guarantor_address', 'guarantor_tel',
            'guarantor_relationship', 'guarantor_organization', 'guarantor_email',
            
            # Adresses
            'home_address_street', 'home_address_city_province', 'home_address_country',
            'home_address_phone', 'home_address_mobile', 'home_address_zipcode',
            'same_current_as_home', 'current_address', 'personal_email',
            
            # Réseaux sociaux
            'facebook_account', 'wechat_account', 'linkedin_account',
            'twitter_account', 'qq_account', 'msn_account',
        ]
        widgets = {
            'family_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500',
                'placeholder': 'Ex: DUPONT'
            }),
            'given_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500',
                'placeholder': 'Ex: Jean'
            }),
            'chinese_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500',
                'placeholder': 'Nom chinois (si disponible)'
            }),
            'gender': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500'
            }),
            'marital_status': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500'
            }),
            'nationality': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500',
                'placeholder': 'Ex: Française'
            }),
            'country_of_birth': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500'
            }),
            'birth_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500'
            }),
            'place_of_birth': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500',
                'placeholder': 'Ville, Province'
            }),
            'native_language': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500'
            }),
            'highest_education': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500'
            }),
            'religion': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500'
            }),
            'employer_or_institution': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500'
            }),
            'occupation': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500'
            }),
            'health_status': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500'
            }),
            'is_emigrant_from_china': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-red-600 focus:ring-red-500'
            }),
            'hobby': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500'
            }),
            'passport_number': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500',
                'placeholder': 'Ex: 123456789'
            }),
            'passport_expiration_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500'
            }),
            'guarantor_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500'
            }),
            'guarantor_address': forms.Textarea(attrs={
                'rows': 3,
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500'
            }),
            'guarantor_tel': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500',
                'placeholder': '+33 1 23 45 67 89'
            }),
            'guarantor_relationship': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500',
                'placeholder': 'Parent, tuteur, etc.'
            }),
            'guarantor_organization': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500'
            }),
            'guarantor_email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500',
                'placeholder': 'email@example.com'
            }),
            'home_address_street': forms.Textarea(attrs={
                'rows': 2,
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500'
            }),
            'home_address_city_province': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500'
            }),
            'home_address_country': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500'
            }),
            'home_address_phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500'
            }),
            'home_address_mobile': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500'
            }),
            'home_address_zipcode': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500'
            }),
            'same_current_as_home': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-red-600 focus:ring-red-500'
            }),
            'current_address': forms.Textarea(attrs={
                'rows': 2,
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500'
            }),
            'personal_email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500'
            }),
            'facebook_account': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500'
            }),
            'wechat_account': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500'
            }),
            'linkedin_account': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500'
            }),
            'twitter_account': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500'
            }),
            'qq_account': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500'
            }),
            'msn_account': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500'
            }),
        }
    
    def clean_passport_number(self):
        passport = self.cleaned_data.get('passport_number')
        if passport and len(passport) < 5:
            raise ValidationError("Le numéro de passeport doit contenir au moins 5 caractères.")
        return passport
    
    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')
        if birth_date:
            today = timezone.now().date()
            age = today.year - birth_date.year
            if age < 16:
                raise ValidationError("Vous devez avoir au moins 16 ans pour faire une demande.")
            if age > 60:
                raise ValidationError("L'âge maximum pour une demande est de 60 ans.")
        return birth_date
    
    def clean_passport_expiration_date(self):
        exp_date = self.cleaned_data.get('passport_expiration_date')
        if exp_date and exp_date <= timezone.now().date():
            raise ValidationError("Le passeport est déjà expiré ou expire aujourd'hui.")
        return exp_date
    
    def clean_personal_email(self):
        email = self.cleaned_data.get('personal_email')
        if email and '@' not in email:
            raise ValidationError("Veuillez entrer une adresse email valide.")
        return email
    
    def clean(self):
        cleaned_data = super().clean()
        
        # Validation du formulaire d'éducation (au moins une entrée)
        education_history = cleaned_data.get('education_history', [])
        if not education_history:
            self.add_error('education_history', "Veuillez ajouter au moins une formation.")
        
        # Validation des membres de la famille (au moins 2)
        family_members = cleaned_data.get('family_members', [])
        if len(family_members) < 2:
            self.add_error('family_members', "Veuillez renseigner au moins 2 membres de la famille.")
        
        # Validation des numéros de téléphone
        tel = cleaned_data.get('guarantor_tel', '')
        if tel and len(tel) < 8:
            self.add_error('guarantor_tel', "Le numéro de téléphone semble trop court.")
        
        return cleaned_data


class EducationEntryForm(forms.Form):
    """Formulaire pour une entrée de formation"""
    from_year = forms.IntegerField(label="Année de début", min_value=1950, max_value=timezone.now().year)
    to_year = forms.IntegerField(label="Année de fin", min_value=1950, max_value=timezone.now().year + 5)
    school_name = forms.CharField(label="Nom de l'établissement", max_length=200)
    field_of_study = forms.CharField(label="Domaine d'étude", max_length=200)
    diploma_received = forms.CharField(label="Diplôme obtenu", max_length=200, required=False)
    
    def clean(self):
        cleaned_data = super().clean()
        from_year = cleaned_data.get('from_year')
        to_year = cleaned_data.get('to_year')
        
        if from_year and to_year and from_year > to_year:
            raise ValidationError("L'année de début ne peut pas être postérieure à l'année de fin.")
        
        return cleaned_data


class WorkEntryForm(forms.Form):
    """Formulaire pour une expérience professionnelle"""
    from_year = forms.IntegerField(label="Année de début", min_value=1950, max_value=timezone.now().year)
    to_year = forms.IntegerField(label="Année de fin", min_value=1950, max_value=timezone.now().year + 5)
    company_name = forms.CharField(label="Nom de l'entreprise", max_length=200)
    position = forms.CharField(label="Poste occupé", max_length=100)
    
    def clean(self):
        cleaned_data = super().clean()
        from_year = cleaned_data.get('from_year')
        to_year = cleaned_data.get('to_year')
        
        if from_year and to_year and from_year > to_year:
            raise ValidationError("L'année de début ne peut pas être postérieure à l'année de fin.")
        
        return cleaned_data


class FamilyMemberForm(forms.Form):
    """Formulaire pour un membre de la famille"""
    member_type = forms.ChoiceField(
        label="Lien de parenté",
        choices=[
            ('FATHER', 'Père'),
            ('MOTHER', 'Mère'),
            ('BROTHER', 'Frère'),
            ('SISTER', 'Sœur'),
            ('SPOUSE', 'Conjoint(e)'),
            ('CHILD', 'Enfant'),
            ('OTHER', 'Autre'),
        ]
    )
    name = forms.CharField(label="Nom", max_length=200)
    phone_number = forms.CharField(label="Numéro de téléphone", max_length=50, required=False)
    email = forms.EmailField(label="Email", required=False)
    position = forms.CharField(label="Profession", max_length=100, required=False)
    work_place = forms.CharField(label="Lieu de travail", max_length=200, required=False)


class PhysicalExaminationForm(forms.ModelForm):
    """
    Formulaire pour l'examen physique
    """
    
    class Meta:
        model = PhysicalExamination
        exclude = ['application', 'created_at', 'updated_at']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500'
            }),
            'gender': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500'
            }),
            'birth_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500'
            }),
            'present_mailing_address': forms.Textarea(attrs={
                'rows': 2,
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500'
            }),
            'nationality': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500'
            }),
            'birth_place': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500'
            }),
            'blood_type': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500'
            }),
            'height_cm': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500',
                'step': '0.1'
            }),
            'weight_kg': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500',
                'step': '0.1'
            }),
            'blood_pressure_systolic': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500'
            }),
            'blood_pressure_diastolic': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500'
            }),
            'vision_left': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500',
                'placeholder': 'Ex: 10/10'
            }),
            'vision_right': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500',
                'placeholder': 'Ex: 10/10'
            }),
            'corrected_vision_left': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500'
            }),
            'corrected_vision_right': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500'
            }),
            'colour_sense': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500'
            }),
            'development': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500'
            }),
            'nourishment': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500'
            }),
            'neck': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500'
            }),
            'skin': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500'
            }),
            'lymph_nodes': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500'
            }),
            'ears': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500'
            }),
            'nose': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500'
            }),
            'tonsils': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500'
            }),
            'heart': forms.Textarea(attrs={
                'rows': 2,
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500'
            }),
            'lungs': forms.Textarea(attrs={
                'rows': 2,
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500'
            }),
            'abdomen': forms.Textarea(attrs={
                'rows': 2,
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500'
            }),
            'spine': forms.Textarea(attrs={
                'rows': 2,
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500'
            }),
            'extremities': forms.Textarea(attrs={
                'rows': 2,
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500'
            }),
            'nervous_system': forms.Textarea(attrs={
                'rows': 2,
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500'
            }),
            'other_findings': forms.Textarea(attrs={
                'rows': 2,
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500'
            }),
            'ecg_result': forms.Textarea(attrs={
                'rows': 2,
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500'
            }),
            'chest_xray_result': forms.Textarea(attrs={
                'rows': 2,
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500'
            }),
            'hiv_test_result': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500'
            }),
            'syphilis_test_result': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500'
            }),
            'medical_opinion': forms.Textarea(attrs={
                'rows': 3,
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500'
            }),
            'is_medically_fit': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-red-600 focus:ring-red-500'
            }),
            'physician_signature': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500'
            }),
            'examination_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500'
            }),
        }
    
    def clean_height_cm(self):
        height = self.cleaned_data.get('height_cm')
        if height and (height < 50 or height > 250):
            raise ValidationError("La taille doit être comprise entre 50 cm et 250 cm.")
        return height
    
    def clean_weight_kg(self):
        weight = self.cleaned_data.get('weight_kg')
        if weight and (weight < 10 or weight > 300):
            raise ValidationError("Le poids doit être compris entre 10 kg et 300 kg.")
        return weight
    
    def clean_blood_pressure(self):
        systolic = self.cleaned_data.get('blood_pressure_systolic')
        diastolic = self.cleaned_data.get('blood_pressure_diastolic')
        
        if systolic and diastolic:
            if systolic < diastolic:
                raise ValidationError("La pression systolique doit être supérieure à la pression diastolique.")
            if systolic < 70 or systolic > 250:
                raise ValidationError("La pression systolique semble anormale.")
            if diastolic < 40 or diastolic > 150:
                raise ValidationError("La pression diastolique semble anormale.")
        
        return self.cleaned_data