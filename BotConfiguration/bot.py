from Twitter_analysis import twitter_function
import telebot
import openai
import random
import keys
from DB.harmful_resources_DB.harmful_resources_manager import ResourcesManager
from DB.harmful_resources_DB.harmful_resources_class import HarmfulResources
from DB.News_request.get_news import get_random_article
from Quiz import questions
from DB.usefull_resources_DB.usefull_resources_manager import UsefulResourcesManager
from DB.incidents_db.incidents_class import Incidents
from DB.incidents_db.incidents_manager import IncidentsManager
import Community.community_resources

bot = telebot.TeleBot(keys.telegram_token)

openai.api_key = keys.chat_gpt_token


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


def start_quiz(message):
    quiz_state = {"questions": list(questions.quiz_data.keys()), "correct_answers": 0}
    ask_question(message, quiz_state)


def ask_question(message, quiz_state):
    if quiz_state["questions"]:
        question = random.choice(quiz_state["questions"])
        quiz_state["questions"].remove(question)
        random.shuffle(questions.quiz_data[question])
        quiz_message = f"{question}\n\n"
        for idx, answer in enumerate(questions.quiz_data[question]):
            quiz_message += f"{idx + 1}. {answer}\n"
        quiz_message += "\nReply with the number of the correct answer."
        bot.reply_to(message, quiz_message)
        bot.register_next_step_handler(message, check_answer, quiz_state, question)
    else:
        end_quiz(message, quiz_state)


def check_answer(message, quiz_state, question):
    try:
        user_answer_index = int(message.text) - 1
        if questions.quiz_data[question][user_answer_index] == questions.quiz_answers[question]:
            response_message = "Correct! 🎉"
            quiz_state["correct_answers"] += 1
            bot.send_message(message.chat.id, response_message)
        else:
            response_message = f"Sorry, the correct answer is {questions.quiz_answers[question]}."
            bot.send_message(message.chat.id, response_message)
        ask_question(message, quiz_state)
    except (ValueError, IndexError):
        response_message = "Please reply with the number of the correct answer."
        bot.reply_to(message, response_message)


def end_quiz(message, quiz_state):
    result_message = f"Quiz ended! You answered {quiz_state['correct_answers']} out of {len(questions.quiz_data)} questions correctly."
    bot.reply_to(message, result_message)


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
        'To receive a list of educational resources press /educational_list\n' +
        'To receive or edit a list of harmful resources press /harmful_list\n' +
        'To talk with AI psychologist press /psychologist \n' +
        'To analyze text for antisemitic language or sentiment press /text_analyzer\n' +
        'Test your antisemitism knowledge - take the /quiz\n' +
        'To anonymously report incidents of antisemitism encountered online or in communities. press /report\n' +
        'To receive a list of resources to join group discussions, share experiences, and connect with '
        'others interested in combating antisemitism press /community_list\n' +
        'To receive last updates on antisemitic incidents and news articles related to antisemitism press /latest'
    )


@bot.message_handler(commands=['psychologist'])
def talk_command(message):
    chat_text = message.text.replace('/psychologist', "Hello! I'm reaching out to engage in a dialogue "
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


@bot.message_handler(commands=['quiz'])
def quiz_command(message):
    start_quiz(message)


@bot.message_handler(commands=['educational_list'])
def educational_list_command(message):
    bot.send_message(
        message.chat.id,
        f"{UsefulResourcesManager.all_items()}"
    )


@bot.message_handler(commands=['report'])
def report_command(message):
    bot.send_message(
        message.chat.id,
        f"Input title of the incident"
    )
    bot.register_next_step_handler(message, register_title)


def register_title(message):
    title = message.text
    bot.send_message(
        message.chat.id,
        f"Input info about the incident"
    )
    bot.register_next_step_handler(message, register_info, title)


def register_info(message, title):
    info = message.text
    bot.send_message(
        message.chat.id,
        f"Input date of the incident (format: YYYY-MM-DD)"
    )
    bot.register_next_step_handler(message, register_date, title, info)


def register_date(message, title, info):
    date = message.text
    bot.send_message(
        message.chat.id,
        f"Input was ir online or not('1' - online, '2' - offline)"
    )
    bot.register_next_step_handler(message, register_is_online, title, info, date)


def register_is_online(message, title, info, date):
    is_online = None
    if message.text == "1":
        is_online = True
    elif message.text == "2":
        is_online = False

    if is_online is not None:
        item = Incidents(title=title, info=info, date=date, is_online=is_online)
        item.save()
    bot.send_message(message.chat.id, f"Incident successfully registered")
    bot.send_message(message.chat.id, f"{IncidentsManager.all_items()}")


@bot.message_handler(commands=['community'])
def community_command(message):
    bot.send_message(
        message.chat.id,
        f"{Community.community_resources.print_resources()}"
    )


@bot.message_handler(commands=['twitter_analysis'])
def twitter_analysis(message):
    bot.send_message(
        message.chat.id,
        f"Who you want to check for antisemitism?"
    )
    bot.register_next_step_handler(message, scrap_tweets)


def scrap_tweets(message):
    bot.send_message(
        message.chat.id,
        f"Loading..."
    )
    username = message.text
    dataset = twitter_function.create_tweets_dataset(username, 15)
    analysed_dataset = twitter_function.analyse_tweets(dataset)
    twitter_function.create_piechart(analysed_dataset)
    if not analysed_dataset['date'].empty:
        with open('piechart.png', 'rb') as photo:
            bot.send_photo(message.chat.id, photo)
        if analysed_dataset['non_antisemitic_posts'].sum() < analysed_dataset['antisemitic_posts'].sum():
            bot.send_message(
                message.chat.id,
                f"This user is antisemitic. \nWe added him/her to our antisemitic database."
                f"\nYou can check it out here: /antisemitic_db"
            )
        elif analysed_dataset['non_antisemitic_posts'].sum() >= analysed_dataset['antisemitic_posts'].sum():
            bot.send_message(
                message.chat.id,
                f"This user is not antisemitic."
                f"\nYou can check another one here: \n/twitter_analysis"
            )
    else:
        bot.send_message(
            message.chat.id,
            f"Oops. Something went wrong. \nPlease try again. /twitter_analysis"
        )


bot.polling()
