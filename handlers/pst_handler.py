# handlers/pst_handler.py
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
import os

# Diccionario con los nombres exactos de los archivos
ARCHIVOS_PST = {
    'pst_descripcion': 'DESCRIPCIÓN DE CADA UNA DE LAS PARTES odt.pdf',
    'pst_normas': 'NORMAS PARA LA ELABORACIÓN Y PRESENTACIÓN DEL PSIT.pdf'
}

# Texto de contexto para el PST
TEXTO_CONTEXTO_PST = (
    "📌 **¿Qué es el PST?**\n\n"
    "El Proyecto Sociotecnológico (PST) es una actividad académica obligatoria "
    "en la UPTTMBI, donde los estudiantes aplican conocimientos tecnológicos "
    "para resolver problemas reales en comunidades o empresas.\n\n"
    "Aquí encontrarás los documentos fundamentales:\n"
    "• Descripción de cada una de las partes del PST\n"
    "• Normas para la elaboración y presentación del PSIT\n\n"
    "⬇️ **Selecciona el documento que necesitas:**"
)

def _keyboard_pst():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("1. Descripción de las Partes", callback_data='pst_descripcion')],
        [InlineKeyboardButton("2. Normas de Elaboración PSIT", callback_data='pst_normas')],
        [InlineKeyboardButton("⬅️ Volver al Inicio", callback_data='volver_inicio')]
    ])

async def mostrar_menu_pst(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Muestra el menú de PST editando el mensaje original (con contexto)."""
    query = update.callback_query
    await query.answer()

    reply_markup = _keyboard_pst()

    await query.edit_message_text(
        TEXTO_CONTEXTO_PST,
        reply_markup=reply_markup, 
        parse_mode='Markdown'
    )

async def manejar_archivo_pst(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    chat_id = query.message.chat_id

    # 1. Eliminar el menú actual (donde se hizo clic)
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
        context.user_data['menu_messages'] = []  # Limpiar la lista

    # 3. Enviar mensaje temporal
    temp_msg = await query.message.reply_text("📄 Enviando documento, por favor espera...")

    # 4. Enviar el documento o mensaje de error
    if data in ARCHIVOS_PST:
        nombre_archivo = ARCHIVOS_PST[data]
        ruta = os.path.join("assets", "PST", nombre_archivo)
        
        try:
            if os.path.exists(ruta):
                with open(ruta, 'rb') as doc:
                    await query.message.reply_document(
                        document=doc,
                        caption=f"Aquí tienes: {nombre_archivo}",
                        read_timeout=60,
                        write_timeout=60,
                        connect_timeout=60,
                        pool_timeout=60
                    )
            else:
                await query.message.reply_text(f"❌ Error: No se encontró el archivo {nombre_archivo} en el servidor.")
        except Exception:
            # Si hay error, no mostramos mensaje adicional al usuario
            pass
    else:
        await query.message.reply_text("❌ Opción no reconocida en el módulo PST.")

    # 5. Borrar mensaje temporal
    try:
        await temp_msg.delete()
    except:
        pass

    # 6. Mostrar el mismo menú de PST como mensaje nuevo al final
    await mostrar_menu_pst_nuevo(chat_id, context)

async def mostrar_menu_pst_nuevo(chat_id, context):
    """Envía un mensaje NUEVO con el menú de PST (con contexto) y registra su ID."""
    reply_markup = _keyboard_pst()
    
    new_msg = await context.bot.send_message(
        chat_id=chat_id,
        text=TEXTO_CONTEXTO_PST,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )
    # Registrar el ID del nuevo menú para poder borrarlo después
    context.user_data.setdefault('menu_messages', []).append(new_msg.message_id)