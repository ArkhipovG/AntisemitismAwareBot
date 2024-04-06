from ntscraper import Nitter
scraper = Nitter(log_level=1, skip_instance_check=False)
import pandas as pd
import openai
import keys
import matplotlib.pyplot as plt

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


def profile_info(username):
    instance = 'https://nitter.privacydev.net'
    profile = scraper.get_profile_info(username, instance=instance)
    return profile

def create_tweets_dataset(username,num_of_tweets):
    instance='https://nitter.privacydev.net'
    tweets = scraper.get_tweets(username,mode='user',number=num_of_tweets, instance=instance)
    data = {
    'date':[],
    'link':[],
    'text':[],
    'user':[],
    'likes':[],
    'quotes':[],
    'retweets':[],
    'comments':[]}

    for tweet in tweets['tweets']:
        data['date'].append(tweet['date'])
        data['link'].append(tweet['link'])
        data['text'].append(tweet['text'])
        data['user'].append(tweet['user']['name'])
        data['likes'].append(tweet['stats']['likes'])
        data['quotes'].append(tweet['stats']['quotes'])
        data['retweets'].append(tweet['stats']['retweets'])
        data['comments'].append(tweet['stats']['comments'])

    df = pd.DataFrame(data)
    return df

def analyse_tweets(df):
    antisemitic_posts = 0
    non_antisemitic_posts = 0
    if not df['date'].empty:
        for index, text in enumerate(df['text']):
            answer = generate_answer("You are Israeli activist. You must analyze this text for antisemitism and antizionism content. Does it contain such content? Answer only 'yes' or 'no'.  If the text contains 'Free Palestine' or 'FreePalestine' answer yes. You have only one life for answer. Text:" + text)
            print(f"{text}, Answer: {answer}")
            if answer.lower() == 'yes':
                antisemitic_posts += 1
                df.at[index, 'antisemitic_post'] = True
                df.at[index, 'non_antisemitic_post'] = False
            elif answer.lower() == 'no':
                non_antisemitic_posts += 1
                df.at[index, 'antisemitic_post'] = False
                df.at[index, 'non_antisemitic_post'] = True
    return df
def create_piechart(df):
    if not df['date'].empty:
        labels = 'Non-Antisemitic Posts', 'Antisemitic Posts'
        sizes = [df['non_antisemitic_post'].sum(), df['antisemitic_post'].sum()]
        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures a circular pie chart
        plt.savefig("piechart.png")

def main():
    df = create_tweets_dataset('RadioGenoa', num_of_tweets=15)
    anylsed_df = analyse_tweets(df)
    create_piechart(anylsed_df)
    return 'piechart.png'

