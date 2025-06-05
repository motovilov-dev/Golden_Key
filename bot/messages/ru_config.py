from .base_config import BaseMessageModel

class RussianMessages(BaseMessageModel):
    start: str = '''
<b>Здравствуйте, {first_name}!</b>

Это бот Golden Key!
Напиши в чат любой вопрос

<b>Выберите действие:</b>
'''
    help: str = "Это помощь на русском языке..."
    unknown_command: str = "Неизвестная команда"
    halls_cities: str = "<b>🏘️ Бизнес залы</b>\n\nВыберите город:"
    hall_card: str = """<b>🏘️ {name}</b>
<b>🌆 {city}</b>

📍 <b>Расположение:</b> {location}
⏰ <b>Режим работы:</b> {working_time}"""
    hall_details: str = """<b>🏘️ {name}</b>
<b>🌆 {city}</b>
📍 {location}
⏰ {working_time}

<b>Услуги:</b>
{services}"""
    no_halls: str = "К сожалению, в данном городе нет доступных залов."
    available_passes: str = "<b>🗓️ Доступные пропуски</b>\n\n"
    main_login: str = "<b>Вход в систему</b>\n\nВыберите действие:"
    auth_choose_method: str = "<b>Выберите способ авторизации:</b>"
    reg_stage1: str = "<b>Регистрация в системе</b>\n\nВведите номер телефона\n\n<i>Подсказка: 79998887766</i>"
    reg_stage2: str = "<b>Регистрация в системе</b>\n\nВведите код из SMS"
    reg_stage3: str = "<b>Регистрация в системе</b>\n\nВведите имя"
    reg_stage4: str = "<b>Регистрация в системе</b>\n\nВведите фамилию"
    reg_stage5: str = "<b>Регистрация в системе</b>\n\nВведите email"
    auth_email_stage1: str = "<b>Вход в систему</b>\n\nВведите email"
    auth_email_stage2: str = "<b>Вход в систему</b>\n\nВведите пароль"
    auth_phone_stage1: str = "<b>Вход в систему</b>\n\nВведите номер телефона\n\n<i>Подсказка: 79998887766</i>"
    auth_phone_stage2: str = "<b>Вход в систему</b>\n\nВведите код из SMS"
    profile: str = '''
<b>👤 Профиль пользователя</b>

<code>🆔 TG ID:</code> <b>{tg_id}</b>
<code>🔑 GK ID:</code> <b>{gk_id}</b>
<code>💳 Card ID:</code> <b>{card_id}</b>
<code>✈️ AeroFlot ID:</code> <b>{af_id}</b>

━━━━━━━━━━━━━━
<i>✨ {first_name} {last_name}</i>
<i>📧 {email}</i>
<i>📞 {phone}</i>
━━━━━━━━━━━━━━

<code>🎫 Доступно проходов:</code> <b>{passes_amount}</b> <i>раз(а)</i>
'''
    service: str = '''
<b>🔌 Дополнительные услуги</b>

<b>{name}</b>
{description}

━━━━━━━━━━━━━━
<i>Промокод на <b>{denomination}</b> рублей</i>
<i><b>1 бонус = 1 рубль</b></i>
━━━━━━━━━━━━━━

<b>Доступно визитов для обмена:</b> <code>{passes_amount}</code>
'''
    success_login: str = "<b>✅ Авторизация: Успешно!</b>\n\nПриветсвуем, {first_name}!\n\n<i>Выберите действие:</i>"
    sessions_main: str = '''
<b>📅 Ваши визиты</b>

<b>Посетитель:</b> <code>{visitor}</code>
<b>Время посещения:</b> <code>{start_time}</code>
<b>Статус:</b> <code>{status}</code>

<b>Зал:</b> <code>{hall}</code>

━━━━━━━━━━━━━━
<i>Визит создан <b>{created_at}</b></i>
━━━━━━━━━━━━━━
'''
    orders_main: str = '''
<b>📅 Ваши заказы</b>    
{orders}
'''
    order: str = '''
<b>📍 Заказ №{order_id}</b>
<b>Статус:</b> <code>{status}</code>
<b>Визитов:</b> <code>{passes_amount}</code>
━━━━━━━━━━━━━━
<b>Цена:</b> <code>{amount} руб.</code>
<b>Создан:</b> <code>{created_at}</code>
'''
    promo: str = '''
<b>🎁 Промокоды</b>
{promos}
'''
    promo_code: str = '''
<b>🎁 Промокод</b>
<b>Код:</b> <code>{code}</code>
<b>Сервис:</b> <code>{service_name}</code>
<b>Статус:</b> <code>{status}</code>
━━━━━━━━━━━━━━
<i><b>Создан:</b> <code>{created_at}</code></i>
'''