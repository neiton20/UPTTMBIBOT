
## 🤖 UPTTMBI Bot — Asistente virtual para la universidad

Bot de Telegram diseñado para estudiantes y personal de la Universidad Politécnica Territorial Mario Briceño Iragorry (UPTTMBI).  
Proporciona acceso rápido a documentos oficiales, información institucional, programas de formación (PNF), sedes y calendario académico.

---------------------------------------------------------------------

## 📦 Requisitos previos

- Python 3.10 o superior
- Token de bot de Telegram (crear con [@BotFather](https://t.me/BotFather))
- Conexión a internet

---------------------------------------------------------------------

## ⚙️ Instalación y configuración

## 1. Clonar el repositorio
bash
git clone https://github.com/tuusuario/UPTTMBIBOT.git
cd UPTTMBIBOT


## 2. Crear y activar entorno virtual (recomendado)

Windows:
bash
python -m venv venv
venv\Scripts\activate


Linux/macOS:
bash
python3 -m venv venv
source venv/bin/activate


## 3. Instalar dependencias
bash
pip install -r requirements.txt


Contenido de `requirements.txt`:

python-telegram-bot>=20.0
httpx
asyncio


## 4. Configurar el token

Crea el archivo `data/config.py` con el siguiente contenido:
python
TELEGRAM_TOKEN = "tu_token_aqui"


> Nunca compartas este archivo ni lo subas a repositorios públicos.

---------------------------------------------------------------------

## 🗂️ Estructura del proyecto (versión actual)


UPTTMBIBOT/
├── main.py                      # Punto de entrada, dispatcher y manejador de errores
├── requirements.txt
├── assets/
│   ├── PST/                     # Documentos del Proyecto Sociotecnológico
│   ├── servicio_comunitario/    # 12 documentos de Servicio Comunitario
│   ├── institucional/           # Planillas de inscripción, reseña histórica
│   └── pnf/                     # Documentos rectores de cada PNF (10 PDFs)
│   └── Calendario Academico 2026 UPTTMBI.pdf
|
├── data/
│   └── config.py                # Token del bot (no incluido en el repo)
└── handlers/
    ├── __init__.py
    ├── start_handler.py         # Menú principal + botón "¿Qué puedo hacer?"
    ├── comunitario_handler.py   # Documentos de Servicio Comunitario
    ├── pst_handler.py           # Documentos de PST
    ├── institucional_handler.py # Planillas, reseña histórica, accesos a PNF y sedes
    ├── pnf_handler.py           # Todos los PNF, perfiles y documentos rectores
    └── sedes_handler.py         # Listado de núcleos y carreras ofertadas


---------------------------------------------------------------------

## 🚀 Ejecutar el bot

bash
python main.py


Si todo está correcto, verás en la terminal:

Bot iniciado correctamente...


El bot comenzará a recibir mensajes a través de `polling`.

----------------------------------------------------------------

## 📌 Funcionalidades principales

🎓 Servicio Comunitario
12 documentos disponibles: fichas de inscripción, carta de postulación, cronograma semanal, guías de elaboración, formatos de evaluación, ley del servicio comunitario y más.

📂 PST (Proyecto Sociotecnológico)
Descripción detallada de cada una de las partes del proyecto y las normas oficiales para su elaboración y presentación.

🏫 Información Institucional
Planillas de inscripción para Pregrado y Posgrado, reseña histórica de la universidad, acceso al listado completo de PNF y consulta de sedes.

📚 PNF (10 carreras disponibles)
Por cada carrera puedes consultar las titulaciones y certificaciones intermedias, los perfiles de egreso (TSU, Ingeniero o Licenciado según el programa) y el Documento Rector oficial del PNF.

📍 Sedes
Información de los 6 núcleos y extensiones de la universidad, con el listado de carreras disponibles en cada una.

📅 Calendario Académico 2026
Descarga directa del calendario oficial en PDF.

❓ ¿Qué puedo hacer?
Botón de ayuda en el menú principal con un resumen de todas las funciones del bot.

---------------------------------------------------------------------

## 🧠 Comportamiento inteligente

- Después de enviar un documento o ver un perfil, el menú correspondiente reaparece automáticamente al final del chat.
- Los menús antiguos se eliminan para evitar saturar la conversación.
- Se incluye un mensaje temporal *"Enviando documento..."* mientras se procesa el archivo.

---------------------------------------------------------------------

## 🔒 Notas sobre permisos

- En chats privados el bot funciona sin restricciones.
- En grupos, para que el bot pueda eliminar mensajes de menús anteriores, debe ser administrador con permiso de *eliminar mensajes*.

---------------------------------------------------------------------

## 🧪 Posibles errores y soluciones

ModuleNotFoundError: No module named 'handlers.pnf_handler'
Causa: el archivo no existe o el nombre no coincide.
Solución: verifica que pnf_handler.py esté dentro de la carpeta handlers/.

Query is too old
Causa: el bot tardó más de 48 segundos en responder.
Solución: mejorar la conexión a internet o usar webhooks en producción.

deleteMessage 400 Bad Request
Causa: se intentó borrar un mensaje que ya había sido eliminado.
Solución: es inofensivo, no afecta al usuario.

---------------------------------------------------------------------

## 👥 Créditos

Desarrollado para la UPTTMBI – Núcleo La Beatriz.  
Datos extraídos de documentos oficiales y del archivo `PNFS.docx`.

------------------------------------------------------------------

## 📄 Licencia

Uso interno universitario. No comercial.

