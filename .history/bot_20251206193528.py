import logging
from typing import Dict, Any

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    InputFile,
    ContentType,
)

# ==================== НАСТРОЙКИ ====================

# TODO: подставь реальные значения
BOT_TOKEN = "8590224138:AAH_GaHndks2jFJjq37vAwSeykbu4mY_m3o"
ADMIN_ID = 237980454  # твой Telegram ID (узнаётся через @userinfobot)

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# состояние пользователя: текущий шаг, ждём ли кнопку и т.п.
user_states: Dict[int, Dict[str, Any]] = {}

# ==================== ШАГИ КВЕСТА ====================
# Схема:
# 1) kind = "text_answer" — большая загадка про локацию
#       prompt: текст загадки
#       answers: варианты ответа (низкий регистр, без лишних пробелов)
#       success_text: текст при правильном ответе
#       image: (опц.) имя файла с картинкой рядом с bot.py
#       needs_button: True → после правильного ответа даём кнопку "Новое задание"
#       next_button_text: текст на этой кнопке
#       retry_text: текст при неправильном ответе
#
# 2) kind = "media" — задание на видео/фото
#       prompt: текст задания
#       После того, как АДМИН нажимает "✅ Одобрить", бот переходит к следующему шагу.
#
# 3) kind = "pin_code" — мини-задание с кодом
#       prompt: текст задания
#       pins: список допустимых строк
#       success_text: текст при верном pin
#       retry_text: текст при неверном
#       После верного pin бот сразу переходит к следующему шагу (обычно новая text_answer).

