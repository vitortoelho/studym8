import firebase_admin
from firebase_admin import credentials

# Inicializa o Firebase
cred = credentials.Certificate("firebase_credentials.json")
firebase_admin.initialize_app(cred)

print("Firebase initialized successfully!")
