import pandas as pd
import numpy as np
from datetime import datetime


def main():
    market_data = pd.read_csv("fiename.csv")
    market_data['volume'] = np.log(market_data['volume'])
    market_data['rolling_volume'] = market_data['volume'].rolling(5).mean()
    market_data['date'] = market_data['date'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d').strftime('%d/%m/%y'))

    sentiment_data = pd.read_csv("India-Data/india_sentiment_data.csv")
    sentiment_data.rename(columns={"Title": "date"}, inplace=True)
    sentiment_data['date'] = sentiment_data['date'].str.replace('Sunday: ', '')
    sentiment_data['date'] = sentiment_data['date'].str.replace('Monday: ', '')
    sentiment_data['date'] = sentiment_data['date'].str.replace('Tuesday: ', '')
    sentiment_data['date'] = sentiment_data['date'].str.replace('Wednesday: ', '')
    sentiment_data['date'] = sentiment_data['date'].str.replace('Thursday: ', '')
    sentiment_data['date'] = sentiment_data['date'].str.replace('Friday: ', '')
    sentiment_data['date'] = sentiment_data['date'].str.replace('Saturday: ', '')
    sentiment_data['date'] = sentiment_data['date'].apply(
        lambda x: datetime.strptime(x, '%d/%m/%Y').strftime('%d/%m/%y'))

    new_df = pd.merge(market_data, sentiment_data, how='left', on='date')
    new_df = new_df.dropna()
    new_df = new_df.drop(['Unnamed: 0', 'Date of First Article'], axis=1)
    new_df['moderna'] = new_df.date.apply(lambda x: 1 if datetime.strptime(x, '%d/%m/%y') > datetime(2020, 4, 14) else 0)
    new_df['pfizer'] = new_df.date.apply(lambda x: 1 if datetime.strptime(x, '%d/%m/%y') > datetime(2020, 4, 20) else 0)
    new_df['election'] = new_df.date.apply(lambda x: 1 if datetime.strptime(x, '%d/%m/%y') > datetime(2020, 8, 19) else 0)

    epu_data = pd.read_csv("EPU-US.csv")
    epu_data = epu_data.drop(['day', 'month', 'year'], axis=1)
    epu_data = epu_data.dropna()
    epu_data['date'] = epu_data['date'].apply(lambda x: datetime.strptime(x, '%m/%d/%y').strftime('%d/%m/%y'))

    final_df = pd.merge(new_df, epu_data, how='left', on='date')
    print(final_df.to_string())
    final_df.to_csv("combined-data.csv")


if __name__ == '__main__':
    main()
