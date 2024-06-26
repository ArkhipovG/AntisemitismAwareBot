from Twitter_analysis import twitter_function
import telebot
import openai
import random
import keys
import os
from DB.harmful_resources_DB.harmful_resources_manager import ResourcesManager
from DB.harmful_resources_DB.harmful_resources_class import HarmfulResources
from DB.News_request.get_news import get_random_article
from Quiz import questions
from DB.usefull_resources_DB.usefull_resources_manager import UsefulResourcesManager
from DB.incidents_db.incidents_class import Incidents
from DB.incidents_db.incidents_manager import IncidentsManager
from dynamic_plots import dynamic_plots
import Community.community_resources
import chart_studio.plotly as py
import chart_studio
chart_studio.tools.set_credentials_file(username='AntisemitismCombatBot', api_key=keys.plotly_token)

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
    random_questions = random.sample(list(questions.quiz_data.items()), 5)
    random_quiz_data = {question: options for question, options in random_questions}

    quiz_state = {"questions": list(random_quiz_data.keys()), "correct_answers": 0}
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
            chat_gpt_response = generate_answer(
                f"Question: {question}.Options: {questions.quiz_data[question]} .Correct answer: {questions.quiz_answers[question]}. Explain the answer")
            response_message = f"Sorry, the correct answer is {questions.quiz_answers[question]} \n \n{chat_gpt_response}."
            bot.send_message(message.chat.id, response_message)
        ask_question(message, quiz_state)
    except (ValueError, IndexError):
        response_message = "Please reply with the number of the correct answer."
        bot.reply_to(message, response_message)


def end_quiz(message, quiz_state):
    result_message = f"Quiz ended! You answered {quiz_state['correct_answers']} out of 5 questions correctly."
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
        'To receive last updates on antisemitic incidents and news articles related to antisemitism press /latest\n' +
        'To receive combined statistics on Twitter dataset press /twitter_plots\n' +
        'To analyze Twitter user for antisemitic content press /twitter_analysis\n' +
        'To create a plot according to your prompt press /dynamic_plots\n'
    )


# Create dict to save history of conversation
user_history = []


@bot.message_handler(commands=['psychologist'])
def talk_command(message):
    chat_text = message.text.replace('/psychologist', "Hello! I'm reaching out to engage in a dialogue "
                                                      "with you as a psychologist. Please communicate "
                                                      "with me in that capacity.").strip()
    bot.reply_to(message, "Hello, I am here to offer my support and guidance. Please feel free to share any thoughts "
                          "or concerns you may have, and I will do my best to assist you. To exit conversation press "
                          "/exit_talk")
    # Save beginning of dialogue
    #user_history.append(f'user: {chat_text}')
    bot.register_next_step_handler(message, continue_conversation)


def continue_conversation(message):
    if message.text.lower() == '/exit_talk':
        bot.reply_to(message, "Exiting conversation. You can start again with /psychologist")
        # Delete history and exit
        del user_history[message.chat.id]
        return
    # Receive history
    user_history.append(f'user: {message.text}')
    print(user_history)
    # Generate response based on history
    response = generate_answer('Analyze the whole conversation in the list below. Answer only on the last user message.'
                               ' Last message is the last element of the list. Answer like you are a human psychologist and you are talking with patient\n'.join(user_history))
    user_history.append(f'bot: {response}')
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
        +
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
        if analysed_dataset['antisemitic_post'].sum() > len(analysed_dataset) * 0.1:
            profile = twitter_function.profile_info(username)
            if profile:
                bot.send_message(
                    message.chat.id,
                    f"Name: {profile['name']} "
                    f"\nLocation: {profile['location']} "
                    f"\nRegistered: {profile['joined']}")
            bot.send_message(
                message.chat.id,
                f"This user is antisemitic. "
                f"\nWe added him/her to our antisemitic database."
                f"\nYou can check it out here: /antisemitic_db"
            )
        elif analysed_dataset['antisemitic_post'].sum() <= len(analysed_dataset) * 0.1:
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


@bot.message_handler(commands=['twitter_plots'])
def user_plot_choice(message):
    bot.send_message(
        message.chat.id,
        f"Choose a plot:\n" +
        f"/Analysis_by_location\n" +
        f"/Analysis_by_month\n" +
        f"/Analysis_by_top_10_antisemists\n" +
        f"/Analysis_by_year\n" +
        f"/Analysis_by_top_20_tweets\n" +
        f"/Analysis_by_likes_and_retweets\n" +
        f"/Set_of_plots"
    )
    bot.register_next_step_handler(message, twitter_plots)


