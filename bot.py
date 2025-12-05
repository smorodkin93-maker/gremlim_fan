import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# ===================== НАСТРОЙКИ =====================

# ВСТАВЬ СВОЙ ТОКЕН БОТА (из BotFather)
BOT_TOKEN = "8590224138:AAH_GaHndks2jFJjq37vAwSeykbu4mY_m3o"

# ВСТАВЬ СВОЙ ADMIN_ID (число из @userinfobot)
ADMIN_ID = 237980454

# =====================================================

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Состояния пользователей: user_states[user_id] = {"index": int}
user_states = {}


def get_state(user_id: int) -> dict:
    if user_id not in user_states:
        user_states[user_id] = {"index": 0}
    return user_states[user_id]


STEPS = [
    {
        "kind": "text_answer",
        "name": "Площадь Ленина (загадка)",
        "prompt": (
            "Штаб ТТ БУБУ:\n\n"
            "Валентина Петровна, первый след увидели там, где один известный человек "
            "стоит на постаменте и всё время показывает рукой в сторону юга.\n"
            "За его спиной — здание, откуда постоянно уезжают в Suomi или Viipuri, "
            "иногда даже вовремя.\n\n"
            "Введи название этой площади."
        ),
        "answers": ["площадь ленина", "пл ленина", "пл. ленина", "ленина"],
    },
    {
        "kind": "media",
        "name": "Площадь Ленина (видео)",
        "prompt": (
            "Принято. Следующая точка — Площадь Ленина.\n\n"
            "Задание:\n"
            "1. Доедь до Площади Ленина.\n"
            "2. Сними видео, где стоишь на фоне памятника Ленину и громко говоришь:\n"
            "   “Я Валюха Будько. Я на месте. Где мой контейнер, товарищ?”\n"
            "3. Отправь видео в штаб."
        ),
    },
    {
        "kind": "text_answer",
        "name": "Площадь Ленина (год памятника)",
        "prompt": "Введи PIN-код для следующего задания: год установки памятника Ленину.",
        "answers": ["1926"],
    },
    {
        "kind": "text_answer",
        "name": "KetchUp (загадка адреса)",
        "prompt": (
            "Задание 3.\n\n"
            "Прекрасная Даша знает толк во вкусных котлетах. Там обитают булки лучше, чем в «Маке».\n"
            "На проспекте, где грозно и монументально стоит здание МВД.\n"
            "В доме, номер которого — решение уравнения:\n\n"
            "log₃( log₂(x − 48) + 1 ) = log₃(4)\n\n"
            "Отправь адрес (например: литейный 56)."
        ),
        "answers": ["литейный 56", "литейный, 56", "литейный проспект 56"],
    },
    {
        "kind": "text_answer",
        "name": "KetchUp (PIN из конверта)",
        "prompt": (
            "Верно, двигайся в Ketch Up Burgers, там тебя ждут.\n\n"
            "Пароль на входе: «А самолёт летит — колёса тёрлися, а вы не ждали нас, а мы припёрлися».\n\n"
            "Введи PIN-код из конверта."
        ),
        "answers": ["0512"],
    },
    {
        "kind": "media",
        "name": "KetchUp (видео с бургером)",
        "prompt": (
            "Закажи маленький бургер и когда его принесут:\n\n"
            "1. Попроси официанта снять тебя на видео.\n"
            "2. На видео, пока ты ешь, скажи примерно так:\n"
            "   — “Э, дядя, подъём, лафа закончилась! Как говорили древние римляне…”\n"
            "   — “Опоздавшим — кости.”\n"
            "   — “А немцы на этот счёт говорили: ин дер гроссен фамилиен нихт клювом клац-клац. Ферштейн?”\n"
            "   Официант: “Ферштейн.”\n\n"
            "3. Отправь видео в штаб."
        ),
    },
    {
        "kind": "text_answer",
        "name": "Адмиралтейство (загадка)",
        "prompt": (
            "Над грохотом и пылью,\n"
            "над шумной суетой\n"
            "плывёт на тонком шпиле\n"
            "символ золотой.\n"
            "Летают рядом чайки,\n"
            "звезда горит вдали.\n"
            "Он бы и рад причалить,\n"
            "да в небе нет земли.\n\n"
            "Ответ: какое это место?"
        ),
        "answers": ["адмиралтейство"],
    },
    {
        "kind": "media",
        "name": "Адмиралтейство (фото)",
        "prompt": (
            "Валюха, ты такая умная. Всё верно.\n\n"
            "Двигайся к Адмиралтейству и на месте сфотографируйся на фоне шпиля.\n"
            "Отправь фото в штаб."
        ),
    },
    {
        "kind": "text_answer",
        "name": "Адмиралтейство (год)",
        "prompt": "PIN-код написан на табличке Адмиралтейства. Введи год.",
        "answers": ["1811"],
    },
    {
        "kind": "text_answer",
        "name": "Медный всадник (загадка)",
        "prompt": (
            "Памятник из бронзы:\n"
            "честь царю, хвала.\n"
            "Мчится, словно ветер,\n"
            "конь тянет удила.\n"
            "На коне сидит герой,\n"
            "молодой, упрямый.\n"
            "Это памятник царю,\n"
            "что «окном в Европу» славен.\n\n"
            "Как его зовут?"
        ),
        "answers": ["медный всадник"],
    },
    {
        "kind": "media",
        "name": "Медный всадник (видео)",
        "prompt": (
            "Иди к Медному всаднику.\n\n"
            "Сними видео, где ты слегка касаешься постамента и говоришь:\n"
            "“Пётр, если увидишь контейнер с надписью ТТ БУБУ — держи его, я заберу!”\n\n"
            "Отправь видео в штаб."
        ),
    },
    {
        "kind": "text_answer",
        "name": "Медный всадник (надпись)",
        "prompt": "На постаменте есть надпись на латыни. Отправь её целиком в штаб.",
        "answers": [
            "petro primo catharina secunda",
            "petro primo catharina secunda.",
        ],
    },
    {
        "kind": "text_answer",
        "name": "Ростральные колонны (загадка)",
        "prompt": (
            "Огромные, красивые, из камня созданы,\n"
            "колонны на Васильевском стоят.\n"
            "В туман и непогоду горят на них огни,\n"
            "дорогу освещая кораблям.\n"
            "Носы побеждённых кораблей\n"
            "крепили на их борта.\n\n"
            "О чём речь?"
        ),
        "answers": ["ростральные колонны", "ростральные колонны стрелка"],
    },
    {
        "kind": "media",
        "name": "Стрелка ВО (видео)",
        "prompt": (
            "Всё верно. Двигайся на Стрелку Васильевского острова, где стоят ростральные колонны.\n\n"
            "Сними видео и громко скажи:\n"
            "“Это всё-таки другой город. Но если уж я сюда приехала, контейнер отсюда не уйдёт!”\n\n"
            "Отправь видео в штаб."
        ),
    },
    {
        "kind": "text_answer",
        "name": "Петропавловская крепость (загадка)",
        "prompt": (
            "Есть орудие одно.\n"
            "С кем же бой ведёт оно?\n"
            "Точно в полдень круглый год\n"
            "свой сигнальный залп даёт.\n"
            "Выпуская белый дым,\n"
            "бьёт зарядом холостым.\n"
            "Если в крепости стреляют —\n"
            "люди время проверяют.\n\n"
            "Что это за место?"
        ),
        "answers": ["петропавловская крепость", "петропавловка"],
    },
    {
        "kind": "media",
        "name": "Петропавловская крепость (видео)",
        "prompt": (
            "Верно, Валюха.\n\n"
            "Двигайся к Невским воротам Петропавловской крепости.\n"
            "Сними видео, где ты идёшь у ворот и говоришь:\n"
            "“Я Валюха Будько. Если контейнер тут, я его вытащу даже из-под пушечного выстрела.”\n\n"
            "Отправь видео в штаб."
        ),
    },
    {
        "kind": "text_answer",
        "name": "Петропавловская крепость (год)",
        "prompt": "Найди табличку с годом постройки. Введи сумму цифр года.",
        "answers": ["23"],
    },
    {
        "kind": "text_answer",
        "name": "ТЦ Голливуд (загадка)",
        "prompt": (
            "Отлично. Ты почти нашла контейнер.\n\n"
            "Финальный след там, новое-преновое, с пионерами и попкорном, "
            "что даже ты бы сказала: “Кто-то пилит на работу, а у нас всегда суббота!”.\n\n"
            "Что это за место?"
        ),
        "answers": ["тц голливуд", "голливуд", "торговый центр голливуд"],
    },
    {
        "kind": "media",
        "name": "ТЦ Голливуд (видео)",
        "prompt": (
            "Да-да-да. Новый ТЦ, двигайся туда поскорее.\n\n"
            "Сними финальное видео у ТЦ и громко скажи:\n"
            "“Я, Валентина Петровна Будько, официально заявляю: контейнер ТТ БУБУ будет найден!”\n\n"
            "Отправь видео в штаб."
        ),
    },
    {
        "kind": "media",
        "name": "Финальное аудио у ёлки",
        "prompt": (
            "Валентина Петровна, вы прошли весь маршрут:\n"
            "от Ленина до Медного всадника, от Адмиралтейства до Петропавловской крепости.\n\n"
            "Остался последний шаг.\n\n"
            "У ёлки (или в центре ТЦ) запиши аудио в штаб со словами:\n"
            "“ТТ БУБУ, везите контейнер с плёнкой мне.”\n\n"
            "Отправь голосовое сообщение."
        ),
    },
    {
        "kind": "end",
        "name": "Финал",
        "prompt": (
            "А теперь оглянись.\n"
            "Один подозрительный человек должен вручить тебе груз.\n\n"
            "Операция ТТ БУБУ завершена."
        ),
    },
]


