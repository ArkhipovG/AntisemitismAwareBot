import matplotlib.pyplot as plt
import keys
import openai

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
    while not created:
        try:
            prompt = user_prompt

            gpt_code = generate_answer(f"You are part of the chatbot function.\n"
                                       f"The user will send the prompt to create a plot using Matplotlib.\n"
                                       f"Prompt: "
                                       f"{prompt}"
                                       "Your answer must be only finished Python code, which can be executed.\n"
                                       "Nobody will be correcting it.\n"
                                       "x and y must have same first dimension.\n"
                                       "Save figure with name 'user_prompt_plot.png'")

            print(gpt_code)

            exec(gpt_code)
            created = True
        except (ValueError, SyntaxError):
            print(f"Created: {created}")
            print("Something went wrong. I will try again")
