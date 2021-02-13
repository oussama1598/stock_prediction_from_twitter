import yfinance as yf

from src.modules.csv_writer import CsvWriter
from src.modules.logger import Logger

logger = Logger('Yahoo')


class YahooData:
    def __init__(self, data_dir):
        self.data_dir = data_dir

    def download_data(self, ticker_name, from_date, to_date):
        logger.info(f'Downloading yahoo data with keyword {ticker_name} from date {from_date} to date {to_date}')

        ticker = yf.Ticker(ticker_name)
        historical_data = ticker.history(start=from_date, end=to_date, auto_adjust=False)
        historical_data['Date'] = [i.date() for i in historical_data.index]

        logger.info(f'Saving stock_{ticker_name}_{from_date}_{to_date}.csv')

        csv_writer = CsvWriter(
            self.data_dir,
            f'stock_{ticker_name}_{from_date}_{to_date}.csv'
        )

        csv_writer.add_row(historical_data.columns)
        csv_writer.add_rows(
            historical_data.values
        )
