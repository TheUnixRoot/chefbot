import streamlit as st
import os
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.chat_models import ChatOllama
from langchain.schema.runnable import RunnablePassthrough
from langchain.prompts import PromptTemplate
from langchain.schema import StrOutputParser
from pathlib import Path

# --- Configuración Inicial ---
PROJECT_ROOT = Path(__file__).parent.parent  # Navega desde scripts/ hacia Kuzco/
DB_PATH = os.path.join(PROJECT_ROOT, "chroma_db")

# 1. Crea una función para cargar los componentes pesados
@st.cache_resource
def load_components():
    print("Cargando componentes (esto solo debería aparecer una vez)...")
    embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    db = Chroma(persist_directory=DB_PATH, embedding_function=embedding_function)
    retriever = db.as_retriever(search_kwargs={"k": 3})
    return retriever

# 2. Llama a la función para obtener el retriever
retriever = load_components()

MODEL_NAME = "phi4-mini:latest"
# --- Definición del Prompt ---
# Este es el cerebro que le dice a Phi-3 cómo comportarse.
template = """
Eres un asistente de cocina amigable y servicial llamado ChefBot.
Tu objetivo es ayudar a los usuarios a encontrar recetas de tu base de datos.
Responde a la pregunta del usuario basándote únicamente en el siguiente contexto:

CONTEXTO:
{context}

PREGUNTA:
{question}

INSTRUCCIONES:
1. Revisa el contexto y encuentra las recetas que mejor respondan a la pregunta.
2. Si encuentras recetas relevantes, preséntalas de forma clara y apetitosa. Menciona sus títulos.
3. Si el usuario pide los detalles de una receta específica, proporciona sus ingredientes y pasos.
4. Si no encuentras ninguna receta en el contexto que responda a la pregunta, di amablemente: "Lo siento, no he encontrado ninguna receta que coincida con tu búsqueda. ¿Quieres intentar con otros ingredientes?". No inventes recetas.
"""
# MODEL_NAME = "orca-mini"

# # REEMPLAZA TU ANTIGUO TEMPLATE POR ESTE:
# template = """### System:
# Eres un asistente de cocina amigable y servicial llamado ChefBot. Tu objetivo es ayudar a los usuarios a encontrar recetas de tu base de datos basándote en el contexto proporcionado. Responde de forma concisa.
# Si no encuentras una receta relevante, di amablemente que no has encontrado nada.

# ### User:
# CONTEXTO:
# {context}

# PREGUNTA:
# {question}

# ### Assistant:
# """

llm = ChatOllama(model=MODEL_NAME)
prompt = PromptTemplate(template=template, input_variables=["context", "question"])

# --- Cadena de Procesamiento (RAG Chain) ---
rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# --- Interfaz de Streamlit ---
st.title("🍳 ChefBot AI")
st.caption("Tu asistente de recetas personal")

# Inicializar el historial de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar mensajes del historial
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Aceptar la entrada del usuario
if user_input := st.chat_input("¿Qué te apetece cocinar hoy?"):
    # Añadir mensaje del usuario al historial
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Obtener y mostrar la respuesta del bot
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            response = rag_chain.invoke(user_input)
            st.markdown(response)
    
    # Añadir respuesta del bot al historial
    st.session_state.messages.append({"role": "assistant", "content": response})