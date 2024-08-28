import telebot
from decouple import config
from loguru import logger
from dotenv import load_dotenv
from django.core.exceptions import ValidationError
import django
import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_scrapper.settings')
django.setup()

from apps.telegram.models import TelegramUser
from apps.news.models import News

load_dotenv()

TELEGRAM_KEY = config('TELEGRAM_BOT_API_KEY', cast=str)
bot = telebot.TeleBot(TELEGRAM_KEY)


def send_news_to_users(news: list[News]):
    logger.info('Iniciando o envio das notícias.')

    if len(news) == 0:
        return
    
    telegram_users_ids: str = TelegramUser.objects.all().values_list('telegram_id', flat=True)
    
    message = 'Olá, esse é o resumo das últimas notícias\n'
    for user_id in telegram_users_ids:
        bot.send_message(user_id, message)
    for n in news:
        message = f'Assunto: {n.query.query_term.capitalize()}\n'
        message += f'Notícia: {n.name}\n'
        if n.description and n.description != n.name:
            if len(n.description) > 100:
                n.description = n.description[:100] + '...'
            message += f'Descrição: {n.description}\n'
        message += f'Data da notícia: {n.date_published}\n'
        message += f'Link: {n.url}\n'
        for user_id in telegram_users_ids:
            bot.send_message(user_id, message)

    message = 'Esse é o fim das notícias, tenha um ótimo dia.'
    for user_id in telegram_users_ids:
        bot.send_message(user_id, message)

    logger.success('As notícias foram enviadas.')


@bot.message_handler(commands=['registrar'])
def register_user(msg: telebot.types.Message):
    user = msg.from_user
    telegram_user = TelegramUser(
        first_name=user.first_name,
        telegram_id=user.id
    )
    try:
        telegram_user.full_clean()
        telegram_user.save()
        bot.reply_to(msg, 'Usuário registrado. Para excluir seu usuário, digite /excluir ou clique no link.')
        logger.success(f'O usuário {telegram_user} foi registrado.')
    except ValidationError as e:
        bot.reply_to(msg, f'Não foi possível registrar o seu usuário devido a: {e}.')
        logger.warning(f'Não foi possível registrar o usuário devido ao erro {e}.')


@bot.message_handler(commands=['excluir'])
def unregister_user(msg: telebot.types.Message):
    user = msg.from_user
    try:
        telegram_user = TelegramUser.objects.get(telegram_id=user.id)
        logger.info(f'O ususário {telegram_user} pediu para cancelar o cadastro.')
        telegram_user.delete()
        bot.reply_to(msg, 'Usuário excluído com sucesso.')
    except TelegramUser.DoesNotExist:
        bot.reply_to(msg, 'O usuário não está cadastrado no siste,a.')


@bot.message_handler(content_types=['text'])
def no_configired_message_handler(msg: telebot.types.Message):
    bot.reply_to(msg, 'Para registrar no bot, digite /registrar ou clique no link.')


if __name__ == '__main__':
    bot.polling()
    