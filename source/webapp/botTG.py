import os
import sys
import django
import telebot
from django.conf import settings

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'detail_shop.settings')
django.setup()

bot = telebot.TeleBot(settings.TELEGRAM_BOT_TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Привет, Константин! Я был разработан специально для вас, чтобы уведомлять вас о "
                              "новых заказах пользователя!")


def send_notifications(chat_id, message):
    try:
        bot.send_message(chat_id=chat_id, text=message)
    except Exception as e:
        telebot.logger.error(f'Ошибка при отправке сообщения: {e}')


def send_waiting_client(chat_id):
    bot.send_message(chat_id, 'Сообщу как будет следующий заказ 😜')


if __name__ == '__main__':
    bot.polling()
