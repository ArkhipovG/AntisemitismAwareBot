import telebot
import openai
from DB.harmful_resources_DB.harmful_resources_manager import ResourcesManager
from DB.harmful_resources_DB.harmful_resources_class import HarmfulResources
from DB.News_request.get_news import get_random_article
bot = telebot.TeleBot('7163202910:AAFsjUt2-j0KNtcb-90pTeehCg33H7-HsQc')

openai.api_key = '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'


def generate_answer(text):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": text},
            ]
        )

        result = ''
        for choice in response.choices:
            result += choice.message.content

    except Exception as e:
        return f"Oops!! Some problems with openAI. Reason: {e}"

    return result


@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(
        message.chat.id,
        "Welcome to the Antisemitism Combat Bot! 🤖\n" +
        "I'm here to help you learn more about antisemitism and how to combat it.\n" +
        "You can ask me questions, get real-time updates, play quizzes, report incidents,and connect with others " +
        "interested in fighting antisemitism.\n" +
        "To get help press /help."
    )


@bot.message_handler(commands=['help'])
def help_command(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(
        telebot.types.InlineKeyboardButton(
            'Message the developer', url='telegram.me/blkmrkt8'
        )
    )
    bot.send_message(
        message.chat.id,
        '1) To receive a list of educational resources press /educational_list\n' +
        '2) To talk with AI psychologist press /talk_with_AI_Psychologist \n' +
        '3) To analyze text for antisemitic language or sentiment press /text_analyzer\n' +
        '4) To see interactive features press /interactive_futures\n' +
        '5) To anonymously report incidents of antisemitism encountered online or in communities. press /report\n' +
        '6) To receive a list of resources to join group discussions, share experiences, and connect with '
        'others interested in combating antisemitism press /community_list\n' +
        '7) To receive last updates on antisemitic incidents and news articles related to antisemitism press /latest'
    )


@bot.message_handler(commands=['talk_with_AI_Psychologist'])
def talk_command(message):
    chat_text = message.text.replace('/talk_with_AI_Psychologist', "Hello! I'm reaching out to engage in a dialogue "
                                                                   "with you as a psychologist. Please communicate "
                                                                   "with me in that capacity. Start with "
                                                                   "'Hello!'").strip()
    response = generate_answer(chat_text)
    bot.reply_to(message, response + " To exit conversation press /exit_talk")
    bot.register_next_step_handler(message, continue_conversation)


def continue_conversation(message):
    if message.text.lower() == '/exit_talk':
        bot.reply_to(message, "Exiting conversation. You can start again with /talk_with_AI_Psychologist.")
        return
    response = generate_answer(message.text)
    bot.reply_to(message, response)
    bot.register_next_step_handler(message, continue_conversation)


@bot.message_handler(commands=['harmful_list'])
def harmful_list_command(message):
    bot.send_message(
        message.chat.id,
        "What do you want to do?\n"
        "/insert \n"
        "/update\n"
        "/remove\n"
        "/view_all_resources\n"
    )
    bot.register_next_step_handler(message, user_input)


def user_input(message):
    if message.text == '/insert':
        bot.send_message(
            message.chat.id,
            "Input comma separated list: vk(name), vk.com(url), 7(score)"
        )
        bot.register_next_step_handler(message, insert)
    elif message.text == '/remove':
        bot.send_message(
            message.chat.id,
            "Input name of the resource you want to remove"
        )
        bot.register_next_step_handler(message, remove)
    elif message.text == '/update':
        bot.send_message(
            message.chat.id,
            "Input name of the resource you want to update"
        )
        bot.register_next_step_handler(message, item_to_update)
    elif message.text == '/view_all_resources':
        bot.send_message(
            message.chat.id,
            f"{ResourcesManager.all_items()}"
        )


def insert(message):
    list_of_item = message.text.split(",")
    item = HarmfulResources(list_of_item[0], list_of_item[1], list_of_item[2])
    item.save()
    bot.send_message(
        message.chat.id,
        "Item saved successfully!"
    )


def remove(message):
    list_of_item = ResourcesManager.get_by_name(message.text)
    item = HarmfulResources(list_of_item[1], list_of_item[2], list_of_item[3])
    item.delete()
    bot.send_message(
        message.chat.id,
        f"{list_of_item}"
    )
    bot.send_message(
        message.chat.id,
        f"{item}"
    )
    bot.send_message(
        message.chat.id,
        "Item removed successfully!"
    )


def item_to_update(message):
    list_of_item = ResourcesManager.get_by_name(message.text)
    item = HarmfulResources(list_of_item[1], list_of_item[2], list_of_item[3])
    bot.register_next_step_handler(message, new_update, item)
    bot.send_message(
        message.chat.id,
        "Input new name"
    )
    return item


def new_update(message, item):
    item.update(message.text)


@bot.message_handler(commands=['text_analyzer'])
def talk_command(message):
    bot.send_message(
        message.chat.id,
        "Input your text to analyze for antisemitic language or sentiment"
    )
    bot.register_next_step_handler(message, analyze_text)


def analyze_text(message):
    response = generate_answer("Analyse this text for antisemitic language or sentiment: " + message.text)
    bot.reply_to(message, response)


@bot.message_handler(commands=['latest'])
def latest_news(message):
    bot.send_message(
        message.chat.id,
        f"{get_random_article()}"
    )



bot.polling()