STEPS = [
    # ===== ЦИКЛ 1: ПЛОЩАДЬ ЛЕНИНА =====
    {
        "kind": "text_answer",
        "name": "Площадь Ленина — загадка",
        "prompt": (
            "Штаб ТТ БУБУ:\n\n"
            "Валентина Петровна, первый след увидели там, где один известный человек стоит "
            "на постаменте и всё время показывает рукой в сторону юга.\n"
            "За его спиной — здание, откуда постоянно уезжают в Suomi или Viipuri, иногда даже вовремя.\n\n"
            "Введи название этой площади."
        ),
        "answers": [
            "площадь ленина",
            "пл ленина",
            "пл. ленина",
            "ленина",
            "площадь ленина, санкт-петербург",
        ],
        "success_text": "Принято. Это Площадь Ленина. Двигайся туда, как будешь там, жми кнопку.",
        "image": "01.png",  # файл рядом с bot.py
        "needs_button": True,
        "next_button_text": "Следующее задание",
        "retry_text": "Ответ не правильный. Попробуй ещё раз.",
    },
    {
        "kind": "media",
        "name": "Площадь Ленина — видео",
        "prompt": (
            "Ты на Площади Ленина:\n\n"
            "Сними видео, где ты стоишь на фоне памятника Ленину и громко говоришь:\n"
            "«Вы сейчас похоже на древнюю царицу. Нефиртити? Ну, я не фертю, честное слово»\n\n"
            "Отправь видео сюда. Штаб передаст его Митяю на проверку."
        ),
    },
    {
        "kind": "pin_code",
        "name": "Площадь Ленина — год установки памятника",
        "prompt": (
            "Мини-задание.\n"
            "Пин код для продложения - год установки памятника. Введи его сюда."
        ),
        "pins": ["1926"],
        "success_text": (
            "Код 1926 принят. Штаб доволен.\n"
            "Теперь слушай новую легенду"
        ),
        "retry_text": "Код не подходит. Думай дальше и введи ещё раз.",
    },

    # ===== ЦИКЛ 2: KETCHUP НА ЛИТЕЙНОМ =====
    {
        "kind": "text_answer",
        "name": "KetchUp — загадка адреса",
        "prompt": (
            "Задание.\n\n"
            "Прекрасная Даша знает толк во вкусных котлетах. Она знает где обитают булки лучше, чем в «Маке».\n"
            "Это проспект, где грозно и монументально стоит здание МВД.\n"
            "Дом с номером, который равен решению уравнения:\n\n"
            "log₃( log₂(x − 51) + 1 ) = log₃(4).\n\n"
            "Отправь адрес полностью (например: Воронцовский 11)."
        ),
        "answers": [
            "литейный 59",
            "литейный, 59",
            "литейный проспект 59",
        ],
        "success_text": (
            "Верно, это KetchUp Burgers на Литейном.\n"
            "Двигайся туда. Как будешь на месте, жми новое задание."
        ),
        "image": "02.png",
        "needs_button": True,
        "next_button_text": "Новое задание",
        "retry_text": "Штаб не узнаёт этот адрес. Попробуй ещё раз.",
    },
    {
        "kind": "media",
        "name": "KetchUp — видео с бургером",
        "prompt": (
            "В KetchUp Burgers скажи на входе пароль с вырожением =) :\n"
            "«А самолёт летит — колёса тёрлися, а вы не ждали нас, а мы припёрлися».\n\n"
            "Тебе дадут конверт с паролем для слеюудщего задания и поможет заказать маленький бургер. Когда его принесут:\n\n"
            "1) Попроси официанта снять тебя на видео.\n"
            "2) Пока ты ешь, произнеси на видео примерно так:\n"
            "   «Как говорили древние римляне — "
            "опоздавшим — кости. А немцы на этот счёт говорили: "
            "ин дер гроссен фамилиен нихт клювом клац-клац. Ферштейн?»\n"
            "   (официант должен ответить: «Ферштейн»)\n\n"
            "Отправь это видео сюда. Штаб передаст его Митяю на проверку."
        ),
    },
    {
        "kind": "pin_code",
        "name": "KetchUp — PIN из конверта",
        "prompt": (
            "Мини-задание.\n"
            "В конверте, который тебе выдали в KetchUp,\n"
            "есть зашифрованный PIN-код, который знают только 2 человека.\n"
            "Введи его сюда."
        ),
        "pins": ["05.12.2022"],
        "success_text": (
            "PIN 05.12.2022 принят. Штаб доволен.\n"
            "Теперь слушай новую легенду...."
        ),
        "retry_text": "PIN не сходится с данными штаба. Перепроверь и попробуй ещё раз.",
    },

    # ===== ЦИКЛ 3: АДМИРАЛТЕЙСТВО =====
    {
        "kind": "text_answer",
        "name": "Адмиралтейство — загадка",
        "prompt": (
            "Над грохотом и пылью,\n"
            "над шумной суетой\n"
            "плывёт на тонком шпиле\n"
            "символ золотой.\n"
            "Летают рядом чайки,\n"
            "звезда горит вдали.\n"
            "Он бы и рад причалить,\n"
            "да в небе нет земли.\n\n"
            "О каком месте идёт речь?"
        ),
        "answers": ["адмиралтейство", "здание адмиралтейства"],
        "success_text": "Верно. Адмиралтейство. Двигайся туда.",
        "image": "03.png",
        "needs_button": True,
        "next_button_text": "Новое задание",
        "retry_text": "Штаб не узнаёт эту загадку. Попробуй ещё раз.",
    },
    {
        "kind": "media",
        "name": "Адмиралтейство — фото со шпилем",
        "prompt": (
            "Когда будешь у Адмиралтейства:\n\n"
            "Сделай фото, где видно тебя и золотой шпиль.\n"
            "Отправь фото сюда. Штаб передаст его Митяю для проверки."
        ),
    },
    {
        "kind": "pin_code",
        "name": "Адмиралтейство — год",
        "prompt": (
            "Мини-задание.\n"
            "На табличке на здании Адмиралтейства найди год постройки, там где еще стоят Нимфы.\n\n"
            "Отправь год постройки с табилчки в Штаб."
        ),
        "pins": ["1811"],
        "success_text": (
            "Год 1811 принят. Штаб доволен.\n"
            "Теперь слушай новую легенду."
        ),
        "retry_text": "Год не сходится с данными штаба. Попробуй ещё раз.",
    },

    # ===== ЦИКЛ 4: МЕДНЫЙ ВСАДНИК =====
    {
        "kind": "text_answer",
        "name": "Медный всадник — загадка",
        "prompt": (
            "Памятник из бронзы:\n"
            "честь царю, хвала.\n"
            "Мчится, словно ветер,\n"
            "конь тянет удила.\n"
            "На коне сидит правитель,\n"
            "что «окном в Европу» славен.\n\n"
            "Как называется этот памятник?"
        ),
        "answers": ["медный всадник"],
        "success_text": "Верно. Медный всадник. Двигайся туда.",
        "image": "04.png",
        "needs_button": True,
        "next_button_text": "Новое задание",
        "retry_text": "Штаб не узнаёт этот памятник. Попробуй ещё раз.",
    },
    {
        "kind": "media",
        "name": "Медный всадник — видео",
        "prompt": (
            "Когда будешь у Медного всадника:\n\n"
            "Сними видео, где ты слегка касаешься постамента и говоришь:\n"
            "«Гля, Я что-то не поняла, ты еще здесь? Здесь. \n"
            "А я тебе что, Юппи что ли - мнгновенно растворяться?»\n\n"
            "Отправь видео сюда. Штаб передаст его ведущему."
        ),
    },
    {
        "kind": "pin_code",
        "name": "Медный всадник — надпись",
        "prompt": (
            "Мини-задание.\n"
            "На постаменте есть надпись на латыни.\n"
            "Отправь первые 4 слова"
        ),
        "pins": [
            "PETRO primo CATHARINA secunda",
            "petro primo catharina secunda",
            "Petro Primo Catharina Secunda",
            "Petro primo Catharina secunda",
            "Petro primo catharina secunda.",
        ],
        "success_text": (
            "Надпись совпала с данными штаба. Валюха, ты хорошо работаешь.\n"
            "Теперь слушай новую легенду"
        ),
        "retry_text": "Надпись не совпадает. Проверь внимательно и попробуй ещё раз.",
    },

    # ===== ЦИКЛ 5: РОСТРАЛЬНЫЕ КОЛОННЫ / СТРЕЛКА ВО =====
    {
        "kind": "text_answer",
        "name": "Ростральные колонны — загадка",
        "prompt": (
            "Огромные, красивые, из камня созданы,\n"
            "колонны на Васильевском стоят.\n"
            "В туман и в непогоду горят на них огни,\n"
            "дорогу освещая кораблям.\n"
            "Носы побеждённых кораблей\n"
            "крепили на их борта...\n\n"
            "О чём речь?"
        ),
        "answers": ["ростральные колонны", "ростральные колонны на стрелке"],
        "success_text": "Верно. Ростральные колонны на Стрелке ВО. Двигайся туда.",
        "image": "05.png",
        "needs_button": True,
        "next_button_text": "Новое задание",
        "retry_text": "Штаб не узнаёт этот объект. Попробуй ещё раз.",
    },
    {
        "kind": "media",
        "name": "Стрелка ВО — видео",
        "prompt": (
            "Когда будешь на Стрелке Васильевского острова у ростральных колонн:\n\n"
            "Сними видео и громко скажи что-то вроде:\n"
            "«Дед, лучше бы вы купили подводную лодку! — А зачем? \n"
            "— Потому что сейчас залечь на дно вам бы ой как не помешало.»\n\n"
            "Отправь видео сюда. Штаб передаст его Митяю на проверку."
        ),
    },

    # ===== ЦИКЛ 6: ПЕТРОПАВЛОВСКАЯ КРЕПОСТЬ =====
    {
        "kind": "text_answer",
        "name": "Петропавловская крепость — загадка",
        "prompt": (
            "Есть орудие одно.\n"
            "С кем же бой ведёт оно?\n"
            "Точно в полдень круглый год\n"
            "свой сигнальный залп даёт.\n"
            "Выпуская белый дым,\n"
            "бьёт зарядом холостым.\n"
            "Если в крепости стреляют —\n"
            "люди время проверяют.\n\n"
            "О каком месте идёт речь?"
        ),
        "answers": [
            "петропавловская крепость",
            "петропавловка",
            "невские ворота петропавловской крепости",
        ],
        "success_text": "Верно. Петропавловская крепость. Двигайся к Невским воротам.",
        "image": "06.png",
        "needs_button": True,
        "next_button_text": "Новое задание",
        "retry_text": "Штаб сомневается. Попробуй ещё раз отгадать место.",
    },
    {
        "kind": "media",
        "name": "Петропавловская крепость — видео у ворот",
        "prompt": (
            "Когда будешь у Невских ворот Петропавловской крепости:\n\n"
            "Сними видео, где ты идёшь у ворот и говоришь:\n"
            "«И сбросил Геракл свои сандалии кожаные, что у Турции\n"
            "за немереные деньги были куплены, и спустился со своим \n"
            "другом Иолаем Николавной в болото, с лернейской гидрой \n"
            "сражаться. Потому шо в такой грязюке и не такая гадость \n" 
            "завестись может.»\n\n"
            "Отправь видео сюда. Штаб передаст его ведущему."
        ),
    },
    {
        "kind": "pin_code",
        "name": "Петропавловская крепость — сумма цифр года",
        "prompt": (
            "Мини-задание.\n"
            "Найди табличку с годом постройки и введи сумму цифр этого года."
        ),
        "pins": ["23"],
        "success_text": (
            "Сумма цифр совпала. Штаб доволен.\n"
            "Теперь слушай последнюю легенду"
        ),
        "retry_text": "Сумма цифр не сходится. Проверь табличку и попробуй ещё раз.",
    },

    # ===== ЦИКЛ 7: ТЦ «ГОЛЛИВУД» + ФИНАЛ =====
    {
        "kind": "text_answer",
        "name": "ТЦ Голливуд — загадка",
        "prompt": (
            "Отлично. Валюха, Ты почти нашла контейнер.\n\n"
            "Финальный след там, где всё новое-преновое, с пионерами и большими строениями, "
            "Как сказал Иван «Кто-то пилит на работу, а у нас всегда суббота!»\n\n"
            "Что это за место?"
        ),
        "answers": ["тц голливуд", "голливуд", "торговый центр голливуд"],
        "success_text": (
            "Верно. ТЦ «Голливуд». Двигайся туда.\n"
            "Финальный этап уже близко."
        ),
        "image": "07.png",
        "needs_button": True,
        "next_button_text": "Новое задание",
        "retry_text": "Штаб не узнаёт это место. Попробуй ещё раз.",
    },
    {
        "kind": "media",
        "name": "ТЦ Голливуд — финальное видео",
        "prompt": (
            "Когда будешь у ТЦ «Голливуд»:\n\n"
            "Сними финальное видео и громко скажи:\n"
            "«Я, Валентина Петровна Будько, официально заявляю: контейнер ТТ БУБУ будет найден!»\n\n"
            "Отправь видео сюда. Штаб передаст его ведущему."
        ),
    },
    {
        "kind": "media",
        "name": "Финальное фото у ёлки",
        "prompt": (
            "Теперь нужно верифицировать получателя.\n\n"
            "Найди ёлку у ТЦ и сделай красивое фото с тобой:\n"
            "«Отправь красивую себяшку на фоне елки сюда. \n\n"
            "Чтобы Штаб отправил агента на вручение контейнера нажми - Получить ГРУЗ.»."
        ),
    },
    
]

