import telebot
import config
import random

from telebot.types import Message
from telebot import types

bot = telebot.TeleBot(config.TOKEN)
ID_ADMIN = 491796088
ID_ADMIN_2 = 1224772856
ID_ADMIN_3 = 268882863
GROUPS = set()

@bot.message_handler(commands=["id"])
def id(message):
    print(message.from_user.id)


@bot.message_handler(commands=["start"])
def welcome(message):
    if message.chat.type == "private" and (
        message.from_user.id == ID_ADMIN
        or message.from_user.id == ID_ADMIN_2
        or message.from_user.id == ID_ADMIN_3
    ):
        bot.send_message(
            message.chat.id,
            "Добро пожаловать, <b>{0.first_name}</b>!\n\nМеня зовут <b>{1.first_name}</b>, я запрограммированый бот на общение с тобой. Моя задача помогать тебе работать с рекламой, отправлять ее в нужные и указанные группы. Также проверять наличие пользователей, админов, узнавать ID групп и их названия. Я постараюсь, как можно больше собрать информации и предоставить ее тебе. Команды для работы со мной предоставлены ниже.\n\n<b>Команды:</b>\n<b>-</b> /start - Запустить бота\n<b>-</b> /ad - Добавить рекламу\n<b>-</b> /list - Получить информацию по группам\n<b>-</b> /help - Помощь в управлении бота\n\n<b>Реклама:</b>\n<b>{0.first_name}</b>, чтобы мне начать работать с рекламой, напиши /ad".format(
                message.from_user, bot.get_me()
            ),
            parse_mode="html",
        )
    else:
        return


@bot.message_handler(commands=["list"])
def list_groups(message: Message):
    if message.chat.type == "private" and (
        message.from_user.id == ID_ADMIN
        or message.from_user.id == ID_ADMIN_2
        or message.from_user.id == ID_ADMIN_3
    ):
        count = 0
        for i in GROUPS:
            admin_list = ""
            for admin in bot.get_chat_administrators(i):
                admin_list += admin.user.first_name + " "
            count += 1
            bot.send_message(
                message.chat.id,
                f'<b>[{count}]</b> Группа "<b>{bot.get_chat(i).title}</b>"\nID: <b>{i}</b>\nClients: <b>{bot.get_chat_members_count(i)}\n</b>Admin: <b>{admin_list}</b>',
                parse_mode="html",
            )
        bot.send_message(message.chat.id, f"Колличество групп: {count}")
    else:
        print("dasdad")


@bot.message_handler(commands=["ad"])
def ad(message):
    if message.chat.type == "private" and (
        message.from_user.id == ID_ADMIN
        or message.from_user.id == ID_ADMIN_2
        or message.from_user.id == ID_ADMIN_3
    ):
        bot.send_message(
            message.chat.id,
            "Отлично <b>{0.first_name}</b>! Начнем работать.\nНиже предоставлена простая инструкция по работе с рекламой. \n\n<b>Инструкция:</b>\n<b>-</b> Напиши рекламный пост.\n<b>-</b> Отправь его мне.\n<b>-</b> А я разошлю рекламу и предоставлю информацию по группам.".format(
                message.from_user
            ),
            parse_mode="html",
        )
        config.LEVEL_ACCESS = 1
    else:
        print("dsadada")


@bot.message_handler(commands=["help"])
def help(message):
    if message.chat.type == "private" and (
        message.from_user.id == ID_ADMIN
        or message.from_user.id == ID_ADMIN_2
        or message.from_user.id == ID_ADMIN_3
    ):
        bot.send_message(
            message.chat.id,
            "<b>Команды:</b>\n<b>-</b> /start - Запустить бота\n<b>-</b> /ad - Добавить рекламу\n<b>-</b> /list - Получить информацию по группам\n<b>-</b> /help - Помощь в управлении бота",
            parse_mode="html",
        )


@bot.message_handler(content_types=["text"])
def message_group(message):
    if message.chat.type == "private" and (
        message.from_user.id == ID_ADMIN
        or message.from_user.id == ID_ADMIN_2
        or message.from_user.id == ID_ADMIN_3
    ):
        if config.LEVEL_ACCESS == 1:
            bot.send_message(
                message.chat.id,
                "Начинаю рассылку рекламы по имеющимся группам в моей базе.",
            )
            count = 0
            for i in GROUPS:
                admin_list = ""
                for admin in bot.get_chat_administrators(i):
                    admin_list += admin.user.first_name + " "
                count += 1
                bot.send_message(i, message.text)
                bot.send_message(
                    message.chat.id,
                    f'<b>[{count}]</b> Группа "<b>{bot.get_chat(i).title}</b>" | Статус: <b><u>отправлено</u></b>\nID: <b>{i}</b>\nClients: <b>{bot.get_chat_members_count(i)}\n</b>Admin: <b>{admin_list}</b>',
                    parse_mode="html",
                )
            bot.send_message(
                message.chat.id,
                f"Колличество групп: {count}\n<b><u>Рассылка завершена!</u></b>",
                parse_mode="html",
            )
            config.LEVEL_ACCESS = 0
        else:
            bot.send_message(
                message.chat.id,
                "{0.first_name}, я не понимаю, что ты пишешь.\nЧтобы я тебе помог, напиши /help".format(
                    message.from_user
                ),
                parse_mode="html",
            )
    else:
        if message.chat.type == "private":
            return
        else:
            if message.chat.id in GROUPS:
                return
            else:
                GROUPS.add(message.chat.id)
                print("HELLO!")


@bot.message_handler(content_types=["left_chat_member"])
def remove_id(message: Message):
    if bot.get_me().id == message.left_chat_member.id:
        print("beepBot remove")
        GROUPS.discard(message.chat.id)


@bot.message_handler(content_types=["new_chat_members"])
def add_id(message: Message):
    if message.chat.type == "private":
        return
    else:
        if message.chat.id in GROUPS:
            return
        else:
            GROUPS.add(message.chat.id)
            print("HELLO!")


# @bot.message_handler(content_types=["text"])
# def lala(message):
#     le = message.text
#     if message.chat.type == "private":
#         if message.text == "Добавать рекламу":
#             bot.send_message(
#                 message.chat.id,
#                 "Хорошо {0.first_name}, добавляем рекламу. \nВведите рекламный-пост, отправьте мне и нажмите кнопку Разместить рекламу".format(
#                     message.from_user, bot.get_me()
#                 ),
#                 parse_mode="html",
#             )
#         else:
#             bot.send_message(GROUP_ID, le)


if __name__ == "__main__":
    bot.polling(none_stop=True)
