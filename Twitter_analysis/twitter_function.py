from ntscraper import Nitter
import pandas as pd
import openai
import keys
import matplotlib.pyplot as plt

openai.api_key = keys.chat_gpt_token

scraper = Nitter(log_level=1, skip_instance_check=False)


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
def create_tweets_dataset(username,num_of_tweets):
    tweets = scraper.get_tweets(username,mode='user',number=num_of_tweets,instance='https://nitter.privacydev.net')
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
    for text in df['text']:
        answer = generate_answer("You are Israeli activist. You must analyze this text for antisemitic language or sentiment. Answer only 'yes' or 'no'.  If the text contains 'Free Palestine' or 'FreePalestine' say yes. You have only one life for answer. Text:" + text)
        print(f"{text}, Answer: {answer}")
        if answer.lower() == 'yes':
            antisemitic_posts += 1
            df['antisemitic_posts'] = True
        if answer.lower() == 'no':
            non_antisemitic_posts += 1
            df['non_antisemitic_posts'] = True
    return df

def create_piechart(df):
  labels = 'Non-Antisemitic Posts', 'Antisemitic Posts'
  sizes = [df['non_antisemitic_posts'].sum(), df['antisemitic_posts'].sum()]
  fig1, ax1 = plt.subplots()
  ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
  ax1.axis('equal')  # Equal aspect ratio ensures a circular pie chart
  plt.savefig("piechart.png")

