# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import router
import firebase_admin
from firebase_admin import credentials, firestore

# Inicializa o Firebase
cred = credentials.Certificate("firebase_credentials.json")
firebase_admin.initialize_app(cred)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ou especifique os domínios do frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")  # Inclui o roteador
