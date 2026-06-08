from django.db import models

# Create your models here.
# main_apps/gestion/models.py
from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator
from django.utils import timezone

# Create your models here.
from django.db import models
from django.core.validators import MinLengthValidator
from django.utils import timezone
import json
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


# main_apps/gestion/models.py
from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator
from django.utils import timezone
from django.conf import settings
import json

class StudentApplication(models.Model):
    """
    Modèle pour le formulaire d'admission (入学申请表)
    """
    
    # === Lien avec l'utilisateur (AJOUTÉ) ===
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='applications',
        null=True,
        blank=True,
        verbose_name="Utilisateur"
    )
    
    # === Informations personnelles ===
    family_name = models.CharField(
        max_length=100,
        verbose_name="Nom de famille (comme sur le passeport)",
        help_text="Family Name (as on passport)"
    )
    given_name = models.CharField(
        max_length=100,
        verbose_name="Prénom (comme sur le passeport)",
        help_text="Given Name (as on passport)"
    )
    chinese_name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Nom chinois",
        help_text="Chinese Name (if available)"
    )
    
    # === Genre ===
    class Gender(models.TextChoices):
        MALE = 'M', 'Masculin'
        FEMALE = 'F', 'Féminin'
    
    gender = models.CharField(
        max_length=1,
        choices=Gender.choices,
        verbose_name="Genre"
    )
    
    # === Situation familiale ===
    class MaritalStatus(models.TextChoices):
        SINGLE = 'SINGLE', 'Célibataire'
        MARRIED = 'MARRIED', 'Marié(e)'
        DIVORCED = 'DIVORCED', 'Divorcé(e)'
        WIDOWED = 'WIDOWED', 'Veuf/Veuve'
    
    marital_status = models.CharField(
        max_length=20,
        choices=MaritalStatus.choices,
        verbose_name="Situation matrimoniale"
    )
    
    nationality = models.CharField(
        max_length=100,
        verbose_name="Nationalité"
    )
    country_of_birth = models.CharField(
        max_length=100,
        verbose_name="Pays de naissance"
    )
    birth_date = models.DateField(
        verbose_name="Date de naissance"
    )
    place_of_birth = models.CharField(
        max_length=200,
        verbose_name="Lieu de naissance (Ville, Province)"
    )
    native_language = models.CharField(
        max_length=100,
        verbose_name="Langue maternelle"
    )
    
    # === Éducation ===
    class EducationLevel(models.TextChoices):
        HIGH_SCHOOL = 'HIGH_SCHOOL', 'Lycée'
        BACHELOR = 'BACHELOR', 'Licence'
        MASTER = 'MASTER', 'Master'
        DOCTORATE = 'DOCTORATE', 'Doctorat'
    
    highest_education = models.CharField(
        max_length=20,
        choices=EducationLevel.choices,
        verbose_name="Plus haut niveau d'éducation"
    )
    
    religion = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Religion"
    )
    
    employer_or_institution = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Employeur ou institution affiliée"
    )
    occupation = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Profession"
    )
    
    # === Santé / Hobbies ===
    class HealthStatus(models.TextChoices):
        EXCELLENT = 'EXCELLENT', 'Excellent'
        GOOD = 'GOOD', 'Bon'
        FAIR = 'FAIR', 'Moyen'
        POOR = 'POOR', 'Mauvais'
    
    health_status = models.CharField(
        max_length=20,
        choices=HealthStatus.choices,
        default='GOOD',
        verbose_name="État de santé"
    )
    
    is_emigrant_from_china = models.BooleanField(
        default=False,
        verbose_name="Émigrant de Chine continentale, Hong Kong, Macao ou Taïwan ?"
    )
    
    hobby = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Loisirs"
    )
    
    # === Passeport et Visa ===
    passport_number = models.CharField(
        max_length=50,
        validators=[MinLengthValidator(5)],
        verbose_name="Numéro de passeport"
    )
    passport_expiration_date = models.DateField(
        verbose_name="Date d'expiration du passeport"
    )
    
    # === Formation académique (JSON) ===
    education_history = models.JSONField(
        default=list,
        verbose_name="Historique des formations",
        help_text="Liste des formations (lycée et supérieur)"
    )
    
    # === Expérience professionnelle (JSON) ===
    work_experience = models.JSONField(
        default=list,
        verbose_name="Expérience professionnelle",
        help_text="Liste des expériences professionnelles"
    )
    
    # === Famille (JSON) ===
    family_members = models.JSONField(
        default=list,
        verbose_name="Membres de la famille",
        help_text="Au moins 2 membres de la famille"
    )
    
    # === Soutien financier ===
    guarantor_name = models.CharField(
        max_length=200,
        verbose_name="Nom du garant"
    )
    guarantor_address = models.TextField(
        verbose_name="Adresse du garant"
    )
    guarantor_tel = models.CharField(
        max_length=50,
        verbose_name="Téléphone du garant"
    )
    guarantor_relationship = models.CharField(
        max_length=100,
        verbose_name="Lien avec le garant"
    )
    guarantor_organization = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Organisation du garant"
    )
    guarantor_email = models.EmailField(
        blank=True,
        null=True,
        verbose_name="Email du garant"
    )
    
    # === Adresses ===
    home_address_street = models.TextField(
        verbose_name="Adresse domicile (rue)"
    )
    home_address_city_province = models.CharField(
        max_length=200,
        verbose_name="Ville/Province"
    )
    home_address_country = models.CharField(
        max_length=100,
        verbose_name="Pays"
    )
    home_address_phone = models.CharField(
        max_length=50,
        verbose_name="Téléphone domicile"
    )
    home_address_mobile = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Mobile domicile"
    )
    home_address_zipcode = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Code postal"
    )
    
    same_current_as_home = models.BooleanField(
        default=True,
        verbose_name="Adresse actuelle identique à l'adresse domicile"
    )
    current_address = models.TextField(
        blank=True,
        null=True,
        verbose_name="Adresse actuelle"
    )
    personal_email = models.EmailField(
        verbose_name="Email personnel"
    )
    
    # === Réseaux sociaux ===
    facebook_account = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Facebook"
    )
    wechat_account = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="WeChat"
    )
    linkedin_account = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="LinkedIn"
    )
    twitter_account = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Twitter"
    )
    qq_account = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="QQ"
    )
    msn_account = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="MSN"
    )
    
    # === Statut de la demande ===
    class Status(models.TextChoices):
        PENDING_PAYMENT = 'PENDING_PAYMENT', 'En attente de paiement'
        PENDING = 'PENDING', 'En attente de validation'
        REVIEWING = 'REVIEWING', 'En cours d\'examen'
        ACCEPTED = 'ACCEPTED', 'Acceptée'
        REJECTED = 'REJECTED', 'Rejetée'
        NEEDS_INFO = 'NEEDS_INFO', 'Informations complémentaires requises'
    
    status = models.CharField(
        max_length=20,
        default=Status.PENDING_PAYMENT,
        choices=Status.choices,
        verbose_name="Statut"
    )
    
    # === Métadonnées ===
    application_date = models.DateTimeField(
        default=timezone.now,
        verbose_name="Date de soumission"
    )
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name="Notes"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Demande d'admission"
        verbose_name_plural = "Demandes d'admission"
        ordering = ['-application_date']
        # Contrainte: un utilisateur ne peut avoir qu'une seule demande par passeport
        unique_together = ['user', 'passport_number']
    
    def __str__(self):
        return f"{self.family_name} {self.given_name} - {self.application_date.strftime('%Y-%m-%d')}"
    
    @property
    def full_name(self):
        return f"{self.family_name} {self.given_name}"
    
    @property
    def age(self):
        """Calcule l'âge à partir de la date de naissance"""
        if self.birth_date:
            today = timezone.now().date()
            age = today.year - self.birth_date.year
            if today.month < self.birth_date.month or (today.month == self.birth_date.month and today.day < self.birth_date.day):
                age -= 1
            return age
        return None

