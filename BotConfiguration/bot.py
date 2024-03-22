import telebot
import openai

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
        '1) To receive a list of educational resources press....\n' +
        '2) To Talk with AI Psychologist press.....\n' +
        '3) To receive a list of educational resources press....\n' +
        'buying rates and selling rates.\n' +
        '4) To receive a list of educational resources press....\n' +
        '5) To receive a list of educational resources press....\n' +
        '6) To receive a list of educational resources press....\n' +
        '7) To receive a list of educational resources press....\n'
    )



bot.polling()
