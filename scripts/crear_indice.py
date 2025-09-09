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

# 2. Configurar el modelo de embeddings
# Usará un modelo ligero para convertir texto en vectores (números)
embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

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

            # Creamos el contenido para la búsqueda (esto no cambia)
            content_for_embedding = (
                f"Título: {data['titulo']}. "
                f"Descripción: {data['descripcion']}. "
                f"Ingredientes: {', '.join([ing['nombre'] for ing in data['ingredientes']])}. "
                f"Etiquetas: {tags_texto}"
            )
            
            # Creamos los metadatos usando los strings que acabamos de generar
            metadata = {
                "titulo": data["titulo"],
                "descripcion": data["descripcion"],
                "tiempo_preparacion": data["tiempo_preparacion"],
                "dificultad": data["dificultad"],
                "ingredientes": ingredientes_texto, # Usamos el string aplanado
                "pasos": pasos_texto,             # Usamos el string aplanado
                "tags": tags_texto                # Usamos el string aplanado
            }

            doc = Document(page_content=content_for_embedding, metadata=metadata)
            documents.append(doc)

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