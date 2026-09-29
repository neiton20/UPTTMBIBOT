# main.py
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext, ContextTypes
from telegram.error import NetworkError, TimedOut, RetryAfter
from data.config import TELEGRAM_TOKEN
from handlers.start_handler import start, mostrar_menu_principal
from handlers.comunitario_handler import mostrar_menu_sc, manejar_archivo_sc 
from handlers.pst_handler import mostrar_menu_pst, manejar_archivo_pst
from handlers.institucional_handler import mostrar_menu_institucional, manejar_archivo_institucional
from handlers.pnf_handler import (
    mostrar_listado_pnf, 
    manejar_pnf_seleccion, 
    manejar_perfil_pnf, 
    manejar_menu_pnf
)
from handlers.sedes_handler import manejar_mostrar_cedes, manejar_sede_detalle
import os
import asyncio

# Configurar logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def error_handler(update, context: CallbackContext):
    logger.error(msg="Exception occurred:", exc_info=context.error)
    if isinstance(context.error, (NetworkError, TimedOut, RetryAfter)):
        logger.warning("Error de red, reintentando...")
    else:
        if update and update.effective_message:
            await update.effective_message.reply_text("Ocurrió un error interno. Ya se reportó.")

# Función para enviar mensaje de ayuda (¿Qué puedo hacer?)
async def mostrar_ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat_id

    # Borrar menú actual y todos los anteriores
    try:
        await query.message.delete()
    except:
        pass
    if 'menu_messages' in context.user_data:
        for msg_id in context.user_data['menu_messages']:
            try:
                await context.bot.delete_message(chat_id=chat_id, message_id=msg_id)
            except:
                pass
        context.user_data['menu_messages'] = []

    # Texto de ayuda explicando todo lo que puede hacer el bot (actualizado con Documento Rector)
    texto_ayuda = (
        "<b>🤖 ¿Qué puedo hacer con este bot?</b>\n\n"
        "✅ <b>Servicio Comunitario</b>\n"
        "Descargar formularios, guías, cronogramas, leyes y normativas (12 documentos disponibles).\n\n"
        "✅ <b>PST (Proyecto Sociotecnológico)</b>\n"
        "Obtener la descripción de las partes y las normas para su elaboración.\n\n"
        "✅ <b>Información Institucional</b>\n"
        "• Planillas de inscripción para Pregrado y Posgrado.\n"
        "• Reseña histórica de la UPTTMBI.\n"
        "• Listado de todos los Programas Nacionales de Formación (PNF) por carrera.\n"
        "• Consulta de perfiles de egreso (TSU, Ingeniero, Licenciado) y certificaciones.\n"
        "• <b>Documento Rector de cada PNF</b> (bases, objetivos y estructura del programa).\n"
        "• Sedes de la universidad y los PNF ofertados en cada una.\n\n"
        "✅ <b>Calendario Académico 2026</b>\n"
        "Descarga el calendario oficial en PDF.\n\n"
        "💡 <i>Selecciona cualquier opción del menú principal para comenzar. Cada vez que consultes un documento o información, el menú correspondiente reaparecerá automáticamente para que sigas navegando.</i>\n\n"
        "📌 <b>Consejo:</b> Puedes volver al inicio en cualquier momento con el botón '⬅️ Volver al Inicio' que aparece en los menús."
    )

    # Enviar mensaje de ayuda (sin botones)
    await context.bot.send_message(chat_id=chat_id, text=texto_ayuda, parse_mode='HTML')

    # Volver a mostrar el menú principal al final
    await mostrar_menu_principal(chat_id, context)

async def callback_dispatcher(update, context):
    query = update.callback_query
    data = query.data
    chat_id = query.message.chat_id

    if 'menu_messages' not in context.user_data:
        context.user_data['menu_messages'] = []

    if data == 'volver_inicio':
        await start(update, context)
        return

    # Servicio Comunitario
    elif data.startswith('sc_'):
        if data == 'sc_menu':
            await mostrar_menu_sc(update, context)
        else:
            await manejar_archivo_sc(update, context)

    # PST
    elif data.startswith('pst_'):
        if data == 'pst_menu':
            await mostrar_menu_pst(update, context)
        else:
            await manejar_archivo_pst(update, context)

    # Institucional
    elif data.startswith('institucional_'):
        if data == 'institucional_menu':
            await mostrar_menu_institucional(update, context)
        else:
            await manejar_archivo_institucional(update, context)

    # PNF
    elif data == 'pnf_listado':
        await mostrar_listado_pnf(update, context)
    elif data.startswith('pnf_detalle_'):
        await manejar_pnf_seleccion(update, context)
    elif data.startswith('pnf_perfil_'):
        await manejar_perfil_pnf(update, context)
    elif data.startswith('pnf_menu_'):
        await manejar_menu_pnf(update, context)

    # Sedes
    elif data == 'mostrar_cedes':
        await manejar_mostrar_cedes(update, context)
    elif data.startswith('sede_detalle_'):
        await manejar_sede_detalle(update, context)

    # Calendario Académico
    elif data == 'calendario_academico':
        await query.answer()
        chat_id = query.message.chat_id  # guardar ANTES de borrar

        try:
            await query.message.delete()
        except:
            pass

        temp_msg = await context.bot.send_message(
            chat_id=chat_id,
            text="📄 Enviando calendario académico, por favor espera..."
        )

        ruta_pdf = os.path.join("assets", "Calendario Academico 2026 UPTTMBI.pdf")
        try:
            if os.path.exists(ruta_pdf):
                with open(ruta_pdf, 'rb') as pdf:
                    await context.bot.send_document(   # ← usar context.bot, no query.message
                        chat_id=chat_id,
                        document=pdf,
                        caption="📅 Calendario Académico 2026 - UPTTMBI",
                        read_timeout=60,
                        write_timeout=60,
                        connect_timeout=60,
                        pool_timeout=60
                    )
            else:
                await context.bot.send_message(
                    chat_id=chat_id,
                    text="❌ El calendario no está disponible temporalmente."
                )
        except Exception as e:
            logger.error(f"Error enviando calendario: {e}")

        try:
            await temp_msg.delete()
        except:
            pass

        await asyncio.sleep(0.5)
        await mostrar_menu_principal(chat_id, context)

    # NUEVO: Ayuda (¿Qué puedo hacer?)
    elif data == 'ayuda':
        await mostrar_ayuda(update, context)

    else:
        await query.answer()
        await query.message.reply_text(f"Opción '{data}' no implementada.")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(callback_dispatcher))
    app.add_error_handler(error_handler)

    print("Bot iniciado correctamente...")
    app.run_polling()

if __name__ == '__main__':
    main()