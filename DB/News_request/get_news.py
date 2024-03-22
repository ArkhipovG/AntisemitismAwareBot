import requests
import random
from datetime import datetime

# Define the URL
url = 'https://newsapi.org/v2/everything?q=antisemitism&apiKey=053c54c8e0d446f299b5c49e99e16dcf'

# Make the GET request
response = requests.get(url)

# Check if the request was successful (status code 200)
def get_random_article():
    if response.status_code == 200:
        data = response.json()
        articles = random.choices(data['articles'],k=10)
        item_str = ''
        for num,article in enumerate(articles):
            date_obj = datetime.strptime(article['publishedAt'], "%Y-%m-%dT%H:%M:%SZ")
            formatted_date = date_obj.strftime("%d %B %Y")
            if article['source']['name'] != '[Removed]':
                item_str += f"Article №{num+1}:\nsource: {article['source']['name']}\nauthor: {article['author']}\ntitle: {article['title']}\nurl: {article['url']}\ndate: {formatted_date}\n"
            item_str += ('--------------------------\n')
        return item_str
    else:
        print("Error:", response.status_code)

print(get_random_article())