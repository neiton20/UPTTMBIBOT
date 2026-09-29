# handlers/sedes_handler.py
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

# Datos extraídos del documento PNFS.docx (Opción B)
SEDES_DATA = {
    "la_beatriz": {
        "nombre": "Núcleo La Beatriz (Valera)",
        "descripcion": "Sede principal definitiva de la UPTTMBI, ubicada en La Beatriz, Valera.",
        "pnf": [
            "Informática", "Administración", "Contaduría Pública",
            "Turismo", "Construcción Civil", "Electricidad", "Psicología Social"
        ]
    },
    "san_luis": {
        "nombre": "Núcleo San Luis (Valera)",
        "descripcion": "Segundo núcleo en Valera, ubicado en San Luis.",
        "pnf": [
            "Ingeniería de Mantenimiento", "Mecánica", "Psicología Social", "Ingeniería Industrial"
        ]
    },
    "trujillo": {
        "nombre": "Núcleo Trujillo",
        "descripcion": "Núcleo en la ciudad de Trujillo.",
        "pnf": ["Informática", "Administración", "Contaduría Pública", "Turismo"]
    },
    "bocono": {
        "nombre": "Núcleo Boconó",
        "descripcion": "Núcleo Fabricio Ojeda en Boconó.",
        "pnf": ["Informática", "Administración", "Contaduría Pública", "Turismo", "Psicología Social"]
    },
    "el_dividive": {
        "nombre": "Núcleo El Dividive",
        "descripcion": "Núcleo Francisco de Miranda en El Dividive.",
        "pnf": ["Informática", "Administración", "Ingeniería de Mantenimiento"]
    },
    "carache": {
        "nombre": "Extensión Carache",
        "descripcion": "Extensión universitaria en Carache.",
        "pnf": ["Informática", "Administración", "Contaduría Pública"]
    }
}

# Texto de contexto para el listado de sedes
TEXTO_CONTEXTO_SEDES = (
    "<b>📍 Sedes de la UPTTMBI</b>\n\n"
    "La universidad cuenta con varios núcleos y extensiones en el estado Trujillo. "
    "Cada sede ofrece diferentes Programas Nacionales de Formación (PNF).\n\n"
    "Selecciona una sede para ver su descripción y la lista de carreras disponibles."
)

def _keyboard_sedes():
    keyboard = []
    for key, data in SEDES_DATA.items():
        keyboard.append([InlineKeyboardButton(data["nombre"], callback_data=f"sede_detalle_{key}")])
    keyboard.append([InlineKeyboardButton("⬅️ Volver a Institucional", callback_data='institucional_menu')])
    return InlineKeyboardMarkup(keyboard)


# FUNCIONES DE MENÚ (con edit_message_text para navegación normal)

async def mostrar_listado_cedes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Muestra el listado de sedes editando el mensaje original (con contexto)."""
    query = update.callback_query
    await query.answer()

    reply_markup = _keyboard_sedes()

    await query.edit_message_text(
        TEXTO_CONTEXTO_SEDES,
        reply_markup=reply_markup,
        parse_mode='HTML'
    )


# FUNCIONES PARA ENVIAR MENÚS COMO MENSAJES NUEVOS (después de una acción)

async def mostrar_listado_cedes_nuevo(chat_id, context):
    """Envía un mensaje NUEVO con el listado de sedes (con contexto) y registra su ID."""
    reply_markup = _keyboard_sedes()
    
    new_msg = await context.bot.send_message(
        chat_id=chat_id,
        text=TEXTO_CONTEXTO_SEDES,
        reply_markup=reply_markup,
        parse_mode='HTML'
    )
    context.user_data.setdefault('menu_messages', []).append(new_msg.message_id)


# MANEJADOR DEL DETALLE DE SEDE (envía la info como mensaje nuevo y luego el listado)

async def mostrar_detalle_sede(update: Update, context: ContextTypes.DEFAULT_TYPE, sede_key: str):
    """Muestra la información de la sede como mensaje nuevo, luego vuelve a mostrar el listado."""
    query = update.callback_query
    chat_id = query.message.chat_id

    # 1. Eliminar el menú actual (desde donde se hizo clic)
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

    # 3. Obtener la información de la sede
    data = SEDES_DATA.get(sede_key)
    if not data:
        await context.bot.send_message(chat_id=chat_id, text="❌ Sede no encontrada.")
    else:
        texto = f"<b>{data['nombre']}</b>\n\n"
        texto += f"<i>{data['descripcion']}</i>\n\n"
        texto += "<b>📚 Programas Nacionales de Formación (PNF) disponibles:</b>\n"
        for pnf in data["pnf"]:
            texto += f"• {pnf}\n"

        # 4. Enviar el texto de la sede como mensaje nuevo SIN BOTONES
        await context.bot.send_message(
            chat_id=chat_id,
            text=texto,
            parse_mode='HTML'
        )

    # 5. Mostrar el listado de sedes como mensaje nuevo al final
    await mostrar_listado_cedes_nuevo(chat_id, context)


# MANEJADORES PRINCIPALES PARA EL ROUTER

async def manejar_mostrar_cedes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Callback para 'mostrar_cedes' (primera vez que se entra a sedes)."""
    await mostrar_listado_cedes(update, context)

async def manejar_sede_detalle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Callback para 'sede_detalle_xxx' (cuando se elige una sede)."""
    query = update.callback_query
    await query.answer()
    data = query.data
    sede_key = data.replace("sede_detalle_", "")
    await mostrar_detalle_sede(update, context, sede_key)