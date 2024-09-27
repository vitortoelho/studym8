# app/routes.py
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from firebase_admin import firestore

router = APIRouter()

# Modelo de dados para representar uma matéria
class Subject(BaseModel):
    subject_name: str
    topics: list[str]

# Modelo de dados para representar uma playlist de estudo
class StudyPlaylist(BaseModel):
    name: str
    subjects: list[Subject]  # Lista de matérias

@router.post("/recommendation")
def recommend_subject(subject: Subject):
    db = firestore.client()  # Inicializa o cliente Firestore
    subjects = db.collection("subjects").get()  # Busca as matérias do Firestore

    # Cria um dicionário para armazenar as matérias e seus tópicos
    subjects_data = {}
    for subject_item in subjects:
        data = subject_item.to_dict()
        subjects_data[data["name"]] = data.get("topics", [])  # Supondo que "topics" está no Firestore

    if subject.subject_name in subjects_data:
        return {"recommendation": subjects_data[subject.subject_name][:1]}
    
    return {"error": "Matéria não encontrada"}

# Rota para adicionar uma nova matéria ao Firestore
@router.post("/add_subject")
def add_subject(subject: Subject):
    db = firestore.client()  # Inicializa o cliente Firestore
    # Verifica se a matéria já existe
    existing_subjects = db.collection("subjects").where("name", "==", subject.subject_name).get()

    if existing_subjects:
        raise HTTPException(status_code=400, detail="Matéria já existe.")

    # Adiciona a matéria com os tópicos recebidos
    doc_ref = db.collection("subjects").add({
        "name": subject.subject_name,
        "topics": subject.topics  # Usa os tópicos enviados no POST
    })

    return {"message": "Matéria adicionada com sucesso", "id": doc_ref.id}  # Acessa o ID do documento

@router.put("/update_subject/{subject_name}")
def update_subject(subject_name: str, subject: Subject):
    db = firestore.client()  # Inicializa o cliente Firestore
    # Busca a matéria pelo nome
    existing_subjects = db.collection("subjects").where("name", "==", subject_name).get()

    if not existing_subjects:
        raise HTTPException(status_code=404, detail="Matéria não encontrada.")

    # Adiciona os tópicos à matéria existente
    for subject_item in existing_subjects:
        subject_item_ref = db.collection("subjects").document(subject_item.id)
        
        # Atualiza o nome da matéria se diferente
        if subject_name != subject.subject_name:
            subject_item_ref.update({"name": subject.subject_name})

        # Atualiza os tópicos, substituindo os existentes ou adicionando novos
        subject_item_ref.update({"topics": subject.topics})  # Substitui os tópicos existentes

    return {"message": "Matéria atualizada com sucesso."}

# Rota para adicionar uma nova playlist de estudo
@router.post("/add_playlist")
def add_playlist(playlist: StudyPlaylist):
    db = firestore.client()  # Inicializa o cliente Firestore
    # Cria um documento da playlist no Firestore
    doc_ref = db.collection("playlists").add({
        "name": playlist.name,
        "subjects": [sub.subject_name for sub in playlist.subjects]
    })

    # Acessa o ID do documento diretamente do doc_ref
    return {"message": "Playlist de estudo adicionada com sucesso", "id": doc_ref.id}
