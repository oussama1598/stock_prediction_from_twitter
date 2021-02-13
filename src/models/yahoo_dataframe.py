import math
import os
import numpy as np
import pandas
from sklearn.preprocessing import StandardScaler


class YahooDataFrame:
    def __init__(self, data_dir, file_name):
        self.data_dir = data_dir
        self.file_name = file_name

        self.query = file_name.split('_')[1]

        self.dataframe = pandas.read_csv(
            os.path.join(self.data_dir, self.file_name),
            delimiter=',',
            quotechar='|'
        )

        # Add value change
        self.dataframe['stock_val_change'] = (self.dataframe['Close'] - self.dataframe['Open']) / self.dataframe[
            'Open'] * 100.0

        # normalize the value change
        scaler = StandardScaler()
        self.dataframe['stock_val_change_scaled'] = scaler.fit_transform(
            self.dataframe[['stock_val_change']]
        )

        forecast_out = int(math.ceil(0.013 * len(self.dataframe)))
        self.dataframe['stock_val_change_pred'] = self.dataframe['stock_val_change'].shift(-forecast_out)

        self.dataframe['buy_sell'] = self.dataframe['stock_val_change_pred'].apply(lambda x: 1 if x >= 0 else -1)

        self.dataframe = self.dataframe.set_index('Date')

    def get_dataframe(self):
        return self.dataframe
