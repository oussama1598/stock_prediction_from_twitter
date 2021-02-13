import math

import requests


def _search(query, subreddit='', after: int = 0):
    response = requests.get(
        f'https://api.pushshift.io/reddit/search/submission/?q={query}&after={after}'
        f'&subreddit={subreddit}&author=&aggs=&metadata=true&frequency=hour&advanced=false'
        '&sort=asc&domain=&sort_type=created_utc&size=100'
    )

    data = response.json()['data']
    metadata = response.json()['metadata']

    return metadata['total_results'], data


def get_posts(query, subreddit='', after: int = 0, before: int = 0):
    last_timestamp = after
    total_results = 0
    total_grabbed_results = 0

    while last_timestamp <= before:
        total, results = _search(query, subreddit=subreddit, after=last_timestamp)

        if len(results) == 0:
            last_timestamp = before + 1

            break

        if total_results == 0:
            total_results = total

        last_timestamp = results[-1]['created_utc']
        total_grabbed_results += len(results)

        yield math.ceil(total_grabbed_results / 100), math.ceil(total_results / 100), results
