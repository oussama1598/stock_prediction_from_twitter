import datetime

from nltk.sentiment import SentimentIntensityAnalyzer
from pushshift_py import PushshiftAPI

from src.lib import reddit
from src.modules.csv_writer import CsvWriter
from src.modules.logger import Logger

logger = Logger('RedditData')
sentiment_analyzer = SentimentIntensityAnalyzer()


def _get_post_row(post):
    if 'selftext' in post:
        full_text = post['selftext']
    else:
        full_text = post['title']

    score = sentiment_analyzer.polarity_scores(full_text)

    return [
               datetime.datetime.fromtimestamp(post['created_utc']).date(),
               full_text,
               post['upvote_ratio']
           ] + list(score.values())


class RedditData:
    def __init__(self, data_dir='./data'):
        self.data_dir = data_dir
        self.csv_header = ['Date', 'Content', 'Up Votes', 'Negative Score', 'Neutral Score', 'Positive Score',
                           'Compound Score']

        logger.info('initializing reddit data')
        self.api = PushshiftAPI()
        logger.info('reddit data initialized')

    def download_data(self, query, subreddit='', from_date: datetime = None, to_date: datetime = None):
        logger.info(
            f'Downloading tweets with keyword {query} from subreddit '
            f'{subreddit} from date {from_date} to date {to_date}')

        posts_by_day = {}

        for page, pages, posts in reddit.get_posts(query, subreddit, int(from_date.timestamp()),
                                                   int(to_date.timestamp())):
            logger.info(f'Fetched {page} of {pages} pages')

            for post in posts:
                post_date = datetime.datetime.fromtimestamp(post['created_utc']).date()

                if post_date not in posts_by_day:
                    posts_by_day[post_date] = []

                posts_by_day[post_date].append(post)

        for day in posts_by_day:
            logger.info(f'Saving posts_{query}_{day}.csv')

            csv_writer = CsvWriter(
                self.data_dir,
                f'posts_{query}_{day}.csv'
            )

            csv_writer.add_row(self.csv_header)

            for post in posts_by_day[day]:
                post = _get_post_row(post)

                if '[removed]' in post[1]:
                    continue

                csv_writer.add_row(post)
