import matplotlib.pyplot as plt
import numpy as np
from typing import List

import pandas

from src.models.yahoo_dataframe import YahooDataFrame


def plot_score_histogram(dataframe: pandas.DataFrame):
    positive_tweets = dataframe[dataframe['positive'] == 1]
    neutral_tweets = dataframe[dataframe['neutral'] == 1]
    negative_tweets = dataframe[dataframe['negative'] == 1]

    x = np.arange(3)
    plt.bar(x, height=[len(positive_tweets), len(neutral_tweets), len(negative_tweets)])
    plt.xticks(x, ['Positive', 'Neutral', 'Negative'])

    plt.show()


def plot_number_of_tweets_per_day(dataframes: List[pandas.DataFrame]):
    dates = []
    dataframes_positive = []
    dataframes_neutral = []
    dataframes_negative = []

    for dataframe in dataframes:
        positive_tweets = dataframe[dataframe['positive'] == 1]
        neutral_tweets = dataframe[dataframe['neutral'] == 1]
        negative_tweets = dataframe[dataframe['negative'] == 1]

        dates.append(dataframe.iloc[0].Date)
        dataframes_positive.append(len(positive_tweets))
        dataframes_neutral.append(len(neutral_tweets))
        dataframes_negative.append(len(negative_tweets))

    x = np.arange(len(dates))
    width = 0.10

    fig, ax = plt.subplots()
    positive_bar = ax.bar(x - width, dataframes_positive, width, label='Positive')
    neutral_bar = ax.bar(x, dataframes_neutral, width, label='Neutral')
    negative_bar = ax.bar(x + width, dataframes_negative, width, label='Negative')

    ax.set_ylabel('Scores')
    ax.set_title('Scores by polarity')
    ax.set_xticks(x)
    ax.set_xticklabels(dates)
    ax.legend()

    for bar in [positive_bar, neutral_bar, negative_bar]:
        for rect in bar:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords='offset points',
                        ha='center', va='bottom')

    fig.tight_layout()
    plt.show()


def plot_stock_adj(dataframe: YahooDataFrame):
    dataframe = dataframe.get_dataframe()

    plt.plot(dataframe['Date'], dataframe['Adj Close'], 'r')
    plt.xlabel('Days')
    plt.ylabel('Price')
    plt.show()
