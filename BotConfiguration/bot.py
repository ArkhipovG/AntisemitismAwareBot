import telebot
import openai
import keys

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
        '1) To receive a list of educational resources press....\n' +
        '2) To Talk with AI Psychologist press.....\n' +
        '3) To receive a list of educational resources press....\n' +
        'buying rates and selling rates.\n' +
        '4) To receive a list of educational resources press....\n' +
        '5) To receive a list of educational resources press....\n' +
        '6) To receive a list of educational resources press....\n' +
        '7) To receive a list of educational resources press....\n'
    )


# Create dict to save history of conversation
user_history = []


@bot.message_handler(commands=['psychologist'])
def talk_command(message):
    chat_text = message.text.replace('/psychologist', "Hello! I'm reaching out to engage in a dialogue "
                                                      "with you as a psychologist. Please communicate "
                                                      "with me in that capacity.").strip()
    #response = generate_answer(chat_text)
    bot.reply_to(message, "Hello, I am here to offer my support and guidance. Please feel free to share any thoughts "
                          "or concerns you may have, and I will do my best to assist you. To exit conversation press "
                          "/exit_talk")
    # Save beginning of dialogue
    user_history.append(f'user: {chat_text}')
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
    response = generate_answer('Analyze the whole conversation in the list below. Answer only on the last user message'
                               ' according to the whole conversation.\n'.join(user_history))
    user_history.append(f'bot: {response}')
    bot.reply_to(message, response)
    bot.register_next_step_handler(message, continue_conversation)


bot.polling()