# ==================== ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ====================

def get_state(user_id: int) -> Dict[str, Any]:
    if user_id not in user_states:
        user_states[user_id] = {"index": 0, "waiting_next_button": False}
    return user_states[user_id]


async def send_step_prompt(user_id: int):
    """Отправляет текст текущего шага согласно state['index']."""
    state = get_state(user_id)
    idx = state["index"]

    if idx >= len(STEPS):
        await bot.send_message(
            user_id,
            "Квест завершён. Если Митяй рядом — жди вручения контейнера."
        )
        return

    step = STEPS[idx]
    prompt = step.get("prompt", "")
    await bot.send_message(user_id, prompt)


# ==================== КОМАНДЫ ====================

@dp.message_handler(commands=["start"])
async def handle_start(message: types.Message):
    user_id = message.from_user.id
    user_states[user_id] = {"index": 0, "waiting_next_button": False}

    greeting = (
       "Если ты читаешь это, значит уже нашел конверт в ресторане и готов к операции БУ.\n\n"
        "Твой позывной Валюха\n"
        "Отвечай на загадки, доезжай до точек, снимай видео — всё по плану ТТ БУБУ.\n"
        "Ты можешь использовать транспорт, чтобы перемещаться между локациями\n"
        "Делай все сам. Не залей сразу в интернет и не ищи ответы, так будет веселе и интереснее\n"
        "Груз ценный и чтобы его получить нужно завершить все задания и пароли.\n "
        "У контейнера есть срок годности, время пошло."
    )
    await message.answer(greeting)

    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("Готов", callback_data="ready"))

    await message.answer(
        "Как будешь морально готов к первому заданию — жми «Готов».",
        reply_markup=kb,
    )