'''class StudentApplication(models.Model):
    """
    Modèle pour le formulaire d'admission (入学申请表)
    """
    
    # === Informations personnelles ===
    family_name = models.CharField(
        max_length=100,
        verbose_name="Nom de famille (comme sur le passeport)",
        help_text="Family Name (as on passport)"
    )
    given_name = models.CharField(
        max_length=100,
        verbose_name="Prénom (comme sur le passeport)",
        help_text="Given Name (as on passport)"
    )
    chinese_name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Nom chinois",
        help_text="Chinese Name (if available)"
    )
    
    # === Genre ===
    class Gender(models.TextChoices):
        MALE = 'M', 'Masculin'
        FEMALE = 'F', 'Féminin'
    
    gender = models.CharField(
        max_length=1,
        choices=Gender.choices,
        verbose_name="Genre"
    )
    
    # === Situation familiale ===
    class MaritalStatus(models.TextChoices):
        SINGLE = 'SINGLE', 'Célibataire'
        MARRIED = 'MARRIED', 'Marié(e)'
        DIVORCED = 'DIVORCED', 'Divorcé(e)'
        WIDOWED = 'WIDOWED', 'Veuf/Veuve'
    
    marital_status = models.CharField(
        max_length=20,
        choices=MaritalStatus.choices,
        verbose_name="Situation matrimoniale"
    )
    
    nationality = models.CharField(
        max_length=100,
        verbose_name="Nationalité"
    )
    country_of_birth = models.CharField(
        max_length=100,
        verbose_name="Pays de naissance"
    )
    birth_date = models.DateField(
        verbose_name="Date de naissance"
    )
    place_of_birth = models.CharField(
        max_length=200,
        verbose_name="Lieu de naissance (Ville, Province)"
    )
    native_language = models.CharField(
        max_length=100,
        verbose_name="Langue maternelle"
    )
    
    # === Éducation ===
    class EducationLevel(models.TextChoices):
        HIGH_SCHOOL = 'HIGH_SCHOOL', 'Lycée'
        BACHELOR = 'BACHELOR', 'Licence'
        MASTER = 'MASTER', 'Master'
        DOCTORATE = 'DOCTORATE', 'Doctorat'
    
    highest_education = models.CharField(
        max_length=20,
        choices=EducationLevel.choices,
        verbose_name="Plus haut niveau d'éducation"
    )
    
    religion = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Religion"
    )
    
    employer_or_institution = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Employeur ou institution affiliée"
    )
    occupation = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Profession"
    )
    
    # === Santé / Hobbies ===
    class HealthStatus(models.TextChoices):
        EXCELLENT = 'EXCELLENT', 'Excellent'
        GOOD = 'GOOD', 'Bon'
        FAIR = 'FAIR', 'Moyen'
        POOR = 'POOR', 'Mauvais'
    
    health_status = models.CharField(
        max_length=20,
        choices=HealthStatus.choices,
        default='GOOD',
        verbose_name="État de santé"
    )
    
    is_emigrant_from_china = models.BooleanField(
        default=False,
        verbose_name="Émigrant de Chine continentale, Hong Kong, Macao ou Taïwan ?"
    )
    
    hobby = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Loisirs"
    )
    
    # === Passeport et Visa ===
    passport_number = models.CharField(
        max_length=50,
        validators=[MinLengthValidator(5)],
        verbose_name="Numéro de passeport"
    )
    passport_expiration_date = models.DateField(
        verbose_name="Date d'expiration du passeport"
    )
    
    # === Formation académique ===
    class EducationEntry(models.Model):
        """Sous-modèle pour les entrées de formation"""
        from_year = models.IntegerField()
        to_year = models.IntegerField()
        school_name = models.CharField(max_length=200)
        field_of_study = models.CharField(max_length=200)
        diploma_received = models.CharField(max_length=200, blank=True)
    
    # Utilisation d'un JSONField pour stocker l'historique des formations
    education_history = models.JSONField(
        default=list,
        verbose_name="Historique des formations",
        help_text="Liste des formations (lycée et supérieur)"
    )
    
    # === Expérience professionnelle ===
    work_experience = models.JSONField(
        default=list,
        verbose_name="Expérience professionnelle",
        help_text="Liste des expériences professionnelles"
    )
    
    # === Famille ===
    family_members = models.JSONField(
        default=list,
        verbose_name="Membres de la famille",
        help_text="Au moins 2 membres de la famille"
    )
    
    # === Soutien financier ===
    guarantor_name = models.CharField(
        max_length=200,
        verbose_name="Nom du garant"
    )
    guarantor_address = models.TextField(
        verbose_name="Adresse du garant"
    )
    guarantor_tel = models.CharField(
        max_length=50,
        verbose_name="Téléphone du garant"
    )
    guarantor_relationship = models.CharField(
        max_length=100,
        verbose_name="Lien avec le garant"
    )
    guarantor_organization = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Organisation du garant"
    )
    guarantor_email = models.EmailField(
        blank=True,
        null=True,
        verbose_name="Email du garant"
    )
    
    # === Adresses ===
    home_address_street = models.TextField(
        verbose_name="Adresse domicile (rue)"
    )
    home_address_city_province = models.CharField(
        max_length=200,
        verbose_name="Ville/Province"
    )
    home_address_country = models.CharField(
        max_length=100,
        verbose_name="Pays"
    )
    home_address_phone = models.CharField(
        max_length=50,
        verbose_name="Téléphone domicile"
    )
    home_address_mobile = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Mobile domicile"
    )
    home_address_zipcode = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Code postal"
    )
    
    same_current_as_home = models.BooleanField(
        default=True,
        verbose_name="Adresse actuelle identique à l'adresse domicile"
    )
    current_address = models.TextField(
        blank=True,
        null=True,
        verbose_name="Adresse actuelle"
    )
    personal_email = models.EmailField(
        verbose_name="Email personnel"
    )
    
    # === Réseaux sociaux ===
    facebook_account = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Facebook"
    )
    wechat_account = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="WeChat"
    )
    linkedin_account = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="LinkedIn"
    )
    twitter_account = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Twitter"
    )
    qq_account = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="QQ"
    )
    msn_account = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="MSN"
    )
    
    # === Métadonnées ===
    application_date = models.DateTimeField(
        default=timezone.now,
        verbose_name="Date de soumission"
    )
    status = models.CharField(
        max_length=20,
        default='PENDING',
        choices=[
            ('PENDING', 'En attente'),
            ('REVIEWING', 'En cours d\'examen'),
            ('ACCEPTED', 'Acceptée'),
            ('REJECTED', 'Rejetée'),
            ('NEEDS_INFO', 'Informations complémentaires requises'),
        ],
        verbose_name="Statut"
    )
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name="Notes"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Demande d'admission"
        verbose_name_plural = "Demandes d'admission"
        ordering = ['-application_date']
    
    def __str__(self):
        return f"{self.family_name} {self.given_name} - {self.application_date.strftime('%Y-%m-%d')}"
    
    @property
    def full_name(self):
        return f"{self.family_name} {self.given_name}"
    #property pour afficher le statut de manière plus lisible
    @property
    def status_display(self):
        return self.Status(self.status).label

    class Status(models.TextChoices):
        PENDING_PAYMENT = 'PENDING_PAYMENT', 'En attente de paiement'
        PENDING = 'PENDING', 'En attente'
        REVIEWING = 'REVIEWING', 'En cours d\'examen'
        ACCEPTED = 'ACCEPTED', 'Acceptée'
        REJECTED = 'REJECTED', 'Rejetée'
        NEEDS_INFO = 'NEEDS_INFO', 'Informations complémentaires requises' '''


