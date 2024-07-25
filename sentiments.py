import os
import tweepy
import csv
import re
from textblob import TextBlob
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from flask import Blueprint, render_template, request

# Create a Blueprint for the sentiment analysis functionality
second = Blueprint("second", __name__, static_folder="static", template_folder="templates")

# Route for sentiment analysis page
@second.route("/sentiment_analyzer")
def sentiment_analyzer():
    return render_template("sentiment_analyzer.html")

class SentimentAnalysis:

    def __init__(self):
        self.tweets = []
        self.tweetText = []

    def DownloadData(self, keyword, tweets):
        # authenticating
        consumerKey = 'Nko0W4Gnvo78KqbOgPPxHpzIm'
        consumerSecret = 'HaseaS0fF0rGMSY3Q0ZjxxMfwkRPWBIi7lHa0u8WMEm1PaLipk'
        accessToken = '1814220243172294656-vxWoXgnxOKPMkM1zfLaNniDuPGKw6E'
        accessTokenSecret = 'iEYDn0wEvlFYQrOyd3JBKU1o4xA8nGkR5T6a299FqPVSm'
        auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
        auth.set_access_token(accessToken, accessTokenSecret)
        api = tweepy.API(auth, wait_on_rate_limit=True)

        tweets = int(tweets)

        # searching for tweets
        self.tweets = tweepy.Cursor(api.search_tweets, q=keyword, lang="en").items(tweets)

        # Open/create a file to append data to
        image_dir = os.path.join(os.path.dirname(__file__), 'static/images')
        if not os.path.exists(image_dir):
            os.makedirs(image_dir)
        strFile = os.path.join(image_dir, 'plot1.png')

        # Use csv writer
        csvFile = open('result.csv', 'a')
        csvWriter = csv.writer(csvFile)

        # creating some variables to store info
        polarity = 0
        positive = 0
        wpositive = 0
        spositive = 0
        negative = 0
        wnegative = 0
        snegative = 0
        neutral = 0

        # iterating through tweets fetched
        for tweet in self.tweets:
            self.tweetText.append(self.cleanTweet(tweet.text).encode('utf-8'))
            analysis = TextBlob(tweet.text)
            polarity += analysis.sentiment.polarity

            if (analysis.sentiment.polarity == 0):
                neutral += 1
            elif (analysis.sentiment.polarity > 0 and analysis.sentiment.polarity <= 0.3):
                wpositive += 1
            elif (analysis.sentiment.polarity > 0.3 and analysis.sentiment.polarity <= 0.6):
                positive += 1
            elif (analysis.sentiment.polarity > 0.6 and analysis.sentiment.polarity <= 1):
                spositive += 1
            elif (analysis.sentiment.polarity > -0.3 and analysis.sentiment.polarity <= 0):
                wnegative += 1
            elif (analysis.sentiment.polarity > -0.6 and analysis.sentiment.polarity <= -0.3):
                negative += 1
            elif (analysis.sentiment.polarity > -1 and analysis.sentiment.polarity <= -0.6):
                snegative += 1

        # Write to csv and close csv file
        csvWriter.writerow(self.tweetText)
        csvFile.close()

        # finding average of how people are reacting
        positive = self.percentage(positive, tweets)
        wpositive = self.percentage(wpositive, tweets)
        spositive = self.percentage(spositive, tweets)
        negative = self.percentage(negative, tweets)
        wnegative = self.percentage(wnegative, tweets)
        snegative = self.percentage(snegative, tweets)
        neutral = self.percentage(neutral, tweets)

        # finding average reaction
        polarity = polarity / tweets

        if (polarity == 0):
            htmlpolarity = "Neutral"
        elif (polarity > 0 and polarity <= 0.3):
            htmlpolarity = "Weakly Positive"
        elif (polarity > 0.3 and polarity <= 0.6):
            htmlpolarity = "Positive"
        elif (polarity > 0.6 and polarity <= 1):
            htmlpolarity = "Strongly Positive"
        elif (polarity > -0.3 and polarity <= 0):
            htmlpolarity = "Weakly Negative"
        elif (polarity > -0.6 and polarity <= -0.3):
            htmlpolarity = "Negative"
        elif (polarity > -1 and polarity <= -0.6):
            htmlpolarity = "Strongly Negative"

        # Generate the pie chart
        try:
            self.plotPieChart(positive, wpositive, spositive, negative, wnegative, snegative, neutral, keyword, tweets)
        except Exception as e:
            print(f"Error creating plot: {e}")

        return polarity, htmlpolarity, positive, wpositive, spositive, negative, wnegative, snegative, neutral, keyword, tweets

    def cleanTweet(self, tweet):
        # Remove Links, Special Characters etc from tweet
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", tweet).split())

    # function to calculate percentage
    def percentage(self, part, whole):
        temp = 100 * float(part) / float(whole)
        return format(temp, '.2f')

    def plotPieChart(self, positive, wpositive, spositive, negative, wnegative, snegative, neutral, keyword, tweets):
        fig = plt.figure()
        labels = ['Positive [' + str(positive) + '%]', 'Weakly Positive [' + str(wpositive) + '%]',
                  'Strongly Positive [' + str(spositive) + '%]', 'Neutral [' + str(neutral) + '%]',
                  'Negative [' + str(negative) + '%]', 'Weakly Negative [' + str(wnegative) + '%]',
                  'Strongly Negative [' + str(snegative) + '%]']
        sizes = [positive, wpositive, spositive, neutral, negative, wnegative, snegative]
        colors = ['yellowgreen', 'lightgreen', 'darkgreen', 'gold', 'red', 'lightsalmon', 'darkred']
        patches, texts = plt.pie(sizes, colors=colors, startangle=90)
        plt.legend(patches, labels, loc="best")
        plt.axis('equal')
        plt.tight_layout()

        image_dir = os.path.join(os.path.dirname(__file__), 'static/images')
        if not os.path.exists(image_dir):
            os.makedirs(image_dir)
        strFile = os.path.join(image_dir, 'plot1.png')

        if os.path.isfile(strFile):
            os.remove(strFile)

        plt.savefig(strFile)
        plt.close()  # Close the figure to free memory

@second.route('/sentiment_logic', methods=['POST', 'GET'])
def sentiment_logic():
    keyword = request.form.get('keyword')
    tweets = request.form.get('tweets')

    sentiment_analyzer = SentimentAnalysis()
    results = sentiment_analyzer.DownloadData(keyword, tweets)

    return render_template('sentiment_analyzer.html', **{
        'polarity': results[0],
        'htmlpolarity': results[1],
        'positive': results[2],
        'wpositive': results[3],
        'spositive': results[4],
        'negative': results[5],
        'wnegative': results[6],
        'snegative': results[7],
        'neutral': results[8],
        'keyword': results[9],
        'tweets': results[10]
    })
