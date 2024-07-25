import tweepy

class TwitterClient:
    def __init__(self):
        # Bearer token from Twitter Dev Console
        self.bearer_token = 'AAAAAAAAAAAAAAAAAAAAAOevuwEAAAAAWzXYH7KVsjHhJ1mMKdCpdTIKQO4%3DjhQcBshyIZgSAhbGEnM2fULkKxRuOOhMwceLFJ529kyx5IOgtV'

        # Create a Tweepy Client object
        self.client = tweepy.Client(bearer_token=self.bearer_token)

    def get_tweets(self, query, max_results=10):
        try:
            response = self.client.search_recent_tweets(query=query, max_results=max_results, tweet_fields=['public_metrics', 'text'])
            tweets = []

            if response.data:
                for tweet in response.data:
                    tweets.append({
                        'text': tweet.text,
                        'id': tweet.id
                    })

            return tweets
        except tweepy.TweepyException as e:
            print("Error : " + str(e))
            return None

def main():
    # Create a TwitterClient object
    client = TwitterClient()
    # Fetch tweets
    tweets = client.get_tweets(query='Donald Trump', max_results=10)

    if tweets:
        for tweet in tweets:
            print(tweet['text'])
    else:
        print("No tweets found.")

if __name__ == "__main__":
    main()