class PhysicalExamination(models.Model):
    """
    Modèle pour l'examen physique (外国人体格检查表)
    """
    
    # === Informations de base ===
    name = models.CharField(max_length=200, verbose_name="Nom")
    gender = models.CharField(
        max_length=1,
        choices=[('M', 'Masculin'), ('F', 'Féminin')],
        verbose_name="Sexe"
    )
    birth_date = models.DateField(verbose_name="Date de naissance")
    present_mailing_address = models.TextField(verbose_name="Adresse actuelle")
    nationality = models.CharField(max_length=100, verbose_name="Nationalité")
    birth_place = models.CharField(max_length=200, verbose_name="Lieu de naissance")
    blood_type = models.CharField(
        max_length=3,
        blank=True,
        null=True,
        choices=[('A', 'A'), ('B', 'B'), ('AB', 'AB'), ('O', 'O')],
        verbose_name="Groupe sanguin"
    )
    
    # === Antécédents médicaux (Yes/No) ===
    has_typhus_fever = models.BooleanField(default=False, verbose_name="Typhus")
    has_bacillary_dysentery = models.BooleanField(default=False, verbose_name="Dysenterie bacillaire")
    has_poliomyelitis = models.BooleanField(default=False, verbose_name="Poliomyélite")
    has_brucellosis = models.BooleanField(default=False, verbose_name="Brucellose")
    has_diphtheria = models.BooleanField(default=False, verbose_name="Diphtérie")
    has_viral_hepatitis = models.BooleanField(default=False, verbose_name="Hépatite virale")
    has_scarlet_fever = models.BooleanField(default=False, verbose_name="Scarlatine")
    has_puerperal_infection = models.BooleanField(default=False, verbose_name="Infection post-partum")
    has_relapsing_fever = models.BooleanField(default=False, verbose_name="Fièvre récurrente")
    has_typhoid_paratyphoid = models.BooleanField(default=False, verbose_name="Typhoïde et paratyphoïde")
    has_epidemic_meningitis = models.BooleanField(default=False, verbose_name="Méningite cérébrospinale")
    
    # === Troubles psychiatriques ===
    has_toxicomania = models.BooleanField(default=False, verbose_name="Toxicomanie")
    has_mental_confusion = models.BooleanField(default=False, verbose_name="Confusion mentale")
    has_manic_psychosis = models.BooleanField(default=False, verbose_name="Psychose maniaque")
    has_paranoid_psychosis = models.BooleanField(default=False, verbose_name="Psychose paranoïaque")
    has_hallucinatory_psychosis = models.BooleanField(default=False, verbose_name="Psychose hallucinatoire")
    
    # === Examens physiques ===
    height_cm = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True, verbose_name="Taille (cm)")
    weight_kg = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True, verbose_name="Poids (kg)")
    blood_pressure_systolic = models.IntegerField(null=True, blank=True, verbose_name="Pression systolique")
    blood_pressure_diastolic = models.IntegerField(null=True, blank=True, verbose_name="Pression diastolique")
    
    development = models.CharField(max_length=100, blank=True, verbose_name="Développement")
    nourishment = models.CharField(max_length=100, blank=True, verbose_name="Nutrition")
    neck = models.CharField(max_length=100, blank=True, verbose_name="Cou")
    
    vision_left = models.CharField(max_length=20, blank=True, verbose_name="Vision gauche")
    vision_right = models.CharField(max_length=20, blank=True, verbose_name="Vision droite")
    corrected_vision_left = models.CharField(max_length=20, blank=True, verbose_name="Vision corrigée gauche")
    corrected_vision_right = models.CharField(max_length=20, blank=True, verbose_name="Vision corrigée droite")
    colour_sense = models.CharField(max_length=50, blank=True, verbose_name="Vision des couleurs")
    
    skin = models.CharField(max_length=100, blank=True, verbose_name="Peau")
    lymph_nodes = models.CharField(max_length=100, blank=True, verbose_name="Ganglions lymphatiques")
    ears = models.CharField(max_length=100, blank=True, verbose_name="Oreilles")
    nose = models.CharField(max_length=100, blank=True, verbose_name="Nez")
    tonsils = models.CharField(max_length=100, blank=True, verbose_name="Amygdales")
    heart = models.CharField(max_length=200, blank=True, verbose_name="Cœur")
    lungs = models.CharField(max_length=200, blank=True, verbose_name="Poumons")
    abdomen = models.CharField(max_length=200, blank=True, verbose_name="Abdomen")
    spine = models.CharField(max_length=200, blank=True, verbose_name="Colonne vertébrale")
    extremities = models.CharField(max_length=200, blank=True, verbose_name="Extrémités")
    nervous_system = models.CharField(max_length=200, blank=True, verbose_name="Système nerveux")
    other_findings = models.TextField(blank=True, null=True, verbose_name="Autres observations")
    
    # === Examens complémentaires ===
    ecg_result = models.TextField(blank=True, null=True, verbose_name="Résultat ECG")
    chest_xray_result = models.TextField(blank=True, null=True, verbose_name="Résultat radiographie pulmonaire")
    chest_xray_report = models.FileField(
        upload_to='exams/chest_xray/',
        blank=True,
        null=True,
        verbose_name="Rapport radiographie pulmonaire"
    )
    
    # === Analyses de laboratoire ===
    hiv_test_result = models.CharField(
        max_length=20,
        blank=True,
        choices=[('NEGATIVE', 'Négatif'), ('POSITIVE', 'Positif'), ('PENDING', 'En attente')],
        verbose_name="Test VIH"
    )
    syphilis_test_result = models.CharField(
        max_length=20,
        blank=True,
        choices=[('NEGATIVE', 'Négatif'), ('POSITIVE', 'Positif'), ('PENDING', 'En attente')],
        verbose_name="Test Syphilis"
    )
    lab_report = models.FileField(
        upload_to='exams/lab/',
        blank=True,
        null=True,
        verbose_name="Rapport de laboratoire"
    )
    
    # === Maladies infectieuses ===
    has_cholera = models.BooleanField(default=False, verbose_name="Choléra")
    has_yellow_fever = models.BooleanField(default=False, verbose_name="Fièvre jaune")
    has_plague = models.BooleanField(default=False, verbose_name="Peste")
    has_leprosy = models.BooleanField(default=False, verbose_name="Lèpre")
    has_venereal_disease = models.BooleanField(default=False, verbose_name="Maladie vénérienne")
    has_lung_tuberculosis = models.BooleanField(default=False, verbose_name="Tuberculose pulmonaire")
    has_aids = models.BooleanField(default=False, verbose_name="SIDA")
    has_psychosis = models.BooleanField(default=False, verbose_name="Psychose")
    
    # === Avis médical ===
    medical_opinion = models.TextField(blank=True, null=True, verbose_name="Avis médical")
    is_medically_fit = models.BooleanField(default=True, verbose_name="Aptitude médicale")
    
    # === Signature ===
    physician_signature = models.CharField(max_length=200, blank=True, verbose_name="Signature du médecin")
    examination_date = models.DateField(null=True, blank=True, verbose_name="Date d'examen")
    
    # === Métadonnées ===
    application = models.OneToOneField(
        StudentApplication,
        on_delete=models.CASCADE,
        related_name='physical_examination',
        null=True,
        blank=True,
        verbose_name="Demande associée"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Examen physique"
        verbose_name_plural = "Examens physiques"
    
    def __str__(self):
        return f"Examen physique - {self.name} ({self.examination_date or 'Date inconnue'})"
    
    @property
    def blood_pressure(self):
        if self.blood_pressure_systolic and self.blood_pressure_diastolic:
            return f"{self.blood_pressure_systolic}/{self.blood_pressure_diastolic} mmHg"
        return "Non renseigné"
    
    def is_healthy(self):
        """Vérifie si l'étudiant est déclaré en bonne santé"""
        dangerous_conditions = [
            self.has_cholera, self.has_yellow_fever, self.has_plague,
            self.has_leprosy, self.has_venereal_disease, self.has_lung_tuberculosis,
            self.has_aids, self.has_psychosis
        ]
        return not any(dangerous_conditions) and self.is_medically_fit

class Payment(models.Model):
    """Modèle pour les paiements des demandes d'admission"""
    
    class PaymentStatus(models.TextChoices):
        PENDING = 'PENDING', 'En attente'
        SUCCESS = 'SUCCESS', 'Payé'
        FAILED = 'FAILED', 'Échoué'
        REFUNDED = 'REFUNDED', 'Remboursé'
    
    class PaymentMethod(models.TextChoices):
        STRIPE = 'STRIPE', 'Carte bancaire'
        PAYPAL = 'PAYPAL', 'PayPal'
        ORANGE_MONEY = 'ORANGE_MONEY', 'Orange Money'
        MTN_MONEY = 'MTN_MONEY', 'MTN Mobile Money'
        WAVE = 'WAVE', 'Wave'
    
    application = models.OneToOneField(
        StudentApplication,
        on_delete=models.CASCADE,
        related_name='payment'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=0, default=5000000)  # 5.000.000 GNF
    currency = models.CharField(max_length=3, default='GNF')
    status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING
    )
    payment_method = models.CharField(
        max_length=20,
        choices=PaymentMethod.choices,
        blank=True,
        null=True
    )
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    payment_intent_id = models.CharField(max_length=100, blank=True, null=True)
    paypal_order_id = models.CharField(max_length=100, blank=True, null=True)
    receipt_url = models.URLField(blank=True, null=True)
    paid_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Paiement"
        verbose_name_plural = "Paiements"
        constraints = [
            models.UniqueConstraint(fields=['application'], name='unique_payment_per_application')
        ]
    
    def __str__(self):
        return f"Paiement #{self.id} - {self.application.family_name} - {self.status}"
    
    def mark_as_paid(self, transaction_id=None):
        """Marque le paiement comme réussi et met à jour le statut de la demande"""
        if self.status == self.PaymentStatus.SUCCESS:
            return False  # Déjà payé, ne pas traiter deux fois
        
        self.status = self.PaymentStatus.SUCCESS
        self.transaction_id = transaction_id
        self.paid_at = timezone.now()
        self.save()
        
        # Mettre à jour le statut de la demande
        self.application.status = StudentApplication.Status.PENDING
        self.application.save()
        return True
    
    @property
    def is_paid(self):
        """Vérifie si le paiement a été effectué"""
        return self.status == self.PaymentStatus.SUCCESS
    
    @property
    def amount_display(self):
        """Affiche le montant formaté"""
        return f"{self.amount:,.0f} GNF"


