import os
from datetime import datetime

import numpy as np
import pandas


class TweetsDataFrame:
    def __init__(self, data_dir, file_name):
        self.data_dir = data_dir
        self.file_name = file_name

        self.query = file_name.split('_')[1]
        self.date = file_name.split('_')[2].replace('.csv', '')

        self.dataframe = pandas.read_csv(
            os.path.join(self.data_dir, self.file_name),
            delimiter=',',
            quotechar='|'
        )

        # Drop duplicates
        self.dataframe.drop_duplicates(inplace=True)

        # Filter tweets with 0 followers
        self.dataframe = self.dataframe[self.dataframe['Up Votes'] != 0]

        self.dataframe['positive'] = np.where(
            self.dataframe['Positive Score'] >= 0.5,
            1, 0
        )

        self.dataframe['neutral'] = np.where(
            self.dataframe['Neutral Score'] >= 0.5,
            1, 0
        )

        self.dataframe['negative'] = np.where(
            self.dataframe['Negative Score'] >= 0.5,
            1, 0
        )

        self.dataframe['sentiment_score'] = self.dataframe['Compound Score'] * self.dataframe['Up Votes']

        self.dataframe['Date'] = [str(datetime.strptime(x, '%Y-%m-%d %H:%M:%S').date()) for x in self.dataframe['Date']]

    def get_dataframe(self):
        return self.dataframe
