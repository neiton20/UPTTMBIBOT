# handlers/institucional_handler.py
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
import os

# Cadenas de texto estructuradas con la información institucional exacta
TEXTO_PREGRADO = (
    "🎓 PREGRADO (Bachilleres - TSU)\n"
    "Para tu inscripción en Pregrado, debes consignar los siguientes recaudos:\n\n"
    "🔹 Planilla de Inscripción: Descargar, llenar e imprimir.\n"
    "🔹 1 Foto Tipo Carnet.\n"
    "🔹 Copia de la Cédula de Identidad (Ampliada y Centrada).\n"
    "🔹 Copia de la Partida de Nacimiento.\n"
    "🔹 Constancia de la OPSU.\n"
    "🔹 Fondo Negro del Título de Bachiller (Autenticado).\n"
    "🔹 Copia de las Notas Certificadas.\n"
    "🔹 Todos los requerimientos adicionales indicados en la planilla.\n"
    "📌 Nota: Asegúrate de tener todos tus documentos en regla antes de acudir a la taquilla."
)

TEXTO_POSGRADO = (
    "🏛️ POSGRADO\n"
    "Para tu inscripción en Posgrado, debes consignar los siguientes recaudos:\n\n"
    "🔹 Planilla de Inscripción: Descargar, llenar e imprimir.\n"
    "🔹 1 Foto Tipo Carnet.\n"
    "🔹 Copia de la Cédula de Identidad (Ampliada y Centrada).\n"
    "🔹 Partida de Nacimiento.\n"
    "🔹 Fondo Negro del Título de Pregrado (Autenticado).\n"
    "🔹 Notas Certificadas.\n"
    "🔹 Comprobante de pago de aranceles (enviado previamente vía correo electrónico).\n\n"
    "📌 Nota: Asegúrate de tener todos tus documentos en regla antes de acudir a la taquilla."
)

TEXTO_HISTORIA = (
    "🏛️ RESEÑA HISTÓRICA DE LA UPTTMBI\n\n"
    "Nuestra casa de estudios nació el 1 de agosto de 1978 bajo el nombre de Instituto Universitario de Tecnología del Estado Trujillo (IUTET) , iniciando sus actividades académicas formalmente el 5 de mayo de 1980.\n\n"
    "Como parte de la Misión Alma Mater , el 2 de mayo de 2014 se oficializó su transformación a Universidad Politécnica Territorial \"Mario Briceño Iragorry\" (UPTTMBI) , estableciendo su sede principal en Valera.\n\n"
    "📍 Nuestros Núcleos Territoriales:\n"
    "🏫 Valera (Núcleo Dr. Pablo Viloria - La Beatriz): Sede principal definitiva construida sobre terrenos cedidos en 1979.\n"
    "🌲 Boconó (Núcleo Fabricio Ojeda): Fundado en marzo de 1988, orientado inicialmente al desarrollo turístico.\n"
    "🌾 El Dividive (Núcleo Francisco de Miranda): Establecido a finales de 1988, iniciando actividades en abril de 1989.\n"
    "⛰️ Trujillo (Núcleo Barbarita de la Torre): Creado en agosto de 1992. Pasó por sedes compartidas hasta consolidarse en su sede actual del sector Santa Rosa.\n"
    "🍇 Extensión Carache: Creada el 14 de febrero de 2019 para impartir Informática, Administración y Contaduría Pública.\n\n"
    "👤 Autoridades Principales:\n"
    "Primer Rector: Dr. Pablo Viloria (2014).\n"
    "Rectora Actual: Dra. Ninoska Darlysbeth Ortiz Ramírez (designada desde mayo de 2017).\n"
    "🎨 Logotipo Oficial: Creado a finales de 2014 mediante un concurso abierto ganado por los ingenieros egresados Andrea León Mijares y Josué García.\n\n"
    "🎯 Enfoque Actual:\n"
    "La universidad ya no se rige por la tradicional Misión y Visión. En su lugar, cuenta con un Objeto, Naturaleza, Encargo Social y Objetivos Estratégicos diseñados para impulsar el desarrollo territorial sustentable, la soberanía tecnológica y el crecimiento socio-productivo junto al Poder Popular trujillano."
)

# Diccionario de configuración para mapear los callback_data
ARCHIVOS_INSTITUCIONAL = {
    'institucional_pregrado': {
        'nombre': 'planilla de inscripcion.docx',
        'texto': TEXTO_PREGRADO
    },
    'institucional_posgrado': {
        'nombre': 'planilla de inscripcion post grado.docx',
        'texto': TEXTO_POSGRADO
    },
    'institucional_historia': {
        'nombre': 'Reseña Histórica .pdf',
        'texto': TEXTO_HISTORIA
    }
}

