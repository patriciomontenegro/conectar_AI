# MECASSIST_AI
# 🚗 Agente de IA para Servicio Automotriz 🛠️

Este proyecto busca brindar soporte técnico en una empresa de mecánica automotriz llamada MECASSIST, mediante la creación de un agente de IA inteligente. Utilizando scripts de Python, el sistema procesará consultas de los usuarios y las conectará directamente con la potente API de Groq AI para generar respuestas rápidas, precisas y contextualizadas. ⚡

### 📄 Gestión de Consultas del Taller

La base de conocimiento se alimentará de PDFs con información clave del negocio. Los clientes podrán consultar de forma exclusiva temas del taller, tales como horarios de atención, políticas de servicio, satisfacción al cliente y las condiciones de garantía de las reparaciones de sus vehículos. 🔍

### 💬 Respuestas Automatizadas y Eficientes

Al integrar Groq AI con nuestra base documental, los mecánicos y clientes recibirán respuesta al instante. Esta herramienta optimizará los tiempos de la sección de consultas en el taller, garantizando un flujo de trabajo digitalizado, moderno y altamente eficiente. 🚀

Aquí tienes la sección final del `README.md` estructurada exactamente con todo lo solicitado, incluyendo la sintaxis Markdown para las imágenes y respetando el límite de 500 caracteres por párrafo:

### 🛠️ Tecnologías, Ejecución y Demostración

🛠️ **Stack Tecnológico y Ejecución:** Construido con **LangChain (LCEL)**, **Groq (Llama 3.3 70B)**, **FAISS**, **HuggingFace Embeddings** y **Streamlit**. Para ejecutarlo localmente: 1) Clona el repositorio e instala dependencias con `pip install -r requirements.txt`. 2) Configura `GROQ_API_KEY` en un archivo `.env`. 3) Inicia la app web ejecutando `streamlit run app.py` en la terminal.

💬 **Casos de Uso e Interfaz en Vivo:** El agente responde consultas precisas sobre políticas corporativas. *Ejemplo de pregunta:* "¿Cuáles son los horarios de atención?". *Ejemplo de respuesta:* "Nuestros horarios son de lunes a viernes de 08:30 a 18:30 horas, con cierre para colación de 13:00 a 14:00 horas. También atendemos sábados de 09:00 a 13:00 horas."

### 🛠️ Desarrollo en VS Code y Despliegue en Streamlit
💻 De Local a Producción con VS Code: En esta etapa, trasladamos la arquitectura desde Google Colab hacia Visual Studio Code, organizando el proyecto en una estructura limpia con entornos virtuales (venv) y variables de entorno ocultas (.env). Optimizamos el enrutador RAG con lógica fallback y ajustamos el chunking a 1000 caracteres para garantizar respuestas hiperprecisas desde los PDF locales.

### 🌐 Interfaz Interactiva y Deploy en la Nube: Finalmente, transformamos la app en una experiencia web moderna implementando Streamlit. Diseñamos una interfaz tipo chat con colores corporativos amables, un sidebar funcional para reiniciar el historial y estilos CSS personalizados. El agente quedó desplegado en Streamlit Cloud integrado a GitHub y configurado con Secrets seguros.

### IMAGENES DE LO REALIZADO

<img width="1280" height="720" alt="codigo_en_vsstudio" src="https://github.com/user-attachments/assets/6ae80d1a-300a-4bc5-a802-a65f98491446" />

<img width="1280" height="720" alt="deploy_streamlit" src="https://github.com/user-attachments/assets/2910c69f-3525-4e08-8808-5fb807e25fd0" />


