import datetime

from nltk.sentiment import SentimentIntensityAnalyzer
from pushshift_py import PushshiftAPI

from src.modules.csv_writer import CsvWriter
from src.modules.logger import Logger

logger = Logger('RedditData')
sentiment_analyzer = SentimentIntensityAnalyzer()


def _get_post_row(post):
    if hasattr(post, 'selftext'):
        full_text = post.selftext
    else:
        full_text = post.title

    score = sentiment_analyzer.polarity_scores(full_text)

    return [
               datetime.datetime.fromtimestamp(post.created).date(),
               full_text,
               post.upvotes
           ] + list(score.values())


class RedditData:
    def __init__(self, data_dir='./data'):
        self.data_dir = data_dir
        self.csv_header = ['Date', 'Content', 'Up Votes', 'Negative Score', 'Neutral Score', 'Positive Score',
                           'Compound Score']

        logger.info('initializing reddit data')
        self.api = PushshiftAPI()
        logger.info('reddit data initialized')

    def download_data(self, query, subreddit='', from_date=None, to_date=None):
        logger.info(
            f'Downloading tweets with keyword {query} from subreddit '
            f'{subreddit} from date {from_date} to date {to_date}')

        posts_by_day = {}

        result = list(
            self.api.search_submissions(
                q='GME',
                after=int(from_date.timestamp()),
                subreddit='wallstreetbets',
                stop_condition=lambda x: x.created > int(to_date.timestamp())
            )
        )

        for post in result:
            post_date = datetime.datetime.fromtimestamp(post.created).date()

            if post_date < from_date:
                continue

            if post_date not in posts_by_day:
                posts_by_day[post_date] = []

            posts_by_day[post_date].append(post)

        print(posts_by_day)

        for day in posts_by_day:
            logger.info(f'Saving posts_{query}_{day}.csv')

            csv_writer = CsvWriter(
                self.data_dir,
                f'posts_{query}_{day}.csv'
            )

            csv_writer.add_row(self.csv_header)

            for post in posts_by_day[day]:

                if '[removed]' in post.title:
                    continue

                csv_writer.add_row(_get_post_row(post))