class PhysicalExamination(models.Model):
    """
    Modèle pour l'examen physique (外国人体格检查表)
    """
    
    # === Informations de base ===
    name = models.CharField(max_length=200, verbose_name="Nom")
    gender = models.CharField(
        max_length=1,
        choices=[('M', 'Masculin'), ('F', 'Féminin')],
        verbose_name="Sexe"
    )
    birth_date = models.DateField(verbose_name="Date de naissance")
    present_mailing_address = models.TextField(verbose_name="Adresse actuelle")
    nationality = models.CharField(max_length=100, verbose_name="Nationalité")
    birth_place = models.CharField(max_length=200, verbose_name="Lieu de naissance")
    blood_type = models.CharField(
        max_length=3,
        blank=True,
        null=True,
        choices=[('A', 'A'), ('B', 'B'), ('AB', 'AB'), ('O', 'O')],
        verbose_name="Groupe sanguin"
    )
    
    # === Antécédents médicaux ===
    has_typhus_fever = models.BooleanField(default=False, verbose_name="Typhus")
    has_bacillary_dysentery = models.BooleanField(default=False, verbose_name="Dysenterie bacillaire")
    has_poliomyelitis = models.BooleanField(default=False, verbose_name="Poliomyélite")
    has_brucellosis = models.BooleanField(default=False, verbose_name="Brucellose")
    has_diphtheria = models.BooleanField(default=False, verbose_name="Diphtérie")
    has_viral_hepatitis = models.BooleanField(default=False, verbose_name="Hépatite virale")
    has_scarlet_fever = models.BooleanField(default=False, verbose_name="Scarlatine")
    has_puerperal_infection = models.BooleanField(default=False, verbose_name="Infection post-partum")
    has_relapsing_fever = models.BooleanField(default=False, verbose_name="Fièvre récurrente")
    has_typhoid_paratyphoid = models.BooleanField(default=False, verbose_name="Typhoïde et paratyphoïde")
    has_epidemic_meningitis = models.BooleanField(default=False, verbose_name="Méningite cérébrospinale")
    
    # === Troubles psychiatriques ===
    has_toxicomania = models.BooleanField(default=False, verbose_name="Toxicomanie")
    has_mental_confusion = models.BooleanField(default=False, verbose_name="Confusion mentale")
    has_manic_psychosis = models.BooleanField(default=False, verbose_name="Psychose maniaque")
    has_paranoid_psychosis = models.BooleanField(default=False, verbose_name="Psychose paranoïaque")
    has_hallucinatory_psychosis = models.BooleanField(default=False, verbose_name="Psychose hallucinatoire")
    
    # === Examens physiques ===
    height_cm = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True, verbose_name="Taille (cm)")
    weight_kg = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True, verbose_name="Poids (kg)")
    blood_pressure_systolic = models.IntegerField(null=True, blank=True, verbose_name="Pression systolique")
    blood_pressure_diastolic = models.IntegerField(null=True, blank=True, verbose_name="Pression diastolique")
    
    development = models.CharField(max_length=100, blank=True, verbose_name="Développement")
    nourishment = models.CharField(max_length=100, blank=True, verbose_name="Nutrition")
    neck = models.CharField(max_length=100, blank=True, verbose_name="Cou")
    
    vision_left = models.CharField(max_length=20, blank=True, verbose_name="Vision gauche")
    vision_right = models.CharField(max_length=20, blank=True, verbose_name="Vision droite")
    corrected_vision_left = models.CharField(max_length=20, blank=True, verbose_name="Vision corrigée gauche")
    corrected_vision_right = models.CharField(max_length=20, blank=True, verbose_name="Vision corrigée droite")
    colour_sense = models.CharField(max_length=50, blank=True, verbose_name="Vision des couleurs")
    
    skin = models.CharField(max_length=100, blank=True, verbose_name="Peau")
    lymph_nodes = models.CharField(max_length=100, blank=True, verbose_name="Ganglions lymphatiques")
    ears = models.CharField(max_length=100, blank=True, verbose_name="Oreilles")
    nose = models.CharField(max_length=100, blank=True, verbose_name="Nez")
    tonsils = models.CharField(max_length=100, blank=True, verbose_name="Amygdales")
    heart = models.CharField(max_length=200, blank=True, verbose_name="Cœur")
    lungs = models.CharField(max_length=200, blank=True, verbose_name="Poumons")
    abdomen = models.CharField(max_length=200, blank=True, verbose_name="Abdomen")
    spine = models.CharField(max_length=200, blank=True, verbose_name="Colonne vertébrale")
    extremities = models.CharField(max_length=200, blank=True, verbose_name="Extrémités")
    nervous_system = models.CharField(max_length=200, blank=True, verbose_name="Système nerveux")
    other_findings = models.TextField(blank=True, null=True, verbose_name="Autres observations")
    
    # === Examens complémentaires ===
    ecg_result = models.TextField(blank=True, null=True, verbose_name="Résultat ECG")
    chest_xray_result = models.TextField(blank=True, null=True, verbose_name="Résultat radiographie pulmonaire")
    chest_xray_report = models.FileField(
        upload_to='exams/chest_xray/',
        blank=True,
        null=True,
        verbose_name="Rapport radiographie pulmonaire"
    )
    
    # === Analyses de laboratoire ===
    hiv_test_result = models.CharField(
        max_length=20,
        blank=True,
        choices=[('NEGATIVE', 'Négatif'), ('POSITIVE', 'Positif'), ('PENDING', 'En attente')],
        verbose_name="Test VIH"
    )
    syphilis_test_result = models.CharField(
        max_length=20,
        blank=True,
        choices=[('NEGATIVE', 'Négatif'), ('POSITIVE', 'Positif'), ('PENDING', 'En attente')],
        verbose_name="Test Syphilis"
    )
    lab_report = models.FileField(
        upload_to='exams/lab/',
        blank=True,
        null=True,
        verbose_name="Rapport de laboratoire"
    )
    
    # === Maladies infectieuses ===
    has_cholera = models.BooleanField(default=False, verbose_name="Choléra")
    has_yellow_fever = models.BooleanField(default=False, verbose_name="Fièvre jaune")
    has_plague = models.BooleanField(default=False, verbose_name="Peste")
    has_leprosy = models.BooleanField(default=False, verbose_name="Lèpre")
    has_venereal_disease = models.BooleanField(default=False, verbose_name="Maladie vénérienne")
    has_lung_tuberculosis = models.BooleanField(default=False, verbose_name="Tuberculose pulmonaire")
    has_aids = models.BooleanField(default=False, verbose_name="SIDA")
    has_psychosis = models.BooleanField(default=False, verbose_name="Psychose")
    
    # === Avis médical ===
    medical_opinion = models.TextField(blank=True, null=True, verbose_name="Avis médical")
    is_medically_fit = models.BooleanField(default=True, verbose_name="Aptitude médicale")
    
    # === Signature ===
    physician_signature = models.CharField(max_length=200, blank=True, verbose_name="Signature du médecin")
    examination_date = models.DateField(null=True, blank=True, verbose_name="Date d'examen")
    
    # === Métadonnées ===
    application = models.OneToOneField(
        StudentApplication,
        on_delete=models.CASCADE,
        related_name='physical_examination',
        null=True,
        blank=True,
        verbose_name="Demande associée"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Examen physique"
        verbose_name_plural = "Examens physiques"
    
    def __str__(self):
        return f"Examen physique - {self.name} ({self.examination_date or 'Date inconnue'})"
    
    @property
    def blood_pressure(self):
        if self.blood_pressure_systolic and self.blood_pressure_diastolic:
            return f"{self.blood_pressure_systolic}/{self.blood_pressure_diastolic} mmHg"
        return "Non renseigné"
    
    def is_healthy(self):
        """Vérifie si l'étudiant est déclaré en bonne santé"""
        dangerous_conditions = [
            self.has_cholera, self.has_yellow_fever, self.has_plague,
            self.has_leprosy, self.has_venereal_disease, self.has_lung_tuberculosis,
            self.has_aids, self.has_psychosis
        ]
        return not any(dangerous_conditions) and self.is_medically_fit
## Modèle pour les paiements des demandes d'admission   
'''class Payment(models.Model):
    """Modèle pour les paiements des demandes d'admission"""
    
    class PaymentStatus(models.TextChoices):
        PENDING = 'PENDING', 'En attente'
        SUCCESS = 'SUCCESS', 'Payé'
        FAILED = 'FAILED', 'Échoué'
        REFUNDED = 'REFUNDED', 'Remboursé'
    
    class PaymentMethod(models.TextChoices):
        STRIPE = 'STRIPE', 'Carte bancaire'
        PAYPAL = 'PAYPAL', 'PayPal'
        ORANGE_MONEY = 'ORANGE_MONEY', 'Orange Money'
        MTN_MONEY = 'MTN_MONEY', 'MTN Mobile Money'
        WAVE = 'WAVE', 'Wave'
        
    application = models.OneToOneField(
        StudentApplication,
        on_delete=models.CASCADE,
        related_name='payment'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=500.00)
    currency = models.CharField(max_length=3, default='EUR')
    status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING
    )
    payment_method = models.CharField(
        max_length=20,
        choices=PaymentMethod.choices,
        blank=True,
        null=True
    )
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    payment_intent_id = models.CharField(max_length=100, blank=True, null=True)  # Pour Stripe
    paypal_order_id = models.CharField(max_length=100, blank=True, null=True)    # Pour PayPal
    receipt_url = models.URLField(blank=True, null=True)
    paid_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Paiement"
        verbose_name_plural = "Paiements"
    
    def __str__(self):
        return f"Paiement #{self.id} - {self.application.family_name} - {self.status}"
    
    def mark_as_paid(self, transaction_id=None):
        self.status = self.PaymentStatus.SUCCESS
        self.transaction_id = transaction_id
        self.paid_at = timezone.now()
        self.save()
        # Mettre à jour le statut de la demande
        self.application.status = 'PENDING'  # En attente de traitement admin
        self.application.save() '''

# main_apps/gestion/models.py - Ajoutez en bas



class UserProfile(models.Model):
    """Extension du modèle User pour ajouter des informations supplémentaires"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    is_student = models.BooleanField(default=True)
    applications = models.ManyToManyField(StudentApplication, blank=True, related_name='applicants')
    
    def __str__(self):
        return f"Profil de {self.user.username}"

# Signal pour créer automatiquement un profil lors de l'inscription
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()