def twitter_plots(message):
    if message.text == "/Analysis_by_location":
        with open('images/analysis_by_location.png', 'rb') as photo:
            bot.send_photo(message.chat.id, photo)
        bot.send_message(
            message.chat.id,
            f"The bar chart illustrates the percentage of antisemitic tweets originating from various countries. Germany "
            f"exhibits the highest proportion, exceeding 100%, while India and Israel show notably lower percentages, "
            f"around 35-40%. Countries like Jordan, Palestine, and the United Kingdom display percentages ranging from "
            f"70-85%. The remaining countries fall within the 45-60% range."
        )
    elif message.text == "/Analysis_by_month":
        with open('images/barchart_by_month.png', 'rb') as photo:
            bot.send_photo(message.chat.id, photo)
        bot.send_message(
            message.chat.id,
            f"The bar chart presents the number of antisemitic posts over several months, from October 2023 to March "
            f"2024. There's a clear upward trend from October, peaking in January 2024, followed by a decline in February "
            f"and March. However, even with this decrease, the number of posts in these months remains higher than the "
            f"initial months of October and November 2023."
        )
    elif message.text == "/Analysis_by_top_10_antisemists":
        with open('images/hist_by_10users.png', 'rb') as photo:
            bot.send_photo(message.chat.id, photo)
        bot.send_message(
            message.chat.id,
            f'The bar chart ranks the top 10 users with the most antisemitic tweets. There is a significant difference '
            f'between the user with the highest number of such tweets, "TorahJudaism," and the rest. The remaining users '
            f'exhibit a more gradual decrease in the number of antisemitic tweets, with "DoveAtherton20" having the least '
            f'among the top 10.'
        )
    elif message.text == "/Analysis_by_year":
        with open('images/hist_numb_acc_by_year.png', 'rb') as photo:
            bot.send_photo(message.chat.id, photo)
        bot.send_message(
            message.chat.id,
            f"The bar chart displays the number of accounts created each year between 2013 and 2023 that have posted "
            f"antisemitic content. There's a general trend of increase, with a slight dip in the middle. The number of "
            f"such accounts is notably higher from 2020 onwards compared to the earlier years."
        )
    elif message.text == "/Analysis_by_top_20_tweets":
        with open('images/lineplot_top20tweets.png', 'rb') as photo:
            bot.send_photo(message.chat.id, photo)
        bot.send_message(
            message.chat.id,
            f"The line chart tracks the number of likes for the top 20 tweets over time, spanning from October 2023 to "
            f"March 2024. There's a significant spike in likes around mid-November 2023, followed by a general downward "
            f"trend with some smaller fluctuations. By March 2024, the number of likes for the top tweets is considerably "
            f"lower than the peak in November."
        )
    elif message.text == "/Analysis_by_likes_and_retweets":
        with open('images/piechart_avarage_likes_retweets.png', 'rb') as photo:
            bot.send_photo(message.chat.id, photo)
        bot.send_message(
            message.chat.id,
            f"""The pie charts compare the average number of retweets and likes for antisemitic and non-antisemitic posts.
    
    Retweets: Antisemitic posts receive a significantly higher average number of retweets (57.4%) compared to non-antisemitic posts (42.6%).
    Likes: The difference is smaller but still present, with antisemitic posts garnering a larger share of average likes (53.2%) than non-antisemitic posts (46.8%)."""
        )
    elif message.text == "/Set_of_plots":
        with open('images/all_plots_combined.png', 'rb') as photo:
            bot.send_photo(message.chat.id, photo)
        bot.send_message(
            message.chat.id,
            f"""The set of charts provides an analysis of antisemitic content on the twitter.
    
    Top Left - Users: The bar chart shows the top 10 users generating the most antisemitic tweets, with a clear outlier ("TorahJudaism") posting significantly more than the others.
    
    Top Right - Monthly Posts: The bar chart illustrates the number of antisemitic posts per month. There's a peak in January, a drop in the following months, and then another rise towards the end of the year.
    
    Bottom Left - Likes: The pie chart compares the average number of likes on antisemitic and non-antisemitic posts.
    While the difference is not as large as with retweets, antisemitic posts still receive more average likes.
    
    Bottom Right - Retweets: This pie chart highlights a more substantial discrepancy, with antisemitic posts receiving a considerably higher average number of retweets compared to non-antisemitic posts."""
        )


@bot.message_handler(commands=['dynamic_plots'])
def user_plot_input(message):
    bot.send_message(
        +
        message.chat.id,
        "You have 'antisemitic_attacks.csv' file which contains antisemitic accidents between 2021 and 2024 with columns 'title', 'date', 'link', 'year', 'month' and 'country'\n"
        "You can ask bot to create a plot from it\n"
        "Write your prompt here:"
    )
    bot.register_next_step_handler(message, plot_creation)


def plot_creation(message):
    user_prompt = message.text
    fig = dynamic_plots.dynamic_plots(user_prompt)
    bot.send_message(
        +
        message.chat.id,
        f"{fig}"
    )


bot.polling()
