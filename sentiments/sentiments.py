import pandas as pd
import re
import nltk
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression


nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')

df = pd.read_csv('Stemmed_df_tweets.csv')

X = df['Text']
y = df['Biased']

vectorizer = TfidfVectorizer()
X_tfidf = vectorizer.fit_transform(X)
X_tfidf.shape

X_train, X_test, y_train, y_test = train_test_split(X_tfidf, y, test_size=0.3, random_state=42)

# Instantiate the LogisticRegression model.
model = LogisticRegression()

# Fit the model on the training data.
model.fit(X_train, y_train)

# Predict on the test data.
y_pred = model.predict(X_test)

def predict_sent(tweet):
  # Lowercase the text
  tweet = tweet.lower()

  # Remove HTML tags
  tweet = re.sub(r'<.*?>', '', tweet)

  # Remove urls
  tweet = re.sub(r'http\S+', '', tweet)

  # Remove hashtags and @ symbols
  tweet = re.sub(r'#', '', tweet)
  tweet = re.sub(r'@', '', tweet)

  # Tokenize the text
  tokens = word_tokenize(tweet)

  tweet = ' '.join(tokens)

  # Convert the review to TF-IDF vectors
  X_tfidf = vectorizer.transform([tweet])

  # Predict the sentiment of the review
  prediction = model.predict(X_tfidf)[0]

  # Print the predicted sentiment
  if prediction == 1:
    return f" {tweet}: The tweet is antisemitic"
  else:
    return f" {tweet}: The tweet is non-antisemitic"
