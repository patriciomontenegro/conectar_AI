# MECASSIST_AI
# 🚗 Agente de IA para Servicio Automotriz 🛠️

Este proyecto busca brindar soporte técnico en una empresa de mecánica automotriz llamada MECASSIST, mediante la creación de un agente de IA inteligente. Utilizando scripts de Python, el sistema procesará consultas de los usuarios y las conectará directamente con la potente API de Gemini AI para generar respuestas rápidas, precisas y contextualizadas. ⚡

### 📄 Gestión de Consultas del Taller

La base de conocimiento se alimentará de PDFs con información clave del negocio. Los clientes podrán consultar de forma exclusiva temas del taller, tales como horarios de atención, políticas de servicio, satisfacción al cliente y las condiciones de garantía de las reparaciones de sus vehículos. 🔍

### 💬 Respuestas Automatizadas y Eficientes

Al integrar Gemini AI con nuestra base documental, los mecánicos y clientes recibirán respuesta al instante. Esta herramienta optimizará los tiempos de la sección de consultas en el taller, garantizando un flujo de trabajo digitalizado, moderno y altamente eficiente. 🚀

### 🛠️ Desarrollo en VS Code y Despliegue en Streamlit
💻 De Local a Producción con VS Code: En esta etapa, trasladamos la arquitectura desde Google Colab hacia Visual Studio Code, organizando el proyecto en una estructura limpia con entornos virtuales (venv) y variables de entorno ocultas (.env). Optimizamos el enrutador RAG con lógica fallback y ajustamos el chunking a 1000 caracteres para garantizar respuestas hiperprecisas desde los PDF locales.

### 🌐 Interfaz Interactiva y Deploy en la Nube: Finalmente, transformamos la app en una experiencia web moderna implementando Streamlit. Diseñamos una interfaz tipo chat con colores corporativos amables, un sidebar funcional para reiniciar el historial y estilos CSS personalizados. El agente quedó desplegado en Streamlit Cloud integrado a GitHub y configurado con Secrets seguros.
