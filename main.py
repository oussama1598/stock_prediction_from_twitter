import datetime
import os

import numpy as np
import pandas
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

from src.models.tweets_dataframe import TweetsDataFrame
from src.models.yahoo_dataframe import YahooDataFrame
from src.modules.twitter_data import TwitterData
from src.modules.yahoo_data import YahooData

DATA_DIR = os.getenv(os.getcwd(), 'data')

twitter_data = TwitterData(
    os.getenv('TWITTER_API_KEY'),
    os.getenv('TWITTER_API_SECRET_KEY'),
    os.getenv('TWITTER_ACCESS_TOKEN'),
    os.getenv('TWITTER_ACCESS_TOKEN_SECRET'),
    data_dir=os.getenv(os.getcwd(), 'data')
)

yahoo_data = YahooData(DATA_DIR)

to_date = datetime.datetime.now().date() + datetime.timedelta(1)
from_date = to_date - datetime.timedelta(days=1)

# twitter_data.download_data(
#     'TESLA',
#     10000,
#     from_date=from_date,
#     to_date=today
# )

# yahoo_data.download_data(
#     'TSLA',
#     from_date,
#     to_date
# )

tweets_dataframes = [
    TweetsDataFrame(DATA_DIR, f).dataframe
    for f in os.listdir(DATA_DIR) if 'tweets' in f and os.path.isfile(os.path.join(DATA_DIR, f))
]

yahoo_dataframe = [
    YahooDataFrame(DATA_DIR, f)
    for f in os.listdir(DATA_DIR) if 'stock' in f and os.path.isfile(os.path.join(DATA_DIR, f))
][0]

tweets_dataframes_combined = pandas.concat(tweets_dataframes)
tweets_dataframes_combined = (tweets_dataframes_combined.groupby(tweets_dataframes_combined.Date).mean())

# plotter.plot_score_histogram(
#     tweets_dataframes_combined
# )
#
# plotter.plot_number_of_tweets_per_day(
#     tweets_dataframes
# )
#
# plotter.plot_stock_adj(yahoo_dataframe)

dataset = pandas.merge(
    yahoo_dataframe.get_dataframe(),
    tweets_dataframes_combined[['sentiment_score']], left_index=True, right_index=True)

print(dataset.head())

train_set = dataset.iloc[:35]
test_set = dataset.iloc[35:]

X_train = np.array(train_set[['sentiment_score']])
X_test = np.array(test_set[['sentiment_score']])

y_train = np.array(train_set['buy_sell'])
y_test = np.array(test_set['buy_sell'])

scaler = StandardScaler()
X_train_std = scaler.fit_transform(X_train)

from sklearn.model_selection import cross_val_score

for i in range(1, 5):
    svc = SVC(kernel="rbf", random_state=0, gamma=i)
    model = svc.fit(X_train_std, y_train)
    scores = cross_val_score(estimator=model, X=X_train, y=y_train, cv=5)
    print(i, ':', np.average(scores))
