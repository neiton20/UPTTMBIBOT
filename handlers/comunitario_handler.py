# handlers/comunitario_handler.py
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
import os
import asyncio

ARCHIVOS_SC = {
    'sc_ficha': '1 ESTUDIANTE Formato Ficha de inscripcion SC Feb 2025.docx',
    'sc_postulacion': '2 ESTUDIANTE Formato postulacion SC Feb 2025.docx',
    'sc_cronograma': '3_ESTUDIANTE_Formato_Cronograma_de_Actividades_Semanales_SC_Feb.docx',
    'sc_guia_elab': '4_GUIA_PARA_ELABORAR_EL_PROYECTO_DE_SERVICIO_COMUNITARIO_Feb_2025.docx',
    'sc_eval_comunidad': '5 ESTUDIANTE Formato Evaluacion Comunidad SC Feb 2025.docx',
    'sc_eval_delegado': '6 ESTUDIANTE Formato Evaluacion Delegado SC Feb 2025.docx',
    'sc_proceso': 'Como_realizar_el_Servicio_Comunitario_en_el_PNFI_Feb_2025_Ver_1.pdf',
    'sc_ley': 'ley_del_servicio_comunitario.pdf',
    'sc_que_es': 'Que es el Servicio Comunitario en la UPTTMBI Feb 2025.pdf',
    'sc_etiqueta': 'ETIQUETA DE CD SC Feb 2025.doc',
    'sc_pasos_carpeta': 'pasos para carpeta PSI.pdf',
    'sc_guia_pnfi': 'Guia-para-el-Servicio-Comunitario-en-el-PNF-en-Informatica.pdf' 
}

# Texto de contexto para el Servicio Comunitario
TEXTO_CONTEXTO_SC = (
    "📌 **¿Qué es el Servicio Comunitario?**\n\n"
    "Es una actividad obligatoria para los estudiantes de la UPTTMBI, "
    "que permite aplicar conocimientos en beneficio de las comunidades.\n\n"
    "Aquí encontrarás todos los formatos, guías y normativas necesarias:\n"
    "• Ficha de inscripción\n"
    "• Carta de postulación\n"
    "• Cronograma semanal\n"
    "• Guía de elaboración del proyecto\n"
    "• Formatos de evaluación\n"
    "• Ley del Servicio Comunitario\n"
    "• Y más documentos esenciales\n\n"
    "⬇️ **Selecciona el documento que necesitas:**"
)

def _keyboard_sc():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("1. Ficha de Inscripción", callback_data='sc_ficha')],
        [InlineKeyboardButton("2. Carta de Postulación", callback_data='sc_postulacion')],
        [InlineKeyboardButton("3. Cronograma Semanal", callback_data='sc_cronograma')],
        [InlineKeyboardButton("4. Guía de Elaboración", callback_data='sc_guia_elab')],
        [InlineKeyboardButton("5. Evalc. Comunidad", callback_data='sc_eval_comunidad')],
        [InlineKeyboardButton("6. Evalc. Delegado", callback_data='sc_eval_delegado')],
        [InlineKeyboardButton("7. ¿Qué es el S.C.?", callback_data='sc_que_es')],
        [InlineKeyboardButton("8. Proceso (Guía PDF)", callback_data='sc_proceso')],
        [InlineKeyboardButton("9. Ley de S.C.", callback_data='sc_ley')],
        [InlineKeyboardButton("10. Etiqueta de CD", callback_data='sc_etiqueta')],
        [InlineKeyboardButton("11. Pasos Carpeta", callback_data='sc_pasos_carpeta')],
        [InlineKeyboardButton("12. Guía SC PNFI", callback_data='sc_guia_pnfi')],
        [InlineKeyboardButton("⬅️ Volver al Inicio", callback_data='volver_inicio')]
    ])

async def mostrar_menu_sc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Muestra el menú de servicio comunitario con contexto (edita el mensaje original)."""
    query = update.callback_query
    await query.answer()

    reply_markup = _keyboard_sc()

    # Mensaje con contexto + pregunta
    await query.edit_message_text(
        TEXTO_CONTEXTO_SC + "\n\n¿Qué documento necesitas?", 
        reply_markup=reply_markup, 
        parse_mode='Markdown'
    )

async def manejar_archivo_sc(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
    if data in ARCHIVOS_SC:
        nombre_archivo = ARCHIVOS_SC[data]
        ruta = os.path.join("assets", "servicio_comunitario", nombre_archivo)
        
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
        await query.message.reply_text("❌ Opción no reconocida.")

    # 5. Borrar mensaje temporal
    try:
        await temp_msg.delete()
    except:
        pass

    # 6. Mostrar el mismo menú de Servicio Comunitario como mensaje nuevo al final
    await mostrar_menu_sc_nuevo(chat_id, context)

async def mostrar_menu_sc_nuevo(chat_id, context):
    """Envía un mensaje NUEVO con el menú de servicio comunitario (con contexto) y registra su ID."""
    reply_markup = _keyboard_sc()
    
    new_msg = await context.bot.send_message(
        chat_id=chat_id,
        text=TEXTO_CONTEXTO_SC + "\n\n¿Qué documento necesitas?",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )
    # Registrar el ID del nuevo menú para poder borrarlo después
    context.user_data.setdefault('menu_messages', []).append(new_msg.message_id)