import os
import json
from pathlib import Path
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain.docstore.document import Document

# 1. Definir las rutas desde la raíz del proyecto Kuzco
PROJECT_ROOT = Path(__file__).parent.parent  # Navega desde scripts/ hacia Kuzco/
RECETAS_PATH = os.path.join(PROJECT_ROOT, "recetas")
DB_PATH = os.path.join(PROJECT_ROOT, "chroma_db")
EMBEDDING_MODEL = "paraphrase-multilingual-MiniLM-L12-V2" # qwen2.5 0.5b
# EMBEDDING_MODEL = "all-MiniLM-L6-v2" # phi3
print(f'Loading embedding model: {EMBEDDING_MODEL}')

# 2. Configurar el modelo de embeddings
# Usará un modelo ligero para convertir texto en vectores (números)
embedding_function = SentenceTransformerEmbeddings(model_name=EMBEDDING_MODEL)

# 3. Cargar las recetas y prepararlas como "Documentos"
documents = []
for filename in os.listdir(RECETAS_PATH):
    if filename.endswith(".json"):
        filepath = os.path.join(RECETAS_PATH, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

            # Creamos un contenido de texto para la búsqueda
            # ¡Esta parte es clave! Combinamos lo más importante para la búsqueda.
            # Aplanamos la lista de ingredientes a un solo string
            ingredientes_texto = "\n".join(
                [f"- {ing['nombre']}: {ing['cantidad']}" for ing in data["ingredientes"]]
            )
            # Aplanamos la lista de pasos a un solo string numerado
            pasos_texto = "\n".join(
                [f"{i+1}. {paso}" for i, paso in enumerate(data["pasos"])]
            )
            # Aplanamos la lista de tags a un solo string
            tags_texto = ", ".join(data.get("tags", []))

            base_metadata = {
                "titulo": data["titulo"],
                "descripcion": data["descripcion"],
                "tiempo_preparacion": data["tiempo_preparacion"],
                "dificultad": data["dificultad"],
                "ingredientes": ingredientes_texto, # Usamos el string aplanado
                "pasos": pasos_texto,             # Usamos el string aplanado
                "tags": tags_texto                # Usamos el string aplanado
            }
            # Creacion de chunks
            chunk_content_title = f"Receta: {data['titulo']}. Descripción: {data['descripcion']}"
            documents.append(Document(page_content=chunk_content_title, metadta=base_metadata))

            for ingrediente in data["ingredientes"]:
                chunk_content_ing = f"La receta '{data['titulo']}' usa el ingrediente '{ingrediente['nombre']}"
                documents.append(Document(page_content=chunk_content_ing, metadata=base_metadata))

# 4. Crear la base de datos Chroma y guardar los documentos
if documents:
    print(f"Indexando {len(documents)} recetas...")
    db = Chroma.from_documents(
        documents,
        embedding_function,
        persist_directory=str(DB_PATH)
    )
    print("¡Índice creado y guardado con éxito!")
else:
    print("No se encontraron recetas para indexar.")