# Texto de contexto para la sección Institucional
TEXTO_CONTEXTO_INSTITUCIONAL = (
    "📌 **¿Qué encontrarás aquí?**\n\n"
    "Esta sección reúne la información general y documentos clave de la UPTTMBI:\n\n"
    "🎓 **Planilla de Pregrado** – Recaudos para inscripción de bachilleres y TSU.\n"
    "🏛️ **Planilla de Posgrado** – Recaudos para especializaciones y maestrías.\n"
    "📜 **Reseña Histórica** – Origen, evolución y autoridades de nuestra universidad.\n"
    "📚 **PNF (Programas Nacionales de Formación)** – Listado completo de carreras, perfiles de egreso y sedes.\n"
    "📍 **Cedes** – Información sobre cada núcleo y los PNF que ofrecen.\n\n"
    "⬇️ **Selecciona una opción:**"
)


def _keyboard_institucional():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🎓 Planilla Pregrado", callback_data='institucional_pregrado'),
            InlineKeyboardButton("🏛️ Planilla Posgrado", callback_data='institucional_posgrado')
        ],
        [
            InlineKeyboardButton("📜 Reseña Histórica", callback_data='institucional_historia'),
            InlineKeyboardButton("📚 PNF", callback_data='pnf_listado')
        ],
        [
            InlineKeyboardButton("📍 Cedes", callback_data='mostrar_cedes')
        ],
        [InlineKeyboardButton("⬅️ Volver al Inicio", callback_data='volver_inicio')]
    ])



async def mostrar_menu_institucional(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Muestra el menú institucional con contexto (edita el mensaje original)."""
    query = update.callback_query
    await query.answer()

    reply_markup = _keyboard_institucional()
    
    await query.edit_message_text(
        TEXTO_CONTEXTO_INSTITUCIONAL,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def manejar_archivo_institucional(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Procesa el envío del documento y texto de recaudos, y luego muestra el menú nuevamente."""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    chat_id = query.message.chat_id

    # 1. Eliminar el menú actual
    try:
        await query.message.delete()
    except:
        pass

    # 2. Borrar todos los mensajes de menú anteriores registrados
    if 'menu_messages' in context.user_data:
        for msg_id in context.user_data['menu_messages']:
            try:
                await context.bot.delete_message(chat_id=chat_id, message_id=msg_id)
            except:
                pass
        context.user_data['menu_messages'] = []

    # 3. Enviar mensaje temporal
    temp_msg = await query.message.reply_text("📄 Enviando documento, por favor espera...")

    # 4. Procesar el documento y texto
    if data in ARCHIVOS_INSTITUCIONAL:
        config = ARCHIVOS_INSTITUCIONAL[data]
        nombre_archivo = config['nombre']
        caption_texto = config['texto']
        ruta = os.path.join("assets", "institucional", nombre_archivo)

        try:
            if os.path.exists(ruta):
                # Enviar el documento
                with open(ruta, 'rb') as doc:
                    if len(caption_texto) > 1024:
                        await query.message.reply_document(
                            document=doc,
                            read_timeout=60,
                            write_timeout=60,
                            connect_timeout=60,
                            pool_timeout=60
                        )
                        # Enviar el texto aparte si es muy largo
                        await query.message.reply_text(text=caption_texto)
                    else:
                        await query.message.reply_document(
                            document=doc,
                            caption=caption_texto,
                            read_timeout=60,
                            write_timeout=60,
                            connect_timeout=60,
                            pool_timeout=60
                        )
            else:
                await query.message.reply_text(
                    f"❌ Error: No se encontró el archivo '{nombre_archivo}' en la ruta esperada: {ruta}"
                )
        except Exception:
            # No mostrar error específico al usuario
            pass
    else:
        await query.message.reply_text("❌ Error: Opción de archivo no reconocida.")

    # 5. Borrar mensaje temporal
    try:
        await temp_msg.delete()
    except:
        pass

    # 6. Mostrar el mismo menú institucional como mensaje nuevo al final
    await mostrar_menu_institucional_nuevo(chat_id, context)

async def mostrar_menu_institucional_nuevo(chat_id, context):
    """Envía un mensaje NUEVO con el menú institucional (con contexto) y registra su ID."""
    reply_markup = _keyboard_institucional()

    new_msg = await context.bot.send_message(
        chat_id=chat_id,
        text=TEXTO_CONTEXTO_INSTITUCIONAL,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )
    context.user_data.setdefault('menu_messages', []).append(new_msg.message_id)