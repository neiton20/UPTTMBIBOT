# handlers/start_handler.py
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

def _build_menu_principal():
    keyboard = [
        [InlineKeyboardButton("¿Qué puedo hacer?❓", callback_data='ayuda')],
        [
            InlineKeyboardButton("🎓 Servicio Comunitario", callback_data='sc_menu'),
            InlineKeyboardButton("📂 PST", callback_data='pst_menu')
        ],
        [InlineKeyboardButton("🏫 Institucional", callback_data='institucional_menu')],
        [InlineKeyboardButton("📅 Calendario Académico 2026", callback_data='calendario_academico')]
    ]
    return InlineKeyboardMarkup(keyboard)

MENSAJE_BIENVENIDA = (
    "¡Bienvenido al Bot de la UPTTMBI! 🤖\n\n"
    "Usa los botones para navegar. Presiona ¿Qué puedo hacer?❓ para conocer todas mis funciones."
)

async def mostrar_menu_principal(chat_id, context):
    """Envía el menú principal usando solo chat_id (sin depender de query.message)."""
    reply_markup = _build_menu_principal()
    new_msg = await context.bot.send_message(
        chat_id=chat_id,
        text=MENSAJE_BIENVENIDA,
        reply_markup=reply_markup
    )
    context.user_data.setdefault('menu_messages', []).append(new_msg.message_id)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        query = update.callback_query
        chat_id = query.message.chat_id
        await query.answer()
        try:
            await query.message.delete()
        except:
            pass
    else:
        chat_id = update.message.chat_id

    # Borrar todos los mensajes de menú anteriores
    if 'menu_messages' in context.user_data:
        for msg_id in context.user_data['menu_messages']:
            try:
                await context.bot.delete_message(chat_id=chat_id, message_id=msg_id)
            except:
                pass
        context.user_data['menu_messages'] = []

    await mostrar_menu_principal(chat_id, context)