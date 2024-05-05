import keys
import openai
import chart_studio.plotly as py
import chart_studio
chart_studio.tools.set_credentials_file(username='AntisemitismCombatBot', api_key=keys.plotly_token)
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


def dynamic_plots(user_prompt):
    created = False
    tries = 0
    link = None
    while tries < 1 or not created:
        tries += 1
        try:
            prompt = user_prompt
            gpt_code = (generate_answer(f"You are part of the chatbot function.\n"
                                       "You have 'antisemitic_attacks.csv' file with columns 'title', 'date', 'link', 'year', 'month' and 'country'"
                                       f"The user will send the prompt to create a plot using Plotly.\n"
                                       f"Prompt: "
                                       f"{prompt}"
                                       "Your answer must be only finished Python code, which can be executed. Dont write the name of programming language\n"
                                       "Nobody will be correcting it.\n"
                                       "Dont use example data, use only real-world data\n"
                                       "x and y must have same first dimension.\n"
                                       "Hide row 'fig.show()'"))
            gpt_code += """
            \nlink = py.plot(fig, filename='created_plot', auto_open=False)
            """
            print(gpt_code)
            local_vars = {}
            exec(gpt_code, globals(), local_vars)
            link = local_vars.get('link')
            created = True
        except (ValueError, AttributeError, SyntaxError, KeyError, NameError, UserWarning) as e:
            print(e)
            print(f"\nCreated: {created}\n")
            print("\nSomething went wrong. I will try again\n")
    if not created:
        print("Sorry, I can't create plot with your prompt. Try again.\n")
    return link




# link = dynamic_plots("Create pie chart on antisemitic attacks by country, if number of accidents more than 50")
# print(link)