async def send_step_prompt(user_id: int):
    state = get_state(user_id)
    idx = state["index"]
    if idx >= len(STEPS):
        return
    step = STEPS[idx]
    await bot.send_message(user_id, step["prompt"])


@dp.message_handler(commands=["start"])
async def handle_start(message: types.Message):
    user_id = message.from_user.id
    user_states[user_id] = {"index": 0}
    greeting = (
        "Штаб ТТ БУБУ:\n\n"
        "Если ты читаешь это, значит уже нашла конверт в ресторане и готова к операции.\n\n"
        "Отвечай на загадки, доезжай до точек, снимай кринж — всё по плану ТТ БУБУ.\n"
    )
    await message.answer(greeting)
    await send_step_prompt(user_id)


@dp.message_handler(commands=["help"])
async def handle_help(message: types.Message):
    await message.answer(
        "Это квест-бот ТТ БУБУ.\n\n"
        "• Он даёт загадку — ты отвечаешь.\n"
        "• Потом даёт задание доехать и снять медиа.\n"
        "• Ведущий (Админ) всё проверяет и запускает следующий шаг.\n\n"
        "Если что-то сломалось — пиши ведущему напрямую."
    )


@dp.message_handler(content_types=["text"])
async def handle_text(message: types.Message):
    user_id = message.from_user.id
    text = (message.text or "").strip()

    if text.startswith("/"):
        return

    state = get_state(user_id)
    idx = state["index"]
    if idx >= len(STEPS):
        await message.reply("Квест уже завершён.")
        return

    step = STEPS[idx]

    if step["kind"] != "text_answer":
        await message.reply(
            "Сейчас штаб ТТ БУБУ ждёт не текст, а медиа с точки (фото/видео/голос). "
            "Посмотри последнее задание."
        )
        return

    normalized = text.lower().strip()
    if normalized in step["answers"]:
        await message.reply("Правильно. Штаб подтверждает.\n")
        state["index"] += 1
        await send_step_prompt(user_id)
    else:
        await message.reply(
            "Ответ не сходится с данными штаба ТТ БУБУ.\n"
            "Попробуй ещё раз. Можно сформулировать по-другому, но по сути то же место/значение."
        )


