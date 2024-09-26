#script4_telegram_bot.py
import os
import asyncio
import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

# Замените на ваш токен
TELEGRAM_TOKEN = "6816816076:AAFDzKtjHCeWU6OFnHzM6iQJRExhP61g8AU"

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Обработка команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info("Получена команда /start")
    keyboard = [
        [KeyboardButton("Поиск поддоменов"), KeyboardButton("Разрешение IP")],
        [KeyboardButton("Сканирование Nmap"), KeyboardButton("Результаты Nmap")],
        [KeyboardButton("Выход")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "Добро пожаловать в бот для сканирования!\n"
        "Выберите команду из меню ниже:",
        reply_markup=reply_markup
    )

# Обработка сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    if user_message == "Поиск поддоменов":
        await start_subdomains(update.message, context)
    elif user_message == "Разрешение IP":
        await resolve_ips(update.message, context)
    elif user_message == "Сканирование Nmap":
        await start_nmap_scan(update.message, context)
    elif user_message == "Результаты Nmap":
        await get_results(update.message, context)
    elif user_message == "Выход":
        await update.message.reply_text("Выход из бота.")
    else:
        await update.message.reply_text("Пожалуйста, выберите команду из меню.")

# Команда для запуска поддоменного скрипта
async def start_subdomains(message, context: ContextTypes.DEFAULT_TYPE):
    logging.info("Запуск поиска поддоменов...")
    await message.reply_text("Запуск поиска поддоменов...")
    process = await asyncio.create_subprocess_exec(
        'python3', 'scripts/script1_subdomain_finder.py'
    )
    await process.wait()
    
    # Подсчет поддоменов
    with open('data/subdomains.txt', 'r') as f:
        subdomain_count = len(f.readlines())
    
    await message.reply_text(f"Поиск поддоменов завершен. Найдено поддоменов: {subdomain_count}.")

# Команда для разрешения IP
async def resolve_ips(message, context: ContextTypes.DEFAULT_TYPE):
    logging.info("Разрешение IP-адресов...")
    await message.reply_text("Разрешение IP-адресов...")
    process = await asyncio.create_subprocess_exec(
        'python3', 'scripts/script2_resolve_ip.py'
    )
    await process.wait()
    
    # Подсчет IP-адресов
    with open('data/ip_addresses.txt', 'r') as f:
        ip_count = len(f.readlines())
    
    await message.reply_text(f"Разрешение IP-адресов завершено. Найдено IP-адресов: {ip_count}.")

# Команда для запуска Nmap
async def start_nmap_scan(message, context: ContextTypes.DEFAULT_TYPE):
    logging.info("Запуск сканирования Nmap...")
    await message.reply_text("Запуск сканирования Nmap...")
    process = await asyncio.create_subprocess_exec(
        'python3', 'scripts/script3_nmap_scan.py'
    )
    await process.wait()
    
    # Подсчет результатов Nmap
    with open('data/nmap_results.txt', 'r') as f:
        result_count = len(f.readlines())
    
    await message.reply_text(f"Сканирование Nmap завершено. Найдено результатов: {result_count}.")

# Чтение результатов
async def get_results(message, context: ContextTypes.DEFAULT_TYPE):
    logging.info("Получена команда для получения результатов Nmap")
    try:
        with open('data/nmap_results.txt', 'r') as f:
            results = f.read()
        await message.reply_text(f"Результаты Nmap:\n{results}")
    except FileNotFoundError:
        await message.reply_text("Результаты Nmap не найдены.")

def main():
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()

if __name__ == "__main__":
    main()