@dp.callback_query_handler(lambda c: c.data == "ready")
async def handle_ready(call: types.CallbackQuery):
    user_id = call.from_user.id
    user_states[user_id] = {"index": 0, "waiting_next_button": False}
    await call.answer("Штаб ТТ БУБУ: начинаем операцию.")
    await send_step_prompt(user_id)


@dp.message_handler(commands=["help"])
async def handle_help(message: types.Message):
    await message.answer(
        "Это квест-бот ТТ БУБУ.\n\n"
        "• Большие задания — отгадать локацию.\n"
        "• После правильного ответа жми «Новое задание» — получишь мини-задание.\n"
        "• После апрува медиа — маленькое задание с PIN-кодом.\n"
        "• После PIN-кода — новая загадка.\n\n"
        "Если что-то пойдёт не так — пиши Митяю."
    )


# ==================== КНОПКА «НОВОЕ / СЛЕДУЮЩЕЕ ЗАДАНИЕ» ====================

@dp.callback_query_handler(lambda c: c.data == "next_step")
async def handle_next_step(call: types.CallbackQuery):
    user_id = call.from_user.id
    state = get_state(user_id)

    if not state.get("waiting_next_button"):
        await call.answer("Штаб сейчас эту кнопку не ждал.", show_alert=False)
        return

    state["waiting_next_button"] = False
    state["index"] += 1

    await call.answer("Принято. Штаб даёт новое задание.")
    await send_step_prompt(user_id)


