import os
import logging
import warnings
from dotenv import load_dotenv

# Silenciar advertencias de consola
warnings.filterwarnings("ignore")
logging.getLogger("langchain").setLevel(logging.ERROR)

# Cargar variables de entorno desde el archivo .env
load_dotenv()

from langchain_groq import ChatGroq
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 1. Validar clave de API
if not os.getenv("GROQ_API_KEY"):
    raise ValueError("No se encontró GROQ_API_KEY. Verifica tu archivo .env")

# 2. Inicializar modelo Groq (Llama 3.3 Versatile)
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.1
)

# 3. Procesamiento de Políticas (PDFs locales)
rutas_politicas = {
    "horarios": "./documentos/01_politica_horarios.pdf",
    "servicio": "./documentos/02_politica_servicio.pdf",
    "satisfaccion": "./documentos/03_politica_satisfaccion.pdf",
    "garantia": "./documentos/04_politica_garantia.pdf"
}

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

recuperadores = {}

print("Cargando y procesando políticas de Mecassist...")
for politica, ruta in rutas_politicas.items():
    if os.path.exists(ruta):
        loader = PyPDFLoader(ruta)
        paginas = loader.load_and_split(text_splitter)
        vector_store = FAISS.from_documents(paginas, embeddings)
        recuperadores[politica] = vector_store.as_retriever(search_kwargs={"k": 2})
    else:
        print(f"Advertencia: No se encontró {ruta}")

# 4. Enrutador de Contexto Optimizado
def obtener_contexto_relevante(consulta: str) -> str:
    consulta_lower = consulta.lower()
    contexto = ""
    archivos_consultados = set()
    
    # Mapeo ampliado de palabras clave por tema
    keywords = {
        "horarios": ["horario", "hora", "atencion", "abren", "cierran", "domingo", "sabado", "festivo", "jornada", "dias", "dia"],
        "servicio": ["servicio", "atender", "procedimiento", "trabajo", "mantenimiento", "revision", "taller", "reparar", "mecanico"],
        "satisfaccion": ["satisfaccion", "reclamo", "devolucion", "queja", "sugerencia", "devolver", "dinero", "postventa", "atencion"],
        "garantia": ["garantia", "falla", "reparacion", "cobertura", "repuesto", "pieza", "defecto", "meses", "año", "cobertura"]
    }
    
    # Evaluar coincidencias
    for categoria, lista_palabras in keywords.items():
        if any(palabra in consulta_lower for palabra in lista_palabras):
            if categoria in recuperadores:
                docs = recuperadores[categoria].invoke(consulta)
                contexto += f"\n[{categoria.upper()}]\n" + "\n".join([d.page_content for d in docs])
                archivos_consultados.add(categoria)

    # RESPALDO (FALLBACK): Si no hizo match con ninguna palabra, busca en todos los PDF
    if not contexto:
        print("(Buscando en todas las políticas...)")
        for categoria, recuperador in recuperadores.items():
            docs = recuperador.invoke(consulta)
            contexto += f"\n[{categoria.upper()}]\n" + "\n".join([d.page_content for d in docs])
            
    return contexto

# 5. Configurar Prompt y Cadena
prompt_sistema = ChatPromptTemplate.from_messages([
    ("system", 
     "Eres el asistente virtual de atención al cliente de la empresa Mecassist.\n"
     "Responde consultas usando ÚNICAMENTE la información corporativa abajo brindada.\n\n"
     "REGLAS:\n"
     "1. Sé amable, breve y conciso (máximo 2 a 3 oraciones).\n"
     "2. Si la respuesta no está en el texto, di: 'Lo siento, no tengo registro de esa información en nuestras políticas actuales. Por favor, comunícate con un agente humano.'\n\n"
     "CONTEXTO:\n{contexto}"),
    ("human", "{input}")
])

cadena_mecassist = prompt_sistema | llm | StrOutputParser()

# 6. Bucle de Conversación Interactiva en Consola
if __name__ == "__main__":
    print("\n==================================================")
    print(" Agente de Atención al Cliente Mecassist Listo")
    print(" (Escribe 'salir' o 'exit' para finalizar)")
    print("==================================================\n")
    
    while True:
        pregunta = input("\nCliente: ")
        if pregunta.lower() in ["salir", "exit"]:
            print("Cerrando sesión del agente...")
            break
            
        if not pregunta.strip():
            continue

        contexto_extraido = obtener_contexto_relevante(pregunta)
        respuesta = cadena_mecassist.invoke({
            "contexto": contexto_extraido,
            "input": pregunta
        })
        
        print(f"\nAgente Mecassist:\n{respuesta}")