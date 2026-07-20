import os
import logging
import warnings
import streamlit as st
from dotenv import load_dotenv

# Silenciar advertencias de consola
warnings.filterwarnings("ignore")
logging.getLogger("langchain").setLevel(logging.ERROR)

# Cargar variables de entorno
load_dotenv()

from langchain_groq import ChatGroq
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# ==========================================
# 1. CONFIGURACIÓN DE PÁGINA Y ESTILOS (CSS)
# ==========================================
st.set_page_config(
    page_title="Mecassist - Atención al Cliente",
    page_icon="⚙️",
    layout="centered"
)

# Inyección de CSS para colores amables y corporativos
st.markdown("""
    <style>
    /* Fondo principal con un tono gris/azul muy suave */
    .stApp {
        background-color: #F4F7F9;
    }
    
    /* Personalización del Panel Lateral (Sidebar) */
    [data-testid="stSidebar"] {
        background-color: #EBF1F5;
        border-right: 1px solid #D1DBE0;
    }

    /* Encabezado y títulos */
    h1 {
        color: #1E3A8A !important; /* Azul corporativo amable */
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Globos de mensaje del Asistente */
    [data-testid="stChatMessage"]:nth-child(even) {
        background-color: #FFFFFF;
        border-radius: 12px;
        padding: 12px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.04);
        border-left: 4px solid #2563EB;
    }

    /* Globos de mensaje del Usuario */
    [data-testid="stChatMessage"]:nth-child(odd) {
        background-color: #E0E7FF;
        border-radius: 12px;
        padding: 12px;
        border-right: 4px solid #4F46E5;
    }

    /* Botones personalizados */
    .stButton>button {
        background-color: #2563EB;
        color: white;
        border-radius: 8px;
        border: none;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #1D4ED8;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. PANEL LATERAL (SIDEBAR)
# ==========================================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1037/1037322.png", width=70)
    st.title("⚙️ Mecassist")
    st.write("**Centro de Ayuda Inteligente**")
    st.markdown("---")
    
    st.subheader("💡 Consultas Frecuentes")
    st.caption("• Horarios de atención en taller")
    st.caption("• Cobertura de la garantía")
    st.caption("• Procedimiento de reclamos")
    st.caption("• Agendamiento de servicio")
    
    st.markdown("---")
    # Botón para reiniciar la conversación
    if st.button("🗑️ Limpiar Conversación", use_container_width=True):
        st.session_state.messages = [
            {"role": "assistant", "content": "¡Hola! Bienvenido a Mecassist. ⚙️ ¿En qué te puedo ayudar hoy?"}
        ]
        st.rerun()

    st.markdown("<br><br><small>Soporte Técnico Mecassist v1.0</small>", unsafe_allow_html=True)

# ==========================================
# 3. ENCABEZADO PRINCIPAL
# ==========================================
st.title("⚙️ Centro de Atención Mecassist")
st.caption("Resuelve tus dudas sobre nuestras políticas de servicio, garantía y horarios al instante.")

# ==========================================
# 4. INICIALIZACIÓN DE MOTOR RAG (CACHED)
# ==========================================
@st.cache_resource(show_spinner="Cargando base de conocimiento...")
def inicializar_sistema():
    if not os.getenv("GROQ_API_KEY"):
        st.error("Falta la GROQ_API_KEY en el archivo .env")
        st.stop()
        
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.1)
    
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    rutas_politicas = {
        "horarios": os.path.join(BASE_DIR, "documentos", "01_politica_horarios.pdf"),
        "servicio": os.path.join(BASE_DIR, "documentos", "02_politica_servicio.pdf"),
        "satisfaccion": os.path.join(BASE_DIR, "documentos", "03_politica_satisfaccion.pdf"),
        "garantia": os.path.join(BASE_DIR, "documentos", "04_politica_garantia.pdf")
    }
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=300)
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    recuperadores = {}
    for politica, ruta in rutas_politicas.items():
        if os.path.exists(ruta):
            loader = PyPDFLoader(ruta)
            paginas = loader.load_and_split(text_splitter)
            vector_store = FAISS.from_documents(paginas, embeddings)
            recuperadores[politica] = vector_store.as_retriever(search_kwargs={"k": 3})
            
    return llm, recuperadores

llm, recuperadores = inicializar_sistema()

# ==========================================
# 5. ENRUTADOR Y CADENA DE PROMPT
# ==========================================
def obtener_contexto_relevante(consulta: str) -> str:
    consulta_lower = consulta.lower()
    contexto = ""
    
    keywords = {
        "horarios": ["horario", "hora", "atencion", "abren", "cierran", "domingo", "sabado", "festivo", "jornada", "dias", "dia"],
        "servicio": ["servicio", "atender", "procedimiento", "trabajo", "mantenimiento", "revision", "taller", "reparar", "mecanico"],
        "satisfaccion": ["satisfaccion", "reclamo", "devolucion", "queja", "sugerencia", "devolver", "dinero", "postventa"],
        "garantia": ["garantia", "falla", "reparacion", "cobertura", "repuesto", "pieza", "defecto", "meses", "cobertura"]
    }
    
    for categoria, lista_palabras in keywords.items():
        if any(palabra in consulta_lower for palabra in lista_palabras):
            if categoria in recuperadores:
                docs = recuperadores[categoria].invoke(consulta)
                contexto += f"\n[{categoria.upper()}]\n" + "\n".join([d.page_content for d in docs])

    if not contexto:
        for categoria, recuperador in recuperadores.items():
            docs = recuperador.invoke(consulta)
            contexto += f"\n[{categoria.upper()}]\n" + "\n".join([d.page_content for d in docs])
            
    return contexto

prompt_sistema = ChatPromptTemplate.from_messages([
    ("system", 
     "Eres el asistente virtual de atención al cliente de Mecassist.\n"
     "Responde consultas usando ÚNICAMENTE la información corporativa abajo brindada.\n\n"
     "REGLAS:\n"
     "1. Sé amable, breve y conciso (máximo 2 a 3 oraciones).\n"
     "2. Si la respuesta no está en el texto, di: 'Lo siento, no tengo registro de esa información en nuestras políticas actuales. Por favor, comunícate con un agente humano.'\n\n"
     "CONTEXTO:\n{contexto}"),
    ("human", "{input}")
])

cadena_mecassist = prompt_sistema | llm | StrOutputParser()

# ==========================================
# 6. HISTORIAL DE MENSAJES Y CHAT
# ==========================================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "¡Hola! Bienvenido a Mecassist. ⚙️ ¿En qué te puedo ayudar hoy? Puedes preguntarme sobre nuestros horarios, garantías, servicios o reclamos."}
    ]

# Mostrar historial con avatares personalizados
for msg in st.session_state.messages:
    avatar = "⚙️" if msg["role"] == "assistant" else "👤"
    with st.chat_message(msg["role"], avatar=avatar):
        st.write(msg["content"])

# Entrada de usuario
if pregunta := st.chat_input("Escribe tu consulta sobre Mecassist..."):
    st.session_state.messages.append({"role": "user", "content": pregunta})
    with st.chat_message("user", avatar="👤"):
        st.write(pregunta)

    with st.chat_message("assistant", avatar="⚙️"):
        with st.spinner("Buscando en nuestras políticas..."):
            contexto = obtener_contexto_relevante(pregunta)
            respuesta = cadena_mecassist.invoke({"contexto": contexto, "input": pregunta})
            st.write(respuesta)

    st.session_state.messages.append({"role": "assistant", "content": respuesta})