# ==================== ТЕКСТ: ЛОКАЦИИ + PIN-КОДЫ ====================

@dp.message_handler(content_types=ContentType.TEXT)
async def handle_text(message: types.Message):
    user_id = message.from_user.id
    text = (message.text or "").strip()

    if text.startswith("/"):
        return

    state = get_state(user_id)
    idx = state["index"]

    if idx >= len(STEPS):
        await message.answer("Ты уже на финале. Жди вручения контейнера.")
        return

    step = STEPS[idx]
    kind = step.get("kind")

    # ==== БОЛЬШАЯ ЗАГАДКА (ЛОКАЦИЯ) ====
    if kind == "text_answer":
        normalized = text.lower()
        answers = [a.lower() for a in step.get("answers", [])]

        if normalized in answers:
      
    # ==== Картинка ====      
            image_name = step.get("image")
            if image_name:
                try:
                    await message.answer_photo(InputFile(image_name))
                except Exception as e:
                    logging.warning(f"Не удалось отправить картинку {image_name}: {e}")
                    await message.answer(
                        "(Штаб пытался отправить картинку, но контейнер где-то застрял.)"
                    )
    # ==== Текст ====
            success_text = step.get("success_text", "Верно. Штаб подтверждает.")
            await message.answer(success_text)

            if step.get("needs_button"):
                kb = InlineKeyboardMarkup()
                kb.add(
                    InlineKeyboardButton(
                        step.get("next_button_text", "Новое задание"),
                        callback_data="next_step",
                    )
                )
                state["waiting_next_button"] = True
                await message.answer(
                    "Как будешь на месте — жми «Новое задание».",
                    reply_markup=kb,
                )
            else:
                state["index"] += 1
                await send_step_prompt(user_id)
        else:
            retry = step.get("retry_text", "Штаб не узнаёт это место. Попробуй ещё раз.")
            await message.answer(retry)

    # ==== МИНИ-ЗАДАНИЕ (PIN-КОД) ====
    elif kind == "pin_code":
        pins = [str(p).strip() for p in step.get("pins", [])]
        input_pin = text.strip()

        if input_pin in pins:
            success_text = step.get("success_text", "Код принят. Штаб доволен.")
            await message.answer(success_text)

            state["index"] += 1
            await send_step_prompt(user_id)
        else:
            retry = step.get("retry_text", "Код не подходит. Попробуй ещё раз.")
            await message.answer(retry)

    else:
        await message.answer(
            "Сейчас штаб ждёт от тебя не текст, а другое действие. Проверь последнее задание."
        )


# ==================== МЕДИА (ВИДЕО / ФОТО / ВОЙС) ====================

