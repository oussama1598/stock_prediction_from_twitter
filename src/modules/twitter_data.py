import tweepy
from nltk.sentiment import SentimentIntensityAnalyzer

from src.modules.csv_writer import CsvWriter
from src.modules.logger import Logger

logger = Logger('TwitterData')
sentiment_analyzer = SentimentIntensityAnalyzer()


def _get_status_row(status):
    if 'retweeted_status' in status._json:
        full_text = status.retweeted_status.full_text
    else:
        full_text = status.full_text

    score = sentiment_analyzer.polarity_scores(full_text)

    return [
               status.created_at,
               full_text,
               status.user.followers_count
           ] + list(score.values())


class TwitterData:
    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret, data_dir='./data'):
        self.data_dir = data_dir
        self.csv_header = ['Date', 'Content', 'Followers', 'Negative Score', 'Neutral Score', 'Positive Score',
                           'Compound Score']

        logger.info('authenticating twitterData')

        self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_token, access_token_secret)

        self.api = tweepy.API(self.auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

        logger.info('twitterData authenticated')

    def search(self, query, count, **kwargs):
        return tweepy.Cursor(self.api.search, q=query, count=200, lang='en', **kwargs).items(count)

    def download_data(self, query, count, from_date, to_date):
        logger.info(f'Downloading tweets with keyword {query} from date {from_date} to date {to_date}')

        tweets_by_day = {}

        for status in self.api.user_timeline(screen_name=query, count=count, tweet_mode='extended'):
            tweet_date = status.created_at.date()

            if tweet_date < from_date:
                continue

            if tweet_date not in tweets_by_day:
                tweets_by_day[tweet_date] = []

            tweets_by_day[tweet_date].append(status)

        for day in tweets_by_day:
            logger.info(f'Saving tweets_{query}_{day}.csv')

            csv_writer = CsvWriter(
                self.data_dir,
                f'tweets_{query}_{day}.csv'
            )

            csv_writer.add_row(self.csv_header)
            csv_writer.add_rows(
                [
                    _get_status_row(status)
                    for status in tweets_by_day[day]
                ]
            )
