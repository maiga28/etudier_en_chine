import os
import django

# 1. On indique à Django où se trouvent les réglages
# Remplace 'ton_projet' par le nom du dossier qui contient ton fichier settings.py
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()
username = 'admin'
email = 'adminstudent@gmail.com'
password = 'adminstudentmaiga1234'

if not User.objects.filter(username=username).exists():
    print("Création du superutilisateur...")
    User.objects.create_superuser(username, email, password)
else:
    print("Le superutilisateur existe déjà.")