@dp.message_handler(
    content_types=[ContentType.PHOTO, ContentType.VIDEO, ContentType.DOCUMENT, ContentType.VOICE]
)
async def handle_media(message: types.Message):
    user_id = message.from_user.id
    state = get_state(user_id)
    idx = state["index"]

    if idx >= len(STEPS):
        await message.answer("Квест уже завершён.")
        return

    step = STEPS[idx]
    kind = step.get("kind")

    if kind != "media":
        await message.answer(
            "Сейчас штаб ждёт текстовый ответ, а не медиа. Проверь последнее задание."
        )
        return

    await message.answer(
        "Штаб получил твоё медиа и передал Митяю на проверку.\n"
        "Жди, пока наверху всё согласуют."
    )

    caption = (
        f"Медиа от пользователя {user_id} на шаге {idx} ({step.get('name')}).\n"
        f"Если всё ок — жми ✅. Если нет — ❌."
    )

    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton("✅ Одобрить", callback_data=f"approve:{user_id}:{idx}"),
        InlineKeyboardButton("❌ Переснять", callback_data=f"reject:{user_id}:{idx}"),
    )

    try:
        await message.forward(ADMIN_ID)
        await bot.send_message(ADMIN_ID, caption, reply_markup=kb)
    except Exception as e:
        logging.error(f"Ошибка при пересылке медиа админу: {e}")


# ==================== АДМИН: ОДОБРЕНИЕ / ПЕРЕСНЯТЬ ====================

@dp.callback_query_handler(lambda c: c.data.startswith(("approve:", "reject:")))
async def handle_approve_reject(call: types.CallbackQuery):
    # Проверяем, что жмёт именно админ
    if call.from_user.id != ADMIN_ID:
        await call.answer("Ты не ведущий ТТ БУБУ.")
        return

try:
    action, user_id_str, step_idx_str = call.data.split(":")
    target_user_id = int(user_id_str)
    step_idx = int(step_idx_str)
except Exception:
    await call.answer("Некорректные данные callback.", show_alert=True)
    return

state = get_state(target_user_id)

# Проверим, что игрок всё ещё на этом шаге
if state["index"] != step_idx:
    await call.answer(
        f"Игрок уже на другом шаге (текущий шаг: {state['index']}).",
        show_alert=False,
    )
    return

# Уберём кнопки у сообщения с approve/reject
try:
    await bot.edit_message_reply_markup(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=None,
    )
except Exception:
    pass

# ====== ОТКЛОНЕНО ======
if action == "reject":
    await call.answer("Попросили переснять.")
    await bot.send_message(
        target_user_id,
        "Штаб ТТ БУБУ: Митяй попросил переснять медиа.\n"
        "Попробуй ещё раз — поближе, чётче и с харизмой Валюхи."
    )
    return

# ====== ОДОБРЕНО ======
if action == "approve":
    await call.answer("Одобрено.")
    await bot.send_message(
        target_user_id,
        "Штаб ТТ БУБУ: медиа одобрено."
    )

    idx = state["index"]

    # ЕСЛИ ЭТО ПОСЛЕДНИЙ ШАГ (ФИНАЛЬНОЕ ФОТО У ЁЛКИ)
    if idx == len(STEPS) - 1:
        keyboard = InlineKeyboardMarkup()
        keyboard.add(
            InlineKeyboardButton(
                "Получить приз",
                callback_data="get_prize"
            )
        )

        await bot.send_message(
            target_user_id,
            "Все этапы пройдены! Нажми «Получить приз», чтобы штаб отправил агента для выдачи.",
            reply_markup=keyboard,
        )

        # Можно повысить индекс, чтобы дальше бот считал, что квест завершён
        state["index"] += 1

    else:
        # Обычное поведение для НЕ последнего шага:
        # после одобрения видео двигаемся к следующему шагу (обычно PIN-код)
        state["index"] += 1
        await send_step_prompt(target_user_id)
# ==================== ЗАПУСК ====================

if __name__ == "__main__":
    print("Bot started...")
    executor.start_polling(dp, skip_updates=True)
# ==================== Приз ====================
@dp.callback_query_handler(lambda c: c.data == "get_prize")
async def handle_prize(call: types.CallbackQuery):
    user_id = call.from_user.id
    try:
        await bot.send_photo(
            user_id,
            InputFile("08.jpg"),
            caption="Контейнер найден и официально вручается тебе. Поздравляем, агент Валюха!"
        )
    except Exception as e:
        logging.error(e)
        await bot.send_message(user_id, "Ошибка при отправке приза. Сообщи ведущему.")
