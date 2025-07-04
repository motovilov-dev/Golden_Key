from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from typing import Optional, Union


def _get_transfers_tabs_keyboard(active: str = "transfer") -> InlineKeyboardMarkup:
    """Возвращает клавиатуру с вкладками «Трансфер», «Аренда с водителем», «Заказы».

    Args:
        active (str): Какая вкладка активна в текущий момент (transfer|rent|orders)
    """
    def _button(name: str, text: str, callback: str):
        # Помечаем активную вкладку «золотым» кружком, а неактивную — пустым.
        prefix = "🔘 " if name == active else "⚪️ "
        return InlineKeyboardButton(text=f"{prefix}{text}", callback_data=callback)

    keyboard = [
        [
            _button("rent", "Аренда с водителем", "transfers:rent"),
        ],
        [
            _button("transfer", "Трансфер", "transfers:main"),
            _button("orders", "Заказы", "transfers:orders"),
        ]
    ]
    # Добавляем универсальную кнопку «Назад» под вкладками
    keyboard.append([InlineKeyboardButton(text="⬅️ Назад", callback_data="back")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


async def main_transfers(call: CallbackQuery, state: FSMContext, data) -> None:
    """Главный обработчик раздела «Трансфер» и под-вкладок.

    Поддерживаемые callback-data:
    • transfers:main – экран выбора маршрута (Трансфер)
    • transfers:rent – аренда с водителем
    Прочие события (например orders) обрабатываются в других handler-ах.
    """
    # Извлекаем под-команду: transfers:<subcommand>
    try:
        query = call.data.split(":")[1]
    except Exception:
        query = "main"

    if query == "main":
        # Показываем экран маршрута
        await _show_route_screen(call, state)
    elif query == "from":
        # Просим пользователя ввести адрес отправления
        await call.answer()
        prompt = await call.message.answer("<b>📍 Укажите адрес отправления</b>")
        await state.update_data(prompt_msg_id=prompt.message_id)
        await state.set_state(STATE_SET_FROM)
    elif query == "to":
        await call.answer()
        prompt = await call.message.answer("<b>🏁 Укажите адрес назначения</b>")
        await state.update_data(prompt_msg_id=prompt.message_id)
        await state.set_state(STATE_SET_TO)
    elif query == "swap":
        state_data = await state.get_data()
        from_addr = state_data.get("transfer_from")
        to_addr = state_data.get("transfer_to")
        await state.update_data(transfer_from=to_addr, transfer_to=from_addr)
        await _show_route_screen(call, state)
    elif query == "rent":
        await call.message.edit_text(
            "<b>🚙 Аренда с водителем</b>\n\n<i>Напишите точку отправления, либо выберите другой раздел.</i>",
            reply_markup=_get_transfers_tabs_keyboard(active="rent")
        )
    elif query == "orders":
        await call.message.edit_text(
            "<b>🚗 Трансфер</b>\n\n<i>Ваши заказы</i>",
            reply_markup=_get_transfers_tabs_keyboard(active="orders")
        )
    else:
        # Неподдерживаемая под-команда – возвращаемся к главному меню трансфера
        await call.message.edit_text(
            "<b>🚗 Трансфер</b>",
            reply_markup=_get_transfers_tabs_keyboard(active="transfer")
        )


# --- Константы состояний ----------------------------------------------------

STATE_SET_FROM = "transfers:set_from"
STATE_SET_TO = "transfers:set_to"

# ---------------------------------------------------------------------------


def _build_route_text(from_addr: Optional[str], to_addr: Optional[str]) -> str:
    """Формирует текст сообщения с текущими данными маршрута."""
    from_part = from_addr if from_addr else "<i>Введите адрес</i>"
    to_part = to_addr if to_addr else "<i>Введите адрес</i>"

    return f"""
<b>🚗 Маршрут</b>

<b>Откуда:</b> {from_part}
<b>Куда:</b> {to_part}
"""


def _get_route_keyboard(from_addr: Optional[str], to_addr: Optional[str]) -> InlineKeyboardMarkup:
    """Клавиатура именно экрана маршрута (когда активна вкладка «Трансфер»)."""
    keyboard: list[list[InlineKeyboardButton]] = []

    # Кнопка «Откуда»
    keyboard.append([
        InlineKeyboardButton(
            text="📍 Откуда" if not from_addr else f"📍 {from_addr[:20]}…" if len(from_addr) > 20 else f"📍 {from_addr}",
            callback_data="transfers:from"
        )
    ])

    # Кнопка «Поменять местами»
    keyboard.append([
        InlineKeyboardButton(text="↕️ Поменять", callback_data="transfers:swap")
    ])

    # Кнопка «Куда»
    keyboard.append([
        InlineKeyboardButton(
            text="🏁 Куда" if not to_addr else f"🏁 {to_addr[:20]}…" if len(to_addr) > 20 else f"🏁 {to_addr}",
            callback_data="transfers:to"
        )
    ])

    # Кнопка «Назад» снизу
    keyboard.append([InlineKeyboardButton(text="⬅️ Назад", callback_data="back")])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


# ---------------------------------------------------------------------------
# Основной callback-обработчик
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# Вспомогательные функции для отображения
# ---------------------------------------------------------------------------


async def _show_route_screen(call: Union[CallbackQuery, Message], state: FSMContext):
    """Всегда удаляет предыдущую карточку и отправляет новую."""

    # Данные маршрута
    st = await state.get_data()
    from_addr = st.get("transfer_from")
    to_addr = st.get("transfer_to")

    text = _build_route_text(from_addr, to_addr)

    # Клавиатура (вкладки + маршрут) без дублирующего «Назад»
    tabs_kb = _get_transfers_tabs_keyboard(active="transfer").inline_keyboard[:-1]  # cut last row (back)
    route_kb = _get_route_keyboard(from_addr, to_addr).inline_keyboard
    keyboard = InlineKeyboardMarkup(inline_keyboard=tabs_kb + route_kb)

    bot = call.bot
    chat_id = call.message.chat.id if isinstance(call, CallbackQuery) else call.chat.id

    # Если вызов пришёл по коллбэку – убираем сообщение, из которого пришёл коллбэк
    if isinstance(call, CallbackQuery):
        try:
            await bot.delete_message(chat_id, call.message.message_id)
        except Exception:
            pass

    # Удаляем предыдущую карточку, если есть
    prev_msg_id = st.get("route_msg_id")
    if prev_msg_id:
        try:
            await bot.delete_message(chat_id, prev_msg_id)
        except Exception:
            pass

    # Отправляем новую
    new_msg = await bot.send_message(chat_id, text, reply_markup=keyboard)

    # Сохраняем новый id
    await state.update_data(route_msg_id=new_msg.message_id)

    # Для callback нужно закрыть «часики»
    if isinstance(call, CallbackQuery):
        try:
            await call.answer()
        except Exception:
            pass


# ---------------------------------------------------------------------------
# Обработчики ввода адресов (Message)
# ---------------------------------------------------------------------------


async def set_from_address(message: Message, state: FSMContext, data):
    """Сохраняет адрес отправления."""
    await state.update_data(transfer_from=message.text)
    await state.set_state(None)
    state_data = await state.get_data()
    # Удаляем prompt и ввод пользователя
    prompt_id = state_data.get("prompt_msg_id")
    if prompt_id:
        try:
            await message.bot.delete_message(message.chat.id, prompt_id)
        except Exception:
            pass
        await state.update_data(prompt_msg_id=None)
    try:
        await message.delete()
    except Exception:
        pass
    # Показываем обновлённый экран маршрута
    await _show_route_screen(message, state)


async def set_to_address(message: Message, state: FSMContext, data):
    """Сохраняет адрес назначения."""
    await state.update_data(transfer_to=message.text)
    await state.set_state(None)
    state_data = await state.get_data()
    prompt_id = state_data.get("prompt_msg_id")
    if prompt_id:
        try:
            await message.bot.delete_message(message.chat.id, prompt_id)
        except Exception:
            pass
        await state.update_data(prompt_msg_id=None)
    try:
        await message.delete()
    except Exception:
        pass
    await _show_route_screen(message, state) 