@dp.message_handler(content_types=["photo", "video", "voice"])
async def handle_media(message: types.Message):
    user_id = message.from_user.id
    state = get_state(user_id)
    idx = state["index"]
    if idx >= len(STEPS):
        await message.reply("Квест уже завершён.")
        return

    step = STEPS[idx]

    if step["kind"] != "media":
        await message.reply(
            "Сейчас штаб ТТ БУБУ ждал текстовый ответ, а не медиа.\n"
            "Посмотри, что написано в последнем сообщении бота."
        )
        return

    await message.reply(
        "Штаб получил твоё медиа.\n"
        "Передаём ведущему на проверку. Жди решения."
    )

    caption = (
        f"Медиа от пользователя {user_id} на шаге {idx} ({step['name']}).\n"
        f"Если всё ок — нажми ✅, если нет — ❌."
    )

    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton(
            "✅ Одобрить", callback_data=f"approve:{user_id}:{idx}"
        ),
        InlineKeyboardButton(
            "❌ Переснять", callback_data=f"reject:{user_id}:{idx}"
        ),
    )

    # Пересылаем медиа админу
    try:
        await message.forward(ADMIN_ID)
    except Exception as e:
        logging.error(f"Ошибка при пересылке медиа админу: {e}")

    await bot.send_message(ADMIN_ID, caption, reply_markup=kb)


@dp.callback_query_handler(lambda c: c.data.startswith(("approve:", "reject:")))
async def handle_approve_reject(call: types.CallbackQuery):
    if call.from_user.id != ADMIN_ID:
        await call.answer("Ты не ведущий ТТ БУБУ.")
        return

    try:
        action, user_id_str, step_idx_str = call.data.split(":")
        target_user_id = int(user_id_str)
        step_idx = int(step_idx_str)
    except Exception:
        await call.answer("Ошибка данных callback.")
        return

    state = get_state(target_user_id)

    if state["index"] != step_idx:
        await call.answer(
            f"Игрок уже на другом шаге (текущий: {state['index']}).",
            show_alert=False,
        )
        return

    # Убираем кнопки у сообщения в чате админа
    try:
        await bot.edit_message_reply_markup(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=None,
        )
    except Exception:
        pass

    if action == "reject":
        await call.answer("Попросили переснять.")
        await bot.send_message(
            target_user_id,
            "Штаб ТТ БУБУ сообщает: ведущий попросил переснять медиа. "
            "Попробуй ещё раз — ближе к объекту/чётче/громче."
        )
        return

    if action == "approve":
        await call.answer("Одобрено. Переходим дальше.")
        await bot.send_message(
            target_user_id,
            "Штаб ТТ БУБУ: медиа одобрено. Двигаемся дальше."
        )

        state["index"] += 1
        idx = state["index"]
        if idx >= len(STEPS):
            # Финал
            await bot.send_message(
                target_user_id,
                "Квест завершён. Если ведущий рядом — жди вручения контейнера."
            )
        else:
            await send_step_prompt(target_user_id)


if __name__ == "__main__":
    print("Bot started...")
    executor.start_polling(dp, skip_updates=True)
