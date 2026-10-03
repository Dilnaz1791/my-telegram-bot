import random
import json
import os

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup

from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)


# Вставьте сюда токен своего Telegram-бота
TOKEN = "8747344234:AAG-4IP8y7WzxzW2DuzMOYq-TXY0OqQgadI"
# Данные пользователей
user_data = {}


# Загружаем данные из файла при запуске бота
def load_data():
    global user_data

    if os.path.exists("user.json"):
        with open("user.json", "r", encoding="utf-8") as f:
            user_data = json.load(f)


# Сохраняем данные пользователей в файл
def save_data():
    with open("user.json", "w", encoding="utf-8") as f:
        json.dump(user_data, f, ensure_ascii=False, indent=4)


# Состояния для создания профиля
NAME, COLOR = range(2)


# Начинаем создание профиля
async def profile_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)

    # Если профиль уже существует — показываем его
    if user_id in user_data:
        profile = user_data[user_id]

        await update.message.reply_text(
            f"Твой профиль:\n"
            f"Имя: {profile['name']}\n"
            f"Цвет: {profile['color']}"
        )

        return ConversationHandler.END

    await update.message.reply_text("Как тебя зовут?")

    return NAME
# Получаем имя пользователя
async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["profile_name"] = update.message.text

    await update.message.reply_text("Какой твой любимый цвет?")

    return COLOR


# Получаем цвет и сохраняем профиль
async def get_color(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)

    name = context.user_data["profile_name"]
    color = update.message.text

    # Сохраняем данные пользователя
    user_data[user_id] = {
        "name": name,
        "color": color
    }

    # Сохраняем данные в JSON-файл
    save_data()

    await update.message.reply_text(
        f"Готово! Профиль сохранён.\n\n"
        f"Имя: {name}\n"
        f"Цвет: {color}"
    )

    return ConversationHandler.END
# Отмена создания профиля
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Создание профиля отменено.")

    return ConversationHandler.END

# 5 фактов про ящериц
LIZARD_FACTS = [
    "Некоторые ящерицы могут отбрасывать хвост, чтобы спастись от хищника.",
    "У некоторых ящериц хвост способен частично восстановиться.",
    "Ящерицы относятся к классу пресмыкающихся.",
    "Большинство ящериц любят тепло и греются на солнце.",
    "Некоторые ящерицы умеют менять окраску тела.",
]


# 5 фактов про горы
MOUNTAIN_FACTS = [
    "Горы образуются, в частности, из-за движения литосферных плит.",
    "Самая высокая гора Земли над уровнем моря — Эверест.",
    "С высотой температура воздуха обычно понижается.",
    "В горах можно встретить ледники даже при относительно тёплом климате.",
    "Горы влияют на движение воздушных масс и количество осадков.",
]
# Шутки
JOKES = [
    "Почему программист не любит природу? Там слишком много багов.",
    "Почему компьютер пошёл к врачу? У него был вирус.",
    "Я хотел пошутить про Python, но это уже слишком питонично.",
    "Почему программист перепутал Хэллоуин и Рождество? Потому что OCT 31 = DEC 25.",
    "— Ты почему опоздал?\n— Я шёл по пробкам.\n— Пешком?\n— Ну да, в голове пробки."
]

## Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("О боте", callback_data="about"),
            InlineKeyboardButton("Шутка", callback_data="joke"),
            InlineKeyboardButton("Автор", callback_data="author")
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Привет!\n\n"
        "Я бот случайных фактов.\n"
        "Напиши мне любое сообщение и я расскажу случайный факт "
        "про ящериц или горы.\n\n"
        "Выбери действие:",
        reply_markup=reply_markup
    )
# Обработка нажатий на inline-кнопки
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    # Подтверждаем нажатие кнопки
    await query.answer()

    if query.data == "about":
        await query.message.reply_text(
            "Я бот случайных фактов и шуток. "
            "Могу рассказать интересный факт или случайную шутку."
        )

    elif query.data == "joke":
        await query.message.reply_text(
            random.choice(JOKES)
        )

    elif query.data == "author":
        await query.message.reply_text(
            "Автор: Dilnaz.Zh"
        )

# Команда /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📚 Доступные команды:\n\n"
        "/start — приветствие и описание бота\n"
        "/help — список команд\n\n"
        "Также можно отправить любое сообщение, "
        "и бот пришлёт случайный факт."
    )


# Ответ на любое обычное сообщение
async def random_fact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Объединяем два списка фактов
    all_facts = LIZARD_FACTS + MOUNTAIN_FACTS

    # Выбираем случайный факт
    fact = random.choice(all_facts)

    await update.message.reply_text(f"💡 Случайный факт:\n\n{fact}")

# Команда /joke
async def joke_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    joke = random.choice(JOKES)
    await update.message.reply_text(joke)


# Запуск бота
def main():

    # Создаём приложение
    application = Application.builder().token(TOKEN).build()

    # Загружаем сохранённые данные пользователей
    load_data()

    # Добавляем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("joke", joke_command))

    # Диалог создания профиля
    profile_conversation = ConversationHandler(
        entry_points=[CommandHandler("profile", profile_start)],
        states={
            NAME: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    get_name
                )
            ],
            COLOR: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    get_color
                )
            ],
        },
        fallbacks=[
            CommandHandler("cancel", cancel)
        ],
    )

    application.add_handler(profile_conversation)

    # Обрабатываем обычные текстовые сообщения
    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            random_fact
        )
    )

    # Запускаем бота
    application.run_polling()


if __name__ == "__main__":